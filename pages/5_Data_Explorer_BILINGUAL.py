"""
================================================================================
PAGE 5: DATA EXPLORER (BILINGUAL - ENGLISH/FRANÇAIS)
================================================================================

This page provides flexible data exploration tools:
- Multi-filter system
- Dynamic data table
- Export functionality
- Quick statistics

BILINGUAL SUPPORT: Full English/French translation

Target Audience: Researchers, analysts needing custom data queries

================================================================================
"""

# ============================================================================
# IMPORTS
# ============================================================================

import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# Language configuration
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from lang_config import get_text

# ============================================================================
# PAGE CONFIGURATION
# ============================================================================

st.set_page_config(
    page_title="Data Explorer - Meningitis Dashboard",
    page_icon="📋",
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
        df = pd.read_csv('cleaned_data/ml_final_100pct_geometry.csv')
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
    """Main function for Data Explorer page"""
    
    # Get language
    lang = st.session_state.get('language', 'en')
    
    # ========================================================================
    # HEADER
    # ========================================================================
    
    st.markdown(f'''
    <div class="dashboard-header">
        <h1>📋 {get_text('data_explorer', lang)} - {get_text('export', lang)}</h1>
    </div>
    ''', unsafe_allow_html=True)
    
    # ========================================================================
    # LOAD DATA
    # ========================================================================
    
    with st.spinner(f"{get_text('loading_data', lang)}"):
        df = load_main_dataset()
    
    if df.empty:
        st.error(f"❌ {get_text('failed_load_data', lang)}")
        st.stop()
    
    # ========================================================================
    # SIDEBAR FILTERS
    # ========================================================================
    
    st.sidebar.header(f"🔍 {get_text('advanced_filters', lang)}")
    st.sidebar.markdown("---")
    
    # Year filter
    st.sidebar.subheader(f"📅 {get_text('time_period', lang)}")
    available_years = sorted(df['data_year'].unique())
    selected_years = st.sidebar.multiselect(
        get_text('years', lang),
        options=available_years,
        default=available_years,
        help=get_text('select', lang) + ' ' + get_text('years', lang)
    )
    
    # Week range
    week_range = st.sidebar.slider(
        f"{get_text('week', lang)} {get_text('distribution', lang) if lang == 'en' else 'Plage'}",
        min_value=1,
        max_value=53,
        value=(1, 53),
        help=get_text('filter_by', lang) + ' ' + get_text('week', lang)
    )
    
    st.sidebar.markdown("---")
    
    # Region filter
    st.sidebar.subheader(f"🌍 {get_text('geographic_distribution', lang)}")
    available_regions = sorted(df['region'].unique())
    selected_regions = st.sidebar.multiselect(
        get_text('regions', lang),
        options=available_regions,
        default=available_regions,
        help=get_text('select', lang) + ' ' + get_text('regions', lang)
    )
    
    # District filter
    show_district_filter = st.sidebar.checkbox(
        f"{get_text('filter_by', lang)} {get_text('districts', lang) if lang == 'en' else 'districts spécifiques'}"
    )
    
    if show_district_filter:
        available_districts = sorted(
            df[df['region'].isin(selected_regions)]['district_clean'].unique()
        )
        selected_districts = st.sidebar.multiselect(
            get_text('districts', lang),
            options=available_districts,
            default=[],
            help=get_text('select', lang) if lang == 'en' else 'Laisser vide pour tous les districts'
        )
    else:
        selected_districts = []
    
    st.sidebar.markdown("---")
    
    # Cases filter
    st.sidebar.subheader(f"📊 {get_text('data_table', lang) if lang == 'en' else 'Plage de Données'}")
    
    cases_filter_options = {
        get_text('total_records', lang) if lang == 'en' else 'Tous les enregistrements': 'all',
        get_text('cases', lang) + ' > 0': 'positive',
        get_text('custom', lang) if lang == 'en' else 'Plage personnalisée': 'custom'
    }
    
    cases_filter = st.sidebar.radio(
        f"{get_text('cases', lang)} {get_text('filters', lang)}",
        options=list(cases_filter_options.keys()),
        index=0
    )
    
    if cases_filter_options[cases_filter] == 'custom':
        cases_min = st.sidebar.number_input(
            f"{get_text('min', lang)} {get_text('cases', lang)}",
            min_value=0,
            value=0
        )
        cases_max = st.sidebar.number_input(
            f"{get_text('max', lang)} {get_text('cases', lang)}",
            min_value=0,
            value=1000
        )
    
    # ========================================================================
    # APPLY FILTERS
    # ========================================================================
    
    df_filtered = df.copy()
    
    # Apply filters
    if selected_years:
        df_filtered = df_filtered[df_filtered['data_year'].isin(selected_years)]
    
    df_filtered = df_filtered[
        (df_filtered['week_number'] >= week_range[0]) &
        (df_filtered['week_number'] <= week_range[1])
    ]
    
    if selected_regions:
        df_filtered = df_filtered[df_filtered['region'].isin(selected_regions)]
    
    if show_district_filter and selected_districts:
        df_filtered = df_filtered[df_filtered['district_clean'].isin(selected_districts)]
    
    if cases_filter_options[cases_filter] == 'positive':
        df_filtered = df_filtered[df_filtered['cases'] > 0]
    elif cases_filter_options[cases_filter] == 'custom':
        df_filtered = df_filtered[
            (df_filtered['cases'] >= cases_min) &
            (df_filtered['cases'] <= cases_max)
        ]
    
    # ========================================================================
    # FILTER SUMMARY
    # ========================================================================
    
    st.subheader(f"📊 {get_text('filtered_records', lang)} {get_text('summary_statistics', lang)}")
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric(
            get_text('total_records', lang),
            f"{len(df_filtered):,}",
            delta=f"{len(df_filtered) - len(df):,}",
            help=f"{get_text('total', lang)}: {len(df):,}"
        )
    
    with col2:
        st.metric(
            get_text('total_cases', lang),
            f"{df_filtered['cases'].sum():,.0f}"
        )
    
    with col3:
        st.metric(
            get_text('total_deaths', lang),
            f"{df_filtered['deaths'].sum():,.0f}"
        )
    
    with col4:
        st.metric(
            get_text('districts', lang),
            df_filtered['district_clean'].nunique()
        )
    
    with col5:
        st.metric(
            get_text('date_range', lang),
            f"{df_filtered['data_year'].min()}-{df_filtered['data_year'].max()}"
        )
    
    st.markdown("---")
    
    # ========================================================================
    # DATA TABLE
    # ========================================================================
    
    st.subheader(f"📋 {get_text('data_table', lang)}")
    
    # Column selector
    all_columns = df_filtered.columns.tolist()
    
    default_cols = ['region', 'district_clean', 'data_year', 'week_number', 
                    'cases', 'deaths', 'population']
    default_cols = [col for col in default_cols if col in all_columns]
    
    selected_columns = st.multiselect(
        get_text('select_columns', lang),
        options=all_columns,
        default=default_cols,
        help=get_text('choose_analysis_mode', lang) if lang == 'en' else 'Choisir les colonnes à afficher'
    )
    
    if not selected_columns:
        st.warning(f"⚠️ {get_text('please_select', lang)}")
        st.stop()
    
    # Limit rows
    max_rows = st.slider(
        get_text('max_rows', lang),
        min_value=100,
        max_value=min(10000, len(df_filtered)),
        value=min(1000, len(df_filtered)),
        step=100,
        help=get_text('select', lang) if lang == 'en' else 'Trop de lignes peut ralentir le navigateur'
    )
    
    # Display table
    df_display = df_filtered[selected_columns].head(max_rows)
    
    st.dataframe(
        df_display,
        use_container_width=True,
        height=500
    )
    
    if len(df_filtered) > max_rows:
        st.info(f"ℹ️ {get_text('displaying', lang)} {max_rows:,} / {len(df_filtered):,} {get_text('records', lang)}")
    
    st.markdown("---")
    
    # ========================================================================
    # QUICK STATISTICS
    # ========================================================================
    
    st.subheader(f"📈 {get_text('quick_statistics', lang)}")
    
    numeric_cols = df_filtered.select_dtypes(include=[np.number]).columns.tolist()
    
    if numeric_cols:
        selected_stat_col = st.selectbox(
            f"{get_text('select', lang)} {get_text('columns', lang)}",
            options=numeric_cols,
            index=numeric_cols.index('cases') if 'cases' in numeric_cols else 0
        )
        
        # Calculate statistics
        stats_data = {
            get_text('statistics', lang): [
                get_text('count', lang),
                get_text('mean', lang),
                get_text('median', lang),
                get_text('std_dev', lang),
                get_text('min', lang),
                get_text('max', lang),
                get_text('sum', lang)
            ],
            get_text('metric', lang) if lang == 'en' else 'Valeur': [
                f"{df_filtered[selected_stat_col].count():,.0f}",
                f"{df_filtered[selected_stat_col].mean():.2f}",
                f"{df_filtered[selected_stat_col].median():.2f}",
                f"{df_filtered[selected_stat_col].std():.2f}",
                f"{df_filtered[selected_stat_col].min():.2f}",
                f"{df_filtered[selected_stat_col].max():.2f}",
                f"{df_filtered[selected_stat_col].sum():,.0f}"
            ]
        }
        
        stats_df = pd.DataFrame(stats_data)
        st.table(stats_df)
    
    st.markdown("---")
    
    # ========================================================================
    # EXPORT FUNCTIONALITY
    # ========================================================================
    
    st.subheader(f"💾 {get_text('export', lang)} {get_text('data_table', lang)}")
    
    export_col1, export_col2 = st.columns(2)
    
    with export_col1:
        csv_data = df_filtered[selected_columns].to_csv(index=False).encode('utf-8')
        
        st.download_button(
            label=f"📥 {get_text('download_filtered_data', lang)}",
            data=csv_data,
            file_name=f"meningitis_filtered_{datetime.now().strftime('%Y%m%d_%H%M')}_{lang}.csv",
            mime="text/csv"
        )
    
    with export_col2:
        if numeric_cols:
            summary_stats = df_filtered[numeric_cols].describe()
            summary_csv = summary_stats.to_csv().encode('utf-8')
            
            st.download_button(
                label=f"📊 {get_text('download_summary_stats', lang)}",
                data=summary_csv,
                file_name=f"statistics_{datetime.now().strftime('%Y%m%d_%H%M')}_{lang}.csv",
                mime="text/csv"
            )
    
    # ========================================================================
    # SAVED QUERIES
    # ========================================================================
    
    st.markdown("---")
    st.subheader(f"💾 {get_text('quick_statistics', lang) if lang == 'en' else 'Requêtes Rapides'}")
    
    query_col1, query_col2, query_col3 = st.columns(3)
    
    with query_col1:
        if st.button(f"🔴 {get_text('case_fatality_rate', lang)} > 10%"):
            high_cfr = df[df['cfr'] > 10] if 'cfr' in df.columns else pd.DataFrame()
            if not high_cfr.empty:
                st.write(f"{len(high_cfr)} {get_text('records', lang)}")
                st.dataframe(high_cfr.head(20))
    
    with query_col2:
        if st.button(f"📈 {get_text('recent', lang) if lang == 'en' else 'Récent'} (4 {get_text('week', lang) if lang == 'en' else 'semaines'})"):
            max_year = df['data_year'].max()
            max_week = df[df['data_year'] == max_year]['week_number'].max()
            recent = df[
                (df['data_year'] == max_year) &
                (df['week_number'] > max_week - 4) &
                (df['cases'] > 0)
            ]
            if not recent.empty:
                st.write(f"{len(recent)} {get_text('records', lang)}")
                st.dataframe(recent.head(20))
    
    with query_col3:
        if st.button(f"⚠️ {get_text('analysis', lang) if lang == 'en' else 'Analyse Zéro-Inflation'}"):
            zero_count = (df['cases'] == 0).sum()
            total_count = len(df)
            zero_pct = (zero_count / total_count * 100)
            st.metric(f"{get_text('threshold', lang) if lang == 'en' else 'Taux Zéro-Inflation'}", f"{zero_pct:.1f}%")
            st.write(f"{zero_count:,} / {total_count:,} {get_text('records', lang)}")
    
    # ========================================================================
    # FOOTER
    # ========================================================================
    
    st.markdown("---")
    st.caption(f"**{get_text('filtered_records', lang)}:** {len(df_filtered):,} / {len(df):,} {get_text('total', lang)}")
    st.caption(f"**{get_text('displaying', lang)}:** {len(df_display):,} {get_text('rows', lang)} | **{get_text('columns', lang)}:** {len(selected_columns)}")


# ============================================================================
# RUN PAGE
# ============================================================================

if __name__ == "__main__":
    main()
