from typing import List, Optional
from datetime import date
from fastapi import APIRouter, Depends, HTTPException, Query, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db, get_jobs_filtered, get_job_by_url, create_job_posting
from api.schemas import (
    JobResponse, JobCreate, JobFilter, JobUpdate
)

router = APIRouter(prefix="/jobs", tags=["jobs"])


@router.get("", response_model=List[JobResponse])
async def list_jobs(
    country: Optional[str] = Query(None),
    skill_keyword: Optional[str] = Query(None),
    platform: Optional[str] = Query(None),
    start_date: Optional[date] = Query(None),
    end_date: Optional[date] = Query(None),
    company_name: Optional[str] = Query(None),
    priority: Optional[str] = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: AsyncSession = Depends(get_db)
):
    """Get jobs with optional filters."""
    jobs = await get_jobs_filtered(
        db,
        country=country,
        skill_keyword=skill_keyword,
        platform=platform,
        start_date=start_date,
        end_date=end_date,
        company_name=company_name,
        priority=priority,
        skip=skip,
        limit=limit
    )
    return jobs


@router.get("/{job_id}", response_model=JobResponse)
async def get_job(
    job_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Get a specific job by ID."""
    from sqlalchemy import select
    from database.models import JobPosting
    
    result = await db.execute(
        select(JobPosting).where(JobPosting.id == job_id)
    )
    job = result.scalar_one_or_none()
    
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    
    return job


@router.post("", response_model=JobResponse)
async def create_job(
    job: JobCreate,
    db: AsyncSession = Depends(get_db)
):
    """Create a new job posting manually."""
    # Check if URL already exists
    existing = await get_job_by_url(db, str(job.job_url))
    if existing:
        raise HTTPException(
            status_code=400,
            detail="Job with this URL already exists"
        )
    
    # Create job with default tracking fields
    job_dict = job.dict()
    job_dict["job_url"] = str(job_dict["job_url"])
    job_dict["first_seen_date"] = date.today()
    job_dict["last_seen_date"] = date.today()
    job_dict["times_posted"] = 1
    job_dict["days_open"] = 0
    
    # Calculate initial demand score
    from utils.demand_scoring import calculate_demand_score, get_priority_tag
    job_dict["demand_score"] = calculate_demand_score(1, 0, job_dict.get("number_of_openings", 1))
    job_dict["priority_tag"] = get_priority_tag(job_dict["demand_score"])
    
    new_job = await create_job_posting(db, job_dict)
    return new_job


@router.put("/{job_id}", response_model=JobResponse)
async def update_job(
    job_id: int,
    job_update: JobUpdate,
    db: AsyncSession = Depends(get_db)
):
    """Update a job posting."""
    from sqlalchemy import select
    from database.models import JobPosting
    
    result = await db.execute(
        select(JobPosting).where(JobPosting.id == job_id)
    )
    job = result.scalar_one_or_none()
    
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    
    # Update fields
    update_data = job_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        if field == "job_url" and value:
            value = str(value)
        setattr(job, field, value)
    
    await db.commit()
    await db.refresh(job)
    return job


@router.delete("/{job_id}")
async def delete_job(
    job_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Delete a job posting."""
    from sqlalchemy import select
    from database.models import JobPosting
    
    result = await db.execute(
        select(JobPosting).where(JobPosting.id == job_id)
    )
    job = result.scalar_one_or_none()
    
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    
    await db.delete(job)
    await db.commit()
    
    return {"message": "Job deleted successfully"}


@router.get("/{job_id}/score-breakdown")
async def get_job_score_breakdown(
    job_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Get detailed demand score breakdown for a job."""
    from sqlalchemy import select
    from database.models import JobPosting
    from utils.demand_scoring import get_demand_score_breakdown
    
    result = await db.execute(
        select(JobPosting).where(JobPosting.id == job_id)
    )
    job = result.scalar_one_or_none()
    
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    
    return get_demand_score_breakdown(
        job.times_posted,
        job.days_open,
        job.number_of_openings
    )
