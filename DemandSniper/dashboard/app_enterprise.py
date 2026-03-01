import streamlit as st
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from datetime import date, timedelta
import pandas as pd
import requests

st.set_page_config(
    page_title="DemandSniper | Enterprise Intelligence",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

API_BASE_URL = "http://localhost:8000/api/v1"

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
* { font-family: 'Inter', sans-serif; }
.stApp { background: #0B0F19 !important; }
.main { background: #0B0F19 !important; }
.block-container { padding: 0 !important; max-width: 100% !important; }
[data-testid="stSidebar"] { background: #0D111C !important; border-right: 1px solid rgba(255,255,255,0.06); }
.glass-card { background: rgba(255,255,255,0.02); backdrop-filter: blur(20px); border: 1px solid rgba(255,255,255,0.08); border-radius: 18px; transition: all 0.2s ease; }
.glass-card:hover { transform: translateY(-4px); border-color: rgba(255,255,255,0.12); box-shadow: 0 20px 40px rgba(0,0,0,0.4); }
.priority-card { background: rgba(255,255,255,0.02); backdrop-filter: blur(20px); border: 1px solid rgba(239,68,68,0.3); border-radius: 18px; box-shadow: 0 0 30px rgba(239,68,68,0.1); }
@keyframes pulse { 0%,100% { opacity: 1; transform: scale(1); } 50% { opacity: 0.5; transform: scale(1.2); } }
.pulse-dot { width: 8px; height: 8px; background: #EF4444; border-radius: 50%; animation: pulse 2s ease-in-out infinite; box-shadow: 0 0 10px rgba(239,68,68,0.6); }
h1, h2, h3 { color: #F8FAFC !important; font-weight: 600 !important; letter-spacing: -0.02em; }
.kpi-value { font-size: 48px; font-weight: 700; color: #F8FAFC; line-height: 1; }
.kpi-label { font-size: 13px; color: #64748B; font-weight: 500; text-transform: uppercase; letter-spacing: 0.05em; }
.trend-up { color: #10B981; font-size: 13px; font-weight: 600; }
.nav-item { padding: 12px 16px; border-radius: 12px; color: #64748B; font-weight: 500; font-size: 14px; transition: all 0.15s ease; cursor: pointer; margin: 4px 0; }
.nav-item:hover { background: rgba(255,255,255,0.04); color: #F8FAFC; }
.nav-item.active { background: rgba(255,255,255,0.08); color: #F8FAFC; }
.badge-high { background: rgba(239,68,68,0.15); color: #EF4444; padding: 6px 12px; border-radius: 6px; font-size: 12px; font-weight: 600; }
.badge-medium { background: rgba(245,158,11,0.15); color: #F59E0B; padding: 6px 12px; border-radius: 6px; font-size: 12px; font-weight: 600; }
.badge-low { background: rgba(16,185,129,0.15); color: #10B981; padding: 6px 12px; border-radius: 6px; font-size: 12px; font-weight: 600; }
.progress-bg { background: rgba(255,255,255,0.06); border-radius: 4px; height: 8px; overflow: hidden; }
</style>
""", unsafe_allow_html=True)

def render_sidebar():
    with st.sidebar:
        st.markdown("""
            <div style="padding: 8px 0 32px 0; border-bottom: 1px solid rgba(255,255,255,0.06);">
                <div style="font-size: 22px; font-weight: 700; color: #F8FAFC; letter-spacing: -0.02em;">DemandSniper</div>
                <div style="font-size: 12px; color: #64748B; margin-top: 4px;">Enterprise Intelligence</div>
            </div>
        """, unsafe_allow_html=True)
        
        nav_items = [("Overview", True), ("Markets", False), ("Companies", False), ("Skills", False), ("Signals", False), ("Reports", False)]
        for item, active in nav_items:
            css = "nav-item active" if active else "nav-item"
            st.markdown(f"<div class='{css}'>{item}</div>", unsafe_allow_html=True)

def main():
    try:
        summary = requests.get(f"{API_BASE_URL}/analytics/dashboard-summary", timeout=5).json()
        companies = requests.get(f"{API_BASE_URL}/companies?limit=10", timeout=5).json()
    except:
        summary = {"total_jobs": 229, "high_priority_companies": 67}
        companies = []
    
    render_sidebar()
    
    st.markdown("""
        <div style="padding: 32px 48px;">
            <h1 style="font-size: 32px; font-weight: 700; color: #F8FAFC; margin: 0;">Dashboard</h1>
            <p style="color: #64748B; margin-top: 8px;">Real-time hiring signal intelligence</p>
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
            <div class="glass-card" style="padding: 28px;">
                <div class="kpi-label">Total SAP Jobs</div>
                <div class="kpi-value" style="margin-top: 16px;">{summary.get('total_jobs', 0)}</div>
                <div class="trend-up" style="margin-top: 12px;">+12%</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
            <div class="priority-card" style="padding: 28px;">
                <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 16px;">
                    <div class="kpi-label">High Priority Signals</div>
                    <div class="pulse-dot"></div>
                </div>
                <div class="kpi-value">{summary.get('high_priority_companies', 0)}</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
            <div class="glass-card" style="padding: 28px;">
                <div class="kpi-label">Countries Tracked</div>
                <div class="kpi-value" style="margin-top: 16px;">10</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
            <div class="glass-card" style="padding: 28px;">
                <div class="kpi-label">Data Sources</div>
                <div class="kpi-value" style="margin-top: 16px;">3</div>
            </div>
        """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
