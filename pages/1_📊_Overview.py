"""
================================================================================
PAGE 1: OVERVIEW (BILINGUAL)
================================================================================

Key performance indicators and summary visualizations.
Supports English and French via language selector.

================================================================================
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import sys
import os

# Add parent directory to path to import lang_config
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from lang_config import get_text

# ============================================================================
# PAGE CONFIGURATION
# ============================================================================

st.set_page_config(
    page_title="Overview - Meningitis Dashboard",
    page_icon="📊",
    layout="wide"
)

# Get language from session state
lang = st.session_state.get('language', 'en')

# Apply custom CSS
st.markdown("""
<style>
    .main { background-color: #FFFFFF; }
    [data-testid="stSidebar"] { background-color: #28119c; }
    .dashboard-header {
        background: linear-gradient(135deg, #1f77b4 0%, #2C3E50 100%);
        color: white;
        padding: 2rem;
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    .dashboard-header h1 { color: white; margin: 0; font-size: 2rem; }
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
# MAIN PAGE FUNCTION
# ============================================================================

def main():
    """Main function for Overview page"""
    
    # Header
    st.markdown(f'''
    <div class="dashboard-header">
        <h1>📊 {get_text('overview', lang)} - {get_text('dashboard_title', lang)}</h1>
    </div>
    ''', unsafe_allow_html=True)
    
    # Load data
    with st.spinner(get_text('loading_data', lang)):
        df = load_main_dataset()
    
    if df.empty:
        st.error(f"❌ {get_text('failed_load_data', lang)}")
        st.stop()
    
    # ========================================================================
    # KEY METRICS
    # ========================================================================
    
    st.subheader(f"📊 {get_text('quick_overview', lang)}")
    
    total_cases = df['cases'].sum()
    total_deaths = df['deaths'].sum()
    overall_cfr = (total_deaths / total_cases * 100) if total_cases > 0 else 0
    num_districts = df['district_clean'].nunique()
    num_regions = df['region'].nunique() if 'region' in df.columns else 0
    affected_districts = df[df['cases'] > 0]['district_clean'].nunique()
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(get_text('total_cases', lang), f"{total_cases:,.0f}")
    
    with col2:
        st.metric(get_text('total_deaths', lang), f"{total_deaths:,.0f}")
    
    with col3:
        st.metric(get_text('case_fatality_rate', lang), f"{overall_cfr:.2f}%")
    
    col4, col5, col6 = st.columns(3)
    
    with col4:
        st.metric(get_text('health_districts', lang), f"{num_districts}")
    
    with col5:
        st.metric(get_text('regions', lang), f"{num_regions}")
    
    with col6:
        st.metric(get_text('affected_districts', lang), f"{affected_districts}")
    
    st.markdown("---")
    
    # ========================================================================
    # TEMPORAL TRENDS
    # ========================================================================
    
    st.subheader(f"📈 {get_text('temporal_trends', lang)}")
    
    # Annual summary
    annual_data = df.groupby('data_year').agg({
        'cases': 'sum',
        'deaths': 'sum'
    }).reset_index()
    
    # Create chart
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=annual_data['data_year'],
        y=annual_data['cases'],
        name=get_text('total_cases', lang),
        marker_color='#1f77b4'
    ))
    
    fig.add_trace(go.Scatter(
        x=annual_data['data_year'],
        y=annual_data['deaths'],
        name=get_text('total_deaths', lang),
        yaxis='y2',
        line=dict(color='#d62728', width=3),
        mode='lines+markers'
    ))
    
    fig.update_layout(
        title=get_text('annual_cases_deaths', lang),
        xaxis_title=get_text('year', lang),
        yaxis_title=get_text('total_cases', lang),
        yaxis2=dict(
            title=get_text('total_deaths', lang),
            overlaying='y',
            side='right'
        ),
        hovermode='x unified',
        height=500
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    
    # ========================================================================
    # REGIONAL DISTRIBUTION
    # ========================================================================
    
    st.subheader(f"🗺️ {get_text('regional_distribution', lang)}")
    
    if 'region' in df.columns:
        regional_data = df.groupby('region').agg({
            'cases': 'sum',
            'deaths': 'sum'
        }).reset_index().sort_values('cases', ascending=True)
        
        fig = go.Figure(go.Bar(
            x=regional_data['cases'],
            y=regional_data['region'],
            orientation='h',
            marker_color='#2ca02c',
            text=regional_data['cases'],
            textposition='auto'
        ))
        
        fig.update_layout(
            title=f"{get_text('total_cases', lang)} - {get_text('regional_distribution', lang)}",
            xaxis_title=get_text('total_cases', lang),
            yaxis_title=get_text('region', lang),
            height=500
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    
    # ========================================================================
    # TOP DISTRICTS
    # ========================================================================
    
    st.subheader(f"🏆 {get_text('top_districts', lang)}")
    
    top_districts = df.groupby('district_clean').agg({
        'cases': 'sum',
        'deaths': 'sum',
        'region': 'first'
    }).reset_index().sort_values('cases', ascending=False).head(15)
    
    top_districts['cfr'] = (top_districts['deaths'] / top_districts['cases'] * 100).fillna(0)
    
    # Display table
    display_df = top_districts.copy()
    display_df.columns = [
        get_text('district', lang),
        get_text('total_cases', lang),
        get_text('total_deaths', lang),
        get_text('region', lang),
        get_text('case_fatality_rate', lang)
    ]
    
    st.dataframe(
        display_df.style.format({
            get_text('total_cases', lang): '{:,.0f}',
            get_text('total_deaths', lang): '{:,.0f}',
            get_text('case_fatality_rate', lang): '{:.2f}%'
        }),
        use_container_width=True,
        height=400
    )
    
    # Footer
    st.markdown("---")
    st.caption(f"**{get_text('total_records', lang)}:** {len(df):,}")

# ============================================================================
# RUN PAGE
# ============================================================================

if __name__ == "__main__":
    main()
