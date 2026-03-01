import httpx
import asyncio
from typing import List, Dict, Any, Optional
from datetime import date, timedelta
import random

from scraper.base import BaseScraper, JobData


class AdzunaScraper(BaseScraper):
    """
    Scraper for Adzuna API - Covers UK, DE, AU, NL, SG, and more.
    
    Adzuna has a public API with generous free tier:
    - 250 requests/day on free tier
    - Covers 16 countries
    - Good for: UK, Germany, Australia, Netherlands, Singapore, etc.
    
    Get API keys at: https://developer.adzuna.com/
    """
    
    def __init__(self, app_id: str = None, api_key: str = None):
        super().__init__("adzuna")
        self.app_id = app_id or "YOUR_ADZUNA_APP_ID"
        self.api_key = api_key or "YOUR_ADZUNA_API_KEY"
        self.base_url = "https://api.adzuna.com/v1/api/jobs"
        
        # Country codes for Adzuna
        self.country_codes = {
            "United Kingdom": "gb",
            "Germany": "de",
            "Australia": "au",
            "Netherlands": "nl",
            "Singapore": "sg",
            "United States": "us",
            "Canada": "ca",
            "France": "fr",
            "Spain": "es",
            "Italy": "it",
            "Switzerland": "ch",
            "India": "in",
            "Brazil": "br",
            "Poland": "pl",
            "Russia": "ru",
        }
    
    async def search(
        self,
        keywords: List[str],
        country: str,
        locations: List[str] = None,
        max_results: int = 50,
        **filters
    ) -> List[JobData]:
        """Search Adzuna API for SAP jobs."""
        jobs = []
        
        # Check if country is supported
        if country not in self.country_codes:
            return jobs
        
        country_code = self.country_codes[country]
        
        # Build search query
        what = "SAP Architect"  # Main keyword
        
        try:
            async with httpx.AsyncClient() as client:
                url = f"{self.base_url}/{country_code}/search/1"
                params = {
                    "app_id": self.app_id,
                    "app_key": self.api_key,
                    "what": what,
                    "max_days_old": 30,
                    "sort_by": "date",
                    "sort_direction": "down",
                    "results_per_page": min(max_results, 50),  # API limit
                }
                
                response = await client.get(url, params=params, timeout=30.0)
                
                if response.status_code == 200:
                    data = response.json()
                    results = data.get("results", [])
                    
                    for result in results:
                        job = self._parse_adzuna_job(result, country)
                        if job:
                            jobs.append(job)
                else:
                    print(f"Adzuna API error: {response.status_code} - {response.text}")
                    
        except Exception as e:
            print(f"Error searching Adzuna: {e}")
        
        return jobs
    
    def _parse_adzuna_job(self, data: Dict[str, Any], country: str) -> Optional[JobData]:
        """Parse Adzuna job data."""
        try:
            # Extract company
            company = data.get("company", {}).get("display_name", "Unknown")
            if not company or company == "Unknown":
                company = data.get("company", {}).get("name", "Unknown")
            
            # Extract title
            title = data.get("title", "SAP Architect")
            
            # Extract location
            location_data = data.get("location", {})
            location = location_data.get("display_name", "")
            
            # Extract salary
            salary_min = data.get("salary_min")
            salary_max = data.get("salary_max")
            salary_currency = data.get("salary_currency", "USD")
            
            if salary_min and salary_max:
                salary_range = f"{salary_currency} {int(salary_min):,} - {int(salary_max):,}"
            else:
                salary_range = data.get("salary", "")
            
            # Extract posting date
            created_at = data.get("created_at", "")
            try:
                posting_date = date.fromisoformat(created_at.split("T")[0])
            except:
                posting_date = date.today()
            
            # Get redirect URL
            job_url = data.get("redirect_url", "")
            
            return JobData(
                company_name=company,
                job_title=title,
                location=location,
                country=country,
                platform_source="adzuna",
                job_url=job_url,
                posting_date=posting_date,
                salary_range=salary_range if salary_range else None,
                number_of_openings=1,  # Adzuna doesn't provide this
                raw_data=data
            )
        except Exception as e:
            print(f"Error parsing Adzuna job: {e}")
            return None


