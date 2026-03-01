import streamlit as st
import pandas as pd
from typing import List, Dict, Any


def render_jobs_table(jobs: List[Dict[str, Any]], show_actions: bool = True):
    """Render a table of job postings."""
    if not jobs:
        st.info("No jobs found")
        return
    
    # Prepare data for display
    display_data = []
    for job in jobs:
        display_data.append({
            "Company": job.get("company_name", "N/A"),
            "Title": job.get("job_title", "N/A"),
            "Location": job.get("location", "N/A"),
            "Platform": job.get("platform_source", "N/A").title(),
            "Posted": job.get("posting_date", "N/A"),
            "Times Posted": job.get("times_posted", 1),
            "Openings": job.get("number_of_openings", 1),
            "Demand Score": round(job.get("demand_score", 0), 2),
            "Priority": job.get("priority_tag", "Low"),
            "Actions": job.get("id")
        })
    
    df = pd.DataFrame(display_data)
    
    # Color code priority column
    def highlight_priority(val):
        if val == "High":
            return "background-color: #ff4b4b; color: white"
        elif val == "Medium":
            return "background-color: #ffa500"
        else:
            return "background-color: #00cc00; color: white"
    
    styled_df = df.style.applymap(
        highlight_priority, 
        subset=["Priority"]
    )
    
    st.dataframe(
        styled_df,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Actions": st.column_config.LinkColumn(
                "View",
                help="Click to view job details",
                disabled=True
            )
        }
    )


def render_companies_table(companies: List[Dict[str, Any]]):
    """Render a table of companies with demand scores."""
    if not companies:
        st.info("No companies found")
        return
    
    # Prepare data
    display_data = []
    for company in companies:
        display_data.append({
            "Company": company.get("company_name", "N/A"),
            "Total Jobs": company.get("total_jobs", 0),
            "Total Openings": company.get("total_openings", 0),
            "Demand Score": round(company.get("total_demand_score", 0), 2),
            "Priority": company.get("highest_priority", "Low"),
            "Last Active": company.get("last_active", "N/A")
        })
    
    df = pd.DataFrame(display_data)
    
    # Color code priority
    def highlight_priority(val):
        if val == "High":
            return "background-color: #ff4b4b; color: white"
        elif val == "Medium":
            return "background-color: #ffa500"
        else:
            return "background-color: #00cc00; color: white"
    
    styled_df = df.style.applymap(
        highlight_priority,
        subset=["Priority"]
    )
    
    st.dataframe(
        styled_df,
        use_container_width=True,
        hide_index=True
    )


def render_company_detail_table(company: Dict[str, Any]):
    """Render detailed company information."""
    if not company:
        st.info("No company data")
        return
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Jobs", company.get("total_jobs", 0))
        st.metric("Total Openings", company.get("total_openings", 0))
    
    with col2:
        st.metric("Demand Score", round(company.get("total_demand_score", 0), 2))
        st.metric("Priority", company.get("highest_priority", "N/A"))
    
    with col3:
        st.metric("Last Active", company.get("last_active", "N/A"))


def render_priority_badge(priority: str):
    """Render a priority badge."""
    colors = {
        "High": "🔴",
        "Medium": "🟡",
        "Low": "🟢"
    }
    
    badge = colors.get(priority, "⚪")
    st.markdown(f"{badge} **{priority} Priority**")


def render_stats_cards(stats: Dict[str, Any]):
    """Render summary statistics cards."""
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="Total Jobs",
            value=stats.get("total_jobs", 0)
        )
    
    with col2:
        st.metric(
            label="This Month",
            value=stats.get("jobs_this_month", 0)
        )
    
    with col3:
        st.metric(
            label="This Week",
            value=stats.get("jobs_this_week", 0)
        )
    
    with col4:
        st.metric(
            label="High Priority",
            value=stats.get("high_priority_companies", 0)
        )
