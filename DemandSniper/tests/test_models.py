import pytest
from datetime import date


class TestJobPosting:
    """Test job posting model and operations."""
    
    @pytest.mark.asyncio
    async def test_create_job_posting(self):
        """Test creating a job posting."""
        # This would test the actual database operations
        # For now, we test the model structure
        from database.models import JobPosting
        
        job = JobPosting(
            company_name="TestCorp",
            job_title="Test Engineer",
            country="United States",
            platform_source="indeed",
            job_url="https://example.com/job/1",
            first_seen_date=date.today(),
            last_seen_date=date.today()
        )
        
        assert job.company_name == "TestCorp"
        assert job.job_title == "Test Engineer"
        assert job.times_posted == 1
        assert job.priority_tag == "Low"
    
    @pytest.mark.asyncio
    async def test_job_posting_defaults(self):
        """Test job posting default values."""
        from database.models import JobPosting
        
        job = JobPosting(
            company_name="TestCorp",
            job_title="Test Engineer",
            country="United States",
            platform_source="indeed",
            job_url="https://example.com/job/1"
        )
        
        assert job.times_posted == 1
        assert job.number_of_openings == 1
        assert job.demand_score == 0.0


class TestCompanyProfile:
    """Test company profile model."""
    
    def test_company_profile_creation(self):
        """Test creating a company profile."""
        from database.models import CompanyProfile
        
        profile = CompanyProfile(
            company_name="TestCorp",
            industry="Technology",
            company_size="51-200",
            headquarters="San Francisco, CA"
        )
        
        assert profile.company_name == "TestCorp"
        assert profile.industry == "Technology"
