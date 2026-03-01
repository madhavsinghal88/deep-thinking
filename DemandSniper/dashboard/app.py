import streamlit as st
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import requests

st.set_page_config(
    page_title="DemandSniper",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

API_BASE_URL = "http://localhost:8000/api/v1"

# Simple, working CSS
st.markdown("""
<style>
    .stApp { background-color: #0f1117 !important; }
    .main { background-color: #0f1117 !important; }
    h1 { color: white !important; }
    h2 { color: white !important; }
    p { color: #9ca3af !important; }
    .stMetric { 
        background-color: #1f2937 !important; 
        border-radius: 10px; 
        padding: 20px !important;
        border: 1px solid #374151;
    }
    .stMetric label { color: #9ca3af !important; font-size: 14px !important; }
    .stMetric .css-1xarl3l { color: white !important; font-size: 36px !important; font-weight: bold !important; }
</style>
""", unsafe_allow_html=True)

st.title("🎯 DemandSniper")
st.subheader("Hiring Signal Intelligence Platform")

# Fetch data
try:
    summary = requests.get(f"{API_BASE_URL}/analytics/dashboard-summary", timeout=5).json()
    companies = requests.get(f"{API_BASE_URL}/companies?limit=10", timeout=5).json()
    
    # KPI Cards
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total SAP Jobs", summary.get('total_jobs', 0), "+12%")
    
    with col2:
        st.metric("High Priority Signals", summary.get('high_priority_companies', 0), "Hot")
    
    with col3:
        st.metric("Countries", 10)
    
    with col4:
        st.metric("Data Sources", len(summary.get('platforms', {})))
    
    st.divider()
    
    # Companies Table
    st.header("Top Companies by Demand Score")
    
    if companies:
        import pandas as pd
        df = pd.DataFrame(companies[:10])
        df = df[['company_name', 'total_demand_score', 'total_openings', 'highest_priority']]
        df.columns = ['Company', 'Demand Score', 'Openings', 'Priority']
        
        # Color code priorities
        def color_priority(val):
            if val == "High":
                return "color: #ef4444; font-weight: bold;"
            elif val == "Medium":
                return "color: #f59e0b; font-weight: bold;"
            else:
                return "color: #10b981; font-weight: bold;"
        
        styled_df = df.style.applymap(color_priority, subset=['Priority'])
        st.dataframe(styled_df, use_container_width=True, hide_index=True)
    else:
        st.info("No company data available")
    
    st.divider()
    
    # Platform Distribution
    st.header("Platform Distribution")
    platforms = summary.get('platforms', {})
    if platforms:
        import pandas as pd
        plat_df = pd.DataFrame(list(platforms.items()), columns=['Platform', 'Jobs'])
        st.bar_chart(plat_df.set_index('Platform'))
    
except Exception as e:
    st.error(f"Error loading data: {e}")
    st.info("Please make sure the API server is running on port 8000")
