"""
================================================================================
MENINGITIS SURVEILLANCE DASHBOARD - CAMEROON
================================================================================

Main Dashboard Entry Point
Developed by: Ishmael Bakpianefene AYENG, AIMS Cameroon
Project: Spatiotemporal Modeling of Meningitis Outbreaks
Partner: DLMEP/MINSANTE, Cameroon Ministry of Health
Data Period: Meningitis Surveillance Data covering 2017-2025

This is the main entry point for a multi-page Streamlit dashboard.
Streamlit automatically detects pages in the 'pages/' folder.

File Structure:
    dashboard_app.py          <- You are here (main entry)
    pages/
        1_Overview.py
        2_Spatial_Analysis.py
        3_Temporal_Analysis.py
        4_Predictions.py
        5_Data_Explorer.py
        6_About.py

================================================================================
"""

# ============================================================================
# IMPORTS
# ============================================================================

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# ============================================================================
# PAGE CONFIGURATION
# ============================================================================

st.set_page_config(
    page_title="Meningitis Surveillance - Cameroon",
    page_icon="🦠",
    layout="wide",  # Use full screen width
    initial_sidebar_state="expanded",  # Sidebar open by default
    menu_items={
        'Get Help': 'https://github.com/IshmaelAyeng98?tab=repositories',
        'Report a bug': 'mailto:ishmael.ayeng@aims-cameroon.org',
        'About': 'Meningitis Surveillance Dashboard for DLMEP/MINSANTE'
    }
)

# ============================================================================
# CUSTOM CSS STYLING
# ============================================================================

st.markdown("""
<style>
    /* ===== MAIN LAYOUT ===== */
    
    /* Main background - clean white */
    .main {
        background-color: #FFFFFF;
    }
    
    /* Sidebar styling - dark purple */
    [data-testid="stSidebar"] {
        background-color: #28119c;
    }
    
    /* ===== HEADER STYLING ===== */
    
    /* Custom dashboard header with gradient */
    .dashboard-header {
        background: linear-gradient(135deg, #1f77b4 0%, #2C3E50 100%);
        color: white;
        padding: 2rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        text-align: center;
    }
    
    .dashboard-header h1 {
        color: white;
        margin: 0;
        font-size: 2.5rem;
        font-weight: 700;
    }
    
    .dashboard-header p {
        color: #E8E8E8;
        margin-top: 0.5rem;
        font-size: 1.1rem;
    }
    
    /* ===== METRIC CARDS ===== */
    
    /* Style metric values */
    [data-testid="stMetricValue"] {
        color: #1f77b4;
        font-weight: 600;
        font-size: 2rem;
    }
    
    /* Style metric labels */
    [data-testid="stMetricLabel"] {
        color: #262730;
        font-weight: 500;
    }
    
    /* ===== CARDS & CONTAINERS ===== */
    
    /* Card backgrounds */
    .metric-card {
        background-color: #F8F9FA;
        border-radius: 10px;
        padding: 1.5rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin-bottom: 1rem;
    }
    
    /* Info boxes */
    .info-box {
        background-color: #51a8e8;
        border-left: 5px solid #1f77b4;
        padding: 1rem;
        border-radius: 5px;
        margin: 1rem 0;
    }
    
    /* Warning boxes */
    .warning-box {
        background-color:  #826508;
        border-left: 5px solid #FFC107;
        padding: 1rem;
        border-radius: 5px;
        margin: 1rem 0;
    }
    
    /* Danger/Alert boxes */
    .alert-box {
        background-color: #751c2b;
        border-left: 5px solid #DC3545;
        padding: 1rem;
        border-radius: 5px;
        margin: 1rem 0;
    }
    
    /* Success boxes */
    .success-box {
        background-color: #2c6b3b;
        border-left: 5px solid #28A745;
        padding: 1rem;
        border-radius: 5px;
        margin: 1rem 0;
    }
    
    /* ===== BUTTONS ===== */
    
    /* Primary button styling */
    .stButton>button {
        background-color: #1f77b4;
        color: white;
        border-radius: 5px;
        padding: 0.5rem 2rem;
        border: none;
        font-weight: 600;
        transition: all 0.3s;
    }
    
    .stButton>button:hover {
        background-color: #155a8a;
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
        transform: translateY(-2px);
    }
    
    /* Download button */
    .stDownloadButton>button {
        background-color: #28A745;
        color: white;
        border-radius: 5px;
        padding: 0.5rem 2rem;
        border: none;
        font-weight: 600;
    }
    
    .stDownloadButton>button:hover {
        background-color: #218838;
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    }
    
    /* ===== DATA TABLES ===== */
    
    /* Dataframe styling */
    .dataframe {
        font-size: 0.9rem;
        border-radius: 5px;
    }
    
    /* Table headers */
    .dataframe thead tr th {
        background-color: #1f77b4 !important;
        color: white !important;
        font-weight: 600 !important;
    }
    
    /* ===== SECTION DIVIDERS ===== */
    
    hr {
        border: none;
        border-top: 2px solid #E5E5E5;
        margin: 2rem 0;
    }
    
    /* ===== SIDEBAR ENHANCEMENTS ===== */
    
    /* Sidebar title */
    [data-testid="stSidebar"] h1 {
        color: #1f77b4;
        font-size: 1.5rem;
    }
    
    /* Sidebar section headers */
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3 {
        color: #2C3E50;
        font-size: 1.2rem;
        margin-top: 1rem;
    }
    
    /* ===== EXPANDER STYLING ===== */
    
    .streamlit-expanderHeader {
        background-color: #F8F9FA;
        border-radius: 5px;
        font-weight: 600;
    }
    
    /* ===== RESPONSIVE DESIGN ===== */
    
    /* Ensure content is readable on smaller screens */
    @media (max-width: 768px) {
        .dashboard-header h1 {
            font-size: 1.8rem;
        }
        
        .dashboard-header p {
            font-size: 0.9rem;
        }
    }
    
</style>
""", unsafe_allow_html=True)

