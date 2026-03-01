from datetime import datetime, date
from typing import Optional, List
from sqlalchemy import (
    Column, Integer, String, DateTime, Date, Float, 
    Text, JSON, ForeignKey, Index, create_engine
)
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.sql import func

from config.settings import settings

Base = declarative_base()


class JobPosting(Base):
    __tablename__ = "job_postings"
    
    id = Column(Integer, primary_key=True, index=True)
    company_name = Column(String(255), nullable=False, index=True)
    job_title = Column(String(500), nullable=False)
    location = Column(String(255), nullable=True)
    country = Column(String(100), nullable=False, index=True)
    platform_source = Column(String(50), nullable=False, index=True)
    posting_date = Column(Date, nullable=True)
    job_url = Column(String(1000), unique=True, nullable=False)
    salary_range = Column(String(255), nullable=True)
    
    # Tracking fields
    first_seen_date = Column(Date, nullable=False, default=date.today)
    last_seen_date = Column(Date, nullable=False, default=date.today)
    times_posted = Column(Integer, default=1, nullable=False)
    number_of_openings = Column(Integer, default=1, nullable=False)
    days_open = Column(Integer, default=0, nullable=False)
    demand_score = Column(Float, default=0.0, nullable=False)
    priority_tag = Column(String(20), default="Low", nullable=False)
    
    # Metadata
    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)
    
    # Relationships
    score_history = relationship("DemandScoreHistory", back_populates="job", cascade="all, delete-orphan")
    company_events = relationship("CompanyEvent", back_populates="job", cascade="all, delete-orphan")
    
    # Indexes for common queries
    __table_args__ = (
        Index('idx_company_country', 'company_name', 'country'),
        Index('idx_demand_score', 'demand_score'),
        Index('idx_priority', 'priority_tag'),
    )


class CompanyProfile(Base):
    __tablename__ = "company_profiles"
    
    id = Column(Integer, primary_key=True, index=True)
    company_name = Column(String(255), unique=True, nullable=False, index=True)
    industry = Column(String(255), nullable=True)
    company_size = Column(String(50), nullable=True)  # "1-50", "51-200", etc.
    headquarters = Column(String(255), nullable=True)
    website = Column(String(500), nullable=True)
    linkedin_url = Column(String(500), nullable=True)
    description = Column(Text, nullable=True)
    enrichment_source = Column(String(100), nullable=True)
    last_enriched = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())


class DemandScoreHistory(Base):
    __tablename__ = "demand_score_history"
    
    id = Column(Integer, primary_key=True, index=True)
    job_posting_id = Column(Integer, ForeignKey("job_postings.id"), nullable=False)
    date = Column(Date, nullable=False)
    demand_score = Column(Float, nullable=False)
    times_posted = Column(Integer, nullable=False)
    days_open = Column(Integer, nullable=False)
    number_of_openings = Column(Integer, nullable=False)
    
    job = relationship("JobPosting", back_populates="score_history")
    
    __table_args__ = (
        Index('idx_job_date', 'job_posting_id', 'date'),
    )


class CompanyEvent(Base):
    __tablename__ = "company_events"
    
    id = Column(Integer, primary_key=True, index=True)
    company_name = Column(String(255), nullable=False, index=True)
    event_type = Column(String(50), nullable=False)  # "job_posted", "repost_detected", "demand_spike"
    event_date = Column(DateTime, default=func.now(), nullable=False)
    job_posting_id = Column(Integer, ForeignKey("job_postings.id"), nullable=True)
    details = Column(JSON, nullable=True)
    
    job = relationship("JobPosting", back_populates="company_events")
    
    __table_args__ = (
        Index('idx_company_event_date', 'company_name', 'event_date'),
    )


# Database connection setup
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,
    future=True
)

async_session_maker = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)


async def init_db():
    """Initialize database tables."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def get_db() -> AsyncSession:
    """Dependency to get database session."""
    async with async_session_maker() as session:
        try:
            yield session
        finally:
            await session.close()
