import streamlit as st
import pandas as pd
from utils.service_matcher import detector, get_service_pitch


def render_kpi_card(title, value, subtext, tag=None, tag_color="#FF4B4B", priority="normal", help_text=None):
    """
    Render a premium KPI card with glassmorphism effect.
    
    Args:
        title: Card title
        value: Primary metric (number)
        subtext: Micro description
        tag: Optional badge text (e.g., "🔥 Hot")
        tag_color: Color for the tag
        priority: "high" for visual emphasis
        help_text: Tooltip text
    """
    # Glassmorphism card styling
    priority_style = """
        border: 2px solid rgba(255, 75, 75, 0.5);
        box-shadow: 0 8px 32px rgba(255, 75, 75, 0.2), 0 0 20px rgba(255, 75, 75, 0.1);
    """ if priority == "high" else """
        border: 1px solid rgba(255, 255, 255, 0.1);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
    """
    
    tag_html = f"""
        <div style="
            display: inline-block;
            background: {tag_color};
            color: white;
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 0.8rem;
            font-weight: 600;
            margin-top: 10px;
        ">{tag}</div>
    """ if tag else ""
    
    help_icon = f"""
        <span title="{help_text}" style="
            cursor: help;
            color: #8B949E;
            font-size: 0.9rem;
            margin-left: 5px;
        ">ⓘ</span>
    """ if help_text else ""
    
    card_html = f"""
        <div class="saas-kpi-card" style="
            background: linear-gradient(135deg, rgba(30, 35, 41, 0.9) 0%, rgba(37, 43, 51, 0.9) 100%);
            backdrop-filter: blur(10px);
            border-radius: 16px;
            padding: 24px;
            margin: 10px 0;
            transition: all 0.3s ease;
            {priority_style}
        ">
            <div style="display: flex; justify-content: space-between; align-items: flex-start;">
                <div>
                    <div style="color: #8B949E; font-size: 0.85rem; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 8px;">
                        {title}{help_icon}
                    </div>
                    <div style="color: #FFFFFF; font-size: 2.8rem; font-weight: 700; line-height: 1;">
                        {value}
                    </div>
                </div>
            </div>
            <div style="color: #8B949E; font-size: 0.9rem; margin-top: 12px; line-height: 1.4;">
                {subtext}
            </div>
            {tag_html}
        </div>
    """
    
    st.markdown(card_html, unsafe_allow_html=True)


def render_opportunity_card(company_data):
    """Render an opportunity card with pitch suggestions."""
    company_name = company_data.get('company_name', 'Unknown')
    demand_score = company_data.get('total_demand_score', 0)
    times_posted = company_data.get('total_jobs', 1)
    days_open = company_data.get('days_open', 0)
    country = company_data.get('country', 'Unknown')
    priority = company_data.get('highest_priority', 'Low')
    
    # Calculate confidence and pitch type
    confidence = calculate_confidence(demand_score, times_posted, days_open)
    pitch_type = determine_pitch_type(demand_score, times_posted, days_open)
    
    # Color based on priority
    priority_colors = {
        "High": ("#FF4B4B", "rgba(255, 75, 75, 0.2)"),
        "Medium": ("#FFA500", "rgba(255, 165, 0, 0.2)"),
        "Low": ("#00C9A7", "rgba(0, 201, 167, 0.2)")
    }
    color, bg_color = priority_colors.get(priority, ("#8B949E", "rgba(139, 148, 158, 0.2)"))
    
    card_html = f"""
        <div class="opportunity-card" style="
            background: linear-gradient(135deg, rgba(30, 35, 41, 0.95) 0%, rgba(37, 43, 51, 0.95) 100%);
            backdrop-filter: blur(10px);
            border-left: 4px solid {color};
            border-radius: 12px;
            padding: 20px;
            margin: 12px 0;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
            transition: all 0.3s ease;
        ">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px;">
                <div style="font-size: 1.2rem; font-weight: 600; color: #FFFFFF;">
                    {company_name}
                </div>
                <div style="background: {color}; color: white; padding: 4px 12px; border-radius: 20px; font-size: 0.8rem; font-weight: 600;">
                    {priority}
                </div>
            </div>
            
            <div style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 16px; margin: 16px 0;">
                <div>
                    <div style="color: #8B949E; font-size: 0.75rem; text-transform: uppercase;">Demand Score</div>
                    <div style="color: #FFFFFF; font-size: 1.4rem; font-weight: 700;">{demand_score:.1f}</div>
                </div>
                <div>
                    <div style="color: #8B949E; font-size: 0.75rem; text-transform: uppercase;">Times Posted</div>
                    <div style="color: #FFFFFF; font-size: 1.4rem; font-weight: 700;">{times_posted}</div>
                </div>
                <div>
                    <div style="color: #8B949E; font-size: 0.75rem; text-transform: uppercase;">Confidence</div>
                    <div style="color: {color}; font-size: 1.4rem; font-weight: 700;">{confidence}%</div>
                </div>
            </div>
            
            <div style="background: {bg_color}; border-radius: 8px; padding: 12px; margin-top: 12px;">
                <div style="color: {color}; font-size: 0.8rem; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 4px;">
                    💡 Recommended Pitch
                </div>
                <div style="color: #FFFFFF; font-size: 1rem; font-weight: 500;">
                    {pitch_type}
                </div>
            </div>
            
            <div style="color: #8B949E; font-size: 0.8rem; margin-top: 10px;">
                📍 {country}
            </div>
        </div>
    """
    
    st.markdown(card_html, unsafe_allow_html=True)


