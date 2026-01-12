"""
================================================================================
PAGE: LISA CLUSTER ANALYSIS (BILINGUAL - ENGLISH/FRANÇAIS)
================================================================================

This page provides Local Indicators of Spatial Association (LISA) analysis:
- Multi-year LISA cluster maps
- Interactive year selection
- Hotspot identification
- Temporal evolution of spatial clusters
- Annotation and notes capability

BILINGUAL SUPPORT: Full English/French translation
FIXED: Caching issues with GeoDataFrame (underscore prefixes)

Target Audience: Epidemiologists, public health officials, intervention planning

================================================================================
"""

# ============================================================================
# IMPORTS
# ============================================================================

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import sys
import os
import warnings
warnings.filterwarnings('ignore')

# Add parent directory to path to import lang_config
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from lang_config import get_text

# Spatial analysis libraries
try:
    import geopandas as gpd
    from libpysal.weights import Queen
    from esda.moran import Moran_Local
    SPATIAL_AVAILABLE = True
except ImportError:
    SPATIAL_AVAILABLE = False

# ============================================================================
# PAGE CONFIGURATION
# ============================================================================

st.set_page_config(
    page_title="LISA Analysis - Meningitis Dashboard",
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
        background: linear-gradient(135deg, #d62728 0%, #8B0000 100%);
        color: white;
        padding: 2rem;
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    .dashboard-header h1 { color: white; margin: 0; font-size: 2rem; }
    [data-testid="stMetricValue"] { color: #d62728; font-weight: 600; }
    .note-box {
        background-color: #fff3cd;
        border-left: 4px solid #ffc107;
        padding: 1rem;
        border-radius: 5px;
        margin: 1rem 0;
    }
    .hotspot-box {
        background-color: #f8d7da;
        border-left: 4px solid #d62728;
        padding: 1rem;
        border-radius: 5px;
        margin: 1rem 0;
    }
    .coldspot-box {
        background-color: #d1ecf1;
        border-left: 4px solid #1f77b4;
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
        df = pd.read_csv('cleaned_data/ml_final_100pct_geometry.csv')
        df['data_year'] = df['data_year'].astype('int16')
        return df
    except:
        try:
            df = pd.read_csv('Dashboard/cleaned_data/ml_final_100pct_geometry.csv')
            df['data_year'] = df['data_year'].astype('int16')
            return df
        except Exception as e:
            st.error(f"{get_text('error_loading_data', lang)}: {str(e)}")
            return pd.DataFrame()

@st.cache_data(ttl=3600)
def load_geojson():
    """Load GeoJSON with district geometries"""
    if not SPATIAL_AVAILABLE:
        return None
    
    try:
        gdf = gpd.read_file('cleaned_data/cameroon_districts_matched.geojson')
        
        # Ensure district_clean column exists
        if 'district_clean' not in gdf.columns:
            if 'district' in gdf.columns:
                gdf['district_clean'] = gdf['district']
            elif 'name' in gdf.columns:
                gdf['district_clean'] = gdf['name'].str.replace('District ', '', regex=False).str.strip()
        
        return gdf
    except:
        try:
            gdf = gpd.read_file('Dashboard/cleaned_data/cameroon_districts_matched.geojson')
            
            if 'district_clean' not in gdf.columns:
                if 'district' in gdf.columns:
                    gdf['district_clean'] = gdf['district']
                elif 'name' in gdf.columns:
                    gdf['district_clean'] = gdf['name'].str.replace('District ', '', regex=False).str.strip()
            
            return gdf
        except Exception as e:
            st.warning(f"⚠️ {get_text('error_loading_data', lang)}: {str(e)}")
            return None

@st.cache_data
def create_spatial_weights(_gdf):
    """
    Create spatial weights matrix
    
    Note: _gdf has underscore prefix to prevent Streamlit from trying to hash
    the GeoDataFrame (which causes UnhashableParamError)
    """
    if _gdf is None:
        return None
    
    try:
        gdf_indexed = _gdf.set_index('district_clean')
        w = Queen.from_dataframe(gdf_indexed)
        return w
    except Exception as e:
        st.warning(f"⚠️ {get_text('error_loading_data', lang)}: {str(e)}")
        return None

@st.cache_data
def compute_lisa_for_year(_gdf, _w, df, year):
    """
    Compute LISA for a specific year
    
    Args:
        _gdf: GeoDataFrame with geometries (underscore = unhashable)
        _w: Spatial weights matrix (underscore = unhashable)
        df: Main surveillance dataframe
        year: Year to analyze
        
    Returns:
        GeoDataFrame with LISA classifications
        
    Note: Parameters prefixed with _ are not hashed by Streamlit cache
    """
    # Aggregate data for year
    year_data = df[df['data_year'] == year].groupby('district_clean').agg({
        'cases': 'sum',
        'deaths': 'sum',
        'population': 'first'
    }).reset_index()
    
    year_data['incidence_rate'] = (
        year_data['cases'] / year_data['population'] * 100000
    )
    
    # Merge with geometry
    gdf_year = _gdf.merge(year_data, on='district_clean', how='left')
    gdf_year['cases'] = gdf_year['cases'].fillna(0)
    gdf_year['incidence_rate'] = gdf_year['incidence_rate'].fillna(0)
    
    # Set index for LISA
    gdf_year_indexed = gdf_year.set_index('district_clean')
    
    # Check if there are cases
    if gdf_year['cases'].sum() == 0:
        return None
    
    # Compute LISA
    y = gdf_year_indexed['cases'].fillna(0).values
    
    try:
        lisa = Moran_Local(y, _w)
        
        # Classify clusters
        gdf_year_indexed['lisa_quadrant'] = lisa.q
        gdf_year_indexed['lisa_pvalue'] = lisa.p_sim
        gdf_year_indexed['lisa_cluster'] = get_text('not_significant', st.session_state.get('language', 'en'))
        
        # Significant clusters (p < 0.05)
        sig_mask = lisa.p_sim < 0.05
        
        # Get translated labels
        lang_current = st.session_state.get('language', 'en')
        quadrant_labels = {
            1: get_text('high_high', lang_current),
            2: get_text('low_high', lang_current),
            3: get_text('low_low', lang_current),
            4: get_text('high_low', lang_current)
        }
        
        for q, label in quadrant_labels.items():
            mask = (lisa.q == q) & sig_mask
            gdf_year_indexed.loc[mask, 'lisa_cluster'] = label
        
        return gdf_year_indexed.reset_index()
        
    except Exception as e:
        st.warning(f"{get_text('error_loading_data', lang)} {year}: {str(e)}")
        return None

# ============================================================================
# MAIN PAGE FUNCTION
# ============================================================================

def main():
    """Main function for LISA Analysis page"""
    
    # Get language
    lang = st.session_state.get('language', 'en')
    
    # ========================================================================
    # HEADER
    # ========================================================================
    
    st.markdown(f'''
    <div class="dashboard-header">
        <h1>🗺️ {get_text('lisa_title', lang)}</h1>
    </div>
    ''', unsafe_allow_html=True)
    
    st.markdown(f"""
    **{get_text('lisa_description', lang)}** {get_text('lisa_helps_identify', lang)}
    - 🔴 **{get_text('lisa_hotspots_desc', lang)}**
    - 🔵 **{get_text('lisa_coldspots_desc', lang)}**
    - 🟠 **{get_text('lisa_outliers_desc', lang)}**
    """)
    
    # ========================================================================
    # CHECK AVAILABILITY
    # ========================================================================
    
    if not SPATIAL_AVAILABLE:
        st.error(f"""
        ❌ **{get_text('spatial_not_available', lang)}**
        
        {get_text('lisa_requires', lang)}
        - geopandas
        - libpysal
        - esda
        
        {get_text('install_with', lang)} `pip install geopandas libpysal esda`
        """)
        st.stop()
    
    # ========================================================================
    # LOAD DATA
    # ========================================================================
    
    with st.spinner(f"{get_text('loading_data', lang)}"):
        df = load_main_dataset()
        gdf = load_geojson()
    
    if df.empty:
        st.error(f"❌ {get_text('failed_load_data', lang)}")
        st.stop()
    
    if gdf is None:
        st.error(f"❌ {get_text('failed_load_geojson', lang)}")
        st.stop()
    
    # Create spatial weights
    with st.spinner(f"{get_text('loading', lang)}..."):
        w = create_spatial_weights(gdf)
    
    if w is None:
        st.error(f"❌ {get_text('failed_spatial_weights', lang)}")
        st.stop()
    
    st.success(f"✓ {get_text('loaded_districts', lang)} {len(gdf)} {get_text('districts_with', lang)} {w.mean_neighbors:.1f} {get_text('average_neighbors_value', lang)}")
    
    # ========================================================================
    # SIDEBAR CONFIGURATION
    # ========================================================================
    
    st.sidebar.header(f"🔍 {get_text('lisa_configuration', lang)}")
    st.sidebar.markdown("---")
    
    # Analysis mode
    mode_options = [
        get_text('single_year', lang),
        get_text('multi_year_comparison', lang),
        get_text('all_years_grid', lang)
    ]
    
    analysis_mode = st.sidebar.radio(
        get_text('analysis_mode', lang),
        options=mode_options,
        help=get_text('choose_analysis_mode', lang)
    )
    
    st.sidebar.markdown("---")
    
    available_years = sorted(df['data_year'].unique())
    
    # Map mode back to English for logic
    mode_map = {
        mode_options[0]: "Single Year",
        mode_options[1]: "Multi-Year Comparison",
        mode_options[2]: "All Years Grid"
    }
    analysis_mode_en = mode_map[analysis_mode]
    
    if analysis_mode_en == "Single Year":
        selected_years = [st.sidebar.selectbox(
            get_text('select_year', lang),
            options=available_years,
            index=len(available_years) - 1,
            help=get_text('choose_single_year', lang)
        )]
        
    elif analysis_mode_en == "Multi-Year Comparison":
        selected_years = st.sidebar.multiselect(
            get_text('select_years_to_compare', lang),
            options=available_years,
            default=available_years[-3:],
            help=get_text('choose_multiple_years', lang)
        )
        
        if len(selected_years) == 0:
            st.warning(f"⚠️ {get_text('please_select_year', lang)}")
            st.stop()
            
    else:  # All Years Grid
        selected_years = available_years
    
    # Significance level
    st.sidebar.markdown("---")
    significance_level = st.sidebar.slider(
        get_text('significance_level', lang),
        min_value=0.01,
        max_value=0.10,
        value=0.05,
        step=0.01,
        help=get_text('pvalue_threshold', lang)
    )
    
    st.sidebar.markdown("---")
    st.sidebar.info(f"""
    **{get_text('current_configuration', lang)}:**
    - {get_text('mode', lang)}: {analysis_mode}
    - {get_text('years', lang)}: {len(selected_years)}
    - α = {significance_level}
    - {get_text('health_districts', lang)}: {len(gdf)}
    - {get_text('avg_neighbors', lang)}: {w.mean_neighbors:.1f}
    """)
    
    # ========================================================================
    # COMPUTE LISA FOR SELECTED YEARS
    # ========================================================================
    
    st.markdown("---")
    st.subheader(f"📊 {get_text('computing_lisa', lang)}")
    
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    lisa_results = {}
    
    for idx, year in enumerate(selected_years):
        status_text.text(f"{get_text('processing_year', lang)} {year}...")
        progress_bar.progress((idx + 1) / len(selected_years))
        
        result = compute_lisa_for_year(gdf, w, df, year)
        
        if result is not None:
            lisa_results[year] = result
    
    progress_bar.empty()
    status_text.empty()
    
    if len(lisa_results) == 0:
        st.error(f"❌ {get_text('no_lisa_results', lang)}")
        st.stop()
    
    st.success(f"✓ {get_text('successfully_computed', lang)} {len(lisa_results)} {get_text('year_s', lang)}")
    
    # ========================================================================
    # VISUALIZATION
    # ========================================================================
    
    st.markdown("---")
    st.subheader(f"🗺️ {get_text('lisa_cluster_maps', lang)}")
    
    # Color scheme (same across languages)
    COLOR_MAP = {
        get_text('high_high', lang): '#d62728',
        get_text('low_low', lang): '#1f77b4',
        get_text('high_low', lang): '#ff9896',
        get_text('low_high', lang): '#aec7e8',
        get_text('not_significant', lang): '#d3d3d3'
    }
    
    if analysis_mode_en == "Single Year":
        # ====================================================================
        # SINGLE YEAR: Large detailed map
        # ====================================================================
        
        year = selected_years[0]
        gdf_lisa = lisa_results[year]
        
        # Create interactive map
        fig = px.choropleth_mapbox(
            gdf_lisa,
            geojson=gdf_lisa.geometry,
            locations=gdf_lisa.index,
            color='lisa_cluster',
            hover_name='district_clean',
            hover_data={
                'cases': ':,.0f',
                'deaths': ':,.0f',
                'incidence_rate': ':.2f',
                'lisa_pvalue': ':.4f',
                'lisa_cluster': True
            },
            color_discrete_map=COLOR_MAP,
            mapbox_style='carto-positron',
            center={'lat': 6.5, 'lon': 12.5},
            zoom=5.5,
            opacity=0.8,
            title=f'<b>{get_text("lisa_clusters", lang)} - {year}</b>',
            category_orders={'lisa_cluster': list(COLOR_MAP.keys())}
        )
        
        fig.update_layout(
            height=700,
            margin=dict(l=0, r=0, t=50, b=0),
            font=dict(size=12)
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Statistics
        col1, col2, col3, col4 = st.columns(4)
        
        cluster_counts = gdf_lisa['lisa_cluster'].value_counts()
        
        with col1:
            st.metric(
                f"🔴 {get_text('hotspots_hh', lang)}",
                cluster_counts.get(get_text('high_high', lang), 0),
                help=get_text('high_cases_high_neighbors', lang)
            )
        
        with col2:
            st.metric(
                f"🔵 {get_text('coldspots_ll', lang)}",
                cluster_counts.get(get_text('low_low', lang), 0),
                help=get_text('low_cases_low_neighbors', lang)
            )
        
        with col3:
            st.metric(
                f"🟠 {get_text('high_low_outliers', lang)}",
                cluster_counts.get(get_text('high_low', lang), 0),
                help=get_text('high_cases_low_neighbors', lang)
            )
        
        with col4:
            st.metric(
                f"🟦 {get_text('low_high_outliers', lang)}",
                cluster_counts.get(get_text('low_high', lang), 0),
                help=get_text('low_cases_high_neighbors', lang)
            )
        
        # Hotspot details
        st.markdown("---")
        st.subheader(f"🔍 {get_text('detailed_analysis', lang)}")
        
        tab_labels = [
            f"🔴 {get_text('hotspots', lang)}",
            f"🔵 {get_text('coldspots_ll', lang).split(' (')[0]}",
            f"📊 {get_text('all_clusters', lang)}"
        ]
        
        tab1, tab2, tab3 = st.tabs(tab_labels)
        
        with tab1:
            hotspots = gdf_lisa[gdf_lisa['lisa_cluster'] == get_text('high_high', lang)].sort_values('cases', ascending=False)
            
            if len(hotspots) > 0:
                st.markdown('<div class="hotspot-box">', unsafe_allow_html=True)
                st.markdown(f"**{len(hotspots)} {get_text('hotspot_districts_identified', lang)}**")
                st.markdown("</div>", unsafe_allow_html=True)
                
                display_df = hotspots[['district_clean', 'cases', 'deaths', 'incidence_rate', 'lisa_pvalue']].copy()
                display_df.columns = [
                    get_text('district', lang),
                    get_text('total_cases', lang),
                    get_text('total_deaths', lang),
                    get_text('incidence_rate', lang),
                    'p-value'
                ]
                
                st.dataframe(
                    display_df.style
                    .background_gradient(subset=[get_text('total_cases', lang)], cmap='Reds')
                    .format({
                        get_text('total_cases', lang): '{:,.0f}',
                        get_text('total_deaths', lang): '{:,.0f}',
                        get_text('incidence_rate', lang): '{:.2f}',
                        'p-value': '{:.4f}'
                    }),
                    use_container_width=True
                )
            else:
                st.info(get_text('no_hotspots', lang))
        
        with tab2:
            coldspots = gdf_lisa[gdf_lisa['lisa_cluster'] == get_text('low_low', lang)].sort_values('cases')
            
            if len(coldspots) > 0:
                st.markdown('<div class="coldspot-box">', unsafe_allow_html=True)
                st.markdown(f"**{len(coldspots)} {get_text('coldspot_districts_identified', lang)}**")
                st.markdown("</div>", unsafe_allow_html=True)
                
                display_df = coldspots[['district_clean', 'cases', 'incidence_rate', 'lisa_pvalue']].copy()
                display_df.columns = [
                    get_text('district', lang),
                    get_text('total_cases', lang),
                    get_text('incidence_rate', lang),
                    'p-value'
                ]
                
                st.dataframe(
                    display_df.style
                    .background_gradient(subset=[get_text('incidence_rate', lang)], cmap='Blues_r')
                    .format({
                        get_text('total_cases', lang): '{:,.0f}',
                        get_text('incidence_rate', lang): '{:.2f}',
                        'p-value': '{:.4f}'
                    }),
                    use_container_width=True
                )
            else:
                st.info(get_text('no_coldspots', lang))
        
        with tab3:
            cluster_summary = gdf_lisa.groupby('lisa_cluster').agg({
                'cases': ['count', 'sum', 'mean'],
                'incidence_rate': 'mean'
            }).round(2)
            
            st.dataframe(cluster_summary, use_container_width=True)
    
    else:
        # ====================================================================
        # MULTI-YEAR OR GRID: Multiple maps
        # ====================================================================
        
        n_years = len(lisa_results)
        n_cols = min(3, n_years)
        n_rows = int(np.ceil(n_years / n_cols))
        
        # Create matplotlib figure
        fig, axes = plt.subplots(
            n_rows, n_cols,
            figsize=(18, 6 * n_rows),
            constrained_layout=True
        )
        
        if n_years == 1:
            axes = np.array([axes])
        elif n_rows == 1:
            axes = axes.reshape(1, -1)
        
        axes_flat = axes.flatten()
        
        # Get English labels for consistency in plotting
        lang_en = 'en'
        color_map_en = {
            get_text('high_high', lang_en): '#d62728',
            get_text('low_low', lang_en): '#1f77b4',
            get_text('high_low', lang_en): '#ff9896',
            get_text('low_high', lang_en): '#aec7e8',
            get_text('not_significant', lang_en): '#d3d3d3'
        }
        
        for idx, (year, gdf_year) in enumerate(lisa_results.items()):
            ax = axes_flat[idx]
            
            # Plot each cluster type
            for cluster_type, color in color_map_en.items():
                cluster_data = gdf_year[gdf_year['lisa_cluster'] == get_text(
                    {v: k for k, v in {
                        'high_high': get_text('high_high', lang_en),
                        'low_low': get_text('low_low', lang_en),
                        'high_low': get_text('high_low', lang_en),
                        'low_high': get_text('low_high', lang_en),
                        'not_significant': get_text('not_significant', lang_en)
                    }.items()}[cluster_type], lang)]
                
                if len(cluster_data) > 0:
                    cluster_data.plot(
                        ax=ax,
                        color=color,
                        edgecolor='black',
                        linewidth=0.5
                    )
            
            # Count clusters
            n_hh = (gdf_year['lisa_cluster'] == get_text('high_high', lang)).sum()
            n_ll = (gdf_year['lisa_cluster'] == get_text('low_low', lang)).sum()
            total_cases = gdf_year['cases'].sum()
            
            ax.set_title(
                f'{year}\n{total_cases:,.0f} {get_text("cases", lang)} | {n_hh} {get_text("hotspots", lang)} | {n_ll} {get_text("coldspots_ll", lang).split(" (")[0]}',
                fontsize=13,
                fontweight='bold',
                pad=10
            )
            ax.axis('off')
            
            # Legend on first plot
            if idx == 0:
                legend_elements = [
                    Rectangle((0, 0), 1, 1, fc='#d62728', label=get_text('high_high_clusters', lang)),
                    Rectangle((0, 0), 1, 1, fc='#1f77b4', label=get_text('low_low_clusters', lang)),
                    Rectangle((0, 0), 1, 1, fc='#ff9896', label=get_text('high_low', lang)),
                    Rectangle((0, 0), 1, 1, fc='#aec7e8', label=get_text('low_high', lang)),
                    Rectangle((0, 0), 1, 1, fc='#d3d3d3', label=get_text('not_significant', lang))
                ]
                
                ax.legend(
                    handles=legend_elements,
                    loc='upper left',
                    fontsize=10,
                    frameon=True,
                    title=get_text('lisa_clusters', lang)
                )
        
        # Hide empty subplots
        for idx in range(n_years, len(axes_flat)):
            axes_flat[idx].axis('off')
        
        fig.suptitle(
            f'{get_text("lisa_analysis", lang)} - {get_text("multi_year_comparison", lang)}',
            fontsize=18,
            fontweight='bold'
        )
        
        st.pyplot(fig)
        plt.close()
        
        # Summary table
        st.markdown("---")
        st.subheader(f"📊 {get_text('summary_statistics', lang)}")
        
        summary_data = []
        for year, gdf_year in lisa_results.items():
            counts = gdf_year['lisa_cluster'].value_counts()
            summary_data.append({
                get_text('year', lang): year,
                get_text('total_cases', lang): gdf_year['cases'].sum(),
                get_text('hotspots', lang): counts.get(get_text('high_high', lang), 0),
                get_text('coldspots_ll', lang).split(' (')[0]: counts.get(get_text('low_low', lang), 0),
                f'HL {get_text("outliers", lang) if lang == "en" else "Aberrantes"}': counts.get(get_text('high_low', lang), 0),
                f'LH {get_text("outliers", lang) if lang == "en" else "Aberrantes"}': counts.get(get_text('low_high', lang), 0),
                get_text('not_significant', lang): counts.get(get_text('not_significant', lang), 0)
            })
        
        summary_df = pd.DataFrame(summary_data)
        
        st.dataframe(
            summary_df.style
            .background_gradient(subset=[get_text('hotspots', lang)], cmap='Reds')
            .background_gradient(subset=[get_text('coldspots_ll', lang).split(' (')[0]], cmap='Blues')
            .format({
                get_text('total_cases', lang): '{:,.0f}'
            }),
            use_container_width=True
        )
        
        # Temporal trend
        if len(lisa_results) > 1:
            fig_trend = go.Figure()
            
            fig_trend.add_trace(go.Scatter(
                x=summary_df[get_text('year', lang)],
                y=summary_df[get_text('hotspots', lang)],
                mode='lines+markers',
                name=get_text('hotspots', lang),
                line=dict(color='#d62728', width=3),
                marker=dict(size=10)
            ))
            
            fig_trend.add_trace(go.Scatter(
                x=summary_df[get_text('year', lang)],
                y=summary_df[get_text('coldspots_ll', lang).split(' (')[0]],
                mode='lines+markers',
                name=get_text('coldspots_ll', lang).split(' (')[0],
                line=dict(color='#1f77b4', width=3),
                marker=dict(size=10)
            ))
            
            fig_trend.update_layout(
                title=f'<b>{get_text("temporal_evolution", lang)}</b>',
                xaxis_title=get_text('year', lang),
                yaxis_title=get_text('number_of_districts', lang),
                height=400,
                hovermode='x unified'
            )
            
            st.plotly_chart(fig_trend, use_container_width=True)
    
    # ========================================================================
    # NOTES AND ANNOTATIONS
    # ========================================================================
    
    st.markdown("---")
    st.subheader(f"📝 {get_text('analysis_notes', lang)}")
    
    with st.expander(f"➕ {get_text('add_custom_notes', lang)}", expanded=False):
        st.markdown(f"""
        {get_text('use_this_space', lang)}
        """)
        
        user_notes = st.text_area(
            get_text('your_notes', lang),
            height=200,
            placeholder=get_text('notes_placeholder', lang),
            help=get_text('notes_session_specific', lang)
        )
        
        if user_notes:
            st.markdown('<div class="note-box">', unsafe_allow_html=True)
            st.markdown(f"**{get_text('your_notes', lang)}:**")
            st.markdown(user_notes)
            st.markdown("</div>", unsafe_allow_html=True)
    
    # ========================================================================
    # INTERPRETATION GUIDE
    # ========================================================================
    
    st.markdown("---")
    st.subheader(f"📖 {get_text('interpretation_guide', lang)}")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"""
        **{get_text('cluster_types', lang)}**
        
        🔴 **{get_text('high_high_clusters', lang)}**
        - {get_text('high_cases_high_neighbor_cases', lang)}
        - {get_text('indicates_spatial_clustering', lang)}
        - **{get_text('action_priority_intervention', lang)}**
        
        🔵 **{get_text('low_low_clusters', lang)}**
        - {get_text('low_cases_low_neighbor_cases', lang)}
        - {get_text('indicates_low_burden', lang)}
        - **{get_text('action_maintain_surveillance', lang)}**
        """)
    
    with col2:
        st.markdown(f"""
        **{get_text('outlier_types', lang)}**
        
        🟠 **{get_text('high_low_outlier', lang)}**
        - {get_text('high_cases_but_low_neighbors', lang)}
        - {get_text('isolated_outbreak', lang)}
        - **{get_text('action_investigate', lang)}**
        
        🟦 **{get_text('low_high_outlier', lang)}**
        - {get_text('low_cases_but_high_neighbors', lang)}
        - {get_text('potential_buffer_zone', lang)}
        - **{get_text('action_enhanced_surveillance', lang)}**
        """)
    
    st.info(f"""
    **{get_text('statistical_significance_note', lang)} {significance_level:.2f} {get_text('are_classified_significant', lang)}**
    """)
    
    # ========================================================================
    # DOWNLOAD OPTIONS
    # ========================================================================
    
    st.markdown("---")
    st.subheader(f"📥 {get_text('download_results', lang)}")
    
    if analysis_mode_en == "Single Year":
        year = selected_years[0]
        gdf_lisa = lisa_results[year]
        
        # Prepare download data
        download_data = gdf_lisa[['district_clean', 'cases', 'deaths', 'incidence_rate', 
                                   'lisa_cluster', 'lisa_pvalue']].copy()
        download_data.columns = [
            get_text('district', lang),
            get_text('total_cases', lang),
            get_text('total_deaths', lang),
            get_text('incidence_rate', lang),
            get_text('lisa_clusters', lang),
            'p-value'
        ]
        
        csv = download_data.to_csv(index=False).encode('utf-8')
        
        st.download_button(
            label=f"📥 {get_text('download_lisa_results', lang)} ({year})",
            data=csv,
            file_name=f"lisa_clusters_{year}_{lang}.csv",
            mime="text/csv"
        )
    else:
        # Multi-year summary
        csv = summary_df.to_csv(index=False).encode('utf-8')
        
        st.download_button(
            label=f"📥 {get_text('download_multi_year_summary', lang)}",
            data=csv,
            file_name=f"lisa_multi_year_summary_{lang}.csv",
            mime="text/csv"
        )
    
    # ========================================================================
    # FOOTER
    # ========================================================================
    
    st.markdown("---")
    st.caption(f"""
    **{get_text('lisa_configuration_footer', lang)}** α={significance_level} | 
    {get_text('spatial_weights', lang)}: {get_text('queen_contiguity', lang)} | 
    {get_text('health_districts', lang)}: {len(gdf)} | {get_text('average_neighbors', lang)}: {w.mean_neighbors:.1f}
    """)


# ============================================================================
# RUN PAGE
# ============================================================================

if __name__ == "__main__":
    main()