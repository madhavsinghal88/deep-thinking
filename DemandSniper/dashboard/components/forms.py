import streamlit as st
from datetime import date
from typing import Optional, Dict, Any


def render_manual_job_form():
    """Render form for manually adding a job posting."""
    st.subheader("➕ Add Job Manually")
    
    with st.form("manual_job_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            company_name = st.text_input(
                "Company Name *",
                placeholder="e.g., TechCorp Inc."
            )
            
            job_title = st.text_input(
                "Job Title *",
                placeholder="e.g., Senior Software Engineer"
            )
            
            location = st.text_input(
                "Location",
                placeholder="e.g., San Francisco, CA"
            )
            
            country = st.selectbox(
                "Country *",
                options=["United States", "United Kingdom", "Canada", "Germany", "India", "Other"]
            )
        
        with col2:
            platform = st.selectbox(
                "Platform *",
                options=["Indeed", "Dice", "LinkedIn", "Other"]
            )
            
            job_url = st.text_input(
                "Job URL *",
                placeholder="https://..."
            )
            
            salary_range = st.text_input(
                "Salary Range",
                placeholder="e.g., $100k - $150k"
            )
            
            number_of_openings = st.number_input(
                "Number of Openings",
                min_value=1,
                value=1
            )
        
        posting_date = st.date_input(
            "Posting Date",
            value=date.today()
        )
        
        submitted = st.form_submit_button("Add Job", use_container_width=True)
        
        if submitted:
            if not all([company_name, job_title, job_url]):
                st.error("Please fill in all required fields (marked with *)")
                return None
            
            return {
                "company_name": company_name,
                "job_title": job_title,
                "location": location if location else None,
                "country": country,
                "platform_source": platform.lower(),
                "job_url": job_url,
                "salary_range": salary_range if salary_range else None,
                "number_of_openings": number_of_openings,
                "posting_date": posting_date.isoformat()
            }
    
    return None


def render_company_profile_form(company_name: str, existing_profile: Optional[Dict] = None):
    """Render form for adding/editing company profile."""
    st.subheader(f"🏢 {company_name} - Profile")
    
    with st.form("company_profile_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            industry = st.text_input(
                "Industry",
                value=existing_profile.get("industry", "") if existing_profile else "",
                placeholder="e.g., Technology, Finance, Healthcare"
            )
            
            company_size = st.selectbox(
                "Company Size",
                options=["", "1-50", "51-200", "201-500", "501-1000", "1001-5000", "5001-10000", "10000+"],
                index=0
            )
            if existing_profile and existing_profile.get("company_size"):
                try:
                    company_size = existing_profile.get("company_size")
                except:
                    pass
            
            headquarters = st.text_input(
                "Headquarters",
                value=existing_profile.get("headquarters", "") if existing_profile else "",
                placeholder="e.g., San Francisco, CA"
            )
        
        with col2:
            website = st.text_input(
                "Website",
                value=existing_profile.get("website", "") if existing_profile else "",
                placeholder="https://company.com"
            )
            
            linkedin_url = st.text_input(
                "LinkedIn URL",
                value=existing_profile.get("linkedin_url", "") if existing_profile else "",
                placeholder="https://linkedin.com/company/..."
            )
        
        description = st.text_area(
            "Description",
            value=existing_profile.get("description", "") if existing_profile else "",
            placeholder="Brief company description..."
        )
        
        submitted = st.form_submit_button("Save Profile", use_container_width=True)
        
        if submitted:
            return {
                "industry": industry if industry else None,
                "company_size": company_size if company_size else None,
                "headquarters": headquarters if headquarters else None,
                "website": website if website else None,
                "linkedin_url": linkedin_url if linkedin_url else None,
                "description": description if description else None
            }
    
    return None


def render_export_form():
    """Render export options form."""
    st.subheader("📥 Export Data")
    
    export_type = st.selectbox(
        "Export Type",
        options=["Jobs", "Companies"]
    )
    
    col1, col2 = st.columns(2)
    
    with col1:
        if export_type == "Jobs":
            export_format = st.selectbox(
                "Format",
                options=["CSV", "JSON"]
            )
            
            include_filters = st.checkbox("Apply current filters", value=True)
    
    with col2:
        filename = st.text_input(
            "Filename",
            value=f"export_{date.today().isoformat()}"
        )
    
    if st.button("Export", use_container_width=True):
        return {
            "type": export_type.lower(),
            "format": export_format.lower() if export_type == "Jobs" else "csv",
            "filename": filename,
            "apply_filters": include_filters if export_type == "Jobs" else False
        }
    
    return None


def render_scraper_control():
    """Render scraper control buttons."""
    st.subheader("🤖 Scraper Control")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("▶️ Start Scraper", use_container_width=True):
            return {"action": "start"}
    
    with col2:
        if st.button("⏹️ Stop Scraper", use_container_width=True):
            return {"action": "stop"}
    
    with col3:
        if st.button("🔄 Run Now", use_container_width=True):
            return {"action": "run"}
    
    return None


def render_scraper_config_form():
    """Render scraper configuration form."""
    st.subheader("⚙️ Scraper Configuration")
    
    with st.form("scraper_config_form"):
        platforms = st.multiselect(
            "Platforms to Scrape",
            options=["Indeed", "Dice", "LinkedIn"],
            default=["Indeed", "Dice"]
        )
        
        frequency = st.selectbox(
            "Scraping Frequency",
            options=["Daily", "Weekly"],
            index=0
        )
        
        max_results = st.slider(
            "Max Results per Platform",
            min_value=10,
            max_value=500,
            value=100,
            step=10
        )
        
        submitted = st.form_submit_button("Save Configuration", use_container_width=True)
        
        if submitted:
            return {
                "platforms": [p.lower() for p in platforms],
                "frequency": frequency.lower(),
                "max_results_per_platform": max_results
            }
    
    return None
