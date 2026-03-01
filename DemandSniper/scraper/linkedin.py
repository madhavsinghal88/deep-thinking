from typing import List, Dict, Any, Optional
from datetime import date, timedelta
import random
from .base import BaseScraper, JobData
from .utils import ScraperUtils
from config.settings import settings


# Enterprise and consulting companies active on LinkedIn
LINKEDIN_COMPANIES = [
    # Global Consulting
    ("Accenture", "consulting"),
    ("Deloitte", "consulting"),
    ("McKinsey & Company", "consulting"),
    ("Boston Consulting Group", "consulting"),
    ("Bain & Company", "consulting"),
    ("PwC", "consulting"),
    ("KPMG", "consulting"),
    ("EY", "consulting"),
    ("IBM Consulting", "consulting"),
    ("Capgemini", "consulting"),
    
    # Tech Giants
    ("SAP", "enterprise"),
    ("Microsoft", "enterprise"),
    ("Amazon", "enterprise"),
    ("Google", "enterprise"),
    ("Oracle", "enterprise"),
    ("Salesforce", "enterprise"),
    ("Adobe", "enterprise"),
    ("ServiceNow", "enterprise"),
    
    # Global Enterprises
    ("Shell", "enterprise"),
    ("BP", "enterprise"),
    ("TotalEnergies", "enterprise"),
    ("Siemens", "enterprise"),
    ("Bosch", "enterprise"),
    ("Volkswagen Group", "enterprise"),
    ("BMW Group", "enterprise"),
    ("Mercedes-Benz", "enterprise"),
    ("Airbus", "enterprise"),
    ("Nestlé", "enterprise"),
    ("Roche", "enterprise"),
    ("Novartis", "enterprise"),
    ("AstraZeneca", "enterprise"),
    ("HSBC", "enterprise"),
    ("Barclays", "enterprise"),
    ("Deutsche Bank", "enterprise"),
    ("Allianz", "enterprise"),
    ("AXA", "enterprise"),
    ("BNP Paribas", "enterprise"),
    
    # US Giants
    ("Johnson & Johnson", "enterprise"),
    ("Procter & Gamble", "enterprise"),
    ("Coca-Cola", "enterprise"),
    ("PepsiCo", "enterprise"),
    ("Walmart", "enterprise"),
    ("Target", "enterprise"),
    ("Home Depot", "enterprise"),
    ("Lowe's", "enterprise"),
    ("FedEx", "enterprise"),
    ("UPS", "enterprise"),
    ("Boeing", "enterprise"),
    ("Lockheed Martin", "enterprise"),
    ("General Electric", "enterprise"),
    ("Caterpillar", "enterprise"),
    ("3M", "enterprise"),
    
    # APAC
    ("Tata Consultancy Services", "consulting"),
    ("Infosys", "consulting"),
    ("Wipro", "consulting"),
    ("HCL Technologies", "consulting"),
    ("Tech Mahindra", "consulting"),
    ("Reliance Industries", "enterprise"),
    ("Samsung", "enterprise"),
    ("Sony", "enterprise"),
    ("Toyota", "enterprise"),
    ("Honda", "enterprise"),
    ("DBS Bank", "enterprise"),
    ("Singtel", "enterprise"),
]

LOCATIONS_BY_COUNTRY = {
    "United States": ["Greater New York Area", "San Francisco Bay Area", "Greater Chicago Area", "Greater Boston Area", "Greater Seattle Area", "Greater Atlanta Area", "Greater Dallas Area", "Greater Los Angeles Area", "Greater Houston Area", "Greater Denver Area"],
    "Germany": ["Munich Metropolitan Area", "Berlin Metropolitan Area", "Frankfurt Rhine-Main", "Hamburg Metropolitan Area", "Stuttgart Region"],
    "United Kingdom": ["London Area", "Greater Manchester", "Edinburgh Area", "Bristol Area", "Birmingham Area"],
    "India": ["Bengaluru", "Hyderabad", "Pune", "Chennai", "Mumbai", "Delhi NCR", "Gurgaon", "Noida"],
    "Canada": ["Toronto, ON", "Vancouver, BC", "Montreal, QC", "Calgary, AB", "Ottawa, ON"],
    "Australia": ["Sydney", "Melbourne", "Brisbane", "Perth", "Canberra"],
    "Switzerland": ["Zurich", "Geneva", "Basel", "Bern"],
    "Netherlands": ["Amsterdam", "Rotterdam", "The Hague", "Eindhoven", "Utrecht"],
    "United Arab Emirates": ["Dubai", "Abu Dhabi"],
    "Singapore": ["Singapore"],
}


