"""
MENINGITIS SURVEILLANCE DASHBOARD - MINIMAL STARTER
Quick implementation to get you started TODAY

Installation:
    pip install streamlit plotly pandas geopandas

Run:
    streamlit run minimal_dashboard.py

Author: Ishmael Bakpianenfene Ayeng
Date: Februrary 2025
Project:  Modeling Spatiotemporal Dynamics of Meningitis Outbreak in Cameroon
"""

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import numpy as np

# ============================================================================
# PAGE CONFIGURATION
# ============================================================================

st.set_page_config(
    page_title="Meningitis Surveillance - Cameroon",
    page_icon="",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================================
# CUSTOM STYLING
# ============================================================================

st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.2rem;
        text-align: center;
        color: #666;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 10px;
        color: white;
    }
    .stAlert {
        background-color: #fff3cd;
        border-left: 5px solid #ffc107;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# DATA LOADING (CACHED FOR PERFORMANCE)
# ============================================================================

@st.cache_data
def load_meningitis_data():
    """
    Load cleaned meningitis surveillance data
    Replace path with your actual data file
    """
    try:
        # IMPORTANT: Update this path to your actual file location
        df = pd.read_csv('C:/Users/HP/Desktop/AYENG/AYENBI/INTERNSHIP/Python for Meningitis Project/cleaned_data/ml_features_engineered.csv')
        
        # Data type conversions
        df['data_year'] = df['data_year'].astype(int)
        df['week_number'] = df['week_number'].astype(int)
        df['cases'] = df['cases'].fillna(0)
        df['deaths'] = df['deaths'].fillna(0)
        
        return df
    except FileNotFoundError:
        st.error(" Data file not found! Please update the file path in load_meningitis_data()")
        return pd.DataFrame()

# Load data
df = load_meningitis_data()

if df.empty:
    st.stop()

# ============================================================================
# HEADER
# ============================================================================

st.markdown('<p class="main-header"> Meningitis Surveillance Dashboard</p>', 
            unsafe_allow_html=True)
st.markdown('<p class="sub-header">DLMEP/MINSANTE - Outbreak Monitoring & Vaccination Strategy Tool - Cameroon (2017-2025 Meningitis Data)</p>', 
            unsafe_allow_html=True)
st.markdown("---")

# ============================================================================
# SIDEBAR FILTERS
# ============================================================================

st.sidebar.title(" Dashboard Controls")
st.sidebar.markdown("---")

st.sidebar.header(" Data Filters")

# Year selector
available_years = sorted(df['data_year'].unique(), reverse=True)
selected_years = st.sidebar.multiselect(
    "Select Years",
    options=available_years,
    default=available_years[:2]  # Default to most recent 2 years
)

# Region selector
available_regions = sorted(df['region'].dropna().unique())
selected_regions = st.sidebar.multiselect(
    "Select Regions",
    options=available_regions,
    default=available_regions[:5]  # Default to first 5 regions
)

# Week range slider
week_range = st.sidebar.slider(
    "Week Range",
    min_value=1,
    max_value=53,
    value=(1, 53)
)

st.sidebar.markdown("---")
st.sidebar.info(" **Tip**: Select multiple years and regions to compare trends")

# ============================================================================
# FILTER DATA BASED ON SELECTIONS
# ============================================================================

filtered_df = df[
    (df['data_year'].isin(selected_years)) & 
    (df['region'].isin(selected_regions)) &
    (df['week_number'] >= week_range[0]) &
    (df['week_number'] <= week_range[1])
].copy()

if filtered_df.empty:
    st.warning(" No data matches your filter selections. Please adjust filters.")
    st.stop()

# ============================================================================
# KEY PERFORMANCE INDICATORS (KPIs)
# ============================================================================

st.subheader(" Key Performance Indicators")

kpi_col1, kpi_col2, kpi_col3, kpi_col4, kpi_col5 = st.columns(5)

# Calculate KPIs
total_cases = filtered_df['cases'].sum()
total_deaths = filtered_df['deaths'].sum()
overall_cfr = (total_deaths / total_cases * 100) if total_cases > 0 else 0
affected_districts = filtered_df[filtered_df['cases'] > 0]['district'].nunique()
total_districts = filtered_df['district'].nunique()

# Display KPIs
with kpi_col1:
    st.metric(
        label="Total Cases",
        value=f"{int(total_cases):,}",
        delta=None
    )

with kpi_col2:
    st.metric(
        label="Total Deaths",
        value=f"{int(total_deaths):,}",
        delta=None
    )

with kpi_col3:
    st.metric(
        label="Case Fatality Rate",
        value=f"{overall_cfr:.2f}%",
        delta=None
    )

with kpi_col4:
    st.metric(
        label="Affected Districts",
        value=f"{affected_districts}",
        delta=None
    )

with kpi_col5:
    st.metric(
        label="District Coverage",
        value=f"{affected_districts}/{total_districts}",
        delta=None
    )

st.markdown("---")

# ============================================================================
# SECTION 1: TEMPORAL TRENDS
# ============================================================================

st.subheader(" Temporal Trends Analysis")

# Aggregate by year
yearly_summary = filtered_df.groupby('data_year').agg({
    'cases': 'sum',
    'deaths': 'sum'
}).reset_index()

yearly_summary['cfr'] = (yearly_summary['deaths'] / yearly_summary['cases'].replace(0, 1) * 100)

# Create dual-axis plot
fig_temporal = go.Figure()

fig_temporal.add_trace(
    go.Bar(
        x=yearly_summary['data_year'],
        y=yearly_summary['cases'],
        name='Cases',
        marker_color='#1f77b4',
        yaxis='y',
        hovertemplate='<b>Year:</b> %{x}<br><b>Cases:</b> %{y:,}<extra></extra>'
    )
)

fig_temporal.add_trace(
    go.Scatter(
        x=yearly_summary['data_year'],
        y=yearly_summary['deaths'],
        name='Deaths',
        mode='lines+markers',
        marker=dict(size=10, color='#d62728'),
        line=dict(width=3, color='#d62728'),
        yaxis='y2',
        hovertemplate='<b>Year:</b> %{x}<br><b>Deaths:</b> %{y:,}<extra></extra>'
    )
)

fig_temporal.update_layout(
    title="<b>Cases and Deaths Over Time</b>",
    xaxis=dict(title="Year", tickmode='linear'),
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
    legend=dict(x=0.01, y=0.99)
)

st.plotly_chart(fig_temporal, use_container_width=True)

# ============================================================================
# SECTION 2: WEEKLY PATTERNS
# ============================================================================

st.subheader(" Weekly Seasonal Patterns")

# Aggregate by week number across all years
weekly_pattern = filtered_df.groupby('week_number').agg({
    'cases': ['mean', 'sum', 'std'],
    'deaths': 'sum'
}).reset_index()

weekly_pattern.columns = ['week_number', 'avg_cases', 'total_cases', 'std_cases', 'total_deaths']

# Identify high-risk weeks (top 25%)
threshold_high = weekly_pattern['avg_cases'].quantile(0.75)
weekly_pattern['risk_level'] = weekly_pattern['avg_cases'].apply(
    lambda x: 'High' if x > threshold_high else 'Moderate' if x > weekly_pattern['avg_cases'].quantile(0.5) else 'Low'
)

# Plot weekly pattern
fig_weekly = px.line(
    weekly_pattern,
    x='week_number',
    y='avg_cases',
    title="<b>Average Cases by Week (Seasonal Pattern)</b>",
    labels={'week_number': 'Week Number', 'avg_cases': 'Average Cases'},
    markers=True
)

# Add high-risk zone
fig_weekly.add_hline(
    y=threshold_high,
    line_dash="dash",
    line_color="red",
    annotation_text="High Risk Threshold (75th percentile)"
)

# Shade high-risk weeks
high_risk_weeks = weekly_pattern[weekly_pattern['risk_level'] == 'High']['week_number']
for week in high_risk_weeks:
    fig_weekly.add_vrect(
        x0=week-0.5, x1=week+0.5,
        fillcolor="red", opacity=0.1,
        layer="below", line_width=0
    )

fig_weekly.update_layout(height=450)
st.plotly_chart(fig_weekly, use_container_width=True)

# High-risk weeks alert
if len(high_risk_weeks) > 0:
    st.warning(f" **High Transmission Weeks Identified**: Weeks {', '.join(map(str, high_risk_weeks.tolist()))}")

st.markdown("---")

# ============================================================================
# SECTION 3: REGIONAL BREAKDOWN
# ============================================================================

st.subheader(" Regional Distribution")

col_left, col_right = st.columns([2, 1])

with col_left:
    # Regional summary
    regional_summary = filtered_df.groupby('region').agg({
        'cases': 'sum',
        'deaths': 'sum',
        'district': 'nunique'
    }).reset_index()
    
    regional_summary.columns = ['region', 'total_cases', 'total_deaths', 'num_districts']
    regional_summary['cfr'] = (regional_summary['total_deaths'] / regional_summary['total_cases'].replace(0, 1) * 100)
    regional_summary = regional_summary.sort_values('total_cases', ascending=True)
    
    # Horizontal bar chart
    fig_regional = px.bar(
        regional_summary,
        x='total_cases',
        y='region',
        orientation='h',
        title="<b>Total Cases by Region</b>",
        labels={'total_cases': 'Total Cases', 'region': 'Region'},
        color='total_cases',
        color_continuous_scale='YlOrRd',
        text='total_cases',
        hover_data={'total_deaths': ':,', 'cfr': ':.2f', 'num_districts': True}
    )
    
    fig_regional.update_traces(texttemplate='%{text:,}', textposition='outside')
    fig_regional.update_layout(height=500, showlegend=False)
    
    st.plotly_chart(fig_regional, use_container_width=True)

with col_right:
    st.markdown("###  Regional Statistics")
    
    # Top 3 regions
    top_3_regions = regional_summary.nlargest(3, 'total_cases')
    
    st.markdown("**Highest Burden Regions:**")
    for idx, row in top_3_regions.iterrows():
        st.markdown(f"""
        **{row['region']}**  
        - Cases: {int(row['total_cases']):,}  
        - Deaths: {int(row['total_deaths']):,}  
        - CFR: {row['cfr']:.2f}%  
        - Districts: {int(row['num_districts'])}
        """)
        st.markdown("---")

st.markdown("---")

# ============================================================================
# SECTION 4: HIGH-RISK DISTRICTS
# ============================================================================

st.subheader(" High-Risk Districts - Top 15")

# District-level summary
district_summary = filtered_df.groupby(['region', 'district']).agg({
    'cases': 'sum',
    'deaths': 'sum',
    'population': 'first'
}).reset_index()

district_summary['incidence_rate'] = (district_summary['cases'] / district_summary['population'] * 100000).round(2)
district_summary['cfr'] = (district_summary['deaths'] / district_summary['cases'].replace(0, 1) * 100).round(2)

top_15_districts = district_summary.nlargest(15, 'cases')

# Format dataframe for display
display_df = top_15_districts[['region', 'district', 'cases', 'deaths', 'incidence_rate', 'cfr']].copy()
display_df.columns = ['Region', 'District', 'Total Cases', 'Total Deaths', 'Incidence Rate (per 100k)', 'CFR (%)']

# Display with styling
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

st.markdown("---")

# ============================================================================
# SECTION 5: DATA EXPORT
# ============================================================================

st.subheader(" Data Export")

export_col1, export_col2 = st.columns(2)

with export_col1:
    # Export filtered data
    csv_data = filtered_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label=" Download Filtered Data (CSV)",
        data=csv_data,
        file_name=f"meningitis_data_{datetime.now().strftime('%Y%m%d')}.csv",
        mime="text/csv"
    )

