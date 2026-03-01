from typing import List, Optional
from datetime import date
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db, get_jobs_filtered, get_companies_by_demand_score, get_hiring_trends
from api.schemas import (
    ExportResponse, TopCompany, HiringTrend
)
from utils.export import jobs_to_csv, companies_to_csv, export_to_file, generate_export_filename

router = APIRouter(prefix="/analytics", tags=["analytics"])


@router.get("/top-companies", response_model=List[TopCompany])
async def get_top_companies(
    limit: int = 10,
    country: Optional[str] = None,
    db: AsyncSession = Depends(get_db)
):
    """Get top companies by demand score."""
    companies = await get_companies_by_demand_score(
        db,
        limit=limit,
        country=country
    )
    
    return [
        TopCompany(
            company_name=c["company_name"],
            total_demand_score=c["total_demand_score"],
            highest_priority=c["highest_priority"],
            total_openings=c["total_openings"]
        )
        for c in companies
    ]


@router.get("/hiring-trends", response_model=List[HiringTrend])
async def get_hiring_trends_endpoint(
    days: int = 30,
    db: AsyncSession = Depends(get_db)
):
    """Get hiring trends over time."""
    trends = await get_hiring_trends(db, days)
    return [HiringTrend(**t) for t in trends]


@router.get("/export/jobs")
async def export_jobs(
    country: Optional[str] = None,
    skill_keyword: Optional[str] = None,
    platform: Optional[str] = None,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    priority: Optional[str] = None,
    db: AsyncSession = Depends(get_db)
):
    """Export jobs to CSV."""
    jobs = await get_jobs_filtered(
        db,
        country=country,
        skill_keyword=skill_keyword,
        platform=platform,
        start_date=start_date,
        end_date=end_date,
        priority=priority,
        limit=10000  # High limit for exports
    )
    
    csv_content = jobs_to_csv(jobs)
    filename = generate_export_filename("jobs")
    filepath = export_to_file(csv_content, filename)
    
    return ExportResponse(
        filename=filename,
        filepath=filepath,
        record_count=len(jobs)
    )


@router.get("/export/companies")
async def export_companies(
    country: Optional[str] = None,
    min_demand_score: float = 0,
    db: AsyncSession = Depends(get_db)
):
    """Export companies to CSV."""
    companies = await get_companies_by_demand_score(
        db,
        limit=10000,  # High limit for exports
        country=country,
        min_demand_score=min_demand_score
    )
    
    csv_content = companies_to_csv(companies)
    filename = generate_export_filename("companies")
    filepath = export_to_file(csv_content, filename)
    
    return ExportResponse(
        filename=filename,
        filepath=filepath,
        record_count=len(companies)
    )


@router.get("/dashboard-summary")
async def get_dashboard_summary(
    db: AsyncSession = Depends(get_db)
):
    """Get summary statistics for dashboard."""
    from database import get_job_posting_count
    from datetime import timedelta
    
    # Total jobs
    total_jobs = await get_job_posting_count(db)
    
    # Jobs this month
    month_start = date.today().replace(day=1)
    jobs_this_month = await get_job_posting_count(db, start_date=month_start)
    
    # Jobs this week
    week_start = date.today() - timedelta(days=date.today().weekday())
    jobs_this_week = await get_job_posting_count(db, start_date=week_start)
    
    # High priority companies
    high_priority = await get_companies_by_demand_score(
        db, limit=1000, min_demand_score=25
    )
    
    # Top platforms
    from sqlalchemy import select, func
    from database.models import JobPosting
    
    result = await db.execute(
        select(
            JobPosting.platform_source,
            func.count(JobPosting.id).label("count")
        )
        .group_by(JobPosting.platform_source)
    )
    platforms = {row.platform_source: row.count for row in result.all()}
    
    return {
        "total_jobs": total_jobs,
        "jobs_this_month": jobs_this_month,
        "jobs_this_week": jobs_this_week,
        "high_priority_companies": len(high_priority),
        "platforms": platforms
    }
