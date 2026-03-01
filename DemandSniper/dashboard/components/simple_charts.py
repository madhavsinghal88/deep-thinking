import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd


def render_simple_bar_chart(companies):
    """Simple working bar chart."""
    if not companies:
        return None
    
    try:
        df = pd.DataFrame(companies[:10])
        
        # Create color column
        df['color'] = df['highest_priority'].map({
            'High': '#FF4B4B',
            'Medium': '#FFA500',
            'Low': '#00C9A7'
        })
        
        fig = px.bar(
            df,
            x='total_demand_score',
            y='company_name',
            orientation='h',
            color='highest_priority',
            color_discrete_map={'High': '#FF4B4B', 'Medium': '#FFA500', 'Low': '#00C9A7'},
            text='total_openings',
            labels={'total_demand_score': 'Demand Score', 'company_name': ''}
        )
        
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='white',
            showlegend=False,
            height=400,
            margin=dict(l=10, r=10, t=10, b=10)
        )
        
        return fig
    except Exception as e:
        st.error(f"Chart error: {e}")
        return None


def render_simple_donut_chart(companies):
    """Simple working donut chart."""
    if not companies:
        return None, ""
    
    try:
        high = sum(1 for c in companies if c.get('highest_priority') == 'High')
        medium = sum(1 for c in companies if c.get('highest_priority') == 'Medium')
        low = sum(1 for c in companies if c.get('highest_priority') == 'Low')
        
        total = len(companies)
        high_pct = (high / total * 100) if total > 0 else 0
        
        if high_pct >= 30:
            insight = f"🔥 {high_pct:.0f}% show urgent recurring demand"
        elif high_pct >= 15:
            insight = f"⚡ {high_pct:.0f}% high-priority signals detected"
        else:
            insight = f"📈 {high_pct:.0f}% baseline detection"
        
        fig = go.Figure(data=[go.Pie(
            labels=['High', 'Medium', 'Low'],
            values=[high, medium, low],
            hole=0.6,
            marker_colors=['#FF4B4B', '#FFA500', '#00C9A7'],
            textinfo='label+percent',
            textfont_color='white'
        )])
        
        fig.add_annotation(
            text=f'{total}',
            x=0.5, y=0.5,
            font=dict(size=24, color='white'),
            showarrow=False
        )
        
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            showlegend=False,
            height=350,
            margin=dict(l=10, r=10, t=10, b=10)
        )
        
        return fig, insight
    except Exception as e:
        st.error(f"Chart error: {e}")
        return None, ""
