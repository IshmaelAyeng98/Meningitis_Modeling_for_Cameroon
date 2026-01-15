"""
================================================================================
BILINGUAL MENINGITIS SURVEILLANCE DASHBOARD - CAMEROON
================================================================================

Single unified dashboard with language switcher (English/French)
Developed by: Ishmael Bakpianefene AYENG, AIMS Cameroon
Project: Spatiotemporal Modeling of Meningitis Outbreaks
Partner: DLMEP/MINSANTE, Cameroon Ministry of Health

Language Support: English 🇬🇧 | Français 🇫🇷
Switch languages using the selector in the top right corner

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

# Import language configuration
from lang_config import translations, get_text

# ============================================================================
# PAGE CONFIGURATION
# ============================================================================

st.set_page_config(
    page_title="Meningitis Surveillance - Cameroon",
    page_icon="🦠",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://github.com/IshmaelAyeng98?tab=repositories',
        'Report a bug': 'mailto:ishmael.ayeng@aims-cameroon.org',
        'About': 'Bilingual Meningitis Surveillance Dashboard for DLMEP/MINSANTE'
    }
)

# ============================================================================
# SESSION STATE INITIALIZATION
# ============================================================================

# Initialize language in session state (default to English)
if 'language' not in st.session_state:
    st.session_state.language = 'en'

# ============================================================================
# LANGUAGE SELECTOR IN TOP RIGHT
# ============================================================================

# Create columns to position language selector in top right
col1, col2, col3 = st.columns([6, 1, 1])

with col3:
    # Language selector
    language_options = {
        'English 🇬🇧': 'en',
        'Français 🇫🇷': 'fr'
    }
    
    # Get current language label
    current_label = [k for k, v in language_options.items() if v == st.session_state.language][0]
    
    selected_language = st.selectbox(
        label='',  # No label
        options=list(language_options.keys()),
        index=list(language_options.keys()).index(current_label),
        key='language_selector'
    )
    
    # Update session state if language changed
    st.session_state.language = language_options[selected_language]

# Get current language
lang = st.session_state.language

# ============================================================================
# CUSTOM CSS STYLING
# ============================================================================

st.markdown("""
<style>
    /* ===== MAIN LAYOUT ===== */
    
    .main {
        background-color: #FFFFFF;
    }
    
    [data-testid="stSidebar"] {
        background-color: #28119c;
    }
    
    /* ===== LANGUAGE SELECTOR STYLING ===== */
    
    /* Position language selector in top right */
    div[data-testid="column"]:nth-child(3) {
        display: flex;
        justify-content: flex-end;
        align-items: flex-start;
    }
    
    /* Style the selectbox */
    div[data-testid="stSelectbox"] {
        margin-top: -50px;
    }
    
    /* ===== HEADER STYLING ===== */
    
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
    
    [data-testid="stMetricValue"] {
        font-size: 2rem;
        font-weight: 700;
        color: #1f77b4;
    }
    
    [data-testid="stMetricLabel"] {
        font-size: 1rem;
        font-weight: 600;
        color: #2C3E50;
    }
    
    /* ===== BUTTONS ===== */
    
    .stButton > button {
        background-color: #1f77b4;
        color: white;
        border: none;
        border-radius: 5px;
        padding: 0.5rem 1rem;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        background-color: #145a8f;
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    }
    
    /* ===== DOWNLOAD BUTTONS ===== */
    
    .stDownloadButton > button {
        background-color: #2ca02c;
        color: white;
        border: none;
        border-radius: 5px;
        padding: 0.5rem 1rem;
        font-weight: 600;
    }
    
    /* ===== ALERTS ===== */
    
    .stAlert {
        border-radius: 5px;
        padding: 1rem;
    }
    
    /* ===== TABLES ===== */
    
    .dataframe {
        font-size: 0.9rem;
        border-radius: 5px;
    }
    
    .dataframe thead tr th {
        background-color: #1f77b4 !important;
        color: white !important;
        font-weight: 600 !important;
    }
    
    /* ===== DIVIDERS ===== */
    
    hr {
        border: none;
        border-top: 2px solid #E5E5E5;
        margin: 2rem 0;
    }
    
