"""
================================================================================
PAGE 2: SPATIAL ANALYSIS
================================================================================

This page provides geographic analysis of meningitis distribution:
- Interactive choropleth maps
- District rankings
- Spatial statistics
- Geographic hotspot identification

Target Audience: Vaccination planning, resource allocation, spatial epidemiology

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
import warnings
warnings.filterwarnings('ignore')

# Try to import geopandas (optional - for advanced mapping)
try:
    import geopandas as gpd
    GEOPANDAS_AVAILABLE = True
except ImportError:
    GEOPANDAS_AVAILABLE = False
    st.warning(" GeoPandas not available. Some advanced spatial features may be limited.")

# ============================================================================
# PAGE CONFIGURATION
# ============================================================================

st.set_page_config(
    page_title="Spatial Analysis - Meningitis Dashboard",
    page_icon="🗺️",
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
</style>
""", unsafe_allow_html=True)

# ============================================================================
# CACHED DATA LOADING
# ============================================================================

@st.cache_data(ttl=3600)
def load_main_dataset():
    """Load primary dataset"""
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
        st.error(f"Error loading data: {str(e)}")
        return pd.DataFrame()


@st.cache_data(ttl=3600)
def load_geojson():
    """
    Load GeoJSON file with district geometries
    
    This file contains the geographic boundaries for mapping
    """
    if not GEOPANDAS_AVAILABLE:
        return None
    
    try:
        gdf = gpd.read_file('Dashboard/cleaned_data/cameroon_districts_matched.geojson')
        return gdf
    except FileNotFoundError:
        st.warning("⚠️ GeoJSON file not found. Maps will use simplified representation.")
        return None
    except Exception as e:
        st.warning(f"⚠️ Could not load GeoJSON: {str(e)}")
        return None


@st.cache_data
def prepare_spatial_data(df, selected_year, selected_regions):
    """
    Prepare district-level spatial data for mapping
    
    Args:
        df: Main dataframe
        selected_year: Single year to display
        selected_regions: List of regions to include
        
    Returns:
        DataFrame with district-level aggregates
    """
    # Filter for selected year and regions
    df_filtered = df[
        (df['data_year'] == selected_year) &
        (df['region'].isin(selected_regions))
    ].copy()
    
    # Aggregate by district
    district_summary = df_filtered.groupby(['region', 'district_clean']).agg({
        'cases': 'sum',
        'deaths': 'sum',
        'population': 'first'
    }).reset_index()
    
    # Calculate metrics
    district_summary['incidence_rate'] = (
        district_summary['cases'] / district_summary['population'] * 100000
    ).fillna(0)
    
    district_summary['cfr'] = (
        district_summary['deaths'] / district_summary['cases'].replace(0, np.nan) * 100
    ).fillna(0)
    
    # Sort by cases
    district_summary = district_summary.sort_values('cases', ascending=False)
    
    return district_summary


# ============================================================================
# MAIN PAGE FUNCTION
# ============================================================================

