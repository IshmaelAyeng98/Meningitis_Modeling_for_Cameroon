"""
================================================================================
PAGE 3: TEMPORAL ANALYSIS
================================================================================

This page provides time-based analysis of meningitis patterns:
- Seasonal patterns (weekly trends)
- Year-over-year comparison
- Epidemic timeline
- Weekly heatmap calendar

Target Audience: Understanding outbreak timing, planning seasonal interventions

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
from plotly.subplots import make_subplots
import warnings
warnings.filterwarnings('ignore')

# ============================================================================
# PAGE CONFIGURATION
# ============================================================================

st.set_page_config(
    page_title="Temporal Analysis - Meningitis Dashboard",
    page_icon="📈",
    layout="wide"
)

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
    [data-testid="stMetricValue"] { color: #1f77b4; font-weight: 600; }
    .warning-box {
        background-color: #fc0303;
        border-left: 5px solid #FFC107;
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
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        return pd.DataFrame()


@st.cache_data
def get_seasonal_pattern(df, selected_years, selected_regions):
    """
    Calculate weekly seasonal pattern
    Average cases by week number across all years
    """
    df_filtered = df[
        (df['data_year'].isin(selected_years)) &
        (df['region'].isin(selected_regions))
    ]
    
    weekly_pattern = df_filtered.groupby('week_number').agg({
        'cases': ['mean', 'sum', 'std', 'min', 'max']
    }).reset_index()
    
    weekly_pattern.columns = ['week_number', 'avg_cases', 'total_cases', 
                               'std_cases', 'min_cases', 'max_cases']
    
    return weekly_pattern


@st.cache_data
def get_yearly_trends(df, selected_years, selected_regions):
    """Get year-by-year weekly trends for comparison"""
    df_filtered = df[
        (df['data_year'].isin(selected_years)) &
        (df['region'].isin(selected_regions))
    ]
    
    yearly_weekly = df_filtered.groupby(['data_year', 'week_number'])['cases'].sum().reset_index()
    
    return yearly_weekly


@st.cache_data  
def identify_epidemic_weeks(df, selected_years, selected_regions, threshold_percentile=90):
    """Identify high-transmission weeks (epidemic weeks)"""
    df_filtered = df[
        (df['data_year'].isin(selected_years)) &
        (df['region'].isin(selected_regions))
    ]
    
    # Calculate threshold (90th percentile by default)
    threshold = df_filtered.groupby(['data_year', 'week_number'])['cases'].sum().quantile(threshold_percentile / 100)
    
    # Identify weeks above threshold
    weekly_cases = df_filtered.groupby(['data_year', 'week_number'])['cases'].sum().reset_index()
    epidemic_weeks = weekly_cases[weekly_cases['cases'] > threshold].copy()
    
    return epidemic_weeks, threshold


# ============================================================================
# MAIN PAGE FUNCTION
# ============================================================================

def main():
    """Main function for Temporal Analysis page"""
    
    # ========================================================================
    # HEADER
    # ========================================================================
    
    st.markdown('''
    <div class="dashboard-header">
        <h1>📈 Temporal Analysis - Seasonal Patterns & Trends</h1>
    </div>
    ''', unsafe_allow_html=True)
    
    # ========================================================================
    # LOAD DATA
    # ========================================================================
    
    with st.spinner("Loading temporal data..."):
        df = load_main_dataset()
    
    if df.empty:
        st.error("❌ Failed to load data.")
        st.stop()
    
    # ========================================================================
    # SIDEBAR FILTERS
    # ========================================================================
    
    st.sidebar.header("🔍 Filters")
    st.sidebar.markdown("---")
    
    # Year filter (multiple years for comparison)
    available_years = sorted(df['data_year'].unique(), reverse=True)
    selected_years = st.sidebar.multiselect(
        "Select Years",
        options=available_years,
        default=available_years[:3],  # Default: most recent 3 years
        help="Choose years to include in temporal analysis"
    )
    
    # Region filter
    available_regions = sorted(df['region'].unique())
    selected_regions = st.sidebar.multiselect(
        "Select Regions",
        options=available_regions,
        default=available_regions,
        help="Choose regions to include"
    )
    
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
    # SEASONAL PATTERN ANALYSIS
    # ========================================================================
    
    st.subheader("🌊 Seasonal Pattern - Weekly Average Cases")
    
    # Get seasonal pattern
    weekly_pattern = get_seasonal_pattern(df, selected_years, selected_regions)
    
    # Identify high-risk weeks (top 25%)
    high_risk_threshold = weekly_pattern['avg_cases'].quantile(0.75)
    
    # Create seasonal pattern chart
    fig_seasonal = go.Figure()
    
    # Add average line
    fig_seasonal.add_trace(
        go.Scatter(
            x=weekly_pattern['week_number'],
            y=weekly_pattern['avg_cases'],
            mode='lines+markers',
            name='Average Cases',
            line=dict(color='#1f77b4', width=3),
            marker=dict(size=6),
            hovertemplate='<b>Week %{x}</b><br>Avg Cases: %{y:.1f}<extra></extra>'
        )
    )
    
    # Add range (min-max) as shaded area
    fig_seasonal.add_trace(
        go.Scatter(
            x=weekly_pattern['week_number'],
            y=weekly_pattern['max_cases'],
            mode='lines',
            name='Max',
            line=dict(width=0),
            showlegend=False,
            hoverinfo='skip'
        )
    )
    
    fig_seasonal.add_trace(
        go.Scatter(
            x=weekly_pattern['week_number'],
            y=weekly_pattern['min_cases'],
            mode='lines',
            name='Range',
            fill='tonexty',
            fillcolor='rgba(31, 119, 180, 0.2)',
            line=dict(width=0),
            hoverinfo='skip'
        )
    )
    
    # Add high-risk threshold line
    fig_seasonal.add_hline(
        y=high_risk_threshold,
        line_dash="dash",
        line_color="red",
        annotation_text="High Risk Threshold (75th percentile)",
        annotation_position="top right"
    )
    
    fig_seasonal.update_layout(
        title="<b>Weekly Seasonal Pattern (Average Across Years)</b>",
        xaxis_title="Week Number",
        yaxis_title="Average Cases",
        height=500,
        hovermode='x unified',
        showlegend=True
    )
    
    st.plotly_chart(fig_seasonal, use_container_width=True)
    
    # Identify and display high-risk weeks
    high_risk_weeks = weekly_pattern[weekly_pattern['avg_cases'] > high_risk_threshold]['week_number'].tolist()
    
    if high_risk_weeks:
        st.markdown(f"""
        <div class="warning-box">
            <strong>⚠️ High Transmission Season Identified</strong><br>
            Weeks with elevated cases (>75th percentile): <strong>{', '.join(map(str, high_risk_weeks))}</strong><br>
            <em>Recommendation: Intensify surveillance and prepare resources during these weeks</em>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # ========================================================================
    # YEAR-OVER-YEAR COMPARISON
    # ========================================================================
    
    st.subheader("📊 Year-over-Year Comparison")
    
    # Get yearly trends
    yearly_weekly = get_yearly_trends(df, selected_years, selected_regions)
    
    # Create year-over-year comparison chart
    fig_yoy = px.line(
        yearly_weekly,
        x='week_number',
        y='cases',
        color='data_year',
        title="<b>Weekly Cases by Year</b>",
        labels={'week_number': 'Week Number', 'cases': 'Total Cases', 'data_year': 'Year'},
        markers=True,
        color_discrete_sequence=px.colors.qualitative.Set2
    )
    
    fig_yoy.update_layout(
        height=500,
        hovermode='x unified',
        legend=dict(title="Year", orientation="h", y=1.1)
    )
    
    st.plotly_chart(fig_yoy, use_container_width=True)
    
    st.markdown("---")
    
    # ========================================================================
    # EPIDEMIC TIMELINE
    # ========================================================================
    
    st.subheader("🔴 Epidemic Weeks Timeline")
    
    # Identify epidemic weeks
    epidemic_weeks, threshold = identify_epidemic_weeks(df, selected_years, selected_regions)
    
    st.info(f"**Epidemic Threshold:** {threshold:.0f} cases per week (90th percentile)")
    
    # Create epidemic timeline heatmap
    if not epidemic_weeks.empty:
        # Pivot for heatmap
        heatmap_data = yearly_weekly.pivot(
            index='data_year',
            columns='week_number',
            values='cases'
        ).fillna(0)
        
        # Create heatmap
        fig_heatmap = px.imshow(
            heatmap_data,
            labels=dict(x="Week Number", y="Year", color="Cases"),
            x=heatmap_data.columns,
            y=heatmap_data.index,
            color_continuous_scale='YlOrRd',
            title="<b>Weekly Cases Heatmap (All Years)</b>",
            aspect='auto'
        )
        
        fig_heatmap.update_layout(
            height=400,
            xaxis_title="Week Number",
            yaxis_title="Year"
        )
        
        st.plotly_chart(fig_heatmap, use_container_width=True)
        
        # Display epidemic weeks table (limit to top 20 for size)
        st.subheader("📋 Top 20 Epidemic Weeks")
        
        epidemic_weeks_display = epidemic_weeks.nlargest(20, 'cases').copy()
        epidemic_weeks_display = epidemic_weeks_display.sort_values(['data_year', 'week_number'])
        
        st.dataframe(
            epidemic_weeks_display,
            use_container_width=True,
            column_config={
                'data_year': st.column_config.NumberColumn('Year', format='%d'),
                'week_number': st.column_config.NumberColumn('Week', format='%d'),
                'cases': st.column_config.NumberColumn('Cases', format='%d')
            },
            hide_index=True
        )
    else:
        st.info("No epidemic weeks identified with current threshold.")
    
    st.markdown("---")
    
    # ========================================================================
    # TEMPORAL STATISTICS
    # ========================================================================
    
    st.subheader("📊 Temporal Summary Statistics")
    
    stat_col1, stat_col2, stat_col3, stat_col4 = st.columns(4)
    
    with stat_col1:
        peak_week = weekly_pattern.loc[weekly_pattern['avg_cases'].idxmax(), 'week_number']
        st.metric(
            "Peak Week",
            f"Week {int(peak_week)}",
            help="Week with highest average cases"
        )
    
    with stat_col2:
        lowest_week = weekly_pattern.loc[weekly_pattern['avg_cases'].idxmin(), 'week_number']
        st.metric(
            "Lowest Week",
            f"Week {int(lowest_week)}",
            help="Week with lowest average cases"
        )
    
    with stat_col3:
        st.metric(
            "High-Risk Weeks",
            len(high_risk_weeks),
            help="Number of weeks in high transmission season"
        )
    
    with stat_col4:
        st.metric(
            "Epidemic Events",
            len(epidemic_weeks),
            help="Number of week-year combinations exceeding epidemic threshold"
        )
    
    # ========================================================================
    # INSIGHTS
    # ========================================================================
    
    st.markdown("---")
    st.subheader("💡 Key Temporal Insights")
    
    insight_col1, insight_col2 = st.columns(2)
    
    with insight_col1:
        st.info(f"""
        **🌊 Seasonal Pattern:**
        
        - **Peak transmission:** Week {int(peak_week)}
        - **Lowest transmission:** Week {int(lowest_week)}
        - **High-risk season:** {len(high_risk_weeks)} weeks identified
        - **Pattern:** {'Strong seasonality detected' if len(high_risk_weeks) > 5 else 'Moderate seasonality'}
        """)
    
    with insight_col2:
        # Compare years
        if len(selected_years) > 1:
            recent_year = max(selected_years)
            prev_year = sorted(selected_years)[-2] if len(selected_years) > 1 else recent_year - 1
            
            recent_total = yearly_weekly[yearly_weekly['data_year'] == recent_year]['cases'].sum()
            prev_total = yearly_weekly[yearly_weekly['data_year'] == prev_year]['cases'].sum()
            
            change = ((recent_total - prev_total) / prev_total * 100) if prev_total > 0 else 0
            
            st.warning(f"""
            **📈 Recent Trend:**
            
            - **{recent_year}:** {int(recent_total):,} total cases
            - **{prev_year}:** {int(prev_total):,} total cases
            - **Change:** {change:+.1f}%
            - **Status:** {'⚠️ Increasing trend' if change > 10 else '✅ Stable or decreasing'}
            """)
    
    # ========================================================================
    # FOOTER
    # ========================================================================
    
    st.markdown("---")
    st.caption(f"**Years Analyzed:** {', '.join(map(str, sorted(selected_years)))}")
    st.caption(f"**Regions:** {len(selected_regions)} | **Total Weeks Analyzed:** {len(weekly_pattern)}")


# ============================================================================
# RUN PAGE
# ============================================================================

if __name__ == "__main__":
    main()
