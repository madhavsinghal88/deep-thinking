import streamlit as st
from typing import Optional
from datetime import date, timedelta


def render_filters():
    """Render global filter widgets in the sidebar."""
    st.sidebar.header("🔍 Filters")
    
    filters = {}
    
    # Country filter
    filters["country"] = st.sidebar.selectbox(
        "Country",
        options=["All", "United States", "United Kingdom", "Canada", "Germany", "India"],
        index=0
    )
    if filters["country"] == "All":
        filters["country"] = None
    
    # Skill keyword filter
    filters["skill_keyword"] = st.sidebar.text_input(
        "Skill Keyword",
        placeholder="e.g., Python, React, AWS"
    )
    if not filters["skill_keyword"]:
        filters["skill_keyword"] = None
    
    # Platform filter
    filters["platform"] = st.sidebar.selectbox(
        "Platform",
        options=["All", "Indeed", "Dice", "LinkedIn"],
        index=0
    )
    if filters["platform"] == "All":
        filters["platform"] = None
    else:
        filters["platform"] = filters["platform"].lower()
    
    # Date range filter
    st.sidebar.subheader("Date Range")
    col1, col2 = st.sidebar.columns(2)
    with col1:
        filters["start_date"] = st.date_input(
            "From",
            value=date.today() - timedelta(days=30),
            max_value=date.today()
        )
    with col2:
        filters["end_date"] = st.date_input(
            "To",
            value=date.today(),
            max_value=date.today()
        )
    
    # Priority filter
    filters["priority"] = st.sidebar.selectbox(
        "Priority",
        options=["All", "High", "Medium", "Low"],
        index=0
    )
    if filters["priority"] == "All":
        filters["priority"] = None
    
    # Company search
    filters["company_search"] = st.sidebar.text_input(
        "Search Company",
        placeholder="Company name..."
    )
    
    return filters


def render_dashboard_filters():
    """Render simplified filters for dashboard view."""
    col1, col2, col3 = st.columns(3)
    
    with col1:
        days = st.selectbox(
            "Time Period",
            options=[7, 14, 30, 60, 90],
            format_func=lambda x: f"Last {x} days"
        )
    
    with col2:
        top_n = st.selectbox(
            "Show Top",
            options=[5, 10, 20, 50],
            index=1
        )
    
    with col3:
        country = st.selectbox(
            "Country",
            options=["All", "United States", "United Kingdom", "Canada"],
            index=0
        )
    
    return {
        "days": days,
        "top_n": top_n,
        "country": country if country != "All" else None
    }