class IndeedPublisherScraper(BaseScraper):
    """
    Scraper using Indeed Publisher API.
    
    Note: Indeed Publisher API requires:
    1. Publisher ID (free to get)
    2. Approval for some features
    
    Sign up: https://www.indeed.com/publisher
    
    The API returns XML by default, but we can request JSON.
    """
    
    def __init__(self, publisher_id: str = None):
        super().__init__("indeed_api")
        self.publisher_id = publisher_id or "YOUR_INDEED_PUBLISHER_ID"
        self.base_url = "https://api.indeed.com/ads/apisearch"
    
    async def search(
        self,
        keywords: List[str],
        country: str,
        locations: List[str] = None,
        max_results: int = 25,
        **filters
    ) -> List[JobData]:
        """Search Indeed Publisher API."""
        jobs = []
        
        # Map countries to Indeed country codes
        country_codes = {
            "United States": "us",
            "United Kingdom": "gb",
            "Germany": "de",
            "Canada": "ca",
            "Australia": "au",
            "India": "in",
        }
        
        if country not in country_codes:
            return jobs
        
        country_code = country_codes[country]
        location = locations[0] if locations else ""
        
        try:
            async with httpx.AsyncClient() as client:
                params = {
                    "publisher": self.publisher_id,
                    "q": "SAP Architect",
                    "l": location,
                    "sort": "date",
                    "radius": "50",
                    "st": "employer",  # Direct employer jobs
                    "limit": min(max_results, 25),
                    "fromage": "30",
                    "filter": "1",
                    "latlong": "1",
                    "co": country_code,
                    "userip": "1.2.3.4",
                    "useragent": "Mozilla/5.0",
                    "v": "2",
                    "format": "json",
                }
                
                response = await client.get(self.base_url, params=params, timeout=30.0)
                
                if response.status_code == 200:
                    data = response.json()
                    results = data.get("results", [])
                    
                    for result in results:
                        job = self._parse_indeed_job(result, country)
                        if job:
                            jobs.append(job)
                else:
                    print(f"Indeed API error: {response.status_code}")
                    
        except Exception as e:
            print(f"Error searching Indeed API: {e}")
        
        return jobs
    
    def _parse_indeed_job(self, data: Dict[str, Any], country: str) -> Optional[JobData]:
        """Parse Indeed job data."""
        try:
            company = data.get("company", "Unknown")
            title = data.get("jobtitle", "SAP Architect")
            location = data.get("formattedLocation", "")
            
            # Indeed doesn't provide salary in basic API
            salary_range = None
            
            # Parse date
            date_str = data.get("date", "")
            try:
                # Format: Mon, 01 Jan 2024 00:00:00 GMT
                posting_date = date.today()  # Simplified
            except:
                posting_date = date.today()
            
            # Build job URL
            jobkey = data.get("jobkey", "")
            job_url = f"https://www.indeed.com/viewjob?jk={jobkey}"
            
            return JobData(
                company_name=company,
                job_title=title,
                location=location,
                country=country,
                platform_source="indeed",
                job_url=job_url,
                posting_date=posting_date,
                salary_range=salary_range,
                number_of_openings=1,
                raw_data=data
            )
        except Exception as e:
            print(f"Error parsing Indeed job: {e}")
            return None


