from .demand_scoring import (
    calculate_demand_score,
    get_priority_tag,
    get_demand_score_breakdown
)
from .deduplication import (
    JobMatcher,
    should_treat_as_repost,
    find_best_match,
    normalize_company_name,
    extract_core_job_title
)
from .notifications import (
    NotificationManager,
    send_notification,
    check_and_notify_triggers,
    notification_manager
)
from .enrichment import (
    CompanyEnricher,
    enrich_company_data,
    company_enricher
)
from .export import (
    jobs_to_csv,
    companies_to_csv,
    export_to_file,
    generate_export_filename
)
from .service_matcher import (
    ServiceOpportunityDetector,
    detect_service_opportunities,
    get_service_pitch,
    detector
)

__all__ = [
    # Demand Scoring
    "calculate_demand_score",
    "get_priority_tag",
    "get_demand_score_breakdown",
    # Deduplication
    "JobMatcher",
    "should_treat_as_repost",
    "find_best_match",
    "normalize_company_name",
    "extract_core_job_title",
    # Notifications
    "NotificationManager",
    "send_notification",
    "check_and_notify_triggers",
    "notification_manager",
    # Enrichment
    "CompanyEnricher",
    "enrich_company_data",
    "company_enricher",
    # Export
    "jobs_to_csv",
    "companies_to_csv",
    "export_to_file",
    "generate_export_filename",
    # Service Matching
    "ServiceOpportunityDetector",
    "detect_service_opportunities",
    "get_service_pitch",
    "detector"
]
