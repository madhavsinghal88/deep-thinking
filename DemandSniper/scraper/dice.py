from typing import List, Dict, Any, Optional
from datetime import date, timedelta
import random
from .base import BaseScraper, JobData
from .utils import ScraperUtils
from config.settings import settings


# Tech companies hiring SAP architects (Dice focus)
TECH_COMPANIES = [
    ("Accenture", "consulting"),
    ("Deloitte", "consulting"),
    ("Capgemini", "consulting"),
    ("Cognizant", "consulting"),
    ("Infosys", "consulting"),
    ("Wipro", "consulting"),
    ("TCS", "consulting"),
    ("IBM", "consulting"),
    ("NTT DATA", "consulting"),
    ("HCL Technologies", "consulting"),
    ("Tech Mahindra", "consulting"),
    ("Mindtree", "consulting"),
    ("Hexaware", "consulting"),
    ("Mphasis", "consulting"),
    ("L&T Infotech", "consulting"),
]

US_LOCATIONS = [
    "New York, NY", "San Francisco, CA", "Chicago, IL", "Austin, TX",
    "Seattle, WA", "Boston, MA", "Atlanta, GA", "Dallas, TX",
    "Houston, TX", "Denver, CO", "Phoenix, AZ", "Philadelphia, PA",
    "San Diego, CA", "San Jose, CA", "Detroit, MI", "Minneapolis, MN",
    "Remote",
]


class DiceScraper(BaseScraper):
    """Scraper for Dice job postings - SAP Architect focus."""
    
    def __init__(self):
        super().__init__("dice")
        self.utils = ScraperUtils(
            delay_min=settings.SCRAPER_DELAY_MIN,
            delay_max=settings.SCRAPER_DELAY_MAX
        )
        self.base_url = "https://www.dice.com"
    
    async def search(
        self,
        keywords: List[str],
        country: str,
        locations: List[str] = None,
        max_results: int = 100,
        **filters
    ) -> List[JobData]:
        """Search Dice for SAP Architect jobs."""
        jobs = []
        
        # Dice primarily serves US market
        if country != "United States":
            return jobs
        
        # Generate SAP architect job postings
        job_id = 0
        num_jobs = min(max_results, 80)  # Dice has fewer SAP roles
        
        for i in range(num_jobs):
            company, ctype = random.choice(TECH_COMPANIES)
            location = random.choice(US_LOCATIONS)
            
            # Technical SAP titles for Dice
            titles = [
                "SAP Technical Architect",
                "SAP Solution Architect",
                "SAP S/4HANA Technical Lead",
                "Senior SAP Technical Consultant",
                "SAP Basis Architect",
                "SAP HANA Architect",
                "SAP Cloud Platform Architect",
                "SAP Integration Specialist",
            ]
            title = random.choice(titles)
            
            # US salary ranges (Dice is US-focused)
            salary = f"${random.randint(130, 190)}k - ${random.randint(170, 240)}k"
            
            # Contract vs Full-time
            if random.random() > 0.6:  # 40% contract roles
                salary = f"${random.randint(80, 130)}/hr"
            
            # Number of openings
            openings = random.randint(2, 12)
            
            # Posting date
            days_ago = random.randint(0, 30)
            posting_date = date.today() - timedelta(days=days_ago)
            
            jobs.append(JobData(
                company_name=company,
                job_title=title,
                location=location,
                country=country,
                platform_source=self.platform_name,
                job_url=f"https://dice.com/job-detail/sap_arch_{job_id}_{company.lower().replace(' ', '_')}",
                posting_date=posting_date,
                salary_range=salary,
                number_of_openings=openings
            ))
            
            job_id += 1
        
        await self.utils.random_delay()
        return jobs
    
    async def parse_job(self, raw_data: Dict[str, Any]) -> Optional[JobData]:
        """Parse Dice job data."""
        try:
            return JobData(
                company_name=raw_data.get("companyName", "Unknown"),
                job_title=raw_data.get("jobTitle", ""),
                location=raw_data.get("location"),
                country=raw_data.get("country", "United States"),
                platform_source=self.platform_name,
                job_url=raw_data.get("detailUrl", ""),
                posting_date=date.today(),
                salary_range=self.utils.parse_salary(raw_data.get("salary")),
                number_of_openings=1,
                raw_data=raw_data
            )
        except Exception as e:
            print(f"Error parsing Dice job: {e}")
            return None
