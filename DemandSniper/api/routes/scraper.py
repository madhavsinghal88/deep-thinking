from typing import List, Optional
from fastapi import APIRouter, HTTPException, BackgroundTasks

from scraper.scheduler import scheduler, run_manual_scrape
from api.schemas import ScraperStatus, ScraperRunRequest, ScraperRunResponse

router = APIRouter(prefix="/scraper", tags=["scraper"])


@router.get("/status", response_model=ScraperStatus)
async def get_scraper_status():
    """Get scraper scheduler status."""
    return scheduler.get_status()


@router.post("/run", response_model=ScraperRunResponse)
async def run_scraper(
    request: Optional[ScraperRunRequest] = None,
    background_tasks: BackgroundTasks = None
):
    """Trigger a manual scrape."""
    platforms = request.platforms if request else None
    
    results = await run_manual_scrape(platforms)
    
    return ScraperRunResponse(**results)


@router.post("/start")
async def start_scheduler():
    """Start the scraping scheduler."""
    await scheduler.start()
    return {"message": "Scheduler started successfully"}


@router.post("/stop")
async def stop_scheduler():
    """Stop the scraping scheduler."""
    await scheduler.stop()
    return {"message": "Scheduler stopped successfully"}