def calculate_confidence(demand_score, times_posted, days_open):
    """Calculate opportunity confidence percentage."""
    base_confidence = 50
    
    # Higher demand score = higher confidence
    if demand_score > 50:
        base_confidence += 25
    elif demand_score > 30:
        base_confidence += 15
    elif demand_score > 15:
        base_confidence += 10
    
    # More reposts = higher confidence
    if times_posted >= 5:
        base_confidence += 15
    elif times_posted >= 3:
        base_confidence += 10
    elif times_posted >= 2:
        base_confidence += 5
    
    # Longer posting duration = higher confidence
    if days_open > 30:
        base_confidence += 10
    elif days_open > 14:
        base_confidence += 5
    
    return min(base_confidence, 98)


def determine_pitch_type(demand_score, times_posted, days_open):
    """Determine the recommended pitch type based on hiring signals."""
    if demand_score > 40 and times_posted >= 4:
        return "🎯 Urgent Implementation Project - High recurring demand suggests active project"
    elif demand_score > 25 and times_posted >= 3 and days_open > 30:
        return "🔧 Managed Service Opportunity - Sustained hiring indicates ongoing needs"
    elif demand_score > 20 and times_posted >= 2:
        return "⚡ Capacity Gap Solution - Company likely needs immediate support"
    elif demand_score > 15:
        return "📈 Growth Partnership - Growing team needs scalable solutions"
    else:
        return "🤝 Advisory Opportunity - Build relationship for future projects"


def render_header_logo():
    """Render the DemandSniper logo."""
    logo_svg = """
    <svg width="40" height="40" viewBox="0 0 40 40" fill="none" xmlns="http://www.w3.org/2000/svg">
        <circle cx="20" cy="20" r="18" stroke="url(#gradient1)" stroke-width="2"/>
        <circle cx="20" cy="20" r="8" fill="url(#gradient2)"/>
        <path d="M20 2 L20 8" stroke="url(#gradient1)" stroke-width="2" stroke-linecap="round"/>
        <path d="M20 32 L20 38" stroke="url(#gradient1)" stroke-width="2" stroke-linecap="round"/>
        <path d="M2 20 L8 20" stroke="url(#gradient1)" stroke-width="2" stroke-linecap="round"/>
        <path d="M32 20 L38 20" stroke="url(#gradient1)" stroke-width="2" stroke-linecap="round"/>
        <circle cx="20" cy="20" r="3" fill="#FFFFFF"/>
        <defs>
            <linearGradient id="gradient1" x1="0%" y1="0%" x2="100%" y2="100%">
                <stop offset="0%" style="stop-color:#FF4B4B"/>
                <stop offset="100%" style="stop-color:#FF6B6B"/>
            </linearGradient>
            <linearGradient id="gradient2" x1="0%" y1="0%" x2="100%" y2="100%">
                <stop offset="0%" style="stop-color:#FF4B4B"/>
                <stop offset="100%" style="stop-color:#FF8B8B"/>
            </linearGradient>
        </defs>
    </svg>
    """
    
    return logo_svg


