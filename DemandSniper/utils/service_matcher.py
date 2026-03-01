"""
Service opportunity detection for SAP EPM/Analytics keywords
Matches job postings to specific service offerings
"""

from typing import Dict, List, Tuple
from rapidfuzz import fuzz


# Service categories with keywords
SERVICE_CATEGORIES = {
    "Financial Planning & Analysis": {
        "keywords": [
            "financial planning", "fp&a", "budgeting", "forecasting", 
            "driver based planning", "scenario analysis", "what-if analysis",
            "predictive planning", "integrated planning", "planning and analysis",
            "financial planner", "fpna", "financial analyst"
        ],
        "pain_points": [
            "Eliminate manual spreadsheet processes",
            "Enable agile planning across departments",
            "Improve forecast accuracy by 40%"
        ],
        "outcomes": [
            "Integrated planning platform",
            "Real-time scenario modeling",
            "Predictive forecasting"
        ]
    },
    
    "Financial Close & Consolidation": {
        "keywords": [
            "financial close", "financial consolidation", "group reporting",
            "group consolidation", "intercompany", "intercompany eliminations",
            "statutory reporting", "management reporting", "financial closing",
            "closing automation", "afc", "advanced financial closing",
            "audit ready", "close cycle", "month end close", "year end close"
        ],
        "pain_points": [
            "Reduce close time by 50%",
            "Automated intercompany reconciliations",
            "Eliminate manual consolidation"
        ],
        "outcomes": [
            "Accelerated financial close",
            "Audit-ready consolidation",
            "Real-time group reporting"
        ]
    },
    
    "SAP Analytics Cloud (SAC)": {
        "keywords": [
            "sap analytics cloud", "sac", "analytics cloud", "sac consultant",
            "sap sac", "business intelligence", "bi analytics", "bi dashboard",
            "data visualization", "self-service analytics"
        ],
        "pain_points": [
            "Disconnected data silos",
            "Lack of real-time insights",
            "Manual report creation"
        ],
        "outcomes": [
            "Unified analytics platform",
            "Self-service BI capabilities",
            "AI-powered insights"
        ]
    },
    
    "SAP Datasphere & Data Management": {
        "keywords": [
            "sap datasphere", "datasphere", "data warehouse", "enterprise data",
            "business data fabric", "data modeling", "data governance",
            "data integration", "data management", "data architecture",
            "data fabric", "data warehouse cloud"
        ],
        "pain_points": [
            "Fragmented data landscape",
            "Data quality issues",
            "Complex data integration"
        ],
        "outcomes": [
            "Unified data fabric",
            "Business-ready data",
            "Real-time data access"
        ]
    },
    
    "Predictive Analytics & AI": {
        "keywords": [
            "predictive analytics", "predictive modeling", "machine learning",
            "ml", "artificial intelligence", "ai", "ai analytics", "forecasting",
            "predictive planning", "smart predict", "predictive forecasting",
            "automl", "data science"
        ],
        "pain_points": [
            "Reactive decision making",
            "Inaccurate forecasts",
            "Missed market opportunities"
        ],
        "outcomes": [
            "AI-powered predictions",
            "Proactive decision support",
            "Automated forecasting"
        ]
    },
    
    "SAP Implementation & Migration": {
        "keywords": [
            "sap implementation", "implementation lead", "implementation manager",
            "cloud migration", "s/4hana migration", "legacy migration",
            "system integration", "solution implementation", "go-live",
            "sap project", "deployment", "rollout", "greenfield", "brownfield"
        ],
        "pain_points": [
            "Complex implementation risks",
            "Legacy system limitations",
            "Resource constraints"
        ],
        "outcomes": [
            "Successful cloud deployment",
            "Seamless system integration",
            "Accelerated time-to-value"
        ]
    },
    
    "SAP Support & Enhancement": {
        "keywords": [
            "sap support", "application support", "maintenance",
            "enhancement", "custom development", "support analyst",
            "production support", "ams", "application management services",
            "system optimization", "performance tuning"
        ],
        "pain_points": [
            "System performance issues",
            "Limited internal expertise",
            "Recurring support tickets"
        ],
        "outcomes": [
            "Proactive system monitoring",
            "Expert support coverage",
            "Continuous optimization"
        ]
    }
}


