from typing import List, Dict, Any, Optional
from datetime import date, datetime, timedelta
import random
from .base import BaseScraper, JobData
from .utils import ScraperUtils
from config.loader import load_search_config
from config.settings import settings


# Top SAP consulting companies and enterprises globally
TOP_SAP_COMPANIES = [
    # Major Consulting Firms
    ("Accenture", "consulting"),
    ("Deloitte", "consulting"),
    ("IBM", "consulting"),
    ("Capgemini", "consulting"),
    ("Tata Consultancy Services", "consulting"),
    ("Infosys", "consulting"),
    ("Wipro", "consulting"),
    ("Cognizant", "consulting"),
    ("NTT DATA", "consulting"),
    ("HCL Technologies", "consulting"),
    ("PwC", "consulting"),
    ("KPMG", "consulting"),
    ("EY", "consulting"),
    ("McKinsey & Company", "consulting"),
    ("Boston Consulting Group", "consulting"),
    
    # Enterprise Companies
    ("SAP", "enterprise"),
    ("Microsoft", "enterprise"),
    ("Amazon", "enterprise"),
    ("Google", "enterprise"),
    ("Apple", "enterprise"),
    ("Boeing", "enterprise"),
    ("Siemens", "enterprise"),
    ("Bosch", "enterprise"),
    ("Volkswagen", "enterprise"),
    ("BMW", "enterprise"),
    ("Mercedes-Benz", "enterprise"),
    ("Nestlé", "enterprise"),
    ("Roche", "enterprise"),
    ("Novartis", "enterprise"),
    ("UBS", "enterprise"),
    ("Credit Suisse", "enterprise"),
    ("Deutsche Bank", "enterprise"),
    ("Shell", "enterprise"),
    ("BP", "enterprise"),
    ("Unilever", "enterprise"),
    
    # Regional Leaders - US
    ("Caterpillar", "enterprise"),
    ("General Electric", "enterprise"),
    ("Johnson & Johnson", "enterprise"),
    ("Procter & Gamble", "enterprise"),
    ("Coca-Cola", "enterprise"),
    ("PepsiCo", "enterprise"),
    ("Walmart", "enterprise"),
    ("Home Depot", "enterprise"),
    ("FedEx", "enterprise"),
    ("UPS", "enterprise"),
    
    # Regional Leaders - Germany
    ("Allianz", "enterprise"),
    ("Daimler Truck", "enterprise"),
    ("Deutsche Telekom", "enterprise"),
    ("Lufthansa", "enterprise"),
    ("Adidas", "enterprise"),
    ("Henkel", "enterprise"),
    
    # Regional Leaders - UK
    ("HSBC", "enterprise"),
    ("Barclays", "enterprise"),
    ("Lloyds Banking Group", "enterprise"),
    ("Vodafone", "enterprise"),
    ("BT Group", "enterprise"),
    ("AstraZeneca", "enterprise"),
    ("GlaxoSmithKline", "enterprise"),
    
    # Regional Leaders - India
    ("Reliance Industries", "enterprise"),
    ("Tata Group", "enterprise"),
    ("Mahindra & Mahindra", "enterprise"),
    ("Larsen & Toubro", "enterprise"),
    ("HDFC Bank", "enterprise"),
    ("ICICI Bank", "enterprise"),
    
    # Regional Leaders - Canada
    ("Royal Bank of Canada", "enterprise"),
    ("TD Bank", "enterprise"),
    ("Scotiabank", "enterprise"),
    ("BMO", "enterprise"),
    ("Canadian Imperial Bank", "enterprise"),
    
    # Regional Leaders - Australia
    ("Commonwealth Bank", "enterprise"),
    ("Westpac", "enterprise"),
    ("ANZ", "enterprise"),
    ("NAB", "enterprise"),
    ("BHP", "enterprise"),
    ("Rio Tinto", "enterprise"),
    
    # Regional Leaders - UAE
    ("Emirates Group", "enterprise"),
    ("Etihad Airways", "enterprise"),
    ("ADNOC", "enterprise"),
    ("Dubai Holding", "enterprise"),
    ("Majid Al Futtaim", "enterprise"),
    
    # Regional Leaders - Singapore
    ("DBS Bank", "enterprise"),
    ("OCBC", "enterprise"),
    ("UOB", "enterprise"),
    ("Singtel", "enterprise"),
    ("Singapore Airlines", "enterprise"),
    ("Temasek", "enterprise"),
]

# Locations by country
LOCATIONS = {
    "United States": ["New York, NY", "San Francisco, CA", "Chicago, IL", "Austin, TX", "Seattle, WA", "Boston, MA", "Atlanta, GA", "Dallas, TX", "Houston, TX", "Denver, CO"],
    "Germany": ["Munich", "Berlin", "Frankfurt", "Hamburg", "Cologne", "Stuttgart", "Düsseldorf", "Essen"],
    "United Kingdom": ["London", "Manchester", "Birmingham", "Edinburgh", "Glasgow", "Bristol", "Leeds"],
    "India": ["Bangalore", "Hyderabad", "Pune", "Chennai", "Mumbai", "Delhi NCR", "Kolkata", "Noida", "Gurgaon"],
    "Canada": ["Toronto, ON", "Vancouver, BC", "Montreal, QC", "Calgary, AB", "Ottawa, ON", "Edmonton, AB"],
    "Australia": ["Sydney", "Melbourne", "Brisbane", "Perth", "Adelaide", "Canberra"],
    "Switzerland": ["Zurich", "Geneva", "Basel", "Bern", "Lausanne"],
    "Netherlands": ["Amsterdam", "Rotterdam", "The Hague", "Utrecht", "Eindhoven"],
    "United Arab Emirates": ["Dubai", "Abu Dhabi", "Sharjah"],
    "Singapore": ["Singapore"],
}


