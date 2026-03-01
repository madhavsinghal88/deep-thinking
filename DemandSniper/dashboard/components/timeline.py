import streamlit as st
from datetime import datetime
from typing import List, Dict, Any
import pandas as pd


def render_company_timeline(events: List[Dict[str, Any]]):
    """Render company event timeline."""
    if not events:
        st.info("No timeline events available")
        return
    
    st.subheader("📅 Company Timeline")
    
    # Sort events by date (newest first)
    sorted_events = sorted(
        events,
        key=lambda x: x.get("event_date", ""),
        reverse=True
    )
    
    # Event type icons
    icons = {
        "job_posted": "📝",
        "repost_detected": "🔄",
        "demand_spike": "📈",
        "enriched": "🔍"
    }
    
    for event in sorted_events[:20]:  # Show last 20 events
        event_type = event.get("event_type", "unknown")
        icon = icons.get(event_type, "📌")
        event_date = event.get("event_date", "Unknown date")
        
        if isinstance(event_date, str):
            try:
                event_date = datetime.fromisoformat(event_date.replace('Z', '+00:00'))
                event_date = event_date.strftime("%Y-%m-%d %H:%M")
            except:
                pass
        
        # Create expander for each event
        with st.expander(f"{icon} {event_type.replace('_', ' ').title()} - {event_date}"):
            details = event.get("details", {})
            if details:
                for key, value in details.items():
                    st.write(f"**{key.replace('_', ' ').title()}:** {value}")
            else:
                st.write("No additional details")


def render_demand_score_history(history: List[Dict[str, Any]]):
    """Render demand score history chart."""
    if not history:
        st.info("No score history available")
        return
    
    st.subheader("📊 Demand Score History")
    
    df = pd.DataFrame(history)
    df['date'] = pd.to_datetime(df['date'])
    
    st.line_chart(df.set_index('date')['demand_score'])
    
    # Show statistics
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Current Score", round(df['demand_score'].iloc[-1], 2))
    with col2:
        st.metric("Peak Score", round(df['demand_score'].max(), 2))
    with col3:
        st.metric("Average Score", round(df['demand_score'].mean(), 2))


def render_company_info_card(profile: Dict[str, Any]):
    """Render company information card."""
    if not profile:
        return
    
    st.subheader("🏢 Company Information")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if profile.get("industry"):
            st.write(f"**Industry:** {profile['industry']}")
        if profile.get("company_size"):
            st.write(f"**Size:** {profile['company_size']}")
        if profile.get("headquarters"):
            st.write(f"**Headquarters:** {profile['headquarters']}")
    
    with col2:
        if profile.get("website"):
            st.write(f"**Website:** [{profile['website']}]({profile['website']})")
        if profile.get("linkedin_url"):
            st.write(f"**LinkedIn:** [View Profile]({profile['linkedin_url']})")
        if profile.get("enrichment_source"):
            st.caption(f"Source: {profile['enrichment_source']}")
    
    if profile.get("description"):
        st.write("**Description:**")
        st.write(profile['description'])


def render_recent_jobs(jobs: List[Dict[str, Any]], max_display: int = 5):
    """Render recent job postings for a company."""
    if not jobs:
        st.info("No recent jobs")
        return
    
    st.subheader("💼 Recent Job Postings")
    
    for job in jobs[:max_display]:
        with st.container():
            col1, col2, col3 = st.columns([3, 1, 1])
            
            with col1:
                st.write(f"**{job.get('job_title', 'N/A')}**")
                st.caption(f"Location: {job.get('location', 'N/A')}")
            
            with col2:
                st.write(f"Score: {round(job.get('demand_score', 0), 2)}")
            
            with col3:
                priority = job.get('priority_tag', 'Low')
                colors = {"High": "🔴", "Medium": "🟡", "Low": "🟢"}
                st.write(f"{colors.get(priority, '⚪')} {priority}")
            
            if job.get('job_url'):
                st.markdown(f"[View Job]({job['job_url']})")
            
            st.divider()
