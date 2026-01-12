"""
================================================================================
PAGE 2: SPATIAL ANALYSIS (BILINGUAL - ENGLISH/FRANÇAIS)
================================================================================

This page provides geographic analysis of meningitis distribution:
- Interactive choropleth maps
- District rankings
- Spatial statistics
- Geographic hotspot identification

Target Audience: Vaccination planning, resource allocation, spatial epidemiology

BILINGUAL SUPPORT: Full English/French translation

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

# Language configuration
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from lang_config import get_text

# Try to import geopandas (optional - for advanced mapping)
try:
    import geopandas as gpd
    GEOPANDAS_AVAILABLE = True
except ImportError:
    GEOPANDAS_AVAILABLE = False

# ============================================================================
# PAGE CONFIGURATION
# ============================================================================

st.set_page_config(
    page_title="Spatial Analysis - Meningitis Dashboard",
    page_icon="🗺️",
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
        st.error(f"{get_text('error_loading_data', lang)}: {str(e)}")
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
        st.warning(f"⚠️ {get_text('failed_load_geojson', lang)}")
        return None
    except Exception as e:
        st.warning(f"⚠️ {get_text('error_loading_data', lang)}: {str(e)}")
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
    
    # Get language
    lang = st.session_state.get('language', 'en')
    
    # ========================================================================
    # HEADER
    # ========================================================================
    
    st.markdown(f'''
    <div class="dashboard-header">
        <h1>🗺️ {get_text('spatial_analysis', lang)} - {get_text('geographic_distribution', lang)}</h1>
    </div>
    ''', unsafe_allow_html=True)
    
    # ========================================================================
    # LOAD DATA
    # ========================================================================
    
    with st.spinner(f"{get_text('loading_data', lang)}"):
        df = load_main_dataset()
        gdf = load_geojson() if GEOPANDAS_AVAILABLE else None
    
    if df.empty:
        st.error(f"❌ {get_text('failed_load_data', lang)}")
        st.stop()
    
    # Show warning if GeoPandas not available
    if not GEOPANDAS_AVAILABLE:
        st.warning(f"⚠️ {get_text('spatial_not_available', lang)}")
    
    # ========================================================================
    # SIDEBAR FILTERS
    # ========================================================================
    
    st.sidebar.header(f"🔍 {get_text('filters', lang)}")
    st.sidebar.markdown("---")
    
    # Year selector (single year for spatial analysis)
    available_years = sorted(df['data_year'].unique(), reverse=True)
    selected_year = st.sidebar.selectbox(
        get_text('select_year', lang),
        options=available_years,
        index=0,  # Default to most recent year
        help=get_text('choose_single_year', lang)
    )
    
    # Region filter
    available_regions = sorted(df['region'].unique())
    selected_regions = st.sidebar.multiselect(
        get_text('select', lang) + ' ' + get_text('regions', lang),
        options=available_regions,
        default=available_regions,
        help=get_text('choose_multiple_years', lang)
    )
    
    if not selected_regions:
        st.warning(f"⚠️ {get_text('please_select', lang)}")
        st.stop()
    
    # Metric selector for choropleth map
    st.sidebar.markdown("---")
    st.sidebar.subheader(f"📊 {get_text('map', lang)} {get_text('display', lang) if lang == 'en' else 'Affichage'}")
    
    # Metric options with translations
    metric_options = {
        get_text('total_cases', lang): 'cases',
        f"{get_text('incidence_rate', lang)} ({get_text('per_100k', lang)})": 'incidence_rate',
        f"{get_text('case_fatality_rate', lang)} (%)": 'cfr',
        get_text('total_deaths', lang): 'deaths'
    }
    
    metric_choice = st.sidebar.radio(
        get_text('select', lang) + ' ' + (get_text('metric', lang) if lang == 'en' else 'Métrique'),
        options=list(metric_options.keys()),
        index=0,
        help=get_text('choose_analysis_mode', lang) if lang == 'en' else 'Choisir quelle métrique visualiser sur la carte'
    )
    
    st.sidebar.markdown("---")
    st.sidebar.info(f"""
    **{get_text('current_configuration', lang)}:**
    - {get_text('year', lang)}: {selected_year}
    - {get_text('regions', lang)}: {len(selected_regions)}
    - {get_text('metric', lang) if lang == 'en' else 'Métrique'}: {metric_choice}
    """)
    
    # ========================================================================
    # PREPARE SPATIAL DATA
    # ========================================================================
    
    with st.spinner(f"{get_text('loading', lang)}..."):
        district_data = prepare_spatial_data(df, selected_year, selected_regions)
    
    # ========================================================================
    # SUMMARY STATISTICS
    # ========================================================================
    
    st.subheader(f"📊 {get_text('summary_statistics', lang)}")
    
    col1, col2, col3, col4 = st.columns(4)
    
    total_cases = district_data['cases'].sum()
    total_deaths = district_data['deaths'].sum()
    avg_incidence = district_data['incidence_rate'].mean()
    districts_affected = (district_data['cases'] > 0).sum()
    
    with col1:
        st.metric(get_text('total_cases', lang), f"{total_cases:,.0f}")
    
    with col2:
        st.metric(get_text('total_deaths', lang), f"{total_deaths:,.0f}")
    
    with col3:
        st.metric(
            f"{get_text('incidence_rate', lang)} ({get_text('mean', lang)})",
            f"{avg_incidence:.2f}"
        )
    
    with col4:
        st.metric(
            get_text('affected_districts', lang),
            f"{districts_affected}/{len(district_data)}"
        )
    
    st.markdown("---")
    
    # ========================================================================
    # INTERACTIVE CHOROPLETH MAP
    # ========================================================================
    
    st.subheader(f"🗺️ {get_text('interactive_maps', lang)}")
    
    # Map metric to column name
    metric_col = metric_options[metric_choice]
    
    # Color scales based on metric
    color_scales = {
        'cases': 'YlOrRd',
        'deaths': 'Reds',
        'incidence_rate': 'YlOrRd',
        'cfr': 'RdYlGn_r'
    }
    color_scale = color_scales.get(metric_col, 'YlOrRd')
    
    # Metric labels for hover/legend
    metric_label = metric_choice
    
    if gdf is not None:
        # ====================================================================
        # OPTION 1: Interactive choropleth with actual geometries
        # ====================================================================
        
        # Merge district data with geometries
        gdf_plot = gdf.merge(district_data, on='district_clean', how='left')
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
            title=f'<b>{metric_choice} - {get_text("district", lang)} - {selected_year}</b>',
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
        
        st.warning(f"📊 {get_text('failed_load_geojson', lang)}")
        
        # Create bar chart
        fig_bar = px.bar(
            district_data.head(30),  # Top 30 districts
            x=metric_col,
            y='district_clean',
            orientation='h',
            color=metric_col,
            color_continuous_scale=color_scale,
            title=f'<b>{get_text("top_districts", lang)} (30) - {metric_choice} - {selected_year}</b>',
            labels={metric_col: metric_label, 'district_clean': get_text('district', lang)},
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
    
    st.subheader(f"📋 {get_text('district', lang)} {get_text('ranking', lang) if lang == 'en' else 'Classement'}")
    
    # Number of districts to show
    top_n = st.slider(
        f"{get_text('number_of_districts', lang) if lang == 'en' else 'Nombre de districts à afficher'}",
        min_value=10,
        max_value=50,
        value=20,
        step=5,
        help=get_text('select', lang) if lang == 'en' else 'Sélectionner combien de districts afficher'
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
        get_text('rank', lang) if lang == 'en' else 'Rang',
        get_text('region', lang),
        get_text('district', lang),
        get_text('total_cases', lang),
        get_text('total_deaths', lang),
        f"{get_text('incidence_rate', lang)} ({get_text('per_100k', lang)})",
        f"{get_text('case_fatality_rate', lang)} (%)",
        get_text('population', lang)
    ]
    
    # Display styled table
    st.dataframe(
        display_df.style
        .background_gradient(subset=[get_text('total_cases', lang)], cmap='YlOrRd')
        .background_gradient(subset=[f"{get_text('case_fatality_rate', lang)} (%)"], cmap='RdYlGn_r')
        .background_gradient(subset=[f"{get_text('incidence_rate', lang)} ({get_text('per_100k', lang)})"], cmap='YlOrRd')
        .format({
            get_text('total_cases', lang): '{:,.0f}',
            get_text('total_deaths', lang): '{:,.0f}',
            f"{get_text('incidence_rate', lang)} ({get_text('per_100k', lang)})": '{:.2f}',
            f"{get_text('case_fatality_rate', lang)} (%)": '{:.2f}',
            get_text('population', lang): '{:,.0f}'
        }),
        use_container_width=True,
        height=600
    )
    
    # Download button for table
    csv_data = display_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label=f"📥 {get_text('download', lang)} {get_text('district', lang)} {get_text('ranking', lang) if lang == 'en' else 'Classement'} (CSV)",
        data=csv_data,
        file_name=f"district_rankings_{selected_year}_{lang}.csv",
        mime="text/csv",
        help=get_text('download_filtered_data', lang)
    )
    
    st.markdown("---")
    
    # ========================================================================
    # REGIONAL COMPARISON
    # ========================================================================
    
    st.subheader(f"🌍 {get_text('regional_distribution', lang)}")
    
    # Aggregate by region
    regional_summary = district_data.groupby('region').agg({
        'cases': 'sum',
        'deaths': 'sum',
        'population': 'sum',
        'district_clean': 'count'
    }).reset_index()
    
    regional_summary.columns = [
        get_text('region', lang),
        get_text('cases', lang),
        get_text('deaths', lang),
        get_text('population', lang),
        get_text('districts', lang) if lang == 'en' else 'Districts'
    ]
    
    # Calculate rates
    regional_summary[get_text('incidence_rate', lang)] = (
        regional_summary[get_text('cases', lang)] / regional_summary[get_text('population', lang)] * 100000
    )
    regional_summary[f"{get_text('case_fatality_rate', lang)} (%)"] = (
        regional_summary[get_text('deaths', lang)] / regional_summary[get_text('cases', lang)] * 100
    ).fillna(0)
    
    # Sort by cases
    regional_summary = regional_summary.sort_values(get_text('cases', lang), ascending=False)
    
    # Display regional table
    st.dataframe(
        regional_summary.style
        .background_gradient(subset=[get_text('cases', lang)], cmap='YlOrRd')
        .background_gradient(subset=[f"{get_text('case_fatality_rate', lang)} (%)"], cmap='RdYlGn_r')
        .format({
            get_text('cases', lang): '{:,.0f}',
            get_text('deaths', lang): '{:,.0f}',
            get_text('population', lang): '{:,.0f}',
            get_text('incidence_rate', lang): '{:.2f}',
            f"{get_text('case_fatality_rate', lang)} (%)": '{:.2f}'
        }),
        use_container_width=True
    )
    
    # Regional bar chart
    fig_regional = px.bar(
        regional_summary,
        x=get_text('cases', lang),
        y=get_text('region', lang),
        orientation='h',
        color=get_text('cases', lang),
        color_continuous_scale='YlOrRd',
        title=f'<b>{get_text("cases", lang)} - {get_text("region", lang)} - {selected_year}</b>',
        text=get_text('cases', lang),
        hover_data=[get_text('deaths', lang), get_text('districts', lang) if lang == 'en' else 'Districts', get_text('incidence_rate', lang), f"{get_text('case_fatality_rate', lang)} (%)"]
    )
    
    fig_regional.update_traces(texttemplate='%{text:,}', textposition='outside')
    fig_regional.update_layout(height=400, showlegend=False)
    
    st.plotly_chart(fig_regional, use_container_width=True)
    
    # ========================================================================
    # SPATIAL INSIGHTS
    # ========================================================================
    
    st.markdown("---")
    st.subheader(f"💡 {get_text('spatial_analysis', lang)} {get_text('insights', lang) if lang == 'en' else 'Aperçus'}")
    
    insight_col1, insight_col2 = st.columns(2)
    
    with insight_col1:
        # Identify highest burden district
        top_district = district_data.iloc[0]
        st.info(f"""
        **🔴 {get_text('highest_burden', lang) if lang == 'en' else 'District le Plus Affecté'}:**
        
        - **{get_text('district', lang)}:** {top_district['district_clean']}
        - **{get_text('region', lang)}:** {top_district['region']}
        - **{get_text('cases', lang)}:** {int(top_district['cases']):,}
        - **{get_text('incidence_rate', lang)}:** {top_district['incidence_rate']:.2f} {get_text('per_100k', lang)}
        - **{get_text('case_fatality_rate', lang)}:** {top_district['cfr']:.2f}%
        """)
    
    with insight_col2:
        # Identify highest CFR
        high_cfr_districts = district_data[district_data['cases'] >= 10].nlargest(1, 'cfr')
        if not high_cfr_districts.empty:
            high_cfr = high_cfr_districts.iloc[0]
            st.warning(f"""
            **⚠️ {get_text('case_fatality_rate', lang)} {get_text('highest', lang) if lang == 'en' else 'le Plus Élevé'} ({get_text('districts', lang) if lang == 'en' else 'districts'} ≥10 {get_text('cases', lang)}):**
            
            - **{get_text('district', lang)}:** {high_cfr['district_clean']}
            - **{get_text('region', lang)}:** {high_cfr['region']}
            - **{get_text('case_fatality_rate', lang)}:** {high_cfr['cfr']:.2f}%
            - **{get_text('cases', lang)}:** {int(high_cfr['cases']):,}
            - **{get_text('deaths', lang)}:** {int(high_cfr['deaths']):,}
            
            *{get_text('action_investigate', lang)}*
            """)
    
    # ========================================================================
    # FOOTER
    # ========================================================================
    
    st.markdown("---")
    st.caption(f"**{get_text('year', lang)}:** {selected_year} | **{get_text('regions', lang)}:** {len(selected_regions)}")
    st.caption(f"**{get_text('total', lang)} {get_text('districts', lang)}:** {len(district_data)} | **{get_text('districts', lang)} {get_text('cases', lang) if lang == 'en' else 'avec cas'}:** {(district_data['cases'] > 0).sum()}")


# ============================================================================
# RUN PAGE
# ============================================================================

if __name__ == "__main__":
    main()
