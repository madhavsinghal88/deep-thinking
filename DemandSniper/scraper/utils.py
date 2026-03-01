import asyncio
import random
from typing import Optional
from playwright.async_api import async_playwright, Page
from fake_useragent import UserAgent


class ScraperUtils:
    """Utility class for scraper operations."""
    
    def __init__(self, delay_min: float = 1.0, delay_max: float = 3.0):
        self.delay_min = delay_min
        self.delay_max = delay_max
        self.ua = UserAgent()
    
    async def random_delay(self):
        """Wait for a random amount of time."""
        await asyncio.sleep(random.uniform(self.delay_min, self.delay_max))
    
    def get_random_user_agent(self) -> str:
        """Get a random user agent string."""
        try:
            return self.ua.random
        except:
            # Fallback user agent
            return "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    
    async def stealth_page(self, page: Page):
        """Apply stealth measures to a page."""
        # Inject stealth script
        await page.add_init_script("""
            // Override webdriver
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined
            });
            
            // Override plugins
            Object.defineProperty(navigator, 'plugins', {
                get: () => [1, 2, 3, 4, 5]
            });
            
            // Override languages
            Object.defineProperty(navigator, 'languages', {
                get: () => ['en-US', 'en']
            });
        """)
    
    def parse_salary(self, salary_text: Optional[str]) -> Optional[str]:
        """Parse and normalize salary text."""
        if not salary_text:
            return None
        
        # Clean up the text
        salary = salary_text.strip()
        
        # Remove extra whitespace
        salary = ' '.join(salary.split())
        
        return salary if salary else None
    
    def parse_location(self, location_text: Optional[str]) -> tuple:
        """Parse location into city and country."""
        if not location_text:
            return None, None
        
        parts = [p.strip() for p in location_text.split(',')]
        
        if len(parts) >= 2:
            city = parts[0]
            country = parts[-1]
            return city, country
        elif len(parts) == 1:
            return parts[0], None
        
        return location_text, None
    
    def clean_company_name(self, name: Optional[str]) -> str:
        """Clean and normalize company name."""
        if not name:
            return "Unknown"
        
        # Remove common suffixes
        name = name.strip()
        suffixes = [' Inc.', ' Inc', ' LLC', ' Ltd.', ' Ltd', ' Corp.', ' Corp']
        for suffix in suffixes:
            if name.endswith(suffix):
                name = name[:-len(suffix)].strip()
        
        return name
