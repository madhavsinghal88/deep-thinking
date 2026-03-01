from .jobs import router as jobs_router
from .companies import router as companies_router
from .config import router as config_router
from .analytics import router as analytics_router
from .scraper import router as scraper_router

__all__ = [
    "jobs_router",
    "companies_router", 
    "config_router",
    "analytics_router",
    "scraper_router"
]