class ServiceOpportunityDetector:
    """Detects SAP service opportunities from job postings."""
    
    def __init__(self):
        self.categories = SERVICE_CATEGORIES
    
    def detect_services(self, job_title: str, job_description: str = "") -> List[Dict]:
        """
        Detect which SAP services a job posting relates to.
        
        Args:
            job_title: The job title
            job_description: Optional job description
            
        Returns:
            List of matching service categories with confidence scores
        """
        matches = []
        combined_text = f"{job_title} {job_description}".lower()
        
        for category_name, category_data in self.categories.items():
            confidence = 0
            matched_keywords = []
            
            for keyword in category_data["keywords"]:
                # Exact match
                if keyword.lower() in combined_text:
                    confidence += 30
                    matched_keywords.append(keyword)
                else:
                    # Fuzzy match for variations
                    for text_part in combined_text.split():
                        score = fuzz.ratio(keyword.lower(), text_part)
                        if score >= 85:
                            confidence += 15
                            matched_keywords.append(keyword)
                            break
            
            # Boost confidence for exact title matches
            title_confidence = self._check_title_match(job_title.lower(), category_data["keywords"])
            confidence += title_confidence
            
            if confidence >= 30:  # Minimum threshold
                matches.append({
                    "service": category_name,
                    "confidence": min(confidence, 100),
                    "keywords": list(set(matched_keywords))[:5],  # Top 5 unique keywords
                    "pain_points": category_data["pain_points"],
                    "outcomes": category_data["outcomes"]
                })
        
        # Sort by confidence
        matches.sort(key=lambda x: x["confidence"], reverse=True)
        return matches
    
    def _check_title_match(self, title: str, keywords: List[str]) -> int:
        """Check if job title contains service keywords."""
        confidence = 0
        
        for keyword in keywords:
            if keyword.lower() in title:
                # Title match is worth more
                if any(word in title for word in ["consultant", "architect", "lead", "manager"]):
                    confidence += 40  # High-value role
                else:
                    confidence += 25
        
        return confidence
    
    def get_primary_service(self, job_title: str, job_description: str = "") -> Dict:
        """Get the primary service category for a job."""
        services = self.detect_services(job_title, job_description)
        return services[0] if services else {
            "service": "General SAP Services",
            "confidence": 50,
            "keywords": [],
            "pain_points": ["Legacy system challenges"],
            "outcomes": ["Modernized SAP landscape"]
        }
    
    def generate_pitch(self, company_name: str, service: Dict) -> str:
        """Generate a service-specific pitch."""
        service_name = service["service"]
        pain_point = service["pain_points"][0] if service["pain_points"] else "Operational inefficiencies"
        outcome = service["outcomes"][0] if service["outcomes"] else "Improved performance"
        
        pitches = {
            "Financial Planning & Analysis": f"""
            🎯 **{service_name} Opportunity**
            
            **The Challenge**: {company_name} is investing heavily in planning capabilities but likely struggling with {pain_point.lower()}.
            
            **Our Solution**: Implement SAP Analytics Cloud with integrated planning to deliver {outcome.lower()}.
            
            **Value Proposition**: Reduce planning cycle time by 60% and improve forecast accuracy.
            """,
            
            "Financial Close & Consolidation": f"""
            🎯 **{service_name} Opportunity**
            
            **The Challenge**: {company_name}'s hiring suggests they need to {pain_point.lower()}.
            
            **Our Solution**: Deploy SAP Group Reporting and AFC to achieve {outcome.lower()}.
            
            **Value Proposition**: Cut close time from days to hours with automated reconciliations.
            """,
            
            "SAP Analytics Cloud (SAC)": f"""
            🎯 **{service_name} Opportunity**
            
            **The Challenge**: {company_name} is building analytics capabilities but faces {pain_point.lower()}.
            
            **Our Solution**: Implement SAP Analytics Cloud for {outcome.lower()}.
            
            **Value Proposition**: Unified analytics platform with AI-powered insights.
            """,
            
            "SAP Datasphere & Data Management": f"""
            🎯 **{service_name} Opportunity**
            
            **The Challenge**: {company_name} needs to address {pain_point.lower()} in their data landscape.
            
            **Our Solution**: Architect SAP Datasphere solution delivering {outcome.lower()}.
            
            **Value Proposition**: Business-ready data fabric with real-time access.
            """,
            
            "Predictive Analytics & AI": f"""
            🎯 **{service_name} Opportunity**
            
            **The Challenge**: {company_name} wants to move from reactive to proactive with {pain_point.lower()}.
            
            **Our Solution**: Implement ML-powered predictive analytics for {outcome.lower()}.
            
            **Value Proposition**: AI-driven forecasting with 40% improved accuracy.
            """,
            
            "SAP Implementation & Migration": f"""
            🎯 **{service_name} Opportunity**
            
            **The Challenge**: {company_name} is embarking on transformation but faces {pain_point.lower()}.
            
            **Our Solution**: Deliver proven implementation methodology for {outcome.lower()}.
            
            **Value Proposition**: Risk-mitigated deployment with accelerated ROI.
            """,
            
            "SAP Support & Enhancement": f"""
            🎯 **{service_name} Opportunity**
            
            **The Challenge**: {company_name} needs ongoing expertise to address {pain_point.lower()}.
            
            **Our Solution**: Provide managed services for {outcome.lower()}.
            
            **Value Proposition**: 24/7 expert support with continuous system optimization.
            """
        }
        
        return pitches.get(service_name, f"""
        🎯 **{service_name} Opportunity**
        
        **The Challenge**: {company_name} is investing in SAP capabilities.
        
        **Our Solution**: Comprehensive SAP services tailored to their needs.
        
        **Value Proposition**: Expert implementation and support services.
        """)


# Global detector instance
detector = ServiceOpportunityDetector()


def detect_service_opportunities(job_title: str, job_description: str = "") -> List[Dict]:
    """Convenience function to detect services."""
    return detector.detect_services(job_title, job_description)


def get_service_pitch(company_name: str, job_title: str, job_description: str = "") -> str:
    """Generate a pitch for a specific job."""
    service = detector.get_primary_service(job_title, job_description)
    return detector.generate_pitch(company_name, service)