# ============================================================================
# CACHED DATA LOADING FUNCTIONS
# ============================================================================
# These functions load data once and cache it in memory
# Subsequent calls will use cached data = MUCH faster!
# ============================================================================

@st.cache_data(ttl=3600)  # Cache for 1 hour (3600 seconds)
def load_main_dataset():
    """
    Load the primary analysis dataset with all features
    
    This is the main dataset containing:
    - 2017-2025 data (9 years)
    - ~108,000 rows
    - 35+ columns including engineered features
    - 100% geometry-matched districts
    
    Returns:
        pandas.DataFrame: Complete analysis dataset
    """
    try:
        # IMPORTANT: Update this path to your actual file location
        df = pd.read_csv('cleaned_data/ml_final_100pct_geometry.csv')
        
        # Optimize data types to save memory
        # int16 can store values -32,768 to 32,767 (enough for years 2017-2025)
        df['data_year'] = df['data_year'].astype('int16')
        
        # int8 can store values -128 to 127 (enough for weeks 1-53)
        df['week_number'] = df['week_number'].astype('int8')
        
        # Category dtype saves memory for repeated string values
        if 'region' in df.columns:
            df['region'] = df['region'].astype('category')
        if 'district_clean' in df.columns:
            df['district_clean'] = df['district_clean'].astype('category')
        
        return df
    
    except FileNotFoundError:
        st.error("""
        ❌ **Data file not found!**
        
        Please ensure the file exists at:
        `cleaned_data/ml_final_100pct_geometry.csv`
        
        Update the path in the `load_main_dataset()` function if needed.
        """)
        return pd.DataFrame()  # Return empty dataframe
    
    except Exception as e:
        st.error(f" Error loading data: {str(e)}")
        return pd.DataFrame()


