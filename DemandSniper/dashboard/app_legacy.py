import sys
import os
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

import streamlit as st
import httpx
import asyncio
from datetime import date, timedelta
import pandas as pd

# Modern styling
st.set_page_config(
    page_title="DemandSniper | SAP Architect Intelligence",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for modern look
st.markdown("""
<style>
    /* Modern color scheme */
    :root {
        --primary-color: #FF4B4B;
        --secondary-color: #0068C9;
        --accent-color: #00C9A7;
        --bg-color: #0E1117;
        --card-bg: #1E2329;
    }
    
    /* Main container */
    .main {
        background: linear-gradient(135deg, #0E1117 0%, #1a1f26 100%);
    }
    
    /* Headers */
    h1 {
        color: #FFFFFF !important;
        font-size: 3rem !important;
        font-weight: 800 !important;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
        margin-bottom: 0.5rem !important;
    }
    
    h2 {
        color: #00C9A7 !important;
        font-size: 2rem !important;
        font-weight: 600 !important;
        border-left: 4px solid #FF4B4B;
        padding-left: 1rem;
        margin-top: 2rem !important;
    }
    
    h3 {
        color: #FFFFFF !important;
        font-size: 1.5rem !important;
        font-weight: 500 !important;
    }
    
    /* Cards */
    .stMetric {
        background: linear-gradient(135deg, #1E2329 0%, #252B33 100%);
        border: 1px solid rgba(255,255,255,0.1);
        border-radius: 16px;
        padding: 1.5rem;
        box-shadow: 0 8px 32px rgba(0,0,0,0.3);
    }
    
    .stMetric:hover {
        transform: translateY(-2px);
        box-shadow: 0 12px 40px rgba(0,0,0,0.4);
    }
    
    .stMetric label {
        color: #8B949E !important;
        font-size: 0.9rem !important;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    .stMetric .css-1xarl3l {
        color: #FFFFFF !important;
        font-size: 2.5rem !important;
        font-weight: 700 !important;
    }
    
    /* Sidebar */
    .css-1d391kg {
        background: linear-gradient(180deg, #161B22 0%, #0E1117 100%);
    }
    
    /* Tables */
    .stDataFrame {
        border-radius: 12px;
        overflow: hidden;
    }
    
    /* Priority badges */
    .priority-high {
        background: linear-gradient(135deg, #FF4B4B, #FF6B6B);
        color: white;
        padding: 4px 12px;
        border-radius: 20px;
        font-weight: 600;
        font-size: 0.85rem;
    }
    
    .priority-medium {
        background: linear-gradient(135deg, #FFA500, #FFB84D);
        color: white;
        padding: 4px 12px;
        border-radius: 20px;
        font-weight: 600;
        font-size: 0.85rem;
    }
    
    .priority-low {
        background: linear-gradient(135deg, #00C9A7, #00E5C1);
        color: white;
        padding: 4px 12px;
        border-radius: 20px;
        font-weight: 600;
        font-size: 0.85rem;
    }
    
    /* Expander */
    .streamlit-expanderHeader {
        background: #1E2329;
        border-radius: 8px;
        border: 1px solid rgba(255,255,255,0.1);
    }
    
    /* Buttons */
    .stButton>button {
        background: linear-gradient(135deg, #FF4B4B, #FF6B6B);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stButton>button:hover {
        transform: scale(1.05);
        box-shadow: 0 8px 25px rgba(255,75,75,0.4);
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: #1E2329;
        border-radius: 8px 8px 0 0;
        padding: 1rem 2rem;
        color: #8B949E;
    }
    
    .stTabs [aria-selected="true"] {
        background: #FF4B4B !important;
        color: white !important;
    }
    
    /* Country cards */
    .country-card {
        background: linear-gradient(135deg, #1E2329 0%, #252B33 100%);
        border: 1px solid rgba(255,255,255,0.1);
        border-radius: 12px;
        padding: 1.5rem;
        margin: 0.5rem 0;
        transition: all 0.3s ease;
    }
    
    .country-card:hover {
        border-color: #FF4B4B;
        transform: translateX(5px);
    }
</style>
""", unsafe_allow_html=True)

API_BASE_URL = "http://localhost:8000/api/v1"

# Navigation
def main():
    """Main dashboard application."""
    # Header
    st.markdown("""
    <div style="text-align: center; padding: 2rem 0;">
        <h1 style="font-size: 3.5rem; margin-bottom: 0;">🎯 DemandSniper</h1>
        <p style="font-size: 1.3rem; color: #8B949E; margin-top: 0.5rem;">
            SAP Architect Hiring Intelligence | Global Opportunity Detection
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.markdown("### 🌍 Global Navigation")
        page = st.radio(
            "",
            ["📊 Dashboard", "🌍 Countries", "🏢 Companies", "💼 Jobs", "➕ Add Job", "⚙️ Settings"],
            label_visibility="collapsed"
        )
        
        st.divider()
        
        # Quick stats in sidebar
        st.markdown("### 📈 Quick Stats")
        try:
            import requests
            response = requests.get(f"{API_BASE_URL}/analytics/dashboard-summary")
            if response.status_code == 200:
                data = response.json()
                st.metric("Total Jobs", data.get('total_jobs', 0))
                st.metric("High Priority", data.get('high_priority_companies', 0))
        except:
            pass
    
    # Route to page
    if "Dashboard" in page:
        render_dashboard()
    elif "Countries" in page:
        render_countries_page()
    elif "Companies" in page:
        render_companies_page()
    elif "Jobs" in page:
        render_jobs_page()
    elif "Add Job" in page:
        render_add_job_page()
    else:
        render_config_page()


def render_dashboard():
    """Render modern dashboard."""
    # Fetch data
    try:
        import requests
        summary = requests.get(f"{API_BASE_URL}/analytics/dashboard-summary").json()
        companies = requests.get(f"{API_BASE_URL}/companies?limit=10").json()
        trends = requests.get(f"{API_BASE_URL}/analytics/hiring-trends?days=30").json()
    except:
        st.error("⚠️ API Connection Error")
        return
    
    # Hero metrics
    st.markdown("### 📊 Global Market Overview")
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric("🎯 Total SAP Jobs", summary.get('total_jobs', 0), delta="+12%")
    with col2:
        st.metric("🔴 High Priority", summary.get('high_priority_companies', 0), delta="Hot")
    with col3:
        st.metric("🟡 Medium Priority", summary.get('total_jobs', 0) - summary.get('high_priority_companies', 0) * 2)
    with col4:
        st.metric("📅 This Month", summary.get('jobs_this_month', 0))
    with col5:
        st.metric("🌍 Platforms", len(summary.get('platforms', {})))
    
    st.divider()
    
    # Charts section
    col_chart1, col_chart2 = st.columns([2, 1])
    
    with col_chart1:
        st.markdown("### 🏆 Top 10 Companies by Demand Score")
        
        if companies:
            import plotly.graph_objects as go
            
            df = pd.DataFrame(companies[:10])
            
            # Color based on priority
            colors = []
            for priority in df['highest_priority']:
                if priority == 'High':
                    colors.append('#FF4B4B')
                elif priority == 'Medium':
                    colors.append('#FFA500')
                else:
                    colors.append('#00C9A7')
            
            fig = go.Figure(go.Bar(
                x=df['total_demand_score'],
                y=df['company_name'],
                orientation='h',
                marker=dict(
                    color=colors,
                    line=dict(color='rgba(255,255,255,0.2)', width=1)
                ),
                text=df['total_openings'].apply(lambda x: f'{x} openings'),
                textposition='inside',
                insidetextanchor='middle',
                textfont=dict(color='white', size=11)
            ))
            
            fig.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='white'),
                xaxis=dict(
                    title='Demand Score',
                    gridcolor='rgba(255,255,255,0.1)',
                    showgrid=True
                ),
                yaxis=dict(
                    title='',
                    gridcolor='rgba(255,255,255,0.1)',
                    autorange='reversed'
                ),
                margin=dict(l=10, r=10, t=30, b=10),
                height=500
            )
            
            st.plotly_chart(fig, use_container_width=True)
    
    with col_chart2:
        st.markdown("### 🎯 Priority Distribution")
        
        high = sum(1 for c in companies if c['highest_priority'] == 'High')
        medium = sum(1 for c in companies if c['highest_priority'] == 'Medium')
        low = sum(1 for c in companies if c['highest_priority'] == 'Low')
        
        fig2 = go.Figure(go.Pie(
            labels=['High Priority', 'Medium Priority', 'Low Priority'],
            values=[high, medium, low],
            hole=0.6,
            marker=dict(
                colors=['#FF4B4B', '#FFA500', '#00C9A7'],
                line=dict(color='rgba(0,0,0,0)', width=0)
            ),
            textinfo='label+percent',
            textfont=dict(color='white', size=12),
            hovertemplate='<b>%{label}</b><br>Companies: %{value}<br>Percentage: %{percent}<extra></extra>'
        ))
        
        fig2.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white'),
            showlegend=False,
            margin=dict(l=10, r=10, t=30, b=10),
            height=400
        )
        
        st.plotly_chart(fig2, use_container_width=True)
    
    st.divider()
    
    # Hiring trends
    st.markdown("### 📈 Hiring Activity (Last 30 Days)")
    
    if trends:
        df_trends = pd.DataFrame(trends)
        df_trends['date'] = pd.to_datetime(df_trends['date'])
        
        fig3 = go.Figure()
        
        fig3.add_trace(go.Scatter(
            x=df_trends['date'],
            y=df_trends['count'],
            mode='lines+markers',
            line=dict(color='#00C9A7', width=3),
            marker=dict(size=8, color='#FF4B4B', line=dict(color='white', width=2)),
            fill='tozeroy',
            fillcolor='rgba(0,201,167,0.2)',
            name='Daily Postings'
        ))
        
        # Add 7-day moving average
        if len(df_trends) >= 7:
            df_trends['ma7'] = df_trends['count'].rolling(window=7, min_periods=1).mean()
            fig3.add_trace(go.Scatter(
                x=df_trends['date'],
                y=df_trends['ma7'],
                mode='lines',
                line=dict(color='#FFA500', width=2, dash='dash'),
                name='7-Day Average'
            ))
        
        fig3.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white'),
            xaxis=dict(
                title='Date',
                gridcolor='rgba(255,255,255,0.1)',
                showgrid=True
            ),
            yaxis=dict(
                title='New Postings',
                gridcolor='rgba(255,255,255,0.1)',
                showgrid=True
            ),
            legend=dict(
                orientation='h',
                yanchor='bottom',
                y=1.02,
                xanchor='right',
                x=1,
                font=dict(color='white')
            ),
            margin=dict(l=10, r=10, t=50, b=10),
            height=400
        )
        
        st.plotly_chart(fig3, use_container_width=True)


def render_countries_page():
    """Render countries overview page."""
    st.markdown("## 🌍 SAP Architect Market by Country")
    
    countries = [
        ("🇺🇸 United States", "High - Thousands", "LinkedIn, Indeed, Dice, Glassdoor", "140k-280k USD"),
        ("🇩🇪 Germany", "~160+ openings", "LinkedIn, Glassdoor, Indeed DE", "80k-150k EUR"),
        ("🇬🇧 United Kingdom", "Hundreds", "LinkedIn, Indeed UK, Adzuna", "70k-160k GBP"),
        ("🇮🇳 India", "~3,000+ jobs", "LinkedIn India, Naukri, Indeed", "25L-100L INR"),
        ("🇨🇦 Canada", "Moderate", "LinkedIn Canada, Indeed Canada", "110k-220k CAD"),
        ("🇦🇺 Australia", "Moderate", "LinkedIn Australia, SEEK, Indeed", "130k-250k AUD"),
        ("🇨🇭 Switzerland", "Moderate", "LinkedIn, Indeed CH, Glassdoor", "120k-200k CHF"),
        ("🇳🇱 Netherlands", "Moderate", "LinkedIn NL, Indeed NL", "80k-140k EUR"),
        ("🇦🇪 UAE", "~20-50+ roles", "Indeed UAE, LinkedIn, Bayt", "25k-55k AED"),
        ("🇸🇬 Singapore", "~1,400+ jobs", "JobStreet, LinkedIn, Indeed", "120k-260k SGD"),
    ]
    
    for i, (country, volume, boards, salary) in enumerate(countries):
        with st.container():
            col1, col2, col3, col4 = st.columns([2, 1, 2, 1])
            
            with col1:
                st.markdown(f"<h3 style='margin:0;'>{country}</h3>", unsafe_allow_html=True)
                st.caption(f"💰 {salary}")
            
            with col2:
                st.metric("Volume", volume)
            
            with col3:
                st.caption(f"📌 **Top Platforms:** {boards}")
            
            with col4:
                if st.button("View Jobs", key=f"country_{i}"):
                    st.session_state.selected_country = country.split()[1]
                    st.rerun()
            
            st.divider()


def render_companies_page():
    """Render companies page with better styling."""
    st.markdown("## 🏢 Top SAP Hiring Companies")
    
    # Filters
    col1, col2, col3 = st.columns([2, 2, 1])
    
    with col1:
        country_filter = st.selectbox(
            "🌍 Filter by Country",
            ["All Countries", "United States", "Germany", "United Kingdom", "India", 
             "Canada", "Australia", "Switzerland", "Netherlands", "UAE", "Singapore"]
        )
    
    with col2:
        priority_filter = st.multiselect(
            "🎯 Priority Level",
            ["High", "Medium", "Low"],
            default=["High", "Medium"]
        )
    
    with col3:
        limit = st.selectbox("Show", [10, 25, 50, 100], index=1)
    
    # Fetch data
    try:
        import requests
        params = {"limit": limit}
        if country_filter != "All Countries":
            params["country"] = country_filter
        
        response = requests.get(f"{API_BASE_URL}/companies", params=params)
        companies = response.json()
        
        # Filter by priority
        if priority_filter:
            companies = [c for c in companies if c['highest_priority'] in priority_filter]
        
    except:
        st.error("Failed to load companies")
        return
    
    # Display
    if companies:
        df = pd.DataFrame(companies)
        
        # Style the dataframe
        def color_priority(val):
            if val == "High":
                return "background-color: #FF4B4B; color: white; font-weight: 600;"
            elif val == "Medium":
                return "background-color: #FFA500; color: white; font-weight: 600;"
            else:
                return "background-color: #00C9A7; color: white; font-weight: 600;"
        
        styled_df = df.style.applymap(
            color_priority,
            subset=["highest_priority"]
        ).format({
            "total_demand_score": "{:.1f}",
            "total_openings": "{}"
        })
        
        st.dataframe(
            styled_df,
            use_container_width=True,
            hide_index=True,
            column_config={
                "company_name": st.column_config.TextColumn("Company", width="large"),
                "total_demand_score": st.column_config.NumberColumn("Demand Score", format="%.1f"),
                "highest_priority": st.column_config.TextColumn("Priority"),
                "total_openings": st.column_config.NumberColumn("Openings"),
                "last_active": st.column_config.DateColumn("Last Active"),
            }
        )
        
        # Company detail view
        st.divider()
        st.markdown("### 🔍 Company Detail")
        
        selected = st.selectbox("Select a company to view details", 
                               [c['company_name'] for c in companies])
        
        if selected:
            render_company_detail(selected)


def render_company_detail(company_name):
    """Render detailed company view."""
    try:
        import requests
        company = requests.get(f"{API_BASE_URL}/companies/{company_name}").json()
        
        if not company:
            return
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Jobs", company.get('total_jobs', 0))
        with col2:
            st.metric("Total Openings", company.get('total_openings', 0))
        with col3:
            st.metric("Demand Score", round(company.get('total_demand_score', 0), 1))
        with col4:
            priority = company.get('highest_priority', 'Low')
            st.markdown(f"**Priority:** <span class='priority-{priority.lower()}'>{priority}</span>", 
                       unsafe_allow_html=True)
        
        # Recent jobs
        if company.get('recent_jobs'):
            st.markdown("#### 💼 Recent Job Postings")
            st.caption("ℹ️ Demo Mode: Links open job search for this company")
            
            for job in company['recent_jobs'][:5]:
                with st.expander(f"{job['job_title']} - {job['location'] or 'Remote'}"):
                    col_j1, col_j2 = st.columns([3, 1])
                    with col_j1:
                        st.write(f"**Platform:** {job['platform_source'].title()}")
                        st.write(f"**Salary:** {job['salary_range'] or 'Not disclosed'}")
                        st.write(f"**Posted:** {job['posting_date']}")
                    with col_j2:
                        st.metric("Demand Score", round(job['demand_score'], 1))
                        st.write(f"**Priority:** {job['priority_tag']}")
                    
                    # Create job search links instead of using mock URLs
                    company_name = job.get('company_name', '')
                    job_title = job.get('job_title', '')
                    
                    # Build search URLs
                    linkedin_search = f"https://www.linkedin.com/jobs/search/?keywords={job_title.replace(' ', '%20')}%20{company_name.replace(' ', '%20')}"
                    indeed_search = f"https://www.indeed.com/jobs?q={job_title.replace(' ', '+')}+{company_name.replace(' ', '+')}"
                    google_search = f"https://www.google.com/search?q={job_title.replace(' ', '+')}+{company_name.replace(' ', '+')}+jobs"
                    
                    st.markdown(f"""
                    <div style="display: flex; gap: 10px; flex-wrap: wrap;">
                        <a href="{linkedin_search}" target="_blank" style="text-decoration: none;">
                            <span style="background: #0077B5; color: white; padding: 5px 15px; border-radius: 20px; font-size: 0.9rem;">💼 LinkedIn</span>
                        </a>
                        <a href="{indeed_search}" target="_blank" style="text-decoration: none;">
                            <span style="background: #2557A7; color: white; padding: 5px 15px; border-radius: 20px; font-size: 0.9rem;">🔍 Indeed</span>
                        </a>
                        <a href="{google_search}" target="_blank" style="text-decoration: none;">
                            <span style="background: #4285F4; color: white; padding: 5px 15px; border-radius: 20px; font-size: 0.9rem;">🌐 Google</span>
                        </a>
                    </div>
                    """, unsafe_allow_html=True)
        
    except Exception as e:
        st.error(f"Error loading company details: {e}")


def render_jobs_page():
    """Render jobs page."""
    st.markdown("## 💼 SAP Architect Job Postings")
    
    # Filters
    col1, col2, col3 = st.columns(3)
    
    with col1:
        country = st.selectbox("🌍 Country", ["All"] + ["United States", "Germany", "United Kingdom", 
                          "India", "Canada", "Australia", "Switzerland", "Netherlands", "UAE", "Singapore"])
    
    with col2:
        platform = st.selectbox("📌 Platform", ["All", "LinkedIn", "Indeed", "Dice"])
    
    with col3:
        priority = st.selectbox("🎯 Priority", ["All", "High", "Medium", "Low"])
    
    try:
        import requests
        params = {"limit": 100}
        if country != "All":
            params["country"] = country
        if platform != "All":
            params["platform"] = platform.lower()
        if priority != "All":
            params["priority"] = priority
        
        jobs = requests.get(f"{API_BASE_URL}/jobs", params=params).json()
        
        if jobs:
            st.caption("ℹ️ Demo Mode: Click 'Search' buttons to find real job postings")
            
            # Display jobs in cards with search links
            for i, job in enumerate(jobs[:20]):  # Limit to 20 for performance
                with st.container():
                    col1, col2, col3 = st.columns([2, 1, 1])
                    
                    with col1:
                        st.markdown(f"**{job['job_title']}**")
                        st.write(f"🏢 {job['company_name']} | 📍 {job['location'] or 'Remote'}")
                        st.write(f"💰 {job['salary_range'] or 'Salary not disclosed'}")
                    
                    with col2:
                        priority_color = "#FF4B4B" if job['priority_tag'] == 'High' else "#FFA500" if job['priority_tag'] == 'Medium' else "#00C9A7"
                        st.markdown(f"<span style='background: {priority_color}; color: white; padding: 4px 12px; border-radius: 20px; font-size: 0.85rem;'>{job['priority_tag']}</span>", unsafe_allow_html=True)
                        st.caption(f"Score: {job['demand_score']:.1f}")
                    
                    with col3:
                        # Create search links
                        company = job.get('company_name', '')
                        title = job.get('job_title', '')
                        
                        linkedin_search = f"https://www.linkedin.com/jobs/search/?keywords={title.replace(' ', '%20')}%20{company.replace(' ', '%20')}"
                        indeed_search = f"https://www.indeed.com/jobs?q={title.replace(' ', '+')}+{company.replace(' ', '+')}"
                        
                        st.markdown(f"<a href='{linkedin_search}' target='_blank'><button style='background: #0077B5; color: white; border: none; padding: 5px 15px; border-radius: 5px; cursor: pointer; width: 100%; margin-bottom: 5px;'>💼 LinkedIn</button></a>", unsafe_allow_html=True)
                        st.markdown(f"<a href='{indeed_search}' target='_blank'><button style='background: #2557A7; color: white; border: none; padding: 5px 15px; border-radius: 5px; cursor: pointer; width: 100%;'>🔍 Indeed</button></a>", unsafe_allow_html=True)
                    
                    st.divider()
            
            if len(jobs) > 20:
                st.info(f"Showing 20 of {len(jobs)} jobs. Use filters to narrow results.")
                
        else:
            st.info("No jobs found matching your criteria")
            
    except:
        st.error("Failed to load jobs")


def render_add_job_page():
    """Render add job form."""
    st.markdown("## ➕ Add New SAP Job")
    
    with st.form("add_job_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            company = st.text_input("🏢 Company Name", placeholder="e.g., Deloitte")
            title = st.selectbox("💼 Job Title", [
                "SAP Architect",
                "SAP Technical Architect",
                "SAP Solution Architect",
                "SAP Enterprise Architect",
                "Senior SAP Architect",
                "Lead SAP Architect",
                "SAP S/4HANA Architect",
                "SAP Cloud Architect"
            ])
            location = st.text_input("📍 Location", placeholder="e.g., New York, NY")
        
        with col2:
            country = st.selectbox("🌍 Country", [
                "United States", "Germany", "United Kingdom", "India",
                "Canada", "Australia", "Switzerland", "Netherlands", "UAE", "Singapore"
            ])
            platform = st.selectbox("📌 Platform", ["LinkedIn", "Indeed", "Dice", "Other"])
            url = st.text_input("🔗 Job URL", placeholder="https://...")
        
        salary = st.text_input("💰 Salary Range", placeholder="e.g., $150k - $200k")
        openings = st.number_input("👥 Number of Openings", min_value=1, max_value=50, value=1)
        
        submitted = st.form_submit_button("🚀 Add Job", use_container_width=True)
        
        if submitted:
            if company and title and url:
                try:
                    import requests
                    job_data = {
                        "company_name": company,
                        "job_title": title,
                        "country": country,
                        "platform_source": platform.lower(),
                        "job_url": url,
                        "location": location if location else None,
                        "salary_range": salary if salary else None,
                        "number_of_openings": openings,
                        "posting_date": date.today().isoformat()
                    }
                    
                    response = requests.post(f"{API_BASE_URL}/jobs", json=job_data)
                    
                    if response.status_code == 200:
                        st.success("✅ Job added successfully!")
                        st.balloons()
                    elif response.status_code == 400:
                        st.warning("⚠️ This job URL already exists in the database")
                    else:
                        st.error(f"❌ Error: {response.text}")
                except Exception as e:
                    st.error(f"❌ Failed to add job: {e}")
            else:
                st.error("❌ Please fill in all required fields")


def render_config_page():
    """Render configuration page."""
    st.markdown("## ⚙️ Configuration")
    
    tab1, tab2, tab3 = st.tabs(["🤖 Scraper Control", "📊 Settings", "🔔 Notifications"])
    
    with tab1:
        st.markdown("### Scraper Control")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("▶️ Start Scheduler", use_container_width=True):
                try:
                    import requests
                    requests.post(f"{API_BASE_URL}/scraper/start")
                    st.success("Scheduler started!")
                except:
                    st.error("Failed to start")
        
        with col2:
            if st.button("⏹️ Stop Scheduler", use_container_width=True):
                try:
                    import requests
                    requests.post(f"{API_BASE_URL}/scraper/stop")
                    st.success("Scheduler stopped!")
                except:
                    st.error("Failed to stop")
        
        with col3:
            if st.button("🔄 Run Now", use_container_width=True):
                with st.spinner("Running scraper..."):
                    try:
                        import requests
                        response = requests.post(f"{API_BASE_URL}/scraper/run")
                        if response.status_code == 200:
                            results = response.json()
                            st.success(f"✅ Scraped {results.get('total_jobs_found', 0)} jobs!")
                    except:
                        st.error("Failed to run scraper")
    
    with tab2:
        st.markdown("### Search Settings")
        st.info("Update config/search_config.yaml to modify search parameters")
        
        with st.expander("📄 View Current Configuration"):
            try:
                with open('/Users/madhavsinghal/code/others/DemandSniper/config/search_config.yaml', 'r') as f:
                    st.code(f.read(), language='yaml')
            except:
                st.error("Could not load configuration file")
    
    with tab3:
        st.markdown("### Notification Settings")
        st.info("Configure webhook and email notifications in config/scoring_config.yaml")


if __name__ == "__main__":
    main()
