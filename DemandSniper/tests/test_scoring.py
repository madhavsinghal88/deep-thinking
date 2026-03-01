import pytest
import asyncio
from datetime import date, timedelta

from utils.demand_scoring import calculate_demand_score, get_priority_tag, get_demand_score_breakdown


class TestDemandScoring:
    """Test demand scoring functionality."""
    
    def test_calculate_demand_score_default_weights(self):
        """Test demand score calculation with default weights."""
        # times_posted=1, days_open=0, number_of_openings=1
        # Expected: (1 * 2) + (0 / 10) + (1 * 3) = 2 + 0 + 3 = 5
        score = calculate_demand_score(1, 0, 1)
        assert score == 5.0
    
    def test_calculate_demand_score_with_days_open(self):
        """Test demand score with days open."""
        # times_posted=2, days_open=30, number_of_openings=1
        # Expected: (2 * 2) + (30 / 10) + (1 * 3) = 4 + 3 + 3 = 10
        score = calculate_demand_score(2, 30, 1)
        assert score == 10.0
    
    def test_calculate_demand_score_high_values(self):
        """Test demand score with high values."""
        # times_posted=5, days_open=100, number_of_openings=10
        # Expected: (5 * 2) + (100 / 10) + (10 * 3) = 10 + 10 + 30 = 50
        score = calculate_demand_score(5, 100, 10)
        assert score == 50.0
    
    def test_get_priority_tag_high(self):
        """Test high priority classification."""
        assert get_priority_tag(30) == "High"
        assert get_priority_tag(25) == "High"
    
    def test_get_priority_tag_medium(self):
        """Test medium priority classification."""
        assert get_priority_tag(15) == "Medium"
        assert get_priority_tag(10) == "Medium"
    
    def test_get_priority_tag_low(self):
        """Test low priority classification."""
        assert get_priority_tag(5) == "Low"
        assert get_priority_tag(0) == "Low"
    
    def test_get_demand_score_breakdown(self):
        """Test demand score breakdown."""
        result = get_demand_score_breakdown(2, 30, 3)
        
        assert "total_score" in result
        assert "priority" in result
        assert "components" in result
        
        # Check priority is correct
        expected_score = (2 * 2) + (30 / 10) + (3 * 3)  # 4 + 3 + 9 = 16
        assert result["total_score"] == expected_score
        assert result["priority"] == "Medium"


class TestDeduplication:
    """Test deduplication functionality."""
    
    def test_job_matcher_exact_match(self):
        """Test exact job matching."""
        from utils.deduplication import JobMatcher
        
        matcher = JobMatcher()
        
        # Exact match should return True
        assert matcher.is_match(
            "TechCorp", "Software Engineer",
            "TechCorp", "Software Engineer"
        ) == True
    
    def test_job_matcher_similar_titles(self):
        """Test similar job title matching."""
        from utils.deduplication import JobMatcher
        
        matcher = JobMatcher()
        
        # Similar titles should match (above threshold)
        result = matcher.get_match_details(
            "TechCorp", "Senior Software Engineer",
            "TechCorp", "Software Engineer Senior"
        )
        
        assert result["company_matches"] == True
        # Title similarity should be high
        assert result["title_similarity"] >= 80
    
    def test_job_matcher_different_companies(self):
        """Test different companies don't match."""
        from utils.deduplication import JobMatcher
        
        matcher = JobMatcher()
        
        # Different companies should not match
        assert matcher.is_match(
            "TechCorp", "Software Engineer",
            "OtherCorp", "Software Engineer"
        ) == False
    
    def test_normalize_company_name(self):
        """Test company name normalization."""
        from utils.deduplication import normalize_company_name
        
        assert normalize_company_name("TechCorp Inc.") == "techcorp"
        assert normalize_company_name("TechCorp LLC") == "techcorp"
        assert normalize_company_name("TechCorp Ltd.") == "techcorp"
    
    def test_extract_core_job_title(self):
        """Test job title extraction."""
        from utils.deduplication import extract_core_job_title
        
        assert extract_core_job_title("Senior Software Engineer") == "software engineer"
        assert extract_core_job_title("Software Engineer - Remote") == "software engineer"
