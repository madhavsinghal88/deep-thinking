from typing import Optional, Dict, Any
from datetime import datetime
import httpx


class CompanyEnricher:
    """Enriches company data with additional information."""
    
    def __init__(self):
        self.cache = {}
    
    async def enrich_company(
        self,
        company_name: str,
        sources: list = None
    ) -> Dict[str, Any]:
        """
        Enrich company data from multiple sources.
        Currently supports manual data and placeholder for future APIs.
        """
        if sources is None:
            sources = ["clearbit", "manual"]
        
        enriched_data = {
            "company_name": company_name,
            "enrichment_source": "manual",
            "last_enriched": datetime.now(),
            "industry": None,
            "company_size": None,
            "headquarters": None,
            "website": None,
            "linkedin_url": None,
            "description": None
        }
        
        # Try Clearbit API (requires API key)
        if "clearbit" in sources:
            clearbit_data = await self._enrich_from_clearbit(company_name)
            if clearbit_data:
                enriched_data.update(clearbit_data)
                enriched_data["enrichment_source"] = "clearbit"
        
        # Try LinkedIn scraping/API
        if "linkedin" in sources:
            linkedin_data = await self._enrich_from_linkedin(company_name)
            if linkedin_data:
                enriched_data.update(linkedin_data)
                if enriched_data["enrichment_source"] == "manual":
                    enriched_data["enrichment_source"] = "linkedin"
        
        return enriched_data
    
    async def _enrich_from_clearbit(
        self, 
        company_name: str
    ) -> Optional[Dict[str, Any]]:
        """
        Enrich company data using Clearbit API.
        Note: Requires CLEARBIT_API_KEY environment variable.
        """
        import os
        api_key = os.getenv("CLEARBIT_API_KEY")
        
        if not api_key:
            return None
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    "https://company.clearbit.com/v2/companies/find",
                    params={"name": company_name},
                    headers={"Authorization": f"Bearer {api_key}"},
                    timeout=10.0
                )
                
                if response.status_code == 200:
                    data = response.json()
                    return {
                        "industry": data.get("category", {}).get("industry"),
                        "company_size": self._format_company_size(
                            data.get("metrics", {}).get("employees")
                        ),
                        "headquarters": self._format_location(data.get("geo")),
                        "website": data.get("domain"),
                        "linkedin_url": data.get("linkedin", {}).get("handle"),
                        "description": data.get("description")
                    }
        except Exception as e:
            print(f"Clearbit enrichment failed for {company_name}: {e}")
        
        return None
    
    async def _enrich_from_linkedin(
        self,
        company_name: str
    ) -> Optional[Dict[str, Any]]:
        """
        Enrich company data from LinkedIn.
        Placeholder for future implementation.
        """
        # This would require LinkedIn API access or scraping
        # For now, return None to allow manual enrichment
        return None
    
    def _format_company_size(self, employee_count: Optional[int]) -> Optional[str]:
        """Format employee count into size ranges."""
        if not employee_count:
            return None
        
        if employee_count < 50:
            return "1-50"
        elif employee_count < 200:
            return "51-200"
        elif employee_count < 500:
            return "201-500"
        elif employee_count < 1000:
            return "501-1000"
        elif employee_count < 5000:
            return "1001-5000"
        elif employee_count < 10000:
            return "5001-10000"
        else:
            return "10000+"
    
    def _format_location(self, geo_data: Optional[Dict]) -> Optional[str]:
        """Format location data."""
        if not geo_data:
            return None
        
        city = geo_data.get("cityName", "")
        state = geo_data.get("stateCode", "")
        country = geo_data.get("country", "")
        
        parts = [p for p in [city, state, country] if p]
        return ", ".join(parts) if parts else None


# Global enricher instance
company_enricher = CompanyEnricher()


async def enrich_company_data(
    company_name: str,
    sources: list = None
) -> Dict[str, Any]:
    """Convenience function to enrich company data."""
    return await company_enricher.enrich_company(company_name, sources)
