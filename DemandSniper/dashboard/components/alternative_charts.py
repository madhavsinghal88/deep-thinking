import streamlit as st
import pandas as pd


def render_table_chart(companies):
    """Render companies as a styled table instead of a chart."""
    if not companies:
        return None
    
    df = pd.DataFrame(companies[:10])
    
    # Select and rename columns
    display_df = df[['company_name', 'total_demand_score', 'total_openings', 'highest_priority']].copy()
    display_df.columns = ['Company', 'Demand Score', 'Openings', 'Priority']
    
    # Style function
    def color_priority(val):
        if val == 'High':
            return 'background-color: #FF4B4B; color: white; font-weight: bold;'
        elif val == 'Medium':
            return 'background-color: #FFA500; color: white; font-weight: bold;'
        else:
            return 'background-color: #00C9A7; color: white; font-weight: bold;'
    
    styled = display_df.style.applymap(color_priority, subset=['Priority'])
    styled = styled.format({'Demand Score': '{:.1f}', 'Openings': '{:.0f}'})
    
    return styled


def render_priority_summary(companies):
    """Render priority distribution as text summary."""
    if not companies:
        return None, ""
    
    high = sum(1 for c in companies if c.get('highest_priority') == 'High')
    medium = sum(1 for c in companies if c.get('highest_priority') == 'Medium')
    low = sum(1 for c in companies if c.get('highest_priority') == 'Low')
    total = len(companies)
    
    # Create simple progress bars
    html = f"""
    <div style="margin: 20px 0;">
        <div style="margin-bottom: 15px;">
            <div style="display: flex; justify-content: space-between; margin-bottom: 5px;">
                <span style="color: #FF4B4B; font-weight: 600;">🔥 High Priority</span>
                <span style="color: white;">{high} ({high/total*100:.0f}%)</span>
            </div>
            <div style="background: rgba(255,255,255,0.1); border-radius: 10px; height: 20px;">
                <div style="background: #FF4B4B; width: {high/total*100}%; height: 100%; border-radius: 10px;"></div>
            </div>
        </div>
        
        <div style="margin-bottom: 15px;">
            <div style="display: flex; justify-content: space-between; margin-bottom: 5px;">
                <span style="color: #FFA500; font-weight: 600;">⚡ Medium Priority</span>
                <span style="color: white;">{medium} ({medium/total*100:.0f}%)</span>
            </div>
            <div style="background: rgba(255,255,255,0.1); border-radius: 10px; height: 20px;">
                <div style="background: #FFA500; width: {medium/total*100}%; height: 100%; border-radius: 10px;"></div>
            </div>
        </div>
        
        <div style="margin-bottom: 15px;">
            <div style="display: flex; justify-content: space-between; margin-bottom: 5px;">
                <span style="color: #00C9A7; font-weight: 600;">✅ Low Priority</span>
                <span style="color: white;">{low} ({low/total*100:.0f}%)</span>
            </div>
            <div style="background: rgba(255,255,255,0.1); border-radius: 10px; height: 20px;">
                <div style="background: #00C9A7; width: {low/total*100}%; height: 100%; border-radius: 10px;"></div>
            </div>
        </div>
    </div>
    """
    
    insight = f"📊 Total Companies: {total} | 🔥 High: {high} | ⚡ Medium: {medium} | ✅ Low: {low}"
    
    return html, insight
