from pathlib import Path
from typing import List, Optional
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "DemandSniper"
    VERSION: str = "1.0.0"
    
    # Database
    DATABASE_URL: str = "sqlite+aiosqlite:///data/demandsniper.db"
    
    # API
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000
    DEBUG: bool = True
    
    # Paths
    BASE_DIR: Path = Path(__file__).parent.parent
    DATA_DIR: Path = BASE_DIR / "data"
    CONFIG_DIR: Path = BASE_DIR / "config"
    
    # Scraper
    SCRAPER_MAX_RETRIES: int = 3
    SCRAPER_DELAY_MIN: float = 1.0
    SCRAPER_DELAY_MAX: float = 3.0
    SCRAPER_CONCURRENT_REQUESTS: int = 3
    
    # Notifications
    SMTP_HOST: Optional[str] = None
    SMTP_PORT: int = 587
    SMTP_USER: Optional[str] = None
    SMTP_PASSWORD: Optional[str] = None
    SMTP_FROM_EMAIL: Optional[str] = None
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