</style>
""", unsafe_allow_html=True)

# ============================================================================
# CACHED DATA LOADING
# ============================================================================

@st.cache_data(ttl=3600)
def load_main_dataset():
    """Load primary dataset"""
    try:
        df = pd.read_csv('Dashboard/cleaned_data/ml_final_100pct_geometry.csv')
        df['data_year'] = df['data_year'].astype('int16')
        df['week_number'] = df['week_number'].astype('int8')
        if 'region' in df.columns:
            df['region'] = df['region'].astype('category')
        if 'district_clean' in df.columns:
            df['district_clean'] = df['district_clean'].astype('category')
        return df
    except:
        try:
            df = pd.read_csv('cleaned_data/ml_final_100pct_geometry.csv')
            df['data_year'] = df['data_year'].astype('int16')
            df['week_number'] = df['week_number'].astype('int8')
            if 'region' in df.columns:
                df['region'] = df['region'].astype('category')
            if 'district_clean' in df.columns:
                df['district_clean'] = df['district_clean'].astype('category')
            return df
        except Exception as e:
            st.error(f"{get_text('error_loading_data', lang)}: {str(e)}")
            return pd.DataFrame()

# ============================================================================
# MAIN DASHBOARD
# ============================================================================

def main():
    """Main dashboard function"""
    
    # ========================================================================
    # HEADER
    # ========================================================================
    
    st.markdown(f'''
    <div class="dashboard-header">
        <h1>{get_text('dashboard_title', lang)}</h1>
        <p>{get_text('dashboard_subtitle', lang)} (2017-2025)</p>
    </div>
    ''', unsafe_allow_html=True)
    
    # ========================================================================
    # LOAD DATA
    # ========================================================================
    
    with st.spinner(get_text('loading_data', lang)):
        df = load_main_dataset()
    
    if df.empty:
        st.error(f"❌ {get_text('failed_load_data', lang)}")
        st.stop()
    
    # Success message
    st.success(f"✅ {get_text('data_loaded', lang)} {len(df):,} {get_text('records_ready', lang)}")
    
    # ========================================================================
    # QUICK OVERVIEW
    # ========================================================================
    
    st.subheader(f"📊 {get_text('quick_overview', lang)}")
    
    # Calculate key metrics
    total_cases = df['cases'].sum()
    total_deaths = df['deaths'].sum()
    overall_cfr = (total_deaths / total_cases * 100) if total_cases > 0 else 0
    num_districts = df['district_clean'].nunique()
    num_regions = df['region'].nunique() if 'region' in df.columns else 0
    
    # Display metrics
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric(
            get_text('total_cases', lang),
            f"{total_cases:,.0f}"
        )
    
    with col2:
        st.metric(
            get_text('total_deaths', lang),
            f"{total_deaths:,.0f}"
        )
    
    with col3:
        st.metric(
            get_text('case_fatality_rate', lang),
            f"{overall_cfr:.2f}%"
        )
    
    with col4:
        st.metric(
            get_text('health_districts', lang),
            f"{num_districts}"
        )
    
    with col5:
        st.metric(
            get_text('regions', lang),
            f"{num_regions}"
        )
    
    st.markdown("---")
    
    # ========================================================================
    # NAVIGATION INFO
    # ========================================================================
    
    st.subheader(f"🧭 {get_text('dashboard_navigation', lang)}")
    
    st.markdown(f"""
    ### 📄 {get_text('available_pages', lang)}
    
    {get_text('use_sidebar', lang)}:
    
    1. 📊 **{get_text('overview', lang)}**
    2. 🗺️ **{get_text('spatial_analysis', lang)}**
    3. 📈 **{get_text('temporal_analysis', lang)}**
    4. 🎯 **{get_text('predictions', lang)}**
    5. 📋 **{get_text('data_explorer', lang)}**
    6. 🗺️ **{get_text('LISA_analysis', lang)}**
    7. ℹ️ **{get_text('about', lang)}**
    """)
    
    st.markdown("---")
    
    # ========================================================================
    # SYSTEM STATUS
    # ========================================================================
    
    st.subheader(f"💻 {get_text('system_status', lang)}")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.info(f"**{get_text('total_records', lang)}:** {len(df):,}")
    
    with col2:
        st.info(f"**{get_text('date_range', lang)}:** {df['data_year'].min()}-{df['data_year'].max()}")
    
    with col3:
        if lang == 'en':
            st.info(f"**Language:** English 🇬🇧")
        else:
            st.info(f"**Langue:** Français 🇫🇷")
    
    # ========================================================================
    # FOOTER
    # ========================================================================
    
    st.markdown("---")
    st.caption(f"**{get_text('developed_by', lang)}:** Ishmael Bakpianefene AYENG, AIMS Cameroon")
    st.caption(f"**{get_text('supervised_by', lang)}:** Dr. Solange Whegang, AIMS Cameroon")
    st.caption(f"**{get_text('partner', lang)}:** DLMEP/MINSANTE")
    st.caption(f"**{get_text('dashboard_version', lang)}:** 2.0 Bilingual | **{get_text('last_updated', lang)}:** {datetime.now().strftime('%B %Y')}")

# ============================================================================
# RUN APPLICATION
# ============================================================================

if __name__ == "__main__":
    main()
