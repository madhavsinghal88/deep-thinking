from datetime import date, datetime
from typing import Optional, List
from pydantic import BaseModel, Field, HttpUrl


# Job Schemas
class JobBase(BaseModel):
    company_name: str = Field(..., min_length=1, max_length=255)
    job_title: str = Field(..., min_length=1, max_length=500)
    location: Optional[str] = Field(None, max_length=255)
    country: str = Field(..., min_length=1, max_length=100)
    platform_source: str = Field(..., min_length=1, max_length=50)
    posting_date: Optional[date] = None
    job_url: HttpUrl
    salary_range: Optional[str] = Field(None, max_length=255)
    number_of_openings: int = Field(default=1, ge=1)


class JobCreate(JobBase):
    pass


class JobUpdate(BaseModel):
    company_name: Optional[str] = Field(None, min_length=1, max_length=255)
    job_title: Optional[str] = Field(None, min_length=1, max_length=500)
    location: Optional[str] = Field(None, max_length=255)
    country: Optional[str] = Field(None, min_length=1, max_length=100)
    platform_source: Optional[str] = Field(None, min_length=1, max_length=50)
    posting_date: Optional[date] = None
    job_url: Optional[HttpUrl] = None
    salary_range: Optional[str] = Field(None, max_length=255)
    number_of_openings: Optional[int] = Field(None, ge=1)


class JobResponse(JobBase):
    id: int
    first_seen_date: date
    last_seen_date: date
    times_posted: int
    days_open: int
    demand_score: float
    priority_tag: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# Company Schemas
class CompanySummary(BaseModel):
    company_name: str
    total_jobs: int
    total_demand_score: float
    highest_priority: str
    last_active: Optional[date]
    total_openings: int


class CompanyProfileBase(BaseModel):
    industry: Optional[str] = None
    company_size: Optional[str] = None
    headquarters: Optional[str] = None
    website: Optional[HttpUrl] = None
    linkedin_url: Optional[HttpUrl] = None
    description: Optional[str] = None


class CompanyProfileCreate(CompanyProfileBase):
    company_name: str = Field(..., min_length=1, max_length=255)


class CompanyProfileResponse(CompanyProfileBase):
    id: int
    company_name: str
    enrichment_source: Optional[str]
    last_enriched: Optional[date]
    created_at: date
    updated_at: date

    class Config:
        from_attributes = True


class CompanyDetail(CompanySummary):
    profile: Optional[CompanyProfileResponse]
    recent_jobs: List[JobResponse]


# Event/Timeline Schemas
class CompanyEventResponse(BaseModel):
    id: int
    company_name: str
    event_type: str
    event_date: date
    details: Optional[dict]

    class Config:
        from_attributes = True


# Filter/Query Schemas
class JobFilter(BaseModel):
    country: Optional[str] = None
    skill_keyword: Optional[str] = None
    platform: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    company_name: Optional[str] = None
    priority: Optional[str] = None
    skip: int = Field(default=0, ge=0)
    limit: int = Field(default=100, ge=1, le=1000)


class CompanyFilter(BaseModel):
    country: Optional[str] = None
    min_demand_score: float = Field(default=0, ge=0)
    limit: int = Field(default=50, ge=1, le=200)


# Analytics Schemas
class HiringTrend(BaseModel):
    date: date
    count: int


class TopCompany(BaseModel):
    company_name: str
    total_demand_score: float
    highest_priority: str
    total_openings: int


class DemandScoreBreakdown(BaseModel):
    total_score: float
    priority: str
    components: dict


# Scraper Schemas
class ScraperStatus(BaseModel):
    running: bool
    jobs: List[dict]


class ScraperRunRequest(BaseModel):
    platforms: Optional[List[str]] = None


class ScraperRunResponse(BaseModel):
    platforms: dict
    total_jobs_found: int
    new_jobs: int
    republished_jobs: int
    errors: List[str]


# Configuration Schemas
class SearchConfig(BaseModel):
    target_country: str
    skill_keywords: List[str]
    job_title_keywords: List[str]
    platforms: List[str]
    search_frequency: str
    date_range_filter: int
    max_results_per_platform: int
    locations: List[str]
    exclude_keywords: List[str]


class ScoringFormula(BaseModel):
    times_posted_weight: int
    days_open_divisor: int
    openings_weight: int


class PriorityThresholds(BaseModel):
    high: int
    medium: int
    low: int


class ScoringConfig(BaseModel):
    demand_score_formula: ScoringFormula
    priority_thresholds: PriorityThresholds
    repost_detection_window_days: int
    similarity_thresholds: dict
    notifications: dict
    scoring: dict


# Export Schema
class ExportResponse(BaseModel):
    filename: str
    filepath: str
    record_count: int