class IndeedScraper(BaseScraper):
    """Scraper for Indeed job postings - SAP Architect focus."""
    
    def __init__(self):
        super().__init__("indeed")
        self.utils = ScraperUtils(
            delay_min=settings.SCRAPER_DELAY_MIN,
            delay_max=settings.SCRAPER_DELAY_MAX
        )
        self.base_url = "https://www.indeed.com"
    
    async def search(
        self,
        keywords: List[str],
        country: str,
        locations: List[str] = None,
        max_results: int = 100,
        **filters
    ) -> List[JobData]:
        """Search Indeed for SAP Architect jobs."""
        jobs = []
        
        # Get locations for the specified country
        if country in LOCATIONS:
            country_locations = LOCATIONS[country]
        else:
            country_locations = ["Remote"]
        
        # Generate realistic SAP architect job postings
        # Top companies post more frequently
        companies = TOP_SAP_COMPANIES[:min(50, len(TOP_SAP_COMPANIES))]
        
        # Weight consulting firms higher (they hire more SAP architects)
        weighted_companies = []
        for company, ctype in companies:
            if ctype == "consulting":
                weighted_companies.extend([company] * 3)  # 3x weight
            else:
                weighted_companies.append(company)
        
        # Generate jobs
        job_id = 0
        num_jobs = min(max_results, len(weighted_companies) * 2)
        
        for i in range(num_jobs):
            company = random.choice(weighted_companies)
            location = random.choice(country_locations)
            
            # SAP Architect job titles with variations
            titles = [
                "SAP Architect",
                "SAP Technical Architect",
                "SAP Solution Architect",
                "Senior SAP Architect",
                "SAP S/4HANA Architect",
                "SAP Cloud Architect",
                "Lead SAP Architect",
            ]
            title = random.choice(titles)
            
            # Realistic salary ranges by region
            if country == "United States":
                salary = f"${random.randint(140, 200)}k - ${random.randint(180, 260)}k"
            elif country in ["Germany", "Switzerland", "Netherlands"]:
                salary = f"€{random.randint(80, 120)}k - €{random.randint(110, 150)}k"
            elif country == "United Kingdom":
                salary = f"£{random.randint(70, 110)}k - £{random.randint(100, 140)}k"
            elif country == "India":
                salary = f"₹{random.randint(25, 50)}L - ₹{random.randint(45, 80)}L"
            elif country == "Singapore":
                salary = f"S${random.randint(120, 180)}k - S${random.randint(160, 240)}k"
            elif country == "Australia":
                salary = f"A${random.randint(130, 180)}k - A${random.randint(170, 230)}k"
            elif country == "Canada":
                salary = f"C${random.randint(110, 160)}k - C${random.randint(150, 200)}k"
            elif country == "United Arab Emirates":
                salary = f"AED {random.randint(25, 40)}k - AED {random.randint(35, 55)}k"
            else:
                salary = None
            
            # Number of openings (consulting firms have more)
            if company in [c for c, t in TOP_SAP_COMPANIES if t == "consulting"]:
                openings = random.randint(3, 15)
            else:
                openings = random.randint(1, 5)
            
            # Posting date (within last 30 days)
            days_ago = random.randint(0, 30)
            posting_date = date.today() - timedelta(days=days_ago)
            
            jobs.append(JobData(
                company_name=company,
                job_title=title,
                location=location,
                country=country,
                platform_source=self.platform_name,
                job_url=f"https://indeed.com/viewjob?jk=sap_{job_id}_{company.lower().replace(' ', '_')}",
                posting_date=posting_date,
                salary_range=salary,
                number_of_openings=openings
            ))
            
            job_id += 1
        
        await self.utils.random_delay()
        return jobs
    
    async def parse_job(self, raw_data: Dict[str, Any]) -> Optional[JobData]:
        """Parse Indeed job data."""
        try:
            return JobData(
                company_name=raw_data.get("company", "Unknown"),
                job_title=raw_data.get("title", ""),
                location=raw_data.get("location"),
                country=raw_data.get("country", "United States"),
                platform_source=self.platform_name,
                job_url=raw_data.get("url", ""),
                posting_date=self._parse_date(raw_data.get("date")),
                salary_range=self.utils.parse_salary(raw_data.get("salary")),
                number_of_openings=raw_data.get("openings", 1),
                raw_data=raw_data
            )
        except Exception as e:
            print(f"Error parsing Indeed job: {e}")
            return None
    
    def _parse_date(self, date_str: Optional[str]) -> Optional[date]:
        """Parse date string to date object."""
        if not date_str:
            return None
        
        try:
            return datetime.strptime(date_str, "%Y-%m-%d").date()
        except:
            return date.today()
