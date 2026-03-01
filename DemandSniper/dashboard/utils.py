import streamlit as st
from typing import List, Dict, Any


def get_priority_color(priority: str) -> str:
    """Get color for priority level."""
    colors = {
        "High": "#ff4b4b",
        "Medium": "#ffa500", 
        "Low": "#00cc00"
    }
    return colors.get(priority, "#808080")


def get_platform_icon(platform: str) -> str:
    """Get icon for platform."""
    icons = {
        "indeed": "🔍",
        "dice": "🎲",
        "linkedin": "💼"
    }
    return icons.get(platform.lower(), "📄")


def format_date(date_value) -> str:
    """Format date value for display."""
    if not date_value:
        return "N/A"
    
    from datetime import datetime, date
    
    if isinstance(date_value, (datetime, date)):
        return date_value.strftime("%Y-%m-%d")
    elif isinstance(date_value, str):
        try:
            dt = datetime.fromisoformat(date_value.replace('Z', '+00:00'))
            return dt.strftime("%Y-%m-%d")
        except:
            return date_value
    
    return str(date_value)


def truncate_text(text: str, max_length: int = 100) -> str:
    """Truncate text to maximum length."""
    if not text:
        return ""
    
    if len(text) <= max_length:
        return text
    
    return text[:max_length - 3] + "..."


def render_metric_card(title: str, value: Any, subtitle: str = None, delta: str = None):
    """Render a metric card with optional delta."""
    st.metric(
        label=title,
        value=value,
        delta=delta,
        help=subtitle
    )


def render_alert(message: str, alert_type: str = "info"):
    """Render an alert message."""
    if alert_type == "success":
        st.success(message)
    elif alert_type == "warning":
        st.warning(message)
    elif alert_type == "error":
        st.error(message)
    else:
        st.info(message)


def paginate_data(data: List[Any], page: int, page_size: int = 20) -> List[Any]:
    """Paginate a list of data."""
    start_idx = (page - 1) * page_size
    end_idx = start_idx + page_size
    return data[start_idx:end_idx]


def render_pagination_controls(total_items: int, page_size: int = 20, key: str = "pagination"):
    """Render pagination controls and return selected page."""
    total_pages = (total_items + page_size - 1) // page_size
    
    if total_pages <= 1:
        return 1
    
    col1, col2, col3 = st.columns([1, 3, 1])
    
    with col2:
        page = st.number_input(
            "Page",
            min_value=1,
            max_value=total_pages,
            value=1,
            key=key
        )
    
    st.caption(f"Showing {page_size} items per page. Total: {total_items} items, {total_pages} pages.")
    
    return page
