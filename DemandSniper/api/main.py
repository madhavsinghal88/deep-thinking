from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from config.settings import settings
from database import init_db
from scraper.scheduler import start_scheduler, stop_scheduler
from api.routes import (
    jobs_router,
    companies_router,
    config_router,
    analytics_router,
    scraper_router
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager."""
    # Startup
    print(f"Starting {settings.PROJECT_NAME} v{settings.VERSION}")
    
    # Initialize database
    await init_db()
    print("Database initialized")
    
    # Start scheduler
    await start_scheduler()
    print("Scraping scheduler started")
    
    yield
    
    # Shutdown
    await stop_scheduler()
    print("Scraping scheduler stopped")


# Create FastAPI app
app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="Hiring-demand intelligence tool for detecting outsourcing opportunities",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(jobs_router, prefix="/api/v1")
app.include_router(companies_router, prefix="/api/v1")
app.include_router(config_router, prefix="/api/v1")
app.include_router(analytics_router, prefix="/api/v1")
app.include_router(scraper_router, prefix="/api/v1")


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "name": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "docs": "/docs"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}
