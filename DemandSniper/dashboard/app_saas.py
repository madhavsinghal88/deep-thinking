"""
DemandSniper SaaS - Premium Intelligence Dashboard
Refactored for client-facing presentations and investor demos.
"""

import sys
import os
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import streamlit as st
from datetime import date, timedelta
import pandas as pd
import requests

# Import modular components
from components.saas_components import (
    render_kpi_card,
    render_opportunity_card,
    render_header_logo
)
from components.saas_charts import (
    render_enhanced_bar_chart,
    render_priority_donut_chart,
    render_trend_line_chart
)

# Premium SaaS Configuration
st.set_page_config(
    page_title="DemandSniper | Hiring Signal Intelligence",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

API_BASE_URL = "http://localhost:8000/api/v1"

# =============================================================================
# PREMIUM CSS - Glassmorphism & Animations
# =============================================================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    * {
        font-family: 'Inter', sans-serif;
    }
    
    /* Glassmorphism Cards */
    .glass-card {
        background: linear-gradient(135deg, rgba(30, 35, 41, 0.8) 0%, rgba(37, 43, 51, 0.8) 100%);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 16px;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
    }
    
    .glass-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.4);
        border-color: rgba(255, 75, 75, 0.3);
    }
    
    /* KPI Card Hover Effects */
    .saas-kpi-card {
        cursor: default;
    }
    
    .saas-kpi-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 12px 40px rgba(0, 0, 0, 0.4) !important;
    }
    
    /* Header Styles */
    .saas-header {
        background: linear-gradient(135deg, rgba(14, 17, 23, 0.95) 0%, rgba(26, 31, 38, 0.95) 100%);
        border-bottom: 1px solid rgba(255, 255, 255, 0.1);
        padding: 24px 0;
        margin-bottom: 32px;
    }
    
    .header-title {
        font-size: 2.5rem;
        font-weight: 800;
        background: linear-gradient(135deg, #FFFFFF 0%, #8B949E 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin: 0;
    }
    
    .header-subtitle {
        color: #8B949E;
        font-size: 1rem;
        font-weight: 400;
        margin-top: 8px;
        letter-spacing: 0.5px;
    }
    
    /* View Toggle */
    .view-toggle {
        display: flex;
        background: rgba(255, 255, 255, 0.05);
        border-radius: 12px;
        padding: 4px;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    .view-toggle-btn {
        padding: 10px 24px;
        border-radius: 8px;
        font-weight: 600;
        font-size: 0.9rem;
        transition: all 0.3s ease;
        cursor: pointer;
    }
    
    .view-toggle-btn.active {
        background: #FF4B4B;
        color: white;
    }
    
    .view-toggle-btn:not(.active) {
        color: #8B949E;
    }
    
    .view-toggle-btn:not(.active):hover {
        color: white;
        background: rgba(255, 255, 255, 0.1);
    }
    
    /* Navigation Styles */
    .nav-section {
        margin-bottom: 24px;
    }
    
    .nav-section-title {
        color: #8B949E;
        font-size: 0.7rem;
        text-transform: uppercase;
        letter-spacing: 2px;
        margin-bottom: 12px;
        padding-left: 16px;
    }
    
    .nav-item {
        padding: 12px 16px;
        border-radius: 10px;
        margin: 4px 0;
        color: #8B949E;
        font-weight: 500;
        transition: all 0.3s ease;
        cursor: pointer;
        display: flex;
        align-items: center;
        gap: 10px;
    }
    
    .nav-item:hover {
        background: rgba(255, 255, 255, 0.05);
        color: white;
        transform: translateX(4px);
    }
    
    .nav-item.active {
        background: linear-gradient(135deg, rgba(255, 75, 75, 0.2) 0%, rgba(255, 75, 75, 0.1) 100%);
        color: white;
        border-left: 3px solid #FF4B4B;
    }
    
    /* Section Headers */
    .section-header {
        font-size: 1.5rem;
        font-weight: 700;
        color: #FFFFFF;
        margin: 32px 0 20px 0;
        padding-left: 16px;
        border-left: 4px solid #FF4B4B;
    }
    
    /* Opportunity Cards */
    .opportunity-card {
        background: linear-gradient(135deg, rgba(30, 35, 41, 0.9) 0%, rgba(37, 43, 51, 0.9) 100%);
        border-left: 4px solid #FF4B4B;
        border-radius: 12px;
        padding: 20px;
        margin: 12px 0;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
        transition: all 0.3s ease;
    }
    
    .opportunity-card:hover {
        transform: translateX(8px);
        box-shadow: 0 8px 30px rgba(0, 0, 0, 0.3);
    }
    
    /* Animations */
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .animate-fade-in {
        animation: fadeInUp 0.6s ease-out forwards;
    }
    
    @keyframes pulse {
        0%, 100% {
            opacity: 1;
        }
        50% {
            opacity: 0.5;
        }
    }
    
    .animate-pulse {
        animation: pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
    }
    
    /* Loading Skeleton */
    .skeleton {
        background: linear-gradient(90deg, rgba(255,255,255,0.05) 25%, rgba(255,255,255,0.1) 50%, rgba(255,255,255,0.05) 75%);
        background-size: 200% 100%;
        animation: shimmer 1.5s infinite;
        border-radius: 8px;
    }
    
    @keyframes shimmer {
        0% {
            background-position: 200% 0;
        }
        100% {
            background-position: -200% 0;
        }
    }
    
    /* Tooltip */
    .tooltip {
        position: relative;
    }
    
    .tooltip:hover::after {
        content: attr(data-tooltip);
        position: absolute;
        bottom: 100%;
        left: 50%;
        transform: translateX(-50%);
        padding: 8px 12px;
        background: rgba(0, 0, 0, 0.9);
        color: white;
        font-size: 0.8rem;
        border-radius: 6px;
        white-space: nowrap;
        z-index: 1000;
    }
    
    /* Export Button */
    .export-btn {
        background: linear-gradient(135deg, #00C9A7 0%, #00E5C1 100%);
        color: white;
        border: none;
        padding: 12px 24px;
        border-radius: 8px;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.3s ease;
    }
    
    .export-btn:hover {
        transform: scale(1.05);
        box-shadow: 0 8px 25px rgba(0, 201, 167, 0.4);
    }
</style>
""", unsafe_allow_html=True)

# =============================================================================
# SESSION STATE INITIALIZATION
# =============================================================================
if 'view_mode' not in st.session_state:
    st.session_state.view_mode = "analytics"
if 'selected_company' not in st.session_state:
    st.session_state.selected_company = None

# =============================================================================
# HEADER COMPONENT
# =============================================================================
def render_saas_header():
    """Render the premium SaaS header with view toggle."""
    logo_svg = render_header_logo()
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col1:
        st.markdown(f"""
            <div style="display: flex; align-items: center; gap: 16px;">
                {logo_svg}
                <div>
                    <h1 style="font-size: 1.8rem; font-weight: 800; margin: 0; color: white;">DemandSniper</h1>
                </div>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
            <div style="text-align: center;">
                <div style="color: #8B949E; font-size: 0.9rem; letter-spacing: 1px; text-transform: uppercase;">
                    Hiring Signal Intelligence Across Skills, Companies & Countries
                </div>
            </div>
        """, unsafe_allow_html=True)
    
    with col3:
        # View Toggle
        col_a, col_b = st.columns(2)
        with col_a:
            if st.button("📊 Analytics", 
                        key="analytics_btn",
                        type="primary" if st.session_state.view_mode == "analytics" else "secondary",
                        use_container_width=True):
                st.session_state.view_mode = "analytics"
                st.rerun()
        with col_b:
            if st.button("🎯 Opportunities", 
                        key="opportunity_btn",
                        type="primary" if st.session_state.view_mode == "opportunity" else "secondary",
                        use_container_width=True):
                st.session_state.view_mode = "opportunity"
                st.rerun()
    
    st.markdown("<hr style='border: none; height: 1px; background: linear-gradient(90deg, transparent, rgba(255,255,255,0.1), transparent); margin: 20px 0;'>", unsafe_allow_html=True)

# =============================================================================
# SIDEBAR NAVIGATION
# =============================================================================
def render_saas_sidebar():
    """Render the premium sidebar navigation."""
    with st.sidebar:
        # Logo Area
        st.markdown("""
            <div style="padding: 20px 0; border-bottom: 1px solid rgba(255,255,255,0.1); margin-bottom: 20px;">
                <div style="font-size: 1.3rem; font-weight: 700; color: white;">🎯 DemandSniper</div>
                <div style="font-size: 0.75rem; color: #8B949E; margin-top: 4px;">SaaS Intelligence Platform</div>
            </div>
        """, unsafe_allow_html=True)
        
        # Global Section
        st.markdown('<div class="nav-section-title">Global</div>', unsafe_allow_html=True)
        
        pages = {
            "📊 Dashboard": "dashboard",
            "📡 Signals": "signals", 
            "🏢 Companies": "companies",
            "💼 Jobs": "jobs"
        }
        
        for label, key in pages.items():
            is_active = st.session_state.get('current_page', 'dashboard') == key
            css_class = "nav-item active" if is_active else "nav-item"
            
            if st.button(label, key=f"nav_{key}", use_container_width=True, 
                        type="primary" if is_active else "secondary"):
                st.session_state.current_page = key
                st.rerun()
        
        # Markets Section
        st.markdown('<div class="nav-section-title" style="margin-top: 24px;">Markets</div>', unsafe_allow_html=True)
        
        market_pages = {
            "🌍 Countries": "countries",
            "📈 Trends": "trends"
        }
        
        for label, key in market_pages.items():
            is_active = st.session_state.get('current_page') == key
            if st.button(label, key=f"nav_{key}", use_container_width=True,
                        type="primary" if is_active else "secondary"):
                st.session_state.current_page = key
                st.rerun()
        
        # Settings Section
        st.markdown('<div class="nav-section-title" style="margin-top: 24px;">System</div>', unsafe_allow_html=True)
        
        if st.button("⚙️ Settings", key="nav_settings", use_container_width=True):
            st.session_state.current_page = "settings"
            st.rerun()
        
        # Quick Stats
        st.markdown("<hr style='border: none; height: 1px; background: rgba(255,255,255,0.1); margin: 24px 0;'>", unsafe_allow_html=True)
        
        try:
            response = requests.get(f"{API_BASE_URL}/analytics/dashboard-summary", timeout=5)
            if response.status_code == 200:
                data = response.json()
                
                st.markdown("""
                    <div style="background: rgba(255, 75, 75, 0.1); border-radius: 12px; padding: 16px; border: 1px solid rgba(255, 75, 75, 0.2);">
                        <div style="color: #8B949E; font-size: 0.75rem; text-transform: uppercase; letter-spacing: 1px;">High Priority</div>
                        <div style="color: #FF4B4B; font-size: 2rem; font-weight: 700; margin-top: 4px;">{}</div>
                        <div style="color: #8B949E; font-size: 0.8rem; margin-top: 4px;">Urgent signals</div>
                    </div>
                """.format(data.get('high_priority_companies', 0)), unsafe_allow_html=True)
        except:
            pass

# =============================================================================
# KPI DASHBOARD (Analytics View)
# =============================================================================
def render_kpi_dashboard(summary):
    """Render premium KPI cards."""
    st.markdown('<div class="animate-fade-in">', unsafe_allow_html=True)
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        render_kpi_card(
            title="Total SAP Jobs",
            value=summary.get('total_jobs', 0),
            subtext="Active hiring signals tracked",
            tag="📊 Live",
            tag_color="#0068C9"
        )
    
    with col2:
        render_kpi_card(
            title="High Priority",
            value=summary.get('high_priority_companies', 0),
            subtext="Recurring hiring signals detected",
            tag="🔥 Hot",
            tag_color="#FF4B4B",
            priority="high",
            help_text="Companies with demand score > 25 and multiple reposts"
        )
    
    with col3:
        render_kpi_card(
            title="This Month",
            value=summary.get('jobs_this_month', 0),
            subtext="New postings detected",
            tag="📈 +12%",
            tag_color="#00C9A7"
        )
    
    with col4:
        render_kpi_card(
            title="Countries",
            value=len(summary.get('platforms', {})),
            subtext="Global markets monitored",
            tag="🌍 Global",
            tag_color="#8B5CF6"
        )
    
    with col5:
        render_kpi_card(
            title="Platforms",
            value=3,
            subtext="Data sources integrated",
            tag="🔗 Active",
            tag_color="#F59E0B"
        )
    
    st.markdown('</div>', unsafe_allow_html=True)

# =============================================================================
# ANALYTICS VIEW
# =============================================================================
def render_analytics_view():
    """Render the Analytics view with charts."""
    try:
        summary = requests.get(f"{API_BASE_URL}/analytics/dashboard-summary").json()
        companies = requests.get(f"{API_BASE_URL}/companies?limit=10").json()
        trends = requests.get(f"{API_BASE_URL}/analytics/hiring-trends?days=30").json()
    except:
        st.error("⚠️ Unable to connect to API")
        return
    
    # KPI Cards
    st.markdown("<div class='section-header'>📊 Market Overview</div>", unsafe_allow_html=True)
    render_kpi_dashboard(summary)
    
    st.markdown("<hr style='border: none; height: 1px; background: rgba(255,255,255,0.1); margin: 32px 0;'>", unsafe_allow_html=True)
    
    # Charts Section
    col_chart1, col_chart2 = st.columns([2, 1])
    
    with col_chart1:
        st.markdown("<div class='section-header'>🏆 Top Companies by Demand Score</div>", unsafe_allow_html=True)
        fig = render_enhanced_bar_chart(companies)
        if fig:
            st.plotly_chart(fig, use_container_width=True)
        
        st.caption("💡 Click on any company to view detailed opportunity analysis")
    
    with col_chart2:
        st.markdown("<div class='section-header'>🎯 Priority Distribution</div>", unsafe_allow_html=True)
        fig2, insight = render_priority_donut_chart(companies)
        if fig2:
            st.plotly_chart(fig2, use_container_width=True)
            
            st.markdown(f"""
                <div style="background: rgba(255, 255, 255, 0.05); border-radius: 12px; padding: 16px; margin-top: 16px;">
                    <div style="color: #8B949E; font-size: 0.85rem; line-height: 1.5;">
                        {insight}
                    </div>
                </div>
            """, unsafe_allow_html=True)
    
    # Trends Section
    st.markdown("<div class='section-header' style='margin-top: 40px;'>📈 Hiring Activity (Last 30 Days)</div>", unsafe_allow_html=True)
    fig3 = render_trend_line_chart(trends)
    if fig3:
        st.plotly_chart(fig3, use_container_width=True)

# =============================================================================
# OPPORTUNITY VIEW
# =============================================================================
def render_opportunity_view():
    """Render the Opportunity view with actionable insights."""
    st.markdown("<div class='section-header'>🎯 Opportunity Intelligence</div>", unsafe_allow_html=True)
    
    st.markdown("""
        <div style="background: linear-gradient(135deg, rgba(255, 75, 75, 0.1) 0%, rgba(255, 75, 75, 0.05) 100%); 
                    border: 1px solid rgba(255, 75, 75, 0.3); border-radius: 12px; padding: 20px; margin-bottom: 32px;">
            <div style="color: #FF4B4B; font-size: 1rem; font-weight: 600; margin-bottom: 8px;">💡 Opportunity Mode Active</div>
            <div style="color: #8B949E; font-size: 0.9rem;">
                AI-powered pitch recommendations based on hiring signals, posting patterns, and market demand.
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    # Filters
    col1, col2, col3 = st.columns([2, 2, 1])
    
    with col1:
        min_score = st.slider("Minimum Demand Score", 0, 100, 20)
    
    with col2:
        country_filter = st.selectbox(
            "Filter by Country",
            ["All Countries"] + ["United States", "Germany", "United Kingdom", "India", 
             "Canada", "Australia", "Switzerland", "Netherlands", "UAE", "Singapore"]
        )
    
    with col3:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("📥 Export CSV", use_container_width=True):
            # Export logic would go here
            st.success("Export functionality ready!")
    
    try:
        params = {"limit": 50}
        if country_filter != "All Countries":
            params["country"] = country_filter
        
        companies = requests.get(f"{API_BASE_URL}/companies", params=params).json()
        
        # Filter by minimum score
        companies = [c for c in companies if c['total_demand_score'] >= min_score]
        
        # Sort by demand score
        companies = sorted(companies, key=lambda x: x['total_demand_score'], reverse=True)
        
    except:
        st.error("Failed to load opportunities")
        return
    
    if companies:
        st.markdown(f"<div style='color: #8B949E; margin-bottom: 20px;'>Showing {len(companies)} opportunities matching your criteria</div>", unsafe_allow_html=True)
        
        # Render opportunity cards
        for company in companies[:20]:  # Limit to top 20
            render_opportunity_card(company)
    else:
        st.info("No opportunities match your criteria. Try lowering the minimum demand score.")

# =============================================================================
# MAIN APPLICATION
# =============================================================================
def main():
    """Main SaaS application."""
    # Render Header
    render_saas_header()
    
    # Render Sidebar
    render_saas_sidebar()
    
    # Get current page
    current_page = st.session_state.get('current_page', 'dashboard')
    
    # Route to appropriate view
    if current_page == 'dashboard':
        if st.session_state.view_mode == 'analytics':
            render_analytics_view()
        else:
            render_opportunity_view()
    elif current_page == 'signals':
        st.markdown("<div class='section-header'>📡 Signal Feed</div>", unsafe_allow_html=True)
        st.info("Real-time hiring signal feed - Coming in next release")
    elif current_page == 'companies':
        st.markdown("<div class='section-header'>🏢 Company Database</div>", unsafe_allow_html=True)
        st.info("Full company directory with detailed profiles - Coming in next release")
    elif current_page == 'jobs':
        st.markdown("<div class='section-header'>💼 Job Postings</div>", unsafe_allow_html=True)
        st.info("Detailed job posting explorer - Coming in next release")
    elif current_page == 'countries':
        st.markdown("<div class='section-header'>🌍 Global Markets</div>", unsafe_allow_html=True)
        st.info("Country-level market intelligence - Coming in next release")
    elif current_page == 'trends':
        st.markdown("<div class='section-header'>📈 Market Trends</div>", unsafe_allow_html=True)
        st.info("Historical trend analysis - Coming in next release")
    elif current_page == 'settings':
        st.markdown("<div class='section-header'>⚙️ Platform Settings</div>", unsafe_allow_html=True)
        st.info("Configuration and API settings - Coming in next release")

if __name__ == "__main__":
    main()
