#!/usr/bin/env python3
"""
DemandSniper - Main entry point

A configurable hiring-demand intelligence tool for detecting 
companies with ongoing hiring demand and outsourcing opportunities.

Usage:
    python main.py run-api        # Start the FastAPI server
    python main.py run-dashboard  # Start the basic Streamlit dashboard
    python main.py run-saas       # Start the premium SaaS dashboard
    python main.py run-scraper    # Run scraper manually
    python main.py run-all        # Start API and dashboard
    python main.py init-db        # Initialize database only
"""

import sys
import asyncio
import argparse
import uvicorn
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from config.settings import settings
from database import init_db


def run_api():
    """Start the FastAPI server."""
    print(f"🚀 Starting {settings.PROJECT_NAME} API server...")
    print(f"📍 API will be available at: http://{settings.API_HOST}:{settings.API_PORT}")
    print(f"📚 API documentation: http://{settings.API_HOST}:{settings.API_PORT}/docs")
    
    uvicorn.run(
        "api.main:app",
        host=settings.API_HOST,
        port=settings.API_PORT,
        reload=settings.DEBUG,
        log_level="info"
    )


def run_dashboard():
    """Start the Streamlit dashboard."""
    print(f"📊 Starting {settings.PROJECT_NAME} Dashboard...")
    
    import subprocess
    dashboard_path = settings.BASE_DIR / "dashboard" / "app.py"
    
    subprocess.run([
        "streamlit", "run",
        str(dashboard_path),
        "--server.port", "8501",
        "--server.address", "0.0.0.0"
    ])


def run_saas_dashboard():
    """Start the premium SaaS Streamlit dashboard."""
    print(f"🎯 Starting {settings.PROJECT_NAME} SaaS Dashboard...")
    print(f"📊 Dashboard will be available at: http://localhost:8501")
    
    import subprocess
    dashboard_path = settings.BASE_DIR / "dashboard" / "app_saas.py"
    streamlit_path = settings.BASE_DIR / "venv" / "bin" / "streamlit"
    
    subprocess.run([
        str(streamlit_path), "run",
        str(dashboard_path),
        "--server.port", "8501",
        "--server.address", "0.0.0.0",
        "--theme.base", "dark"
    ])


async def run_scraper():
    """Run the scraper manually."""
    print(f"🤖 Running scraper...")
    
    from scraper.scheduler import run_manual_scrape
    
    results = await run_manual_scrape()
    
    print("\n✅ Scraper completed!")
    print(f"Total jobs found: {results.get('total_jobs_found', 0)}")
    print(f"New jobs: {results.get('new_jobs', 0)}")
    print(f"Republished jobs: {results.get('republished_jobs', 0)}")
    
    if results.get('errors'):
        print(f"\n⚠️  Errors: {len(results['errors'])}")
        for error in results['errors']:
            print(f"  - {error}")


async def init_database():
    """Initialize the database."""
    print("🗄️  Initializing database...")
    await init_db()
    print("✅ Database initialized successfully!")


def run_all():
    """Start API and dashboard together."""
    import multiprocessing
    
    def start_api():
        uvicorn.run(
            "api.main:app",
            host=settings.API_HOST,
            port=settings.API_PORT,
            reload=False
        )
    
    def start_dashboard():
        import subprocess
        dashboard_path = settings.BASE_DIR / "dashboard" / "app.py"
        subprocess.run([
            "streamlit", "run",
            str(dashboard_path),
            "--server.port", "8501",
            "--server.address", "0.0.0.0"
        ])
    
    print(f"🚀 Starting {settings.PROJECT_NAME} - Full Stack Mode")
    print(f"📍 API: http://{settings.API_HOST}:{settings.API_PORT}")
    print(f"📊 Dashboard: http://localhost:8501")
    
    # Start API in separate process
    api_process = multiprocessing.Process(target=start_api)
    api_process.start()
    
    # Start dashboard in main process
    try:
        start_dashboard()
    except KeyboardInterrupt:
        print("\n👋 Shutting down...")
    finally:
        api_process.terminate()
        api_process.join()


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="DemandSniper - Hiring Demand Intelligence Tool"
    )
    
    parser.add_argument(
        "command",
        choices=[
            "run-api",
            "run-dashboard",
            "run-saas",
            "run-scraper",
            "run-all",
            "init-db"
        ],
        help="Command to execute"
    )
    
    args = parser.parse_args()
    
    if args.command == "run-api":
        run_api()
    elif args.command == "run-dashboard":
        run_dashboard()
    elif args.command == "run-saas":
        run_saas_dashboard()
    elif args.command == "run-scraper":
        asyncio.run(run_scraper())
    elif args.command == "run-all":
        run_all()
    elif args.command == "init-db":
        asyncio.run(init_database())


if __name__ == "__main__":
    main()
