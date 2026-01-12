"""
================================================================================
PAGE 3: TEMPORAL ANALYSIS (BILINGUAL - ENGLISH/FRANÇAIS)
================================================================================

This page provides time-based analysis of meningitis patterns:
- Seasonal patterns (weekly trends)
- Year-over-year comparison
- Epidemic timeline
- Weekly heatmap calendar

Target Audience: Understanding outbreak timing, planning seasonal interventions

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
from plotly.subplots import make_subplots
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
    page_title="Temporal Analysis - Meningitis Dashboard",
    page_icon="📈",
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
        st.error(f"{get_text('error_loading_data', lang)}: {str(e)}")
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
    
    # Get language
    lang = st.session_state.get('language', 'en')
    
    # ========================================================================
    # HEADER
    # ========================================================================
    
    st.markdown(f'''
    <div class="dashboard-header">
        <h1>📈 {get_text('temporal_analysis', lang)} - {get_text('seasonal_pattern', lang)} & {get_text('temporal_trends', lang)}</h1>
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
    
    st.sidebar.header(f"🔍 {get_text('filters', lang)}")
    st.sidebar.markdown("---")
    
    # Year filter (multiple years for comparison)
    available_years = sorted(df['data_year'].unique(), reverse=True)
    selected_years = st.sidebar.multiselect(
        get_text('select', lang) + ' ' + get_text('years', lang),
        options=available_years,
        default=available_years[:3],  # Default: most recent 3 years
        help=get_text('choose_multiple_years', lang)
    )
    
    # Region filter
    available_regions = sorted(df['region'].unique())
    selected_regions = st.sidebar.multiselect(
        get_text('select', lang) + ' ' + get_text('regions', lang),
        options=available_regions,
        default=available_regions,
        help=get_text('choose_multiple_years', lang) if lang == 'en' else 'Choisir les régions à inclure'
    )
    
    if not selected_years or not selected_regions:
        st.warning(f"⚠️ {get_text('please_select', lang)}")
        st.stop()
    
    st.sidebar.markdown("---")
    st.sidebar.info(f"""
    **{get_text('current_configuration', lang)}:**
    - {get_text('years', lang)}: {len(selected_years)}
    - {get_text('regions', lang)}: {len(selected_regions)}
    """)
    
    # ========================================================================
    # SEASONAL PATTERN ANALYSIS
    # ========================================================================
    
    st.subheader(f"🌊 {get_text('seasonal_pattern', lang)} - {get_text('weekly_average', lang)} {get_text('cases', lang)}")
    
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
            name=get_text('mean', lang) + ' ' + get_text('cases', lang),
            line=dict(color='#1f77b4', width=3),
            marker=dict(size=6),
            hovertemplate=f'<b>{get_text("week", lang)} %{{x}}</b><br>{get_text("mean", lang)}: %{{y:.1f}}<extra></extra>'
        )
    )
    
    # Add range (min-max) as shaded area
    fig_seasonal.add_trace(
        go.Scatter(
            x=weekly_pattern['week_number'],
            y=weekly_pattern['max_cases'],
            mode='lines',
            name=get_text('max', lang),
            line=dict(width=0),
            hoverinfo='skip'
        )
    )
    
    fig_seasonal.add_trace(
        go.Scatter(
            x=weekly_pattern['week_number'],
            y=weekly_pattern['min_cases'],
            mode='lines',
            name=get_text('distribution', lang) if lang == 'en' else 'Plage',
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
        annotation_text=f"{get_text('high_risk', lang)} {get_text('threshold', lang) if lang == 'en' else 'Seuil'} (75e percentile)",
        annotation_position="top right"
    )
    
    fig_seasonal.update_layout(
        title=f"<b>{get_text('weekly_average', lang)} {get_text('seasonal_pattern', lang)}</b>",
        xaxis_title=get_text('week_number', lang),
        yaxis_title=get_text('mean', lang) + ' ' + get_text('cases', lang),
        height=500,
        hovermode='x unified',
        showlegend=True
    )
    
    st.plotly_chart(fig_seasonal, use_container_width=True)
    
    # Identify and display high-risk weeks
    high_risk_weeks = weekly_pattern[weekly_pattern['avg_cases'] > high_risk_threshold]['week_number'].tolist()
    
    if high_risk_weeks:
        weeks_text = ', '.join(map(str, high_risk_weeks))
        recommendation_text = get_text('action_enhanced_surveillance', lang) if lang == 'en' else 'Intensifier la surveillance et préparer les ressources pendant ces semaines'
        
        st.markdown(f"""
        <div class="warning-box">
            <strong>⚠️ {get_text('high_risk', lang) if lang == 'en' else 'Saison de Transmission Élevée Identifiée'}</strong><br>
            {get_text('week', lang) if lang == 'en' else 'Semaines'} ({'>75e percentile' if lang == 'en' else '>75e percentile'}): <strong>{weeks_text}</strong><br>
            <em>{recommendation_text}</em>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # ========================================================================
    # YEAR-OVER-YEAR COMPARISON
    # ========================================================================
    
    st.subheader(f"📊 {get_text('comparison', lang)} {get_text('year', lang) if lang == 'en' else 'Année après Année'}")
    
    # Get yearly trends
    yearly_weekly = get_yearly_trends(df, selected_years, selected_regions)
    
    # Create year-over-year comparison chart
    fig_yoy = px.line(
        yearly_weekly,
        x='week_number',
        y='cases',
        color='data_year',
        title=f"<b>{get_text('weekly_average', lang)} {get_text('cases', lang)} - {get_text('year', lang)}</b>",
        labels={
            'week_number': get_text('week_number', lang),
            'cases': get_text('total_cases', lang),
            'data_year': get_text('year', lang)
        },
        markers=True,
        color_discrete_sequence=px.colors.qualitative.Set2
    )
    
    fig_yoy.update_layout(
        height=500,
        hovermode='x unified',
        legend=dict(title=get_text('year', lang), orientation="h", y=1.1)
    )
    
    st.plotly_chart(fig_yoy, use_container_width=True)
    
    st.markdown("---")
    
    # ========================================================================
    # EPIDEMIC TIMELINE
    # ========================================================================
    
    st.subheader(f"🔴 {get_text('outbreak_pattern', lang) if lang == 'en' else 'Chronologie des Semaines Épidémiques'}")
    
    # Identify epidemic weeks
    epidemic_weeks, threshold = identify_epidemic_weeks(df, selected_years, selected_regions)
    
    st.info(f"**{get_text('threshold', lang) if lang == 'en' else 'Seuil Épidémique'}:** {threshold:.0f} {get_text('cases', lang)}/{get_text('week', lang)} (90e percentile)")
    
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
            labels=dict(
                x=get_text('week_number', lang),
                y=get_text('year', lang),
                color=get_text('cases', lang)
            ),
            x=heatmap_data.columns,
            y=heatmap_data.index,
            color_continuous_scale='YlOrRd',
            title=f"<b>{get_text('heatmap', lang)} - {get_text('cases', lang)} ({get_text('years', lang)})</b>",
            aspect='auto'
        )
        
        fig_heatmap.update_layout(
            height=400,
            xaxis_title=get_text('week_number', lang),
            yaxis_title=get_text('year', lang)
        )
        
        st.plotly_chart(fig_heatmap, use_container_width=True)
        
        # Display epidemic weeks table (limit to top 20 for size)
        st.subheader(f"📋 {get_text('top_districts', lang).replace('Districts', '20 ' + (get_text('week', lang) if lang == 'en' else 'Semaines Épidémiques'))}")
        
        epidemic_weeks_display = epidemic_weeks.nlargest(20, 'cases').copy()
        epidemic_weeks_display = epidemic_weeks_display.sort_values(['data_year', 'week_number'])
        
        st.dataframe(
            epidemic_weeks_display,
            use_container_width=True,
            column_config={
                'data_year': st.column_config.NumberColumn(get_text('year', lang), format='%d'),
                'week_number': st.column_config.NumberColumn(get_text('week', lang), format='%d'),
                'cases': st.column_config.NumberColumn(get_text('cases', lang), format='%d')
            },
            hide_index=True
        )
    else:
        st.info(f"{get_text('no_data_available', lang)}")
    
    st.markdown("---")
    
    # ========================================================================
    # TEMPORAL STATISTICS
    # ========================================================================
    
    st.subheader(f"📊 {get_text('summary_statistics', lang)} {get_text('temporal_analysis', lang)}")
    
    stat_col1, stat_col2, stat_col3, stat_col4 = st.columns(4)
    
    with stat_col1:
        peak_week = weekly_pattern.loc[weekly_pattern['avg_cases'].idxmax(), 'week_number']
        st.metric(
            f"{get_text('peak', lang) if lang == 'en' else 'Semaine de Pointe'} {get_text('week', lang)}",
            f"{get_text('week', lang)} {int(peak_week)}",
            help=get_text('highest', lang) if lang == 'en' else 'Semaine avec le plus de cas moyens'
        )
    
    with stat_col2:
        lowest_week = weekly_pattern.loc[weekly_pattern['avg_cases'].idxmin(), 'week_number']
        st.metric(
            f"{get_text('lowest', lang) if lang == 'en' else 'Semaine la Plus Basse'}",
            f"{get_text('week', lang)} {int(lowest_week)}",
            help=get_text('min', lang) if lang == 'en' else 'Semaine avec le moins de cas moyens'
        )
    
    with stat_col3:
        st.metric(
            f"{get_text('high_risk', lang)} {get_text('week', lang) if lang == 'en' else 'Semaines'}",
            len(high_risk_weeks),
            help=get_text('high_risk_districts', lang) if lang == 'en' else 'Nombre de semaines en saison de transmission élevée'
        )
    
    with stat_col4:
        st.metric(
            get_text('outbreak_pattern', lang) if lang == 'en' else 'Événements Épidémiques',
            len(epidemic_weeks),
            help=get_text('outbreak_detection', lang) if lang == 'en' else 'Nombre de semaines dépassant le seuil épidémique'
        )
    
    # ========================================================================
    # INSIGHTS
    # ========================================================================
    
    st.markdown("---")
    st.subheader(f"💡 {get_text('insights', lang)} {get_text('temporal_analysis', lang)}")
    
    insight_col1, insight_col2 = st.columns(2)
    
    with insight_col1:
        seasonality_text = get_text('seasonal_pattern', lang) if lang == 'en' else 'Forte saisonnalité détectée' if len(high_risk_weeks) > 5 else 'Saisonnalité modérée'
        
        st.info(f"""
        **🌊 {get_text('seasonal_pattern', lang)}:**
        
        - **{get_text('peak', lang) if lang == 'en' else 'Transmission pic'}:** {get_text('week', lang)} {int(peak_week)}
        - **{get_text('lowest', lang) if lang == 'en' else 'Transmission la plus basse'}:** {get_text('week', lang)} {int(lowest_week)}
        - **{get_text('high_risk', lang)} {get_text('week', lang) if lang == 'en' else 'saison'}:** {len(high_risk_weeks)} {get_text('week', lang) if lang == 'en' else 'semaines identifiées'}
        - **{get_text('outbreak_pattern', lang) if lang == 'en' else 'Schéma'}:** {seasonality_text}
        """)
    
    with insight_col2:
        # Compare years
        if len(selected_years) > 1:
            recent_year = max(selected_years)
            prev_year = sorted(selected_years)[-2] if len(selected_years) > 1 else recent_year - 1
            
            recent_total = yearly_weekly[yearly_weekly['data_year'] == recent_year]['cases'].sum()
            prev_total = yearly_weekly[yearly_weekly['data_year'] == prev_year]['cases'].sum()
            
            change = ((recent_total - prev_total) / prev_total * 100) if prev_total > 0 else 0
            
            status_text = f"⚠️ {get_text('increasing', lang) if lang == 'en' else 'Tendance croissante'}" if change > 10 else f"✅ {get_text('stable', lang) if lang == 'en' else 'Stable ou décroissant'}"
            
            st.warning(f"""
            **📈 {get_text('temporal_trends', lang) if lang == 'en' else 'Tendance Récente'}:**
            
            - **{recent_year}:** {int(recent_total):,} {get_text('total_cases', lang)}
            - **{prev_year}:** {int(prev_total):,} {get_text('total_cases', lang)}
            - **{get_text('change', lang) if lang == 'en' else 'Changement'}:** {change:+.1f}%
            - **{get_text('status', lang) if lang == 'en' else 'Statut'}:** {status_text}
            """)
    
    # ========================================================================
    # FOOTER
    # ========================================================================
    
    st.markdown("---")
    st.caption(f"**{get_text('years', lang)}:** {', '.join(map(str, sorted(selected_years)))}")
    st.caption(f"**{get_text('regions', lang)}:** {len(selected_regions)} | **{get_text('total', lang)} {get_text('week', lang) if lang == 'en' else 'Semaines Analysées'}:** {len(weekly_pattern)}")


# ============================================================================
# RUN PAGE
# ============================================================================

if __name__ == "__main__":
    main()
