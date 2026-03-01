import csv
import io
from datetime import date
from typing import List, Dict, Any
from database.models import JobPosting


def jobs_to_csv(jobs: List[JobPosting]) -> str:
    """
    Convert list of JobPosting objects to CSV format.
    Returns CSV string.
    """
    if not jobs:
        return ""
    
    output = io.StringIO()
    writer = csv.writer(output)
    
    # Write header
    writer.writerow([
        "id",
        "company_name",
        "job_title",
        "location",
        "country",
        "platform_source",
        "posting_date",
        "job_url",
        "salary_range",
        "first_seen_date",
        "last_seen_date",
        "times_posted",
        "number_of_openings",
        "days_open",
        "demand_score",
        "priority_tag",
        "created_at",
        "updated_at"
    ])
    
    # Write data
    for job in jobs:
        writer.writerow([
            job.id,
            job.company_name,
            job.job_title,
            job.location,
            job.country,
            job.platform_source,
            job.posting_date.isoformat() if job.posting_date else "",
            job.job_url,
            job.salary_range or "",
            job.first_seen_date.isoformat() if job.first_seen_date else "",
            job.last_seen_date.isoformat() if job.last_seen_date else "",
            job.times_posted,
            job.number_of_openings,
            job.days_open,
            round(job.demand_score, 2),
            job.priority_tag,
            job.created_at.isoformat() if job.created_at else "",
            job.updated_at.isoformat() if job.updated_at else ""
        ])
    
    return output.getvalue()


def companies_to_csv(companies: List[Dict[str, Any]]) -> str:
    """
    Convert list of company dictionaries to CSV format.
    Returns CSV string.
    """
    if not companies:
        return ""
    
    output = io.StringIO()
    writer = csv.writer(output)
    
    # Write header
    writer.writerow([
        "company_name",
        "total_jobs",
        "total_demand_score",
        "highest_priority",
        "last_active",
        "total_openings"
    ])
    
    # Write data
    for company in companies:
        writer.writerow([
            company.get("company_name", ""),
            company.get("total_jobs", 0),
            round(company.get("total_demand_score", 0), 2),
            company.get("highest_priority", ""),
            company.get("last_active", ""),
            company.get("total_openings", 0)
        ])
    
    return output.getvalue()


def export_to_file(csv_content: str, filename: str) -> str:
    """
    Save CSV content to a file.
    Returns the file path.
    """
    from pathlib import Path
    from config.settings import settings
    
    exports_dir = settings.DATA_DIR / "exports"
    exports_dir.mkdir(parents=True, exist_ok=True)
    
    filepath = exports_dir / filename
    
    with open(filepath, 'w', newline='', encoding='utf-8') as f:
        f.write(csv_content)
    
    return str(filepath)


def generate_export_filename(prefix: str = "demandsniper") -> str:
    """Generate a timestamped export filename."""
    from datetime import datetime
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"{prefix}_{timestamp}.csv"