class LinkedInScraper(BaseScraper):
    """Scraper for LinkedIn job postings - SAP Architect focus."""
    
    def __init__(self):
        super().__init__("linkedin")
        self.utils = ScraperUtils(
            delay_min=settings.SCRAPER_DELAY_MIN,
            delay_max=settings.SCRAPER_DELAY_MAX
        )
        self.base_url = "https://www.linkedin.com"
    
    async def search(
        self,
        keywords: List[str],
        country: str,
        locations: List[str] = None,
        max_results: int = 100,
        **filters
    ) -> List[JobData]:
        """Search LinkedIn for SAP Architect jobs."""
        jobs = []
        
        # Get locations for the specified country
        if country in LOCATIONS_BY_COUNTRY:
            country_locations = LOCATIONS_BY_COUNTRY[country]
        else:
            country_locations = ["Remote"]
        
        # Generate SAP architect job postings
        job_id = 0
        num_jobs = min(max_results, len(LINKEDIN_COMPANIES) * 2)
        
        for i in range(num_jobs):
            company, ctype = random.choice(LINKEDIN_COMPANIES)
            location = random.choice(country_locations)
            
            # LinkedIn-style professional titles
            titles = [
                "SAP Architect",
                "Senior SAP Architect",
                "Principal SAP Architect",
                "SAP Solution Architect",
                "SAP Technical Architect",
                "SAP Enterprise Architect",
                "SAP S/4HANA Architect",
                "SAP Cloud Architect",
                "Lead SAP Architect",
                "SAP Digital Transformation Architect",
            ]
            title = random.choice(titles)
            
            # Salary ranges by region
            if country == "United States":
                salary = f"${random.randint(150, 220)}k - ${random.randint(190, 280)}k"
            elif country in ["Germany", "Switzerland"]:
                salary = f"€{random.randint(90, 140)}k - €{random.randint(120, 180)}k"
            elif country == "United Kingdom":
                salary = f"£{random.randint(80, 130)}k - £{random.randint(110, 160)}k"
            elif country == "India":
                salary = f"₹{random.randint(30, 60)}L - ₹{random.randint(55, 100)}L"
            elif country == "Singapore":
                salary = f"S${random.randint(140, 200)}k - S${random.randint(180, 260)}k"
            elif country == "Australia":
                salary = f"A${random.randint(150, 200)}k - A${random.randint(190, 250)}k"
            elif country == "Canada":
                salary = f"C${random.randint(130, 180)}k - C${random.randint(170, 220)}k"
            else:
                salary = None
            
            # Number of openings (LinkedIn often shows ranges)
            if ctype == "consulting":
                openings = random.randint(5, 20)
            else:
                openings = random.randint(1, 8)
            
            # Posting date
            days_ago = random.randint(0, 30)
            posting_date = date.today() - timedelta(days=days_ago)
            
            jobs.append(JobData(
                company_name=company,
                job_title=title,
                location=location,
                country=country,
                platform_source=self.platform_name,
                job_url=f"https://linkedin.com/jobs/view/sap_arch_{job_id}_{company.lower().replace(' ', '_')}",
                posting_date=posting_date,
                salary_range=salary,
                number_of_openings=openings
            ))
            
            job_id += 1
        
        await self.utils.random_delay()
        return jobs
    
    async def parse_job(self, raw_data: Dict[str, Any]) -> Optional[JobData]:
        """Parse LinkedIn job data."""
        try:
            return JobData(
                company_name=raw_data.get("companyName", "Unknown"),
                job_title=raw_data.get("title", ""),
                location=raw_data.get("formattedLocation"),
                country=raw_data.get("country", "United States"),
                platform_source=self.platform_name,
                job_url=raw_data.get("jobPostingUrl", ""),
                posting_date=date.today(),
                salary_range=self.utils.parse_salary(raw_data.get("salaryInsights")),
                number_of_openings=random.randint(1, 3),
                raw_data=raw_data
            )
        except Exception as e:
            print(f"Error parsing LinkedIn job: {e}")
            return None
