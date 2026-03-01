import pytest
import asyncio

# Configure pytest-asyncio
pytest_plugins = ('pytest_asyncio',)

@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest.fixture(scope="function")
async def db_session():
    """Create a database session for testing."""
    # This would create a test database session
    # For now, return None
    yield None

@pytest.fixture
def sample_job_data():
    """Provide sample job data for tests."""
    from datetime import date
    
    return {
        "company_name": "TestCorp",
        "job_title": "Software Engineer",
        "country": "United States",
        "platform_source": "indeed",
        "job_url": "https://example.com/job/1",
        "posting_date": date.today(),
        "salary_range": "$100k - $150k",
        "number_of_openings": 2
    }

@pytest.fixture
def sample_company_data():
    """Provide sample company data for tests."""
    return {
        "company_name": "TestCorp",
        "industry": "Technology",
        "company_size": "51-200",
        "headquarters": "San Francisco, CA",
        "website": "https://testcorp.com"
    }