class LinkedInAPITracker(BaseScraper):
    """
    LinkedIn Job Search API (Requires OAuth 2.0)
    
    Note: LinkedIn's API is very restrictive. You need:
    1. LinkedIn Developer Account
    2. OAuth 2.0 tokens
    3. Marketing Developer Platform access for job posting APIs
    
    This implementation provides the structure but requires valid tokens.
    
    Alternative: Use LinkedIn Job Search widget or scraping (with caution)
    """
    
    def __init__(self, access_token: str = None):
        super().__init__("linkedin_api")
        self.access_token = access_token or "YOUR_LINKEDIN_ACCESS_TOKEN"
        self.base_url = "https://api.linkedin.com/v2"
    
    async def search(
        self,
        keywords: List[str],
        country: str,
        locations: List[str] = None,
        max_results: int = 25,
        **filters
    ) -> List[JobData]:
        """
        Search LinkedIn jobs.
        
        Note: This requires OAuth 2.0 and specific LinkedIn API permissions.
        The basic access doesn't include job search.
        """
        jobs = []
        
        # LinkedIn API requires special permissions for job search
        # This is a placeholder for the API structure
        print("LinkedIn API: Requires OAuth 2.0 and partnership agreement")
        print("Consider using LinkedIn Job Search widget or careful scraping instead")
        
        return jobs


class JSearchRapidAPI(BaseScraper):
    """
    JSearch API via RapidAPI (Real-time job aggregator)
    
    This is a paid API that aggregates jobs from multiple sources including:
    - LinkedIn
    - Indeed  
    - Glassdoor
    - ZipRecruiter
    
    Website: https://rapidapi.com/letscrape-6bRBa3QguO5/api/jsearch
    Cost: Free tier available (100 requests/month)
    """
    
    def __init__(self, api_key: str = None):
        super().__init__("jsearch")
        self.api_key = api_key or "YOUR_RAPIDAPI_KEY"
        self.base_url = "https://jsearch.p.rapidapi.com"
        self.headers = {
            "X-RapidAPI-Key": self.api_key,
            "X-RapidAPI-Host": "jsearch.p.rapidapi.com"
        }
    
    async def search(
        self,
        keywords: List[str],
        country: str,
        locations: List[str] = None,
        max_results: int = 10,
        **filters
    ) -> List[JobData]:
        """Search JSearch API."""
        jobs = []
        
        # Map countries to JSearch format
        country_map = {
            "United States": "US",
            "United Kingdom": "UK",
            "Germany": "DE",
            "Canada": "CA",
            "Australia": "AU",
            "India": "IN",
            "Singapore": "SG",
            "Switzerland": "CH",
            "Netherlands": "NL",
        }
        
        country_code = country_map.get(country, "US")
        
        try:
            async with httpx.AsyncClient() as client:
                query = "SAP Architect"
                location = locations[0] if locations else country
                
                url = f"{self.base_url}/search"
                querystring = {
                    "query": f"{query} in {location}",
                    "page": "1",
                    "num_pages": "1",
                }
                
                response = await client.get(
                    url, 
                    headers=self.headers, 
                    params=querystring,
                    timeout=30.0
                )
                
                if response.status_code == 200:
                    data = response.json()
                    results = data.get("data", [])
                    
                    for result in results[:max_results]:
                        job = self._parse_jsearch_job(result, country)
                        if job:
                            jobs.append(job)
                else:
                    print(f"JSearch API error: {response.status_code}")
                    
        except Exception as e:
            print(f"Error searching JSearch: {e}")
        
        return jobs
    
    def _parse_jsearch_job(self, data: Dict[str, Any], country: str) -> Optional[JobData]:
        """Parse JSearch job data."""
        try:
            employer = data.get("employer_name", "Unknown")
            title = data.get("job_title", "SAP Architect")
            location = data.get("job_city", "") + ", " + data.get("job_country", "")
            
            # Salary info
            salary_min = data.get("job_min_salary")
            salary_max = data.get("job_max_salary")
            salary_period = data.get("job_salary_period", "year")
            
            if salary_min and salary_max:
                salary_range = f"${salary_min:,} - ${salary_max:,} / {salary_period}"
            else:
                salary_range = data.get("job_salary", None)
            
            # Parse date
            date_posted = data.get("job_posted_at_datetime_utc", "")
            try:
                posting_date = date.fromisoformat(date_posted.split("T")[0])
            except:
                posting_date = date.today()
            
            job_url = data.get("job_apply_link", "")
            
            return JobData(
                company_name=employer,
                job_title=title,
                location=location,
                country=country,
                platform_source=data.get("job_publisher", "jsearch").lower(),
                job_url=job_url,
                posting_date=posting_date,
                salary_range=salary_range,
                number_of_openings=1,
                raw_data=data
            )
        except Exception as e:
            print(f"Error parsing JSearch job: {e}")
            return None


