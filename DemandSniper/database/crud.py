from typing import Optional, List, Dict, Any
from datetime import date, datetime, timedelta
from sqlalchemy import select, update, and_, or_, desc, func
from sqlalchemy.ext.asyncio import AsyncSession
from rapidfuzz import fuzz
from .models import JobPosting, CompanyProfile, DemandScoreHistory, CompanyEvent
from config.loader import load_scoring_config
from utils.demand_scoring import calculate_demand_score, get_priority_tag


async def create_job_posting(
    db: AsyncSession,
    job_data: Dict[str, Any]
) -> JobPosting:
    """Create a new job posting."""
    job = JobPosting(**job_data)
    db.add(job)
    await db.commit()
    await db.refresh(job)
    return job


async def get_job_by_url(db: AsyncSession, job_url: str) -> Optional[JobPosting]:
    """Get job posting by URL."""
    result = await db.execute(
        select(JobPosting).where(JobPosting.job_url == job_url)
    )
    return result.scalar_one_or_none()


async def find_similar_posting(
    db: AsyncSession,
    company_name: str,
    job_title: str,
    country: str,
    window_days: int = 60
) -> Optional[JobPosting]:
    """
    Find a similar posting within the repost detection window.
    Returns the most recent matching posting.
    """
    config = load_scoring_config()
    thresholds = config.get("similarity_thresholds", {})
    title_threshold = thresholds.get("job_title", 85)
    company_threshold = thresholds.get("company_name", 95)
    
    cutoff_date = date.today() - timedelta(days=window_days)
    
    # Get recent postings from same company and country
    result = await db.execute(
        select(JobPosting).where(
            and_(
                JobPosting.country == country,
                JobPosting.last_seen_date >= cutoff_date
            )
        )
    )
    recent_postings = result.scalars().all()
    
    best_match = None
    best_score = 0
    
    for posting in recent_postings:
        # Check company name similarity
        company_score = fuzz.ratio(
            company_name.lower(), 
            posting.company_name.lower()
        )
        
        if company_score < company_threshold:
            continue
        
        # Check job title similarity
        title_score = fuzz.ratio(
            job_title.lower(),
            posting.job_title.lower()
        )
        
        if title_score >= title_threshold and title_score > best_score:
            best_score = title_score
            best_match = posting
    
    return best_match


async def update_reposted_job(
    db: AsyncSession,
    job: JobPosting,
    new_posting_date: Optional[date] = None,
    number_of_openings: int = 1
) -> JobPosting:
    """Update an existing job posting as a repost."""
    job.times_posted += 1
    job.last_seen_date = date.today()
    job.number_of_openings = max(job.number_of_openings, number_of_openings)
    
    # Recalculate days open
    job.days_open = (job.last_seen_date - job.first_seen_date).days
    
    # Recalculate demand score
    job.demand_score = calculate_demand_score(
        times_posted=job.times_posted,
        days_open=job.days_open,
        number_of_openings=job.number_of_openings
    )
    
    # Update priority tag
    job.priority_tag = get_priority_tag(job.demand_score)
    
    await db.commit()
    await db.refresh(job)
    
    # Record score history
    await record_score_history(db, job)
    
    return job


async def record_score_history(db: AsyncSession, job: JobPosting) -> None:
    """Record current demand score in history table."""
    config = load_scoring_config()
    if not config.get("scoring", {}).get("track_score_history", True):
        return
    
    history = DemandScoreHistory(
        job_posting_id=job.id,
        date=date.today(),
        demand_score=job.demand_score,
        times_posted=job.times_posted,
        days_open=job.days_open,
        number_of_openings=job.number_of_openings
    )
    db.add(history)
    await db.commit()


async def get_jobs_filtered(
    db: AsyncSession,
    country: Optional[str] = None,
    skill_keyword: Optional[str] = None,
    platform: Optional[str] = None,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    company_name: Optional[str] = None,
    priority: Optional[str] = None,
    skip: int = 0,
    limit: int = 100
) -> List[JobPosting]:
    """Get jobs with filters."""
    query = select(JobPosting)
    
    if country:
        query = query.where(JobPosting.country == country)
    
    if skill_keyword:
        query = query.where(
            JobPosting.job_title.ilike(f"%{skill_keyword}%")
        )
    
    if platform:
        query = query.where(JobPosting.platform_source == platform)
    
    if start_date:
        query = query.where(JobPosting.posting_date >= start_date)
    
    if end_date:
        query = query.where(JobPosting.posting_date <= end_date)
    
    if company_name:
        query = query.where(
            JobPosting.company_name.ilike(f"%{company_name}%")
        )
    
    if priority:
        query = query.where(JobPosting.priority_tag == priority)
    
    query = query.order_by(desc(JobPosting.demand_score))
    query = query.offset(skip).limit(limit)
    
    result = await db.execute(query)
    return result.scalars().all()


