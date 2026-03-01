from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from database import (
    get_db, 
    get_companies_by_demand_score,
    get_company_timeline,
    get_company_profile,
    upsert_company_profile
)
from api.schemas import (
    CompanySummary, CompanyDetail, CompanyEventResponse,
    CompanyProfileCreate, CompanyProfileResponse
)

router = APIRouter(prefix="/companies", tags=["companies"])


@router.get("", response_model=List[CompanySummary])
async def list_companies(
    country: Optional[str] = Query(None),
    min_demand_score: float = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=200),
    db: AsyncSession = Depends(get_db)
):
    """Get companies sorted by total demand score."""
    companies = await get_companies_by_demand_score(
        db,
        limit=limit,
        country=country,
        min_demand_score=min_demand_score
    )
    return companies


@router.get("/{company_name}", response_model=CompanyDetail)
async def get_company(
    company_name: str,
    db: AsyncSession = Depends(get_db)
):
    """Get detailed information about a company."""
    from sqlalchemy import select
    from database.models import JobPosting
    from database import get_jobs_filtered
    
    # Get company summary
    companies = await get_companies_by_demand_score(
        db,
        limit=1,
        min_demand_score=0
    )
    
    company_summary = None
    for c in companies:
        if c["company_name"] == company_name:
            company_summary = c
            break
    
    if not company_summary:
        raise HTTPException(status_code=404, detail="Company not found")
    
    # Get profile
    profile = await get_company_profile(db, company_name)
    
    # Get recent jobs
    recent_jobs = await get_jobs_filtered(
        db,
        company_name=company_name,
        limit=10
    )
    
    return CompanyDetail(
        **company_summary,
        profile=profile,
        recent_jobs=recent_jobs
    )


@router.get("/{company_name}/timeline", response_model=List[CompanyEventResponse])
async def get_company_timeline_endpoint(
    company_name: str,
    limit: int = Query(100, ge=1, le=500),
    db: AsyncSession = Depends(get_db)
):
    """Get event timeline for a company."""
    events = await get_company_timeline(db, company_name, limit)
    return events


@router.get("/{company_name}/profile", response_model=CompanyProfileResponse)
async def get_company_profile_endpoint(
    company_name: str,
    db: AsyncSession = Depends(get_db)
):
    """Get enriched profile for a company."""
    profile = await get_company_profile(db, company_name)
    
    if not profile:
        raise HTTPException(
            status_code=404, 
            detail="Company profile not found. Create one using POST /companies/{name}/profile"
        )
    
    return profile


@router.post("/{company_name}/profile", response_model=CompanyProfileResponse)
async def create_or_update_company_profile(
    company_name: str,
    profile: CompanyProfileCreate,
    db: AsyncSession = Depends(get_db)
):
    """Create or update company profile."""
    profile_data = profile.dict(exclude={"company_name"})
    
    # Convert URLs to strings
    if profile_data.get("website"):
        profile_data["website"] = str(profile_data["website"])
    if profile_data.get("linkedin_url"):
        profile_data["linkedin_url"] = str(profile_data["linkedin_url"])
    
    updated_profile = await upsert_company_profile(
        db,
        company_name,
        profile_data
    )
    
    return updated_profile


@router.post("/{company_name}/enrich")
async def enrich_company(
    company_name: str,
    db: AsyncSession = Depends(get_db)
):
    """Trigger company enrichment from external sources."""
    from utils.enrichment import enrich_company_data
    
    enriched_data = await enrich_company_data(company_name)
    
    # Save enriched data
    profile_data = {
        "industry": enriched_data.get("industry"),
        "company_size": enriched_data.get("company_size"),
        "headquarters": enriched_data.get("headquarters"),
        "website": enriched_data.get("website"),
        "linkedin_url": enriched_data.get("linkedin_url"),
        "description": enriched_data.get("description"),
        "enrichment_source": enriched_data.get("enrichment_source")
    }
    
    profile = await upsert_company_profile(db, company_name, profile_data)
    
    return {
        "message": f"Company '{company_name}' enriched successfully",
        "source": enriched_data.get("enrichment_source"),
        "profile": profile
    }
