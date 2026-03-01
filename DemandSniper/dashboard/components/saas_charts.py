import streamlit as st
import plotly.graph_objects as go
import pandas as pd


def render_enhanced_bar_chart(companies, on_click_callback=None):
    """
    Render an enhanced horizontal bar chart with tooltips and clickable bars.
    
    Args:
        companies: List of company dicts with demand scores
        on_click_callback: Function to call when bar is clicked
    """
    if not companies:
        st.info("No data available")
        return
    
    df = pd.DataFrame(companies[:10])
    
    # Color based on priority
    colors = []
    hover_texts = []
    
    for _, row in df.iterrows():
        priority = row['highest_priority']
        if priority == 'High':
            colors.append('#FF4B4B')
        elif priority == 'Medium':
            colors.append('#FFA500')
        else:
            colors.append('#00C9A7')
        
        # Enhanced tooltip
        tooltip = f"""
        <b>{row['company_name']}</b><br>
        Demand Score: {row['total_demand_score']:.1f}<br>
        Openings: {row['total_openings']}<br>
        Jobs Posted: {row['total_jobs']}<br>
        Priority: {priority}<br>
        <br>
        <i>💡 Click to view company details</i>
        """
        hover_texts.append(tooltip)
    
    fig = go.Figure(go.Bar(
        x=df['total_demand_score'],
        y=df['company_name'],
        orientation='h',
        marker=dict(
            color=colors,
            line=dict(color='rgba(255,255,255,0.3)', width=1.5),
            cornerradius=8
        ),
        text=df['total_openings'].apply(lambda x: f'{x} openings'),
        textposition='inside',
        insidetextanchor='middle',
        textfont=dict(color='white', size=11, family='Inter'),
        hovertemplate='%{customdata}<extra></extra>',
        customdata=hover_texts,
        hoverlabel=dict(
            bgcolor='rgba(30, 35, 41, 0.95)',
            bordercolor='rgba(255, 75, 75, 0.5)',
            font=dict(color='white', size=12)
        )
    ))
    
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white', family='Inter'),
        xaxis=dict(
            title=dict(text='Demand Score', font=dict(size=13, color='#8B949E')),
            gridcolor='rgba(255,255,255,0.08)',
            showgrid=True,
            zeroline=False
        ),
        yaxis=dict(
            title='',
            gridcolor='rgba(255,255,255,0.08)',
            autorange='reversed',
            tickfont=dict(size=12)
        ),
        margin=dict(l=10, r=10, t=20, b=40),
        height=450,
        hovermode='closest',
        clickmode='event+select'
    )
    
    # Add click event handling
    if on_click_callback:
        fig.update_traces(
            selectedpoints=[],
            selector=dict(type='bar')
        )
    
    return fig