async def get_companies_by_demand_score(
    db: AsyncSession,
    limit: int = 50,
    country: Optional[str] = None,
    min_demand_score: float = 0
) -> List[Dict[str, Any]]:
    """Get companies aggregated by total demand score."""
    query = select(
        JobPosting.company_name,
        func.count(JobPosting.id).label("total_jobs"),
        func.sum(JobPosting.demand_score).label("total_demand_score"),
        func.max(JobPosting.priority_tag).label("highest_priority"),
        func.max(JobPosting.last_seen_date).label("last_active"),
        func.sum(JobPosting.number_of_openings).label("total_openings")
    ).group_by(JobPosting.company_name)
    
    if country:
        query = query.where(JobPosting.country == country)
    
    query = query.having(func.sum(JobPosting.demand_score) >= min_demand_score)
    query = query.order_by(desc(func.sum(JobPosting.demand_score)))
    query = query.limit(limit)
    
    result = await db.execute(query)
    rows = result.all()
    
    return [
        {
            "company_name": row.company_name,
            "total_jobs": row.total_jobs,
            "total_demand_score": float(row.total_demand_score or 0),
            "highest_priority": row.highest_priority,
            "last_active": row.last_active,
            "total_openings": row.total_openings
        }
        for row in rows
    ]


async def get_company_timeline(
    db: AsyncSession,
    company_name: str,
    limit: int = 100
) -> List[CompanyEvent]:
    """Get company event timeline."""
    result = await db.execute(
        select(CompanyEvent)
        .where(CompanyEvent.company_name == company_name)
        .order_by(desc(CompanyEvent.event_date))
        .limit(limit)
    )
    return result.scalars().all()


async def create_company_event(
    db: AsyncSession,
    company_name: str,
    event_type: str,
    job_posting_id: Optional[int] = None,
    details: Optional[Dict] = None
) -> CompanyEvent:
    """Create a company event."""
    event = CompanyEvent(
        company_name=company_name,
        event_type=event_type,
        job_posting_id=job_posting_id,
        details=details
    )
    db.add(event)
    await db.commit()
    await db.refresh(event)
    return event


async def get_company_profile(
    db: AsyncSession,
    company_name: str
) -> Optional[CompanyProfile]:
    """Get company profile by name."""
    result = await db.execute(
        select(CompanyProfile).where(
            CompanyProfile.company_name == company_name
        )
    )
    return result.scalar_one_or_none()


async def upsert_company_profile(
    db: AsyncSession,
    company_name: str,
    profile_data: Dict[str, Any]
) -> CompanyProfile:
    """Create or update company profile."""
    existing = await get_company_profile(db, company_name)
    
    if existing:
        for key, value in profile_data.items():
            if hasattr(existing, key) and value is not None:
                setattr(existing, key, value)
        existing.last_enriched = datetime.now()
        await db.commit()
        await db.refresh(existing)
        return existing
    else:
        profile_data["company_name"] = company_name
        profile_data["last_enriched"] = datetime.now()
        profile = CompanyProfile(**profile_data)
        db.add(profile)
        await db.commit()
        await db.refresh(profile)
        return profile


async def get_job_posting_count(
    db: AsyncSession,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None
) -> int:
    """Get total job posting count."""
    query = select(func.count(JobPosting.id))
    
    if start_date:
        query = query.where(JobPosting.first_seen_date >= start_date)
    if end_date:
        query = query.where(JobPosting.first_seen_date <= end_date)
    
    result = await db.execute(query)
    return result.scalar()


async def get_hiring_trends(
    db: AsyncSession,
    days: int = 30
) -> List[Dict[str, Any]]:
    """Get hiring trends over time."""
    start_date = date.today() - timedelta(days=days)
    
    result = await db.execute(
        select(
            JobPosting.first_seen_date.label("date"),
            func.count(JobPosting.id).label("count")
        )
        .where(JobPosting.first_seen_date >= start_date)
        .group_by(JobPosting.first_seen_date)
        .order_by(JobPosting.first_seen_date)
    )
    
    return [
        {"date": row.date, "count": row.count}
        for row in result.all()
    ]
