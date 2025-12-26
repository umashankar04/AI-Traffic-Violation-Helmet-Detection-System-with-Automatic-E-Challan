"""
Streamlit Dashboard - Main Application
Real-time Traffic Violation Monitoring & Analytics
"""

import streamlit as st
import pandas as pd
import numpy as np
import folium
from streamlit_folium import st_folium
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import requests
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Page configuration
st.set_page_config(
    page_title="Traffic Violation Detection Dashboard",
    page_icon="🚨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .metric-card {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        text-align: center;
    }
    .violation-critical {
        background-color: #ffcccc;
        padding: 10px;
        border-radius: 5px;
        border-left: 4px solid #ff0000;
    }
    .violation-high {
        background-color: #ffe6cc;
        padding: 10px;
        border-radius: 5px;
        border-left: 4px solid #ff9900;
    }
    .violation-medium {
        background-color: #ffffcc;
        padding: 10px;
        border-radius: 5px;
        border-left: 4px solid #ffff00;
    }
    </style>
""", unsafe_allow_html=True)


def get_api_base_url():
    """Get API base URL from config."""
    return st.secrets.get("API_BASE_URL", "http://localhost:8000")


def fetch_analytics_summary(days: int = 7):
    """Fetch analytics summary from API."""
    try:
        response = requests.get(
            f"{get_api_base_url()}/api/analytics/summary",
            params={"days": days},
            timeout=5
        )
        if response.status_code == 200:
            return response.json()
    except Exception as e:
        logger.error(f"Error fetching analytics: {str(e)}")
    return None


def fetch_heatmap_data(days: int = 7):
    """Fetch heatmap data from API."""
    try:
        response = requests.get(
            f"{get_api_base_url()}/api/analytics/heatmap/data",
            params={"days": days},
            timeout=5
        )
        if response.status_code == 200:
            return response.json()
    except Exception as e:
        logger.error(f"Error fetching heatmap data: {str(e)}")
    return None


def fetch_high_risk_zones(days: int = 30):
    """Fetch high-risk zones from API."""
    try:
        response = requests.get(
            f"{get_api_base_url()}/api/analytics/high-risk-zones",
            params={"days": days, "limit": 10},
            timeout=5
        )
        if response.status_code == 200:
            return response.json()
    except Exception as e:
        logger.error(f"Error fetching high-risk zones: {str(e)}")
    return None


def create_violation_heatmap(heatmap_data):
    """Create Folium heatmap from violation data."""
    # Center map on India (Delhi)
    m = folium.Map(
        location=[28.7041, 77.1025],
        zoom_start=12,
        tiles="OpenStreetMap"
    )
    
    # TODO: Add heatmap markers from data
    # For now, show sample marker
    folium.Marker(
        location=[28.7041, 77.1025],
        popup="Sample Violation Location",
        icon=folium.Icon(color='red', icon='exclamation')
    ).add_to(m)
    
    return m


def create_violation_trends_chart(days: int = 30):
    """Create violation trends chart."""
    # Generate sample data
    dates = pd.date_range(end=datetime.now(), periods=days, freq='D')
    violations = np.random.randint(10, 50, days)
    
    df = pd.DataFrame({
        'Date': dates,
        'Violations': violations
    })
    
    fig = px.line(
        df,
        x='Date',
        y='Violations',
        title='Daily Violations Trend',
        markers=True,
        line_shape='linear'
    )
    fig.update_layout(
        hovermode='x unified',
        plot_bgcolor='white',
        xaxis_title='Date',
        yaxis_title='Number of Violations'
    )
    return fig


def create_violation_type_chart():
    """Create violation type distribution chart."""
    violations_by_type = {
        'Helmet Not Worn': 45,
        'Triple Riding': 25,
        'Signal Violation': 20,
        'Speed Violation': 10
    }
    
    fig = px.pie(
        values=list(violations_by_type.values()),
        names=list(violations_by_type.keys()),
        title='Violations by Type',
        hole=0.3
    )
    return fig


def create_hourly_distribution_chart():
    """Create hourly violation distribution."""
    hours = list(range(24))
    violations_per_hour = np.random.randint(5, 30, 24)
    
    fig = go.Figure(data=[
        go.Bar(
            x=hours,
            y=violations_per_hour,
            marker_color='rgba(255, 100, 100, 0.7)'
        )
    ])
    
    fig.update_layout(
        title='Violations by Hour of Day',
        xaxis_title='Hour',
        yaxis_title='Number of Violations',
        plot_bgcolor='white',
        hovermode='x unified'
    )
    return fig


# Main dashboard layout
st.title("🚨 Traffic Violation Detection Dashboard")
st.markdown("---")

# Sidebar configuration
with st.sidebar:
    st.header("Configuration")
    
    # Date range filter
    days_filter = st.slider(
        "Select time period (days)",
        min_value=1,
        max_value=365,
        value=7,
        step=1
    )
    
    # Violation type filter
    violation_types = st.multiselect(
        "Filter by Violation Type",
        ["Helmet Not Worn", "Triple Riding", "Signal Violation", "Speed Violation"],
        default=["Helmet Not Worn", "Triple Riding"]
    )
    
    # Severity filter
    severity_levels = st.multiselect(
        "Filter by Severity",
        ["Critical", "High", "Medium", "Low"],
        default=["Critical", "High"]
    )
    
    # Refresh interval
    refresh_interval = st.select_slider(
        "Refresh interval (seconds)",
        options=[5, 10, 30, 60, 300],
        value=30
    )
    
    st.markdown("---")
    st.info("ℹ️ Dashboard auto-refreshes based on selected interval")


# KPI Cards
st.subheader("📊 Summary Metrics")
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        label="Total Violations (7d)",
        value="1,250",
        delta="+45 today",
        delta_color="inverse"
    )

with col2:
    st.metric(
        label="E-Challans Issued",
        value="980",
        delta="+38 today"
    )

with col3:
    st.metric(
        label="Revenue Collected",
        value="₹4,90,000",
        delta="+₹19,000 today"
    )

with col4:
    st.metric(
        label="Payment Rate",
        value="78%",
        delta="+2% from last week"
    )

st.markdown("---")

# Main content tabs
tab1, tab2, tab3, tab4, tab5 = st.tabs(
    ["📍 Heatmap", "📈 Analytics", "🚗 Recent Violations", "💰 Challans", "🎯 High-Risk Zones"]
)

# Tab 1: Heatmap
with tab1:
    st.subheader("Violation Heatmap")
    st.markdown(f"Showing violations from the last {days_filter} days")
    
    # Create and display map
    violation_map = create_violation_heatmap(None)
    st_folium(violation_map, width=st.column_config.width, height=600)
    
    st.info("🔴 Red zones indicate high violation density areas")


# Tab 2: Analytics
with tab2:
    st.subheader("Analytics & Trends")
    
    # Charts in 2x2 grid
    col1, col2 = st.columns(2)
    
    with col1:
        fig_trends = create_violation_trends_chart(days_filter)
        st.plotly_chart(fig_trends, use_container_width=True)
    
    with col2:
        fig_types = create_violation_type_chart()
        st.plotly_chart(fig_types, use_container_width=True)
    
    col3, col4 = st.columns(2)
    
    with col3:
        fig_hourly = create_hourly_distribution_chart()
        st.plotly_chart(fig_hourly, use_container_width=True)
    
    with col4:
        # Payment status chart
        payment_data = {
            'Paid': 760,
            'Pending': 180,
            'Disputed': 40
        }
        fig_payment = px.pie(
            values=list(payment_data.values()),
            names=list(payment_data.keys()),
            title='Challan Payment Status',
            color_discrete_map={'Paid': '#90EE90', 'Pending': '#FFD700', 'Disputed': '#FF6B6B'}
        )
        st.plotly_chart(fig_payment, use_container_width=True)


# Tab 3: Recent Violations
with tab3:
    st.subheader("Recent Violations")
    
    # Sample data
    violations_df = pd.DataFrame({
        'Timestamp': pd.date_range(end=datetime.now(), periods=10, freq='H'),
        'Vehicle': ['DL-01AB1234', 'DL-02CD5678', 'DL-03EF9012', 'DL-04GH3456', 'DL-05IJ7890',
                   'DL-06KL1234', 'DL-07MN5678', 'DL-08OP9012', 'DL-09QR3456', 'DL-10ST7890'],
        'Violation Type': ['Helmet Not Worn', 'Triple Riding', 'Signal Violation', 
                          'Helmet Not Worn', 'Speed Violation'] * 2,
        'Severity': ['High', 'High', 'Medium', 'High', 'Medium'] * 2,
        'Location': ['NH-48 Toll', 'Ring Road', 'ITO Signal', 'NH-48 Toll', 'Airport Road'] * 2,
        'Confidence': [0.95, 0.87, 0.92, 0.88, 0.91, 0.93, 0.85, 0.89, 0.94, 0.86]
    })
    
    # Display with filtering
    filtered_df = violations_df[violations_df['Violation Type'].isin(violation_types)]
    
    st.dataframe(
        filtered_df,
        use_container_width=True,
        height=400,
        hide_index=True
    )


# Tab 4: Challans
with tab4:
    st.subheader("E-Challans Management")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Challans", "980")
    with col2:
        st.metric("Paid", "760")
    with col3:
        st.metric("Pending", "220")
    
    st.markdown("---")
    
    # Challan search
    search_challan = st.text_input("Search Challan Number or Vehicle...")
    
    if search_challan:
        # Sample search results
        st.success(f"Found challan for {search_challan}")
        st.info("Challan Details:\n- Status: ISSUED\n- Amount: ₹500\n- Vehicle: DL-01AB1234")
    else:
        st.markdown("Enter challan number or vehicle registration to search")


# Tab 5: High-Risk Zones
with tab5:
    st.subheader("High-Risk Violation Zones")
    st.markdown("Areas with highest violation frequency")
    
    # Sample high-risk zones
    high_risk_zones = pd.DataFrame({
        'Rank': [1, 2, 3, 4, 5],
        'Location': ['NH-48 Toll', 'Ring Road-ITO', 'Airport Road', 'Mathura Road', 'Yamuna Expressway'],
        'Violations (7d)': [245, 189, 156, 134, 128],
        'Severity Score': [9.8, 9.2, 8.5, 7.9, 7.6],
        'Primary Type': ['Helmet Not Worn', 'Triple Riding', 'Signal Violation', 
                        'Helmet Not Worn', 'Speed Violation']
    })
    
    st.dataframe(
        high_risk_zones,
        use_container_width=True,
        hide_index=True
    )
    
    st.markdown("---")
    st.subheader("Recommendations")
    st.warning("⚠️ NH-48 Toll: Recommend increased CCTV deployment in this zone")
    st.warning("⚠️ Ring Road-ITO: Consider speed control measures")
    st.info("✅ Yamuna Expressway: Violation trend stabilizing, maintain current strategy")


# Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: gray; font-size: 12px;'>
        Traffic Violation Detection System | Last Updated: """ + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + """
    </div>
    """,
    unsafe_allow_html=True
)

# Auto refresh
import time
time.sleep(refresh_interval)
st.rerun()