with export_col2:
    # Export summary statistics
    summary_data = district_summary.to_csv(index=False).encode('utf-8')
    st.download_button(
        label=" Download District Summary (CSV)",
        data=summary_data,
        file_name=f"district_summary_{datetime.now().strftime('%Y%m%d')}.csv",
        mime="text/csv"
    )

st.markdown("---")

# ============================================================================
# FOOTER
# ============================================================================

footer_col1, footer_col2, footer_col3 = st.columns(3)

with footer_col1:
    st.caption(f"**Dashboard Updated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

with footer_col2:
    st.caption(f"**Data Coverage:** {df['data_year'].min()} - {df['data_year'].max()}")

with footer_col3:
    st.caption(f"**Total Districts:** {df['district'].nunique()}")

st.caption("---")
st.caption("**Data Source:** DLMEP/MINSANTE Meningitis Surveillance System, Cameroon")
st.caption("**Developed by:** Ishmael Bakpianenfene Ayeng | AIMS Cameroon 2025 Internship Program")

# ============================================================================
# SIDEBAR FOOTER
# ============================================================================

st.sidebar.markdown("---")
st.sidebar.markdown("###  About")
st.sidebar.info("""
This dashboard provides real-time surveillance and analysis of meningitis outbreaks 
across health districts in Cameroon. 

**Features:**
- Temporal trend analysis
- Regional distribution
- High-risk district identification
- Seasonal pattern detection
- Data export capabilities
""")

st.sidebar.markdown("###  Quick Links")
st.sidebar.markdown("""
- [Data Quality Report](#)
- [Methodology](#)
- [User Guide](#)
""")

# ============================================================================
# END OF DASHBOARD
# ============================================================================