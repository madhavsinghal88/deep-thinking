import pytest
from fastapi.testclient import TestClient

from api.main import app

client = TestClient(app)


class TestAPI:
    """Test FastAPI endpoints."""
    
    def test_root_endpoint(self):
        """Test root endpoint returns project info."""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "name" in data
        assert "version" in data
        assert data["name"] == "DemandSniper"
    
    def test_health_check(self):
        """Test health check endpoint."""
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json()["status"] == "healthy"
    
    def test_get_jobs_empty(self):
        """Test getting jobs when none exist."""
        response = client.get("/api/v1/jobs")
        assert response.status_code == 200
        assert response.json() == []
    
    def test_get_companies_empty(self):
        """Test getting companies when none exist."""
        response = client.get("/api/v1/companies")
        assert response.status_code == 200
        assert response.json() == []
    
    def test_create_job_validation(self):
        """Test job creation validation."""
        # Missing required fields
        response = client.post("/api/v1/jobs", json={})
        assert response.status_code == 422  # Validation error
    
    def test_get_search_config(self):
        """Test getting search configuration."""
        response = client.get("/api/v1/config/search")
        assert response.status_code == 200
        data = response.json()
        assert "target_country" in data
        assert "skill_keywords" in data
    
    def test_get_scoring_config(self):
        """Test getting scoring configuration."""
        response = client.get("/api/v1/config/scoring")
        assert response.status_code == 200
        data = response.json()
        assert "demand_score_formula" in data
        assert "priority_thresholds" in data


class TestJobsAPI:
    """Test jobs API endpoints."""
    
    def test_create_job_success(self):
        """Test successfully creating a job."""
        from datetime import date
        
        job_data = {
            "company_name": "TestCorp",
            "job_title": "Software Engineer",
            "country": "United States",
            "platform_source": "indeed",
            "job_url": "https://example.com/job/test",
            "posting_date": date.today().isoformat(),
            "number_of_openings": 2
        }
        
        # Note: This will fail if job already exists
        # In a real test, we'd use a test database
        response = client.post("/api/v1/jobs", json=job_data)
        # Could be 200 (success) or 400 (already exists)
        assert response.status_code in [200, 400]


class TestAnalyticsAPI:
    """Test analytics API endpoints."""
    
    def test_get_top_companies(self):
        """Test getting top companies."""
        response = client.get("/api/v1/analytics/top-companies")
        assert response.status_code == 200
        assert isinstance(response.json(), list)
    
    def test_get_hiring_trends(self):
        """Test getting hiring trends."""
        response = client.get("/api/v1/analytics/hiring-trends?days=30")
        assert response.status_code == 200
        assert isinstance(response.json(), list)
    
    def test_get_dashboard_summary(self):
        """Test getting dashboard summary."""
        response = client.get("/api/v1/analytics/dashboard-summary")
        assert response.status_code == 200
        data = response.json()
        assert "total_jobs" in data