def render_priority_donut_chart(companies):
    """
    Render a donut chart with insight summary.
    
    Returns:
        tuple: (figure, insight_text)
    """
    if not companies:
        return None, ""
    
    high = sum(1 for c in companies if c['highest_priority'] == 'High')
    medium = sum(1 for c in companies if c['highest_priority'] == 'Medium')
    low = sum(1 for c in companies if c['highest_priority'] == 'Low')
    total = len(companies)
    
    colors = ['#FF4B4B', '#FFA500', '#00C9A7']
    labels = ['High Priority', 'Medium Priority', 'Low Priority']
    values = [high, medium, low]
    
    # Calculate percentages
    high_pct = (high / total * 100) if total > 0 else 0
    medium_pct = (medium / total * 100) if total > 0 else 0
    
    # Generate insight text
    if high_pct >= 30:
        insight = f"🔥 <b>{high_pct:.0f}%</b> of tracked companies show urgent recurring demand. <span style='color:#FF4B4B'>Immediate action recommended.</span>"
    elif high_pct >= 15:
        insight = f"⚡ <b>{high_pct:.0f}%</b> high-priority signals detected. Strong opportunity pipeline."
    elif medium_pct >= 50:
        insight = f"📊 Majority showing medium signals ({medium_pct:.0f}%). Monitor for escalation."
    else:
        insight = f"📈 Market baseline with {low} low-priority companies. Early stage detection."
    
    fig = go.Figure(go.Pie(
        labels=labels,
        values=values,
        hole=0.65,
        marker=dict(
            colors=colors,
            line=dict(color='rgba(0,0,0,0)', width=0)
        ),
        textinfo='label+percent',
        textfont=dict(color='white', size=11, family='Inter'),
        textposition='outside',
        automargin=True,
        hovertemplate='<b>%{label}</b><br>Companies: %{value}<br>Share: %{percent}<extra></extra>',
        hoverlabel=dict(
            bgcolor='rgba(30, 35, 41, 0.95)',
            bordercolor='rgba(255, 255, 255, 0.2)',
            font=dict(color='white', size=12)
        )
    ))
    
    # Add center text
    fig.add_annotation(
        text=f'<b>{total}</b><br>Total',
        x=0.5, y=0.5,
        font=dict(size=20, color='white', family='Inter'),
        showarrow=False
    )
    
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white', family='Inter'),
        showlegend=False,
        margin=dict(l=20, r=20, t=30, b=30),
        height=400
    )
    
    return fig, insight


def render_trend_line_chart(trends):
    """Render an enhanced trend line chart with moving average."""
    if not trends:
        return None
    
    df = pd.DataFrame(trends)
    df['date'] = pd.to_datetime(df['date'])
    
    fig = go.Figure()
    
    # Area fill
    fig.add_trace(go.Scatter(
        x=df['date'],
        y=df['count'],
        mode='lines',
        line=dict(color='#00C9A7', width=0),
        fill='tozeroy',
        fillcolor='rgba(0, 201, 167, 0.15)',
        showlegend=False,
        hoverinfo='skip'
    ))
    
    # Main line
    fig.add_trace(go.Scatter(
        x=df['date'],
        y=df['count'],
        mode='lines+markers',
        name='Daily Postings',
        line=dict(color='#00C9A7', width=3),
        marker=dict(
            size=8,
            color='#00C9A7',
            line=dict(color='white', width=2),
            symbol='circle'
        ),
        hovertemplate='%{x|%b %d, %Y}<br>New Postings: %{y}<extra></extra>',
        hoverlabel=dict(bgcolor='rgba(0, 201, 167, 0.9)')
    ))
    
    # Add 7-day moving average
    if len(df) >= 7:
        df['ma7'] = df['count'].rolling(window=7, min_periods=1).mean()
        fig.add_trace(go.Scatter(
            x=df['date'],
            y=df['ma7'],
            mode='lines',
            name='7-Day Trend',
            line=dict(color='#FFA500', width=2, dash='dot'),
            hovertemplate='%{x|%b %d, %Y}<br>7-Day Avg: %{y:.1f}<extra></extra>',
            hoverlabel=dict(bgcolor='rgba(255, 165, 0, 0.9)')
        ))
    
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white', family='Inter'),
        xaxis=dict(
            title=dict(text='Date', font=dict(size=13, color='#8B949E')),
            gridcolor='rgba(255,255,255,0.08)',
            showgrid=True,
            zeroline=False,
            tickformat='%b %d'
        ),
        yaxis=dict(
            title=dict(text='New Postings', font=dict(size=13, color='#8B949E')),
            gridcolor='rgba(255,255,255,0.08)',
            showgrid=True,
            zeroline=False
        ),
        legend=dict(
            orientation='h',
            yanchor='bottom',
            y=1.02,
            xanchor='right',
            x=1,
            font=dict(color='#8B949E', size=11),
            bgcolor='rgba(0,0,0,0)'
        ),
        margin=dict(l=10, r=10, t=60, b=40),
        height=400,
        hovermode='x unified'
    )
    
    return fig