def render_service_opportunity_card(company_data, job_title=""):
    """
    Render a service-specific opportunity card with SAP EPM/Analytics focus.
    
    Args:
        company_data: Company dict with hiring signals
        job_title: Job title to analyze for service matching
    """
    company_name = company_data.get('company_name', 'Unknown')
    demand_score = company_data.get('total_demand_score', 0)
    times_posted = company_data.get('total_jobs', 1)
    country = company_data.get('country', 'Unknown')
    priority = company_data.get('highest_priority', 'Low')
    
    # Detect service opportunities
    services = detector.detect_services(job_title) if job_title else []
    primary_service = services[0] if services else {
        "service": "SAP EPM/Analytics Services",
        "confidence": 70,
        "keywords": ["SAP"],
        "pain_points": ["Complex financial processes"],
        "outcomes": ["Streamlined operations"]
    }
    
    # Calculate overall confidence
    base_confidence = calculate_confidence(demand_score, times_posted, 0)
    service_confidence = primary_service.get('confidence', 50)
    overall_confidence = min((base_confidence + service_confidence) / 2, 98)
    
    # Service colors
    service_colors = {
        "Financial Planning & Analysis": ("#FF6B6B", "rgba(255, 107, 107, 0.2)"),
        "Financial Close & Consolidation": ("#4ECDC4", "rgba(78, 205, 196, 0.2)"),
        "SAP Analytics Cloud (SAC)": ("#45B7D1", "rgba(69, 183, 209, 0.2)"),
        "SAP Datasphere & Data Management": ("#96CEB4", "rgba(150, 206, 180, 0.2)"),
        "Predictive Analytics & AI": ("#FFEAA7", "rgba(255, 234, 167, 0.2)"),
        "SAP Implementation & Migration": ("#DDA0DD", "rgba(221, 160, 221, 0.2)"),
        "SAP Support & Enhancement": ("#98D8C8", "rgba(152, 216, 200, 0.2)"),
        "SAP EPM/Analytics Services": ("#FF4B4B", "rgba(255, 75, 75, 0.2)")
    }
    
    color, bg_color = service_colors.get(
        primary_service['service'], 
        ("#FF4B4B", "rgba(255, 75, 75, 0.2)")
    )
    
    # Generate pitch
    pitch = get_service_pitch(company_name, job_title)
    
    card_html = f"""
        <div class="opportunity-card" style="
            background: linear-gradient(135deg, rgba(30, 35, 41, 0.95) 0%, rgba(37, 43, 51, 0.95) 100%);
            border-left: 4px solid {color};
            border-radius: 12px;
            padding: 24px;
            margin: 16px 0;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
            transition: all 0.3s ease;
        ">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px;">
                <div>
                    <div style="font-size: 1.3rem; font-weight: 700; color: #FFFFFF;">
                        {company_name}
                    </div>
                    <div style="color: #8B949E; font-size: 0.85rem; margin-top: 4px;">
                        📍 {country} | 🎯 {priority} Priority
                    </div>
                </div>
                <div style="text-align: right;">
                    <div style="font-size: 2rem; font-weight: 800; color: {color};">
                        {overall_confidence:.0f}%
                    </div>
                    <div style="color: #8B949E; font-size: 0.75rem;">Match Confidence</div>
                </div>
            </div>
            
            <div style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 16px; margin: 20px 0;">
                <div style="background: rgba(255,255,255,0.05); border-radius: 8px; padding: 12px;">
                    <div style="color: #8B949E; font-size: 0.7rem; text-transform: uppercase; letter-spacing: 0.5px;">Demand Score</div>
                    <div style="color: #FFFFFF; font-size: 1.3rem; font-weight: 700; margin-top: 4px;">{demand_score:.1f}</div>
                </div>
                <div style="background: rgba(255,255,255,0.05); border-radius: 8px; padding: 12px;">
                    <div style="color: #8B949E; font-size: 0.7rem; text-transform: uppercase; letter-spacing: 0.5px;">Job Postings</div>
                    <div style="color: #FFFFFF; font-size: 1.3rem; font-weight: 700; margin-top: 4px;">{times_posted}</div>
                </div>
                <div style="background: rgba(255,255,255,0.05); border-radius: 8px; padding: 12px;">
                    <div style="color: #8B949E; font-size: 0.7rem; text-transform: uppercase; letter-spacing: 0.5px;">Service Match</div>
                    <div style="color: {color}; font-size: 1.3rem; font-weight: 700; margin-top: 4px;">{service_confidence:.0f}%</div>
                </div>
            </div>
            
            <div style="background: {bg_color}; border-radius: 10px; padding: 16px; margin-top: 16px; border: 1px solid {color}40;">
                <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 8px;">
                    <span style="font-size: 1.2rem;">🎯</span>
                    <span style="color: {color}; font-size: 0.85rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px;">
                        {primary_service['service']}
                    </span>
                </div>
                <div style="color: #FFFFFF; font-size: 0.95rem; line-height: 1.5; margin-top: 8px;">
                    <strong>Key Indicators:</strong> {', '.join(primary_service['keywords'][:3])}
                </div>
                <div style="color: #8B949E; font-size: 0.85rem; line-height: 1.4; margin-top: 8px;">
                    💡 {primary_service['pain_points'][0] if primary_service['pain_points'] else 'Operational inefficiencies detected'}
                </div>
            </div>
            
            <div style="margin-top: 16px; padding: 16px; background: rgba(0,0,0,0.2); border-radius: 8px;">
                <div style="color: #8B949E; font-size: 0.75rem; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 8px;">
                    💼 Recommended Approach
                </div>
                <div style="color: #FFFFFF; font-size: 0.9rem; line-height: 1.5;">
                    {pitch.replace(chr(10), '<br>')}
                </div>
            </div>
        </div>
    """
    
    st.markdown(card_html, unsafe_allow_html=True)
