from datetime import date, datetime, timedelta
from typing import Optional, List, Dict, Any
from rapidfuzz import fuzz


class JobMatcher:
    """Handles job posting deduplication and matching logic."""
    
    def __init__(
        self,
        company_similarity_threshold: float = 95.0,
        title_similarity_threshold: float = 85.0,
        window_days: int = 60
    ):
        self.company_threshold = company_similarity_threshold
        self.title_threshold = title_similarity_threshold
        self.window_days = window_days
    
    def is_match(
        self,
        company_name: str,
        job_title: str,
        existing_company: str,
        existing_title: str
    ) -> bool:
        """
        Check if two job postings match based on company and title similarity.
        """
        # Company name similarity
        company_score = fuzz.ratio(
            company_name.lower().strip(),
            existing_company.lower().strip()
        )
        
        if company_score < self.company_threshold:
            return False
        
        # Job title similarity
        title_score = fuzz.ratio(
            job_title.lower().strip(),
            existing_title.lower().strip()
        )
        
        return title_score >= self.title_threshold
    
    def get_match_details(
        self,
        company_name: str,
        job_title: str,
        existing_company: str,
        existing_title: str
    ) -> Dict[str, Any]:
        """Get detailed matching information."""
        company_score = fuzz.ratio(
            company_name.lower().strip(),
            existing_company.lower().strip()
        )
        
        title_score = fuzz.ratio(
            job_title.lower().strip(),
            existing_title.lower().strip()
        )
        
        is_match = (
            company_score >= self.company_threshold and 
            title_score >= self.title_threshold
        )
        
        return {
            "is_match": is_match,
            "company_similarity": company_score,
            "title_similarity": title_score,
            "company_matches": company_score >= self.company_threshold,
            "title_matches": title_score >= self.title_threshold
        }


def should_treat_as_repost(
    posting_date: date,
    last_seen_date: date,
    window_days: int = 60
) -> bool:
    """
    Determine if a job posting should be treated as a repost
    based on the time window.
    """
    cutoff_date = date.today() - timedelta(days=window_days)
    return last_seen_date >= cutoff_date


def find_best_match(
    company_name: str,
    job_title: str,
    country: str,
    existing_jobs: List[Any],
    company_threshold: float = 95.0,
    title_threshold: float = 85.0
) -> Optional[Any]:
    """
    Find the best matching job from a list of existing jobs.
    Returns the job with the highest combined similarity score.
    """
    matcher = JobMatcher(company_threshold, title_threshold)
    
    best_match = None
    best_score = 0
    
    for job in existing_jobs:
        # Only consider jobs from same country
        if job.country != country:
            continue
        
        details = matcher.get_match_details(
            company_name, job_title,
            job.company_name, job.job_title
        )
        
        if details["is_match"]:
            combined_score = (
                details["company_similarity"] + 
                details["title_similarity"]
            ) / 2
            
            if combined_score > best_score:
                best_score = combined_score
                best_match = job
    
    return best_match


def normalize_company_name(name: str) -> str:
    """Normalize company name for better matching."""
    # Remove common suffixes
    suffixes = [
        'inc.', 'inc', 'llc', 'ltd.', 'ltd', 
        'corp.', 'corp', 'co.', 'co',
        'limited', 'incorporated', 'corporation'
    ]
    
    normalized = name.lower().strip()
    
    for suffix in suffixes:
        if normalized.endswith(f' {suffix}'):
            normalized = normalized[:-len(suffix) - 1].strip()
        elif normalized.endswith(suffix):
            normalized = normalized[:-len(suffix)].strip()
    
    # Remove extra whitespace
    normalized = ' '.join(normalized.split())
    
    return normalized


def extract_core_job_title(title: str) -> str:
    """Extract core job title by removing level and location info."""
    # Common prefixes to remove
    prefixes = [
        'senior', 'sr.', 'sr', 'junior', 'jr.', 'jr',
        'lead', 'principal', 'staff', 'associate',
        'entry level', 'mid-level', 'experienced'
    ]
    
    # Common suffixes to remove
    suffixes = [
        '- remote', '(remote)', 'remote',
        '- hybrid', '(hybrid)', 'hybrid',
        '- onsite', '(onsite)', 'onsite'
    ]
    
    normalized = title.lower().strip()
    
    # Remove prefixes
    for prefix in prefixes:
        if normalized.startswith(f'{prefix} '):
            normalized = normalized[len(prefix):].strip()
        if normalized.startswith(prefix):
            normalized = normalized[len(prefix):].strip()
    
    # Remove suffixes
    for suffix in suffixes:
        if suffix in normalized:
            normalized = normalized.replace(suffix, '').strip()
    
    # Remove extra whitespace
    normalized = ' '.join(normalized.split())
    
    return normalized