def main():
    """Main function for Spatial Analysis page"""
    
    # ========================================================================
    # HEADER
    # ========================================================================
    
    st.markdown('''
    <div class="dashboard-header">
        <h1>🗺️ Spatial Analysis - Geographic Distribution</h1>
    </div>
    ''', unsafe_allow_html=True)
    
    # ========================================================================
    # LOAD DATA
    # ========================================================================
    
    with st.spinner("Loading spatial data..."):
        df = load_main_dataset()
        gdf = load_geojson() if GEOPANDAS_AVAILABLE else None
    
    if df.empty:
        st.error("❌ Failed to load data.")
        st.stop()
    
    # ========================================================================
    # SIDEBAR FILTERS
    # ========================================================================
    
    st.sidebar.header("🔍 Filters")
    st.sidebar.markdown("---")
    
    # Year selector (single year for spatial analysis)
    available_years = sorted(df['data_year'].unique(), reverse=True)
    selected_year = st.sidebar.selectbox(
        "Select Year",
        options=available_years,
        index=0,  # Default to most recent year
        help="Choose a single year to visualize"
    )
    
    # Region filter
    available_regions = sorted(df['region'].unique())
    selected_regions = st.sidebar.multiselect(
        "Select Regions",
        options=available_regions,
        default=available_regions,
        help="Choose which regions to display on the map"
    )
    
    if not selected_regions:
        st.warning("⚠️ Please select at least one region.")
        st.stop()
    
    # Metric selector for choropleth map
    st.sidebar.markdown("---")
    st.sidebar.subheader("📊 Map Display")
    
    metric_choice = st.sidebar.radio(
        "Select Metric to Display",
        options=[
            "Total Cases",
            "Incidence Rate (per 100,000)",
            "Case Fatality Rate (%)",
            "Total Deaths"
        ],
        index=0,
        help="Choose which metric to visualize on the map"
    )
    
    st.sidebar.markdown("---")
    st.sidebar.info(f"""
    **Current Selection:**
    - Year: {selected_year}
    - Regions: {len(selected_regions)}
    - Metric: {metric_choice}
    """)
    
    # ========================================================================
    # PREPARE SPATIAL DATA
    # ========================================================================
    
    with st.spinner("Preparing spatial data..."):
        district_data = prepare_spatial_data(df, selected_year, selected_regions)
    
    # ========================================================================
    # SUMMARY STATISTICS
    # ========================================================================
    
    st.subheader("📊 Summary Statistics")
    
    sum_col1, sum_col2, sum_col3, sum_col4 = st.columns(4)
    
    with sum_col1:
        st.metric(
            "Total Cases",
            f"{district_data['cases'].sum():,.0f}",
            help=f"Total cases in {selected_year}"
        )
    
    with sum_col2:
        st.metric(
            "Mean Incidence Rate",
            f"{district_data['incidence_rate'].mean():.2f}",
            help="Average incidence rate per 100,000 population"
        )
    
    with sum_col3:
        st.metric(
            "Districts Affected",
            f"{(district_data['cases'] > 0).sum()}",
            help="Number of districts with at least 1 case"
        )
    
    with sum_col4:
        st.metric(
            "Overall CFR",
            f"{(district_data['deaths'].sum() / district_data['cases'].sum() * 100):.2f}%",
            help="Overall case fatality rate"
        )
    
    st.markdown("---")
    
    # ========================================================================
    # INTERACTIVE MAP
    # ========================================================================
    
    st.subheader(f"🗺️ Interactive Map: {metric_choice} ({selected_year})")
    
    # Determine which column to map
    metric_mapping = {
        "Total Cases": ('cases', 'YlOrRd', 'Total Cases'),
        "Incidence Rate (per 100,000)": ('incidence_rate', 'RdYlGn_r', 'Incidence Rate'),
        "Case Fatality Rate (%)": ('cfr', 'YlOrBr', 'CFR (%)'),
        "Total Deaths": ('deaths', 'Reds', 'Total Deaths')
    }
    
    metric_col, color_scale, metric_label = metric_mapping[metric_choice]
    
    # Create map based on data availability
    if gdf is not None and 'district_clean' in gdf.columns:
        # ====================================================================
        # OPTION 1: Full choropleth map with GeoJSON
        # ====================================================================
        
        st.info("📍 Displaying geographic choropleth map")
        
        # Merge district data with geometry
        gdf_plot = gdf.merge(
            district_data,
            on='district_clean',
            how='left'
        )
        
        # Fill NaN values with 0
        gdf_plot[metric_col] = gdf_plot[metric_col].fillna(0)
        
        # Create choropleth map
        fig_map = px.choropleth_mapbox(
            gdf_plot,
            geojson=gdf_plot.geometry,
            locations=gdf_plot.index,
            color=metric_col,
            hover_name='district_clean',
            hover_data={
                'cases': ':,.0f',
                'deaths': ':,.0f',
                'incidence_rate': ':.2f',
                'cfr': ':.2f',
                'region': True
            },
            color_continuous_scale=color_scale,
            mapbox_style='carto-positron',
            center={'lat': 6.5, 'lon': 12.5},  # Cameroon center
            zoom=5.5,
            opacity=0.7,
            title=f'<b>{metric_choice} by District - {selected_year}</b>',
            labels={metric_col: metric_label}
        )
        
        fig_map.update_layout(
            height=700,
            margin=dict(l=0, r=0, t=50, b=0),
            font=dict(size=12)
        )
        
        st.plotly_chart(fig_map, use_container_width=True)
    
    else:
        # ====================================================================
        # OPTION 2: Bar chart representation (fallback if no GeoJSON)
        # ====================================================================
        
        st.warning("📊 Geographic boundaries not available. Displaying bar chart instead.")
        
        # Create bar chart
        fig_bar = px.bar(
            district_data.head(30),  # Top 30 districts
            x=metric_col,
            y='district_clean',
            orientation='h',
            color=metric_col,
            color_continuous_scale=color_scale,
            title=f'<b>Top 30 Districts by {metric_choice} - {selected_year}</b>',
            labels={metric_col: metric_label, 'district_clean': 'District'},
            hover_data=['region', 'cases', 'deaths']
        )
        
        fig_bar.update_layout(
            height=800,
            showlegend=False,
            yaxis={'categoryorder': 'total ascending'}
        )
        
        st.plotly_chart(fig_bar, use_container_width=True)
    
    st.markdown("---")
    
    # ========================================================================
    # DISTRICT RANKINGS TABLE
    # ========================================================================
    
    st.subheader("📋 District Rankings")
    
    # Number of districts to show
    top_n = st.slider(
        "Number of districts to display",
        min_value=10,
        max_value=50,
        value=20,
        step=5,
        help="Select how many top districts to show"
    )
    
    # Prepare display dataframe
    display_df = district_data.head(top_n).copy()
    
    # Add rank column
    display_df.insert(0, 'Rank', range(1, len(display_df) + 1))
    
    # Select columns for display
    display_columns = [
        'Rank', 'region', 'district_clean', 'cases', 'deaths',
        'incidence_rate', 'cfr', 'population'
    ]
    
    display_df = display_df[display_columns].copy()
    display_df.columns = [
        'Rank', 'Region', 'District', 'Total Cases', 'Total Deaths',
        'Incidence Rate (per 100k)', 'CFR (%)', 'Population'
    ]
    
    # Display styled table
    st.dataframe(
        display_df.style
        .background_gradient(subset=['Total Cases'], cmap='YlOrRd')
        .background_gradient(subset=['CFR (%)'], cmap='RdYlGn_r')
        .background_gradient(subset=['Incidence Rate (per 100k)'], cmap='YlOrRd')
        .format({
            'Total Cases': '{:,.0f}',
            'Total Deaths': '{:,.0f}',
            'Incidence Rate (per 100k)': '{:.2f}',
            'CFR (%)': '{:.2f}',
            'Population': '{:,.0f}'
        }),
        use_container_width=True,
        height=600
    )
    
    # Download button for table
    csv_data = display_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Download District Rankings (CSV)",
        data=csv_data,
        file_name=f"district_rankings_{selected_year}.csv",
        mime="text/csv",
        help="Download the district rankings table"
    )
    
    st.markdown("---")
    
    # ========================================================================
    # REGIONAL COMPARISON
    # ========================================================================
    
    st.subheader("🌍 Regional Comparison")
    
    # Aggregate by region
    regional_summary = district_data.groupby('region').agg({
        'cases': 'sum',
        'deaths': 'sum',
        'population': 'sum',
        'district_clean': 'count'
    }).reset_index()
    
    regional_summary.columns = ['Region', 'Cases', 'Deaths', 'Population', 'Districts']
    
    # Calculate rates
    regional_summary['Incidence Rate'] = (
        regional_summary['Cases'] / regional_summary['Population'] * 100000
    )
    regional_summary['CFR (%)'] = (
        regional_summary['Deaths'] / regional_summary['Cases'] * 100
    ).fillna(0)
    
    # Sort by cases
    regional_summary = regional_summary.sort_values('Cases', ascending=False)
    
    # Display regional table
    st.dataframe(
        regional_summary.style
        .background_gradient(subset=['Cases'], cmap='YlOrRd')
        .background_gradient(subset=['CFR (%)'], cmap='RdYlGn_r')
        .format({
            'Cases': '{:,.0f}',
            'Deaths': '{:,.0f}',
            'Population': '{:,.0f}',
            'Incidence Rate': '{:.2f}',
            'CFR (%)': '{:.2f}'
        }),
        use_container_width=True
    )
    
    # Regional bar chart
    fig_regional = px.bar(
        regional_summary,
        x='Cases',
        y='Region',
        orientation='h',
        color='Cases',
        color_continuous_scale='YlOrRd',
        title=f'<b>Cases by Region - {selected_year}</b>',
        text='Cases',
        hover_data=['Deaths', 'Districts', 'Incidence Rate', 'CFR (%)']
    )
    
    fig_regional.update_traces(texttemplate='%{text:,}', textposition='outside')
    fig_regional.update_layout(height=400, showlegend=False)
    
    st.plotly_chart(fig_regional, use_container_width=True)
    
    # ========================================================================
    # SPATIAL INSIGHTS
    # ========================================================================
    
    st.markdown("---")
    st.subheader("💡 Spatial Insights")
    
    insight_col1, insight_col2 = st.columns(2)
    
    with insight_col1:
        # Identify highest burden district
        top_district = district_data.iloc[0]
        st.info(f"""
        **🔴 Highest Burden District:**
        
        - **District:** {top_district['district_clean']}
        - **Region:** {top_district['region']}
        - **Cases:** {int(top_district['cases']):,}
        - **Incidence Rate:** {top_district['incidence_rate']:.2f} per 100,000
        - **CFR:** {top_district['cfr']:.2f}%
        """)
    
    with insight_col2:
        # Identify highest CFR
        high_cfr_districts = district_data[district_data['cases'] >= 10].nlargest(1, 'cfr')
        if not high_cfr_districts.empty:
            high_cfr = high_cfr_districts.iloc[0]
            st.warning(f"""
            **⚠️ Highest CFR (districts with ≥10 cases):**
            
            - **District:** {high_cfr['district_clean']}
            - **Region:** {high_cfr['region']}
            - **CFR:** {high_cfr['cfr']:.2f}%
            - **Cases:** {int(high_cfr['cases']):,}
            - **Deaths:** {int(high_cfr['deaths']):,}
            
            *Action: Review healthcare access and quality*
            """)
    
    # ========================================================================
    # FOOTER
    # ========================================================================
    
    st.markdown("---")
    st.caption(f"**Data Year:** {selected_year} | **Regions Displayed:** {len(selected_regions)}")
    st.caption(f"**Total Districts:** {len(district_data)} | **Districts with Cases:** {(district_data['cases'] > 0).sum()}")


# ============================================================================
# RUN PAGE
# ============================================================================

if __name__ == "__main__":
    main()