class MockRealisticScraper(BaseScraper):
    """
    Generates realistic mock data for demonstration when APIs aren't available.
    This uses the real company and job data but generates mock postings.
    """
    
    def __init__(self):
        super().__init__("realistic_mock")
    
    async def search(
        self,
        keywords: List[str],
        country: str,
        locations: List[str] = None,
        max_results: int = 50,
        **filters
    ) -> List[JobData]:
        """Generate realistic mock SAP job data."""
        # Import from indeed.py which has all the company data
        from scraper.indeed import TOP_SAP_COMPANIES, LOCATIONS
        
        jobs = []
        
        # Get locations for this country
        country_locations = LOCATIONS.get(country, ["Remote"])
        
        # Filter to consulting and enterprise companies
        companies = TOP_SAP_COMPANIES[:min(60, len(TOP_SAP_COMPANIES))]
        
        # Weight consulting firms higher
        weighted_companies = []
        for company, ctype in companies:
            if ctype == "consulting":
                weighted_companies.extend([company] * 4)  # 4x weight for consulting
            else:
                weighted_companies.append(company)
        
        # SAP job titles
        titles = [
            "SAP Architect",
            "SAP Technical Architect", 
            "SAP Solution Architect",
            "SAP Enterprise Architect",
            "Senior SAP Architect",
            "Lead SAP Architect",
            "Principal SAP Architect",
            "SAP S/4HANA Architect",
            "SAP Cloud Architect",
            "SAP Integration Architect",
        ]
        
        # Generate jobs
        for i in range(min(max_results, len(weighted_companies))):
            company = random.choice(weighted_companies)
            location = random.choice(country_locations)
            title = random.choice(titles)
            
            # Realistic salary by country
            salary_ranges = {
                "United States": (140000, 260000),
                "Germany": (80000, 150000),
                "United Kingdom": (70000, 160000),
                "India": (2500000, 10000000),  # INR
                "Canada": (110000, 220000),
                "Australia": (130000, 250000),
                "Switzerland": (120000, 200000),
                "Netherlands": (80000, 140000),
                "United Arab Emirates": (25000, 55000),  # Monthly
                "Singapore": (120000, 260000),
            }
            
            if country in salary_ranges:
                min_sal, max_sal = salary_ranges[country]
                if country == "India":
                    salary = f"₹{int(min_sal/100000)}L - ₹{int(max_sal/100000)}L"
                elif country == "United Arab Emirates":
                    salary = f"AED {min_sal:,} - {max_sal:,} / month"
                else:
                    currency = "$" if country in ["United States", "Canada", "Australia", "Singapore"] else "€" if country in ["Germany", "Netherlands"] else "£"
                    salary = f"{currency}{min_sal:,} - {currency}{max_sal:,}"
            else:
                salary = None
            
            # Determine openings (consulting firms hire more)
            is_consulting = company in [c for c, t in companies if t == "consulting"]
            openings = random.randint(3, 20) if is_consulting else random.randint(1, 5)
            
            # Posting date within last 30 days
            days_ago = random.randint(0, 30)
            posting_date = date.today() - timedelta(days=days_ago)
            
            jobs.append(JobData(
                company_name=company,
                job_title=title,
                location=location,
                country=country,
                platform_source=random.choice(["linkedin", "indeed", "company_careers"]),
                job_url=f"https://example.com/job/{company.replace(' ', '_').lower()}_{i}",
                posting_date=posting_date,
                salary_range=salary,
                number_of_openings=openings
            ))
        
        await asyncio.sleep(0.1)  # Simulate API delay
        return jobs
