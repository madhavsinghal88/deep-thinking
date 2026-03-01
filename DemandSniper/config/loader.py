import yaml
from pathlib import Path
from typing import Dict, Any
from .settings import settings


def load_search_config() -> Dict[str, Any]:
    """Load search configuration from YAML file."""
    config_path = settings.CONFIG_DIR / "search_config.yaml"
    try:
        with open(config_path, 'r') as f:
            return yaml.safe_load(f)
    except FileNotFoundError:
        return get_default_search_config()


def load_scoring_config() -> Dict[str, Any]:
    """Load scoring configuration from YAML file."""
    config_path = settings.CONFIG_DIR / "scoring_config.yaml"
    try:
        with open(config_path, 'r') as f:
            return yaml.safe_load(f)
    except FileNotFoundError:
        return get_default_scoring_config()


def get_default_search_config() -> Dict[str, Any]:
    """Return default search configuration."""
    return {
        "target_country": "United States",
        "skill_keywords": ["Python", "FastAPI", "React"],
        "job_title_keywords": ["Software Engineer", "Developer"],
        "platforms": ["indeed", "dice", "linkedin"],
        "search_frequency": "daily",
        "date_range_filter": 30,
        "max_results_per_platform": 100,
        "locations": [],
        "exclude_keywords": []
    }


def get_default_scoring_config() -> Dict[str, Any]:
    """Return default scoring configuration."""
    return {
        "demand_score_formula": {
            "times_posted_weight": 2,
            "days_open_divisor": 10,
            "openings_weight": 3
        },
        "priority_thresholds": {
            "high": 25,
            "medium": 10,
            "low": 0
        },
        "repost_detection_window_days": 60,
        "similarity_thresholds": {
            "job_title": 85,
            "company_name": 95
        },
        "notifications": {
            "enabled": True,
            "webhook": {"url": "", "headers": {}},
            "email": {"enabled": False, "recipients": []},
            "triggers": []
        },
        "scoring": {
            "track_score_history": True,
            "auto_update_on_scrape": True
        }
    }
