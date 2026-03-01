import asyncio
from datetime import datetime
from typing import List, Dict, Any, Optional
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger

from config.loader import load_search_config, load_scoring_config
from config.settings import settings
from database import async_session_maker, create_job_posting, find_similar_posting, update_reposted_job, create_company_event
from database.models import JobPosting
from scraper.indeed import IndeedScraper
from scraper.dice import DiceScraper
from scraper.linkedin import LinkedInScraper
from utils.demand_scoring import calculate_demand_score, get_priority_tag
from utils.notifications import check_and_notify_triggers


class ScrapingScheduler:
    """Manages scheduled scraping operations."""
    
    def __init__(self):
        self.scheduler = None
        self.scrapers = {
            "indeed": IndeedScraper(),
            "dice": DiceScraper(),
            "linkedin": LinkedInScraper()
        }
        self._running = False
    
    async def start(self):
        """Initialize and start the scheduler."""
        if self.scheduler and self.scheduler.running:
            return
        
        # Use memory-based jobstore to avoid serialization issues
        self.scheduler = AsyncIOScheduler()
        self.scheduler.start()
        
        # Schedule jobs based on configuration
        await self._schedule_jobs()
        
        self._running = True
        print("Scraping scheduler started")
    
    async def stop(self):
        """Stop the scheduler."""
        if self.scheduler:
            self.scheduler.shutdown()
            self._running = False
            print("Scraping scheduler stopped")
    
    async def _schedule_jobs(self):
        """Schedule scraping jobs based on configuration."""
        config = load_search_config()
        frequency = config.get("search_frequency", "daily")
        platforms = config.get("platforms", [])
        
        if not platforms:
            return
        
        # Schedule scraping job
        if frequency == "daily":
            trigger = CronTrigger(hour=2, minute=0)  # Run at 2 AM daily
        elif frequency == "weekly":
            trigger = CronTrigger(day_of_week="mon", hour=2, minute=0)  # Run Monday 2 AM
        else:
            trigger = CronTrigger(hour=2, minute=0)  # Default to daily
        
        # Use a module-level function to avoid serialization issues
        self.scheduler.add_job(
            _run_scheduled_scrape,
            trigger=trigger,
            id="scheduled_scrape",
            replace_existing=True
        )
    
    async def run_scrape(self, platforms: List[str] = None) -> Dict[str, Any]:
        """
        Run scraping across specified platforms and countries.
        
        Args:
            platforms: List of platform names to scrape. If None, uses configured platforms.
        
        Returns:
            Dictionary with scraping results
        """
        config = load_search_config()
        
        if platforms is None:
            platforms = config.get("platforms", ["indeed"])
        
        keywords = config.get("skill_keywords", [])
        # Get all countries to scrape
        countries = config.get("countries", ["United States"])
        locations = config.get("locations", [])
        max_results = config.get("max_results_per_platform", 100)
        
        results = {
            "platforms": {},
            "countries": {},
            "total_jobs_found": 0,
            "new_jobs": 0,
            "republished_jobs": 0,
            "errors": []
        }
        
        async with async_session_maker() as db:
            # Loop through each country
            for country in countries:
                results["countries"][country] = {"jobs_found": 0, "new": 0, "republished": 0}
                
                for platform_name in platforms:
                    if platform_name not in self.scrapers:
                        results["errors"].append(f"Unknown platform: {platform_name}")
                        continue
                    
                    scraper = self.scrapers[platform_name]
                    
                    try:
                        # Scrape jobs for this country
                        jobs = await scraper.search(
                            keywords=keywords,
                            country=country,
                            locations=locations,
                            max_results=max_results
                        )
                        
                        platform_results = {
                            "jobs_found": len(jobs),
                            "new": 0,
                            "republished": 0,
                            "errors": 0
                        }
                        
                        # Process each job
                        for job_data in jobs:
                            try:
                                processed = await self._process_job(db, job_data)
                                if processed == "new":
                                    platform_results["new"] += 1
                                    results["new_jobs"] += 1
                                    results["countries"][country]["new"] += 1
                                elif processed == "republished":
                                    platform_results["republished"] += 1
                                    results["republished_jobs"] += 1
                                    results["countries"][country]["republished"] += 1
                            except Exception as e:
                                print(f"Error processing job: {e}")
                                platform_results["errors"] += 1
                        
                        results["platforms"][platform_name] = platform_results
                        results["total_jobs_found"] += len(jobs)
                        results["countries"][country]["jobs_found"] += len(jobs)
                        
                    except Exception as e:
                        error_msg = f"Error scraping {platform_name} in {country}: {str(e)}"
                        print(error_msg)
                        results["errors"].append(error_msg)
                        results["platforms"][platform_name] = {"error": str(e)}
        
        return results
    
    async def _process_job(self, db, job_data) -> str:
        """
        Process a single job posting.
        
        Returns:
            "new" if new job, "republished" if repost, "error" if failed
        """
        # Check for exact URL match
        existing_by_url = await self._get_job_by_url(db, job_data.job_url)
        
        if existing_by_url:
            # URL exists, check if it's a repost
            window_days = load_scoring_config().get("repost_detection_window_days", 60)
            
            if self._is_repost(existing_by_url, window_days):
                # Update as repost
                await update_reposted_job(
                    db,
                    existing_by_url,
                    job_data.posting_date,
                    job_data.number_of_openings
                )
                
                # Create event
                await create_company_event(
                    db,
                    job_data.company_name,
                    "repost_detected",
                    existing_by_url.id,
                    {"previous_times_posted": existing_by_url.times_posted - 1}
                )
                
                return "republished"
            else:
                # Just update last seen
                existing_by_url.last_seen_date = datetime.now().date()
                await db.commit()
                return "existing"
        
        # Check for similar posting (fuzzy match)
        similar = await find_similar_posting(
            db,
            job_data.company_name,
            job_data.job_title,
            job_data.country
        )
        
        if similar:
            # Update existing as repost
            await update_reposted_job(
                db,
                similar,
                job_data.posting_date,
                job_data.number_of_openings
            )
            
            # Create event
            await create_company_event(
                db,
                job_data.company_name,
                "repost_detected",
                similar.id,
                {"matched_job_url": job_data.job_url}
            )
            
            return "republished"
        
        # New job posting
        job_dict = {
            "company_name": job_data.company_name,
            "job_title": job_data.job_title,
            "location": job_data.location,
            "country": job_data.country,
            "platform_source": job_data.platform_source,
            "posting_date": job_data.posting_date,
            "job_url": job_data.job_url,
            "salary_range": job_data.salary_range,
            "number_of_openings": job_data.number_of_openings,
            "demand_score": calculate_demand_score(1, 0, job_data.number_of_openings),
            "priority_tag": get_priority_tag(
                calculate_demand_score(1, 0, job_data.number_of_openings)
            )
        }
        
        new_job = await create_job_posting(db, job_dict)
        
        # Create event
        await create_company_event(
            db,
            job_data.company_name,
            "job_posted",
            new_job.id
        )
        
        # Check notification triggers
        await check_and_notify_triggers({
            "company_name": job_data.company_name,
            "demand_score": new_job.demand_score,
            "priority_tag": new_job.priority_tag,
            "total_openings": job_data.number_of_openings,
            "first_seen_date": new_job.first_seen_date.isoformat()
        })
        
        return "new"
    
    async def _get_job_by_url(self, db, job_url: str) -> Optional[JobPosting]:
        """Get job by URL."""
        from sqlalchemy import select
        result = await db.execute(
            select(JobPosting).where(JobPosting.job_url == job_url)
        )
        return result.scalar_one_or_none()
    
    def _is_repost(self, job: JobPosting, window_days: int) -> bool:
        """Check if job should be treated as a repost."""
        from datetime import date, timedelta
        cutoff_date = date.today() - timedelta(days=window_days)
        return job.last_seen_date >= cutoff_date
    
    def get_status(self) -> Dict[str, Any]:
        """Get scheduler status."""
        if not self.scheduler:
            return {"running": False, "jobs": []}
        
        jobs = []
        for job in self.scheduler.get_jobs():
            jobs.append({
                "id": job.id,
                "name": job.name,
                "next_run": job.next_run_time.isoformat() if job.next_run_time else None
            })
        
        return {
            "running": self.scheduler.running,
            "jobs": jobs
        }


# Global scheduler instance
scheduler = ScrapingScheduler()


async def start_scheduler():
    """Start the global scheduler."""
    await scheduler.start()


async def stop_scheduler():
    """Stop the global scheduler."""
    await scheduler.stop()


async def run_manual_scrape(platforms: List[str] = None) -> Dict[str, Any]:
    """Run a manual scrape."""
    return await scheduler.run_scrape(platforms)


def _run_scheduled_scrape():
    """Module-level function for scheduled scraping to avoid serialization issues."""
    import asyncio
    asyncio.run(scheduler.run_scrape())
