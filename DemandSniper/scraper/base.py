from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from datetime import date


@dataclass
class JobData:
    """Data class for job posting information."""
    company_name: str
    job_title: str
    location: Optional[str]
    country: str
    platform_source: str
    job_url: str
    posting_date: Optional[date]
    salary_range: Optional[str]
    number_of_openings: int = 1
    description: Optional[str] = None
    raw_data: Optional[Dict[str, Any]] = None


class BaseScraper(ABC):
    """Abstract base class for job scrapers."""
    
    def __init__(self, platform_name: str):
        self.platform_name = platform_name
        self.enabled = True
    
    @abstractmethod
    async def search(
        self,
        keywords: List[str],
        country: str,
        locations: List[str] = None,
        max_results: int = 100,
        **filters
    ) -> List[JobData]:
        """
        Search for jobs on the platform.
        
        Args:
            keywords: List of keywords to search for
            country: Target country
            locations: Optional list of specific locations
            max_results: Maximum number of results to return
            **filters: Additional platform-specific filters
        
        Returns:
            List of JobData objects
        """
        pass
    
    @abstractmethod
    async def parse_job(self, raw_data: Dict[str, Any]) -> Optional[JobData]:
        """
        Parse raw job data into JobData object.
        
        Args:
            raw_data: Raw job data from the platform
        
        Returns:
            JobData object or None if parsing fails
        """
        pass
    
    async def health_check(self) -> bool:
        """
        Check if the scraper is healthy and can make requests.
        
        Returns:
            True if healthy, False otherwise
        """
        return True
    
    def get_platform_config(self) -> Dict[str, Any]:
        """
        Get platform-specific configuration.
        
        Returns:
            Dictionary with configuration options
        """
        return {
            "name": self.platform_name,
            "enabled": self.enabled
        }
