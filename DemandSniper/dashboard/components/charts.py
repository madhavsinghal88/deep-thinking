import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
from typing import List, Dict, Any


def render_top_companies_chart(companies: List[Dict[str, Any]], top_n: int = 10):
    """Render bar chart of top companies by demand score."""
    if not companies:
        st.info("No company data available")
        return
    
    # Take top N companies
    top_companies = companies[:top_n]
    
    # Create color mapping for priorities
    color_map = {
        "High": "#ff4b4b",
        "Medium": "#ffa500",
        "Low": "#00cc00"
    }
    
    df = pd.DataFrame(top_companies)
    
    fig = px.bar(
        df,
        x="company_name",
        y="total_demand_score",
        color="highest_priority",
        color_discrete_map=color_map,
        title=f"🏆 Top {top_n} Companies by Demand Score",
        labels={
            "company_name": "Company",
            "total_demand_score": "Demand Score",
            "highest_priority": "Priority"
        }
    )
    
    fig.update_layout(
        xaxis_tickangle=-45,
        showlegend=True,
        legend_title_text="Priority",
        height=500
    )
    
    st.plotly_chart(fig, use_container_width=True)


def render_hiring_trends_chart(trends: List[Dict[str, Any]]):
    """Render line chart of hiring trends over time."""
    if not trends:
        st.info("No trend data available")
        return
    
    df = pd.DataFrame(trends)
    df['date'] = pd.to_datetime(df['date'])
    
    fig = px.line(
        df,
        x="date",
        y="count",
        title="📈 Hiring Frequency Over Time",
        labels={
            "date": "Date",
            "count": "New Postings"
        }
    )
    
    fig.update_layout(
        height=400,
        xaxis_title="Date",
        yaxis_title="Number of Postings"
    )
    
    # Add rolling average
    df['rolling_avg'] = df['count'].rolling(window=7, min_periods=1).mean()
    fig.add_trace(
        go.Scatter(
            x=df['date'],
            y=df['rolling_avg'],
            mode='lines',
            name='7-day Average',
            line=dict(color='red', dash='dash')
        )
    )
    
    st.plotly_chart(fig, use_container_width=True)


def render_priority_distribution(companies: List[Dict[str, Any]]):
    """Render pie chart of priority distribution."""
    if not companies:
        st.info("No data available")
        return
    
    # Count by priority
    priority_counts = {"High": 0, "Medium": 0, "Low": 0}
    for company in companies:
        priority = company.get("highest_priority", "Low")
        if priority in priority_counts:
            priority_counts[priority] += 1
    
    colors = ["#ff4b4b", "#ffa500", "#00cc00"]
    
    fig = go.Figure(data=[go.Pie(
        labels=list(priority_counts.keys()),
        values=list(priority_counts.values()),
        hole=0.4,
        marker_colors=colors
    )])
    
    fig.update_layout(
        title="🎯 Priority Distribution",
        showlegend=True,
        height=400
    )
    
    st.plotly_chart(fig, use_container_width=True)


def render_platform_distribution(platforms: Dict[str, int]):
    """Render bar chart of job distribution by platform."""
    if not platforms:
        st.info("No platform data available")
        return
    
    df = pd.DataFrame([
        {"Platform": k.title(), "Jobs": v}
        for k, v in platforms.items()
    ])
    
    fig = px.bar(
        df,
        x="Platform",
        y="Jobs",
        title="📊 Jobs by Platform",
        color="Platform"
    )
    
    fig.update_layout(
        height=400,
        showlegend=False
    )
    
    st.plotly_chart(fig, use_container_width=True)


def render_company_timeline(events: List[Dict[str, Any]]):
    """Render company event timeline."""
    if not events:
        st.info("No timeline events available")
        return
    
    df = pd.DataFrame(events)
    df['event_date'] = pd.to_datetime(df['event_date'])
    
    # Color mapping for event types
    color_map = {
        "job_posted": "#3498db",
        "repost_detected": "#e74c3c",
        "demand_spike": "#f39c12"
    }
    
    fig = px.scatter(
        df,
        x="event_date",
        y="event_type",
        color="event_type",
        color_discrete_map=color_map,
        title="📅 Company Timeline",
        labels={
            "event_date": "Date",
            "event_type": "Event Type"
        },
        hover_data=["details"]
    )
    
    fig.update_layout(
        height=400,
        showlegend=True
    )
    
    st.plotly_chart(fig, use_container_width=True)


def render_demand_score_gauge(score: float, max_score: float = 100):
    """Render a gauge chart for demand score."""
    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=score,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': "Demand Score"},
        gauge={
            'axis': {'range': [None, max_score]},
            'bar': {'color': "darkblue"},
            'steps': [
                {'range': [0, 10], 'color': "lightgray"},
                {'range': [10, 25], 'color': "yellow"},
                {'range': [25, max_score], 'color': "red"}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': 25
            }
        }
    ))
    
    fig.update_layout(height=300)
    st.plotly_chart(fig, use_container_width=True)