@st.cache_data(ttl=3600)
def load_summary_stats():
    """
    Load pre-computed summary statistics from EDA
    
    Contains:
    - Total cases/deaths
    - Epidemic years
    - High-burden regions
    - Peak transmission weeks
    
    Returns:
        dict: Summary statistics
    """
    try:
        import json
        with open('cleaned_data/eda_summary.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        st.warning(" Summary statistics file not found. Using calculated values.")
        return {}
    except Exception as e:
        st.warning(f" Could not load summary stats: {str(e)}")
        return {}


@st.cache_data(ttl=3600)
def compute_quick_stats(df):
    """
    Compute quick summary statistics from the dataset
    
    Args:
        df (pd.DataFrame): Main dataset
        
    Returns:
        dict: Quick statistics for display
    """
    if df.empty:
        return {}
    
    return {
        'total_cases': int(df['cases'].sum()),
        'total_deaths': int(df['deaths'].sum()),
        'overall_cfr': (df['deaths'].sum() / df['cases'].sum() * 100) if df['cases'].sum() > 0 else 0,
        'num_districts': df['district_clean'].nunique() if 'district_clean' in df.columns else 0,
        'num_regions': df['region'].nunique() if 'region' in df.columns else 0,
        'date_range': f"{df['data_year'].min()}-{df['data_year'].max()}",
        'total_records': len(df)
    }

# ============================================================================
# MAIN WELCOME PAGE
# ============================================================================

def main():
    """
    Main function for the landing/welcome page
    
    This page provides:
    - Welcome message
    - Quick overview statistics
    - Navigation instructions
    - System status
    """
    
    # ========================================================================
    # HEADER SECTION
    # ========================================================================
    
    st.markdown('''
    <div class="dashboard-header">
        <h1>🦠 Meningitis Outbreak Surveillance Dashboard</h1>
        <p>DLMEP/MINSANTE - Cameroon Health Districts (2017-2025)</p>
    </div>
    ''', unsafe_allow_html=True)
    
    # ========================================================================
    # LOAD DATA
    # ========================================================================
    
    # Show loading spinner while data loads
    with st.spinner("Loading data..."):
        df = load_main_dataset()
        summary_stats = load_summary_stats()
    
    # Check if data loaded successfully
    if df.empty:
        st.error(" Failed to load data. Please check the file path and try again.")
        st.stop()  # Stop execution if no data
    
    # Success message
    st.success(f"✅ Data loaded successfully! {len(df):,} records ready for analysis.")
    
    # ========================================================================
    # QUICK STATISTICS
    # ========================================================================
    
    st.subheader("📊 Quick Overview")
    
    # Compute statistics
    stats = compute_quick_stats(df)
    
    # Display in 5 columns
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric(
            label="Total Cases",
            value=f"{stats['total_cases']:,}",
            help="Total meningitis cases reported (2017-2025)"
        )
    
    with col2:
        st.metric(
            label="Total Deaths",
            value=f"{stats['total_deaths']:,}",
            help="Total deaths from meningitis (2017-2025)"
        )
    
    with col3:
        st.metric(
            label="Case Fatality Rate",
            value=f"{stats['overall_cfr']:.2f}%",
            help="Overall CFR = (Deaths / Cases) × 100"
        )
    
    with col4:
        st.metric(
            label="Health Districts",
            value=f"{stats['num_districts']}",
            help="Number of health districts with data"
        )
    
    with col5:
        st.metric(
            label="Regions",
            value=f"{stats['num_regions']}",
            help="Number of regions covered"
        )
    
    st.markdown("---")
    
    # ========================================================================
    # NAVIGATION GUIDE
    # ========================================================================
    
    st.subheader("🧭 Dashboard Navigation")
    
    # Create 2 columns for navigation instructions
    nav_col1, nav_col2 = st.columns(2)
    
    with nav_col1:
        st.markdown("""
        ### 📄 Available Pages
        
        Use the **sidebar** (← rleft) to navigate between pages:
        
        1. **📊 Overview**
           - Key performance indicators
           - Temporal trends
           - Regional distribution
           - High-risk districts
        
        2. **🗺️ Spatial Analysis**
           - Interactive maps
           - Geographic hotspots
           - District rankings
           - Spatial patterns
        
        3. **📈 Temporal Analysis**
           - Seasonal patterns
           - Epidemic timeline
           - Year-over-year trends
           - Weekly heatmaps
        """)
    
    with nav_col2:
        st.markdown("""
        
        
        4. **🎯 Predictions**
           - Outbreak forecasting
           - Risk classification
           - ML model predictions
           - Early warning system
        
        5. **📋 Data Explorer**
           - Custom filters
           - Dynamic data tables
           - Export functionality
           - Advanced queries
        
        6. **ℹ️ About**
           - Methodology
           - Data sources
           - Model documentation
           - Contact information
        """)
    
    st.markdown("---")
    
    # ========================================================================
    # SYSTEM STATUS
    # ========================================================================
    
    st.subheader("⚙️ System Status")
    
    # Create 3 columns for status information
    status_col1, status_col2, status_col3 = st.columns(3)
    
    with status_col1:
        st.markdown("""
        <div class="success-box">
            <strong>✅ Data Status</strong><br>
            All datasets loaded successfully<br>
            Coverage: 2017-2025 (9 years)
        </div>
        """, unsafe_allow_html=True)
    
    with status_col2:
        st.markdown(f"""
        <div class="info-box">
            <strong>📅 Last Updated</strong><br>
            Dashboard: {datetime.now().strftime('%Y-%m-%d %H:%M')}<br>
            Data: 2025 Week 52
        </div>
        """, unsafe_allow_html=True)
    
    with status_col3:
        st.markdown("""
        <div class="info-box">
            <strong>🔧 Features</strong><br>
            6 interactive pages<br>
            20+ visualizations
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # ========================================================================
    # KEY FINDINGS (if available from summary stats)
    # ========================================================================
    
    if summary_stats:
        st.subheader("🔍 Key Findings")
        
        findings_col1, findings_col2 = st.columns(2)
        
        with findings_col1:
            # Epidemic years
            if 'epidemic_years' in summary_stats:
                epidemic_years = summary_stats['epidemic_years']
                st.markdown(f"""
                <div class="warning-box">
                    <strong>⚠️ Epidemic Years Identified</strong><br>
                    Years with significantly elevated cases:<br>
                    <strong>{', '.join(map(str, epidemic_years))}</strong>
                </div>
                """, unsafe_allow_html=True)
        
        with findings_col2:
            # High burden regions
            if 'high_burden_regions' in summary_stats:
                high_regions = summary_stats['high_burden_regions']
                st.markdown(f"""
                <div class="alert-box">
                    <strong>🔴 High-Burden Regions</strong><br>
                    Regions with highest case counts:<br>
                    <strong>{', '.join(high_regions)}</strong>
                </div>
                """, unsafe_allow_html=True)
    
    # ========================================================================
    # GETTING STARTED
    # ========================================================================
    
    st.subheader("🚀 Getting Started")
    
    st.markdown("""
    ### For DLMEP/MINSANTE Decision-Makers:
    
    1. **Quick Assessment** → Go to **📊 Overview** page
       - See current outbreak status
       - Identify high-risk districts
       - Track temporal trends
    
    2. **Vaccination Planning** → Go to **🗺️ Spatial Analysis** page
       - View geographic distribution
       - Identify hotspots
       - Plan intervention strategies
    
    3. **Early Warning** → Go to **🎯 Predictions** page
       - View outbreak forecasts
       - See risk classifications
       - Plan resource allocation
    
    4. **Data Investigation** → Go to **📋 Data Explorer** page
       - Filter and explore data
       - Export custom reports
       - Generate summaries
    
    ---
    
    ### 💡 Tips:
    - Use **filters in the sidebar** to focus on specific years/regions
    - **Hover over charts** for detailed information
    - **Click on map districts** to see details
    - **Download data** using export buttons
    - Check the **About page** for methodology details
    """)
    
    # ========================================================================
    # FOOTER
    # ========================================================================
    
    st.markdown("---")
    
    footer_col1, footer_col2, footer_col3 = st.columns(3)
    
    with footer_col1:
        st.caption("**Developed by:** Ishmael Bakpianefene AYENG, AIMS Cameroon")
    
    with footer_col2:
        st.caption(f"**Data Coverage:** {stats['date_range']}")
    
    with footer_col3:
        st.caption(f"**Total Records:** {stats['total_records']:,}")
    
    st.caption("---")
    st.caption("**Host Ministry:** DLMEP/MINSANTE, Ministry of Public Health, Cameroon")
    st.caption("**Project:** Spatiotemporal Modeling Dynamics of Meningitis Outbreaks in Cameroon")


# ============================================================================
# RUN APPLICATION
# ============================================================================

if __name__ == "__main__":
    main()
