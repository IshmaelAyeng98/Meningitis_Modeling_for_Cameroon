"""
================================================================================
PAGE 1: OVERVIEW / EXECUTIVE SUMMARY
================================================================================

This page provides a high-level overview of the meningitis situation:
- Key Performance Indicators (KPIs)
- Temporal trends (cases and deaths over time)
- Regional distribution
- High-risk districts
- Current alerts

Target Audience: DLMEP/MINSANTE decision-makers needing quick insights

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
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

# ============================================================================
# PAGE CONFIGURATION
# ============================================================================

st.set_page_config(
    page_title="Overview - Meningitis Dashboard",
    page_icon="📊",
    layout="wide"
)

# Apply the same custom CSS from main dashboard
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
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .dashboard-header h1 { color: white; margin: 0; font-size: 2rem; }
    [data-testid="stMetricValue"] { color: #1f77b4; font-weight: 600; }
    .alert-box {
        background-color: #F8D7DA;
        border-left: 5px solid #DC3545;
        padding: 1rem;
        border-radius: 5px;
        margin: 1rem 0;
    }
    .warning-box {
        background-color: #FFF3CD;
        border-left: 5px solid #FFC107;
        padding: 1rem;
        border-radius: 5px;
        margin: 1rem 0;
    }
    .info-box {
        background-color: #d945a5;
        border-left: 5px solid #1f77b4;
        padding: 1rem;
        border-radius: 5px;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# CACHED DATA LOADING
# ============================================================================

@st.cache_data(ttl=3600)
def load_main_dataset():
    """Load primary dataset (same as main dashboard)"""
    try:
        df = pd.read_csv('Dashboard/cleaned_data/ml_final_100pct_geometry.csv')
        df['data_year'] = df['data_year'].astype('int16')
        df['week_number'] = df['week_number'].astype('int8')
        if 'region' in df.columns:
            df['region'] = df['region'].astype('category')
        if 'district_clean' in df.columns:
            df['district_clean'] = df['district_clean'].astype('category')
        return df
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        return pd.DataFrame()


@st.cache_data
def compute_kpis(df, selected_years, selected_regions):
    """
    Compute Key Performance Indicators for the overview page
    
    Args:
        df: Main dataframe
        selected_years: List of years to include
        selected_regions: List of regions to include
        
    Returns:
        dict: Dictionary of KPIs
    """
    # Filter data based on selections
    df_filtered = df[
        (df['data_year'].isin(selected_years)) &
        (df['region'].isin(selected_regions))
    ].copy()
    
    # Basic statistics
    total_cases = int(df_filtered['cases'].sum())
    total_deaths = int(df_filtered['deaths'].sum())
    overall_cfr = (total_deaths / total_cases * 100) if total_cases > 0 else 0
    
    # Districts affected (districts with at least 1 case)
    affected_districts = df_filtered[df_filtered['cases'] > 0]['district_clean'].nunique()
    total_districts = df_filtered['district_clean'].nunique()
    
    # Current year/week activity (most recent data)
    latest_year = df_filtered['data_year'].max()
    latest_week = df_filtered[df_filtered['data_year'] == latest_year]['week_number'].max()
    
    # Current week cases
    current_week_data = df_filtered[
        (df_filtered['data_year'] == latest_year) &
        (df_filtered['week_number'] == latest_week)
    ]
    current_week_cases = int(current_week_data['cases'].sum())
    
    # Active outbreaks (districts with cases in latest week)
    active_outbreaks = len(current_week_data[current_week_data['cases'] > 0])
    
    # Calculate changes (compare to previous period)
    # Get previous year's same period
    prev_year_data = df_filtered[
        (df_filtered['data_year'] == latest_year - 1) &
        (df_filtered['week_number'] == latest_week)
    ]
    prev_year_cases = int(prev_year_data['cases'].sum())
    
    # Year-over-year change
    if prev_year_cases > 0:
        yoy_change = ((current_week_cases - prev_year_cases) / prev_year_cases * 100)
    else:
        yoy_change = 0
    
    return {
        'total_cases': total_cases,
        'total_deaths': total_deaths,
        'overall_cfr': overall_cfr,
        'affected_districts': affected_districts,
        'total_districts': total_districts,
        'current_week_cases': current_week_cases,
        'active_outbreaks': active_outbreaks,
        'latest_year': latest_year,
        'latest_week': latest_week,
        'yoy_change': yoy_change,
        'prev_year_cases': prev_year_cases
    }


@st.cache_data
def get_temporal_data(df, selected_years, selected_regions):
    """
    Prepare temporal trend data
    
    Returns yearly aggregated cases and deaths
    """
    df_filtered = df[
        (df['data_year'].isin(selected_years)) &
        (df['region'].isin(selected_regions))
    ]
    
    yearly_data = df_filtered.groupby('data_year').agg({
        'cases': 'sum',
        'deaths': 'sum'
    }).reset_index()
    
    # Calculate CFR for each year
    yearly_data['cfr'] = (yearly_data['deaths'] / yearly_data['cases'] * 100).fillna(0)
    
    return yearly_data


@st.cache_data
def get_regional_data(df, selected_years, selected_regions):
    """
    Prepare regional distribution data
    
    Returns regional aggregates sorted by cases
    """
    df_filtered = df[
        (df['data_year'].isin(selected_years)) &
        (df['region'].isin(selected_regions))
    ]
    
    regional_data = df_filtered.groupby('region').agg({
        'cases': 'sum',
        'deaths': 'sum',
        'district_clean': 'nunique',
        'population': 'first'
    }).reset_index()
    
    regional_data.columns = ['region', 'total_cases', 'total_deaths', 'num_districts', 'population']
    
    # Calculate CFR and incidence rate
    regional_data['cfr'] = (regional_data['total_deaths'] / regional_data['total_cases'] * 100).fillna(0)
    regional_data['incidence_rate'] = (regional_data['total_cases'] / regional_data['population'] * 100000).fillna(0)
    
    # Sort by total cases descending
    regional_data = regional_data.sort_values('total_cases', ascending=False)
    
    return regional_data


@st.cache_data
def get_high_risk_districts(df, selected_years, selected_regions, top_n=15):
    """
    Identify high-risk districts based on total cases
    
    Returns top N districts by case count
    """
    df_filtered = df[
        (df['data_year'].isin(selected_years)) &
        (df['region'].isin(selected_regions))
    ]
    
    district_data = df_filtered.groupby(['region', 'district_clean']).agg({
        'cases': 'sum',
        'deaths': 'sum',
        'population': 'first'
    }).reset_index()
    
    # Calculate metrics
    district_data['cfr'] = (district_data['deaths'] / district_data['cases'] * 100).fillna(0)
    district_data['incidence_rate'] = (district_data['cases'] / district_data['population'] * 100000).fillna(0)
    
    # Get top N districts
    top_districts = district_data.nlargest(top_n, 'cases')
    
    # Add risk level classification
    def classify_risk(cases):
        if cases > district_data['cases'].quantile(0.90):
            return "🔴 Critical"
        elif cases > district_data['cases'].quantile(0.75):
            return "🟠 High"
        elif cases > district_data['cases'].quantile(0.50):
            return "🟡 Moderate"
        else:
            return "🟢 Low"
    
    top_districts['risk_level'] = top_districts['cases'].apply(classify_risk)
    
    return top_districts


# ============================================================================
# MAIN PAGE FUNCTION
# ============================================================================

def main():
    """Main function for Overview page"""
    
    # ========================================================================
    # HEADER
    # ========================================================================
    
    st.markdown('''
    <div class="dashboard-header">
        <h1>📊 Overview - Executive Summary</h1>
    </div>
    ''', unsafe_allow_html=True)
    
    # ========================================================================
    # LOAD DATA
    # ========================================================================
    
    with st.spinner("Loading data..."):
        df = load_main_dataset()
    
    if df.empty:
        st.error("❌ Failed to load data. Please check file path.")
        st.stop()
    
    # ========================================================================
    # SIDEBAR FILTERS
    # ========================================================================
    
    st.sidebar.header("🔍 Filters")
    st.sidebar.markdown("---")
    
    # Year filter
    available_years = sorted(df['data_year'].unique(), reverse=True)
    selected_years = st.sidebar.multiselect(
        "Select Years",
        options=available_years,
        default=available_years[:2],  # Default: most recent 2 years
        help="Choose which years to include in the analysis"
    )
    
    # Region filter
    available_regions = sorted(df['region'].unique())
    selected_regions = st.sidebar.multiselect(
        "Select Regions",
        options=available_regions,
        default=available_regions,  # Default: all regions
        help="Choose which regions to include"
    )
    
    # Ensure at least some data is selected
    if not selected_years or not selected_regions:
        st.warning("⚠️ Please select at least one year and one region.")
        st.stop()
    
    st.sidebar.markdown("---")
    st.sidebar.info(f"""
    **Current Selection:**
    - Years: {len(selected_years)}
    - Regions: {len(selected_regions)}
    """)
    
    # ========================================================================
    # COMPUTE METRICS
    # ========================================================================
    
    with st.spinner("Computing metrics..."):
        kpis = compute_kpis(df, selected_years, selected_regions)
    
    # ========================================================================
    # KEY PERFORMANCE INDICATORS
    # ========================================================================
    
    st.subheader("📈 Key Performance Indicators")
    
    # Display KPIs in 5 columns
    kpi_col1, kpi_col2, kpi_col3, kpi_col4, kpi_col5 = st.columns(5)
    
    with kpi_col1:
        st.metric(
            label="Total Cases",
            value=f"{kpis['total_cases']:,}",
            delta=None,
            help=f"Total meningitis cases ({min(selected_years)}-{max(selected_years)})"
        )
    
    with kpi_col2:
        st.metric(
            label="Total Deaths",
            value=f"{kpis['total_deaths']:,}",
            delta=None,
            help="Total deaths from meningitis"
        )
    
    with kpi_col3:
        st.metric(
            label="Case Fatality Rate",
            value=f"{kpis['overall_cfr']:.2f}%",
            delta=None,
            help="Overall CFR = (Deaths / Cases) × 100"
        )
    
    with kpi_col4:
        st.metric(
            label="Affected Districts",
            value=f"{kpis['affected_districts']}/{kpis['total_districts']}",
            delta=None,
            help="Districts with at least 1 case / Total districts"
        )
    
    with kpi_col5:
        st.metric(
            label="Active Outbreaks",
            value=f"{kpis['active_outbreaks']}",
            delta=None,
            help=f"Districts with cases in Week {kpis['latest_week']}, {kpis['latest_year']}"
        )
    
    # Current week summary
    st.markdown(f"""
    <div class="info-box">
        <strong>📅 Current Period:</strong> Week {kpis['latest_week']}, {kpis['latest_year']}<br>
        <strong>Cases this week:</strong> {kpis['current_week_cases']:,} 
        <strong>({kpis['yoy_change']:+.1f}% vs. same week last year)</strong>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # ========================================================================
    # TEMPORAL TRENDS
    # ========================================================================
    
    st.subheader("📊 Temporal Trends")
    
    # Get temporal data
    yearly_data = get_temporal_data(df, selected_years, selected_regions)
    
    # Create dual-axis chart
    fig_temporal = go.Figure()
    
    # Add cases as bars
    fig_temporal.add_trace(
        go.Bar(
            x=yearly_data['data_year'],
            y=yearly_data['cases'],
            name='Cases',
            marker_color='#1f77b4',
            yaxis='y',
            hovertemplate='<b>Year:</b> %{x}<br><b>Cases:</b> %{y:,}<extra></extra>'
        )
    )
    
    # Add deaths as line on secondary axis
    fig_temporal.add_trace(
        go.Scatter(
            x=yearly_data['data_year'],
            y=yearly_data['deaths'],
            name='Deaths',
            mode='lines+markers',
            marker=dict(size=10, color='#d62728'),
            line=dict(width=3, color='#d62728'),
            yaxis='y2',
            hovertemplate='<b>Year:</b> %{x}<br><b>Deaths:</b> %{y:,}<extra></extra>'
        )
    )
    
    # Update layout
    fig_temporal.update_layout(
        title=dict(
            text="<b>Cases and Deaths Over Time</b>",
            font=dict(size=16)
        ),
        xaxis=dict(
            title="Year",
            tickmode='linear'
        ),
        yaxis=dict(
            title=dict(text="<b>Cases</b>", font=dict(color='#1f77b4')),
            tickformat=','
        ),
        yaxis2=dict(
            title=dict(text="<b>Deaths</b>", font=dict(color='#d62728')),
            overlaying='y',
            side='right',
            tickformat=','
        ),
        hovermode='x unified',
        height=500,
        showlegend=True,
        legend=dict(x=0.01, y=0.99, bgcolor='rgba(255,255,255,0.8)')
    )
    
    st.plotly_chart(fig_temporal, use_container_width=True)
    
    st.markdown("---")
    
    # ========================================================================
    # REGIONAL DISTRIBUTION
    # ========================================================================
    
    st.subheader("🗺️ Regional Distribution")
    
    # Get regional data
    regional_data = get_regional_data(df, selected_years, selected_regions)
    
    # Create horizontal bar chart
    fig_regional = px.bar(
        regional_data,
        x='total_cases',
        y='region',
        orientation='h',
        title="<b>Total Cases by Region</b>",
        labels={'total_cases': 'Total Cases', 'region': 'Region'},
        color='total_cases',
        color_continuous_scale='YlOrRd',
        text='total_cases',
        hover_data={
            'total_deaths': ':,',
            'cfr': ':.2f',
            'num_districts': True,
            'incidence_rate': ':.2f'
        }
    )
    
    fig_regional.update_traces(
        texttemplate='%{text:,}',
        textposition='outside'
    )
    
    fig_regional.update_layout(
        height=400,
        showlegend=False,
        xaxis_title="Total Cases",
        yaxis_title="Region"
    )
    
    st.plotly_chart(fig_regional, use_container_width=True)
    
    st.markdown("---")
    
    # ========================================================================
    # HIGH-RISK DISTRICTS
    # ========================================================================
    
    st.subheader("⚠️ High-Risk Districts - Top 15")
    
    # Get high-risk districts
    top_districts = get_high_risk_districts(df, selected_years, selected_regions, top_n=15)
    
    # Prepare display dataframe
    display_df = top_districts[[
        'region', 'district_clean', 'cases', 'deaths', 'incidence_rate', 'cfr', 'risk_level'
    ]].copy()
    
    display_df.columns = [
        'Region', 'District', 'Total Cases', 'Total Deaths',
        'Incidence Rate (per 100k)', 'CFR (%)', 'Risk Level'
    ]
    
    # Display styled dataframe
    st.dataframe(
        display_df.style
        .background_gradient(subset=['Total Cases'], cmap='YlOrRd')
        .background_gradient(subset=['CFR (%)'], cmap='RdYlGn_r')
        .format({
            'Total Cases': '{:,.0f}',
            'Total Deaths': '{:,.0f}',
            'Incidence Rate (per 100k)': '{:.2f}',
            'CFR (%)': '{:.2f}'
        }),
        use_container_width=True,
        height=400
    )
    
    # ========================================================================
    # ALERTS & WARNINGS
    # ========================================================================
    
    st.markdown("---")
    st.subheader("🚨 Alerts & Warnings")
    
    alert_col1, alert_col2 = st.columns(2)
    
    with alert_col1:
        # Check for high CFR
        high_cfr_threshold = 10.0
        if kpis['overall_cfr'] > high_cfr_threshold:
            st.markdown(f"""
            <div class="alert-box">
                <strong>🔴 High Case Fatality Rate</strong><br>
                Overall CFR of {kpis['overall_cfr']:.2f}% exceeds threshold of {high_cfr_threshold}%<br>
                <em>Action: Review healthcare access and treatment protocols</em>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="info-box">
                <strong>✅ CFR Within Normal Range</strong><br>
                Overall CFR: {kpis['overall_cfr']:.2f}%
            </div>
            """, unsafe_allow_html=True)
    
    with alert_col2:
        # Check for increasing trend
        if kpis['yoy_change'] > 20:
            st.markdown(f"""
            <div class="warning-box">
                <strong>⚠️ Increasing Trend Detected</strong><br>
                Cases increased by {kpis['yoy_change']:.1f}% vs. last year<br>
                <em>Action: Monitor closely and prepare response resources</em>
            </div>
            """, unsafe_allow_html=True)
        elif kpis['yoy_change'] < -20:
            st.markdown(f"""
            <div class="info-box">
                <strong>📉 Decreasing Trend</strong><br>
                Cases decreased by {abs(kpis['yoy_change']):.1f}% vs. last year
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="info-box">
                <strong>➡️ Stable Trend</strong><br>
                Cases changed by {kpis['yoy_change']:+.1f}% vs. last year
            </div>
            """, unsafe_allow_html=True)
    
    # ========================================================================
    # FOOTER
    # ========================================================================
    
    st.markdown("---")
    st.caption(f"**Page Updated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    st.caption(f"**Data Range:** {min(selected_years)}-{max(selected_years)} | **Regions:** {len(selected_regions)}")


# ============================================================================
# RUN PAGE
# ============================================================================

if __name__ == "__main__":
    main()
