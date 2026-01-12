"""
================================================================================
PAGE 4: OUTBREAK PREDICTIONS & FORECASTING (BILINGUAL)
================================================================================

This page provides ML-based outbreak predictions:
- Next 4-12 week forecasts
- Risk classification by district
- Statistical predictions based on historical patterns

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
from datetime import datetime, timedelta
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
    page_title="Predictions - Meningitis Dashboard",
    page_icon="🎯",
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
    .risk-critical {
        background-color: #F8D7DA;
        border-left: 5px solid #DC3545;
        padding: 1rem;
        border-radius: 5px;
    }
    .risk-high {
        background-color: #FFF3CD;
        border-left: 5px solid #FFC107;
        padding: 1rem;
        border-radius: 5px;
    }
    .risk-moderate {
        background-color: #D1ECF1;
        border-left: 5px solid #17A2B8;
        padding: 1rem;
        border-radius: 5px;
    }
    .risk-low {
        background-color: #D4EDDA;
        border-left: 5px solid #28A745;
        padding: 1rem;
        border-radius: 5px;
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
# PREDICTION FUNCTIONS
# ============================================================================

def make_simple_prediction(df, district, weeks_ahead):
    """
    Simple statistical prediction based on recent trends
    
    Uses 12-week rolling average with trend adjustment
    """
    district_data = df[df['district_clean'] == district].copy()
    
    if len(district_data) < 12:
        return None
    
    # Get most recent data
    recent_data = district_data.nlargest(12, ['data_year', 'week_number'])
    
    # Calculate average
    avg_cases = recent_data['cases'].mean()
    
    # Calculate trend (last 4 weeks vs previous 8 weeks)
    if len(recent_data) >= 12:
        recent_4 = recent_data.nlargest(4, ['data_year', 'week_number'])['cases'].mean()
        previous_8 = recent_data.nlargest(12, ['data_year', 'week_number']).nsmallest(8, ['data_year', 'week_number'])['cases'].mean()
        
        if previous_8 > 0:
            trend_factor = recent_4 / previous_8
        else:
            trend_factor = 1.0
    else:
        trend_factor = 1.0
    
    # Apply trend with dampening for longer horizons
    dampening = 1.0 - (weeks_ahead - 1) * 0.05  # Reduce trend effect for longer predictions
    dampening = max(dampening, 0.7)  # Minimum 70% of trend
    
    predicted = avg_cases * (trend_factor ** dampening)
    
    return max(0, predicted)


def classify_risk_level(predicted_cases, district_data, lang='en'):
    """Classify predicted risk level based on historical distribution"""
    
    # Calculate percentiles from historical data
    cases_series = district_data['cases']
    p50 = cases_series.quantile(0.50)
    p75 = cases_series.quantile(0.75)
    p90 = cases_series.quantile(0.90)
    
    if predicted_cases > p90:
        return f"🔴 {get_text('critical_risk', lang)}", "risk-critical", "#DC3545"
    elif predicted_cases > p75:
        return f"🟠 {get_text('high_risk', lang)}", "risk-high", "#FFC107"
    elif predicted_cases > p50:
        return f"🟡 {get_text('moderate_risk', lang)}", "risk-moderate", "#17A2B8"
    else:
        return f"🟢 {get_text('low_risk', lang)}", "risk-low", "#28A745"


# ============================================================================
# MAIN PAGE FUNCTION
# ============================================================================

def main():
    """Main function for Predictions page"""
    
    # Get language
    lang = st.session_state.get('language', 'en')
    
    # ========================================================================
    # HEADER
    # ========================================================================
    
    st.markdown(f'''
    <div class="dashboard-header">
        <h1>🎯 {get_text('predictions_forecasting', lang)}</h1>
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
    # MODEL INFO
    # ========================================================================
    
    st.info(f"""
    📊 **{get_text('statistical_mode', lang)}**
    
    {get_text('predictions', lang) if lang == 'en' else 'Les prévisions'} {'are based on' if lang == 'en' else 'sont basées sur'}:
    - {'12-week historical averages' if lang == 'en' else 'Moyennes historiques de 12 semaines'}
    - {'Recent trend analysis' if lang == 'en' else 'Analyse des tendances récentes'}
    - {'Risk classification based on historical thresholds' if lang == 'en' else 'Classification des risques basée sur des seuils historiques'}
    """)
    
    # ========================================================================
    # SIDEBAR FILTERS
    # ========================================================================
    
    st.sidebar.header(f"🎯 {get_text('prediction_settings', lang)}")
    st.sidebar.markdown("---")
    
    # Get current period
    current_year = int(df['data_year'].max())
    current_week = int(df[df['data_year'] == current_year]['week_number'].max())
    
    st.sidebar.info(f"""
    **{get_text('current_period', lang)}:**
    - {get_text('year', lang)}: {current_year}
    - {get_text('week', lang)}: {current_week}
    """)
    
    # Prediction horizon
    weeks_ahead = st.sidebar.slider(
        f"{get_text('forecast_horizon', lang)} ({get_text('week', lang) if lang == 'en' else 'semaines'})",
        min_value=1,
        max_value=12,
        value=4,
        help=get_text('weeks_ahead', lang) if lang == 'en' else 'Nombre de semaines à prévoir'
    )
    
    st.sidebar.markdown("---")
    
    # Region filter
    available_regions = sorted(df['region'].unique())
    selected_regions = st.sidebar.multiselect(
        get_text('filter_by_regions', lang),
        options=available_regions,
        default=available_regions[:3],
        help=get_text('select', lang) + ' ' + get_text('regions', lang)
    )
    
    if not selected_regions:
        st.warning(f"⚠️ {get_text('please_select', lang)}")
        st.stop()
    
    # ========================================================================
    # GENERATE PREDICTIONS
    # ========================================================================
    
    st.subheader(f"🔮 {get_text('district_level_predictions', lang)}")
    
    with st.spinner(f"{get_text('generating_predictions', lang)}"):
        # Get districts in selected regions
        districts_to_predict = df[df['region'].isin(selected_regions)]['district_clean'].unique()
        
        predictions = []
        
        for district in districts_to_predict:
            predicted_cases = make_simple_prediction(df, district, weeks_ahead)
            
            if predicted_cases is not None:
                district_data = df[df['district_clean'] == district]
                region = district_data.iloc[0]['region']
                
                risk_level, risk_class, risk_color = classify_risk_level(
                    predicted_cases, 
                    district_data,
                    lang
                )
                
                predictions.append({
                    get_text('district', lang): district,
                    get_text('region', lang): region,
                    get_text('predicted_cases', lang): round(predicted_cases, 1),
                    get_text('risk_level', lang): risk_level,
                    'risk_class': risk_class,
                    'risk_color': risk_color
                })
        
        predictions_df = pd.DataFrame(predictions)
    
    if predictions_df.empty:
        st.warning(f"⚠️ {get_text('no_predictions', lang)}")
        st.stop()
    
    # ========================================================================
    # SUMMARY METRICS
    # ========================================================================
    
    st.subheader(f"📊 {get_text('prediction_summary', lang)}")
    
    col1, col2, col3, col4 = st.columns(4)
    
    total_predicted = predictions_df[get_text('predicted_cases', lang)].sum()
    critical_count = sum(predictions_df['risk_class'] == 'risk-critical')
    high_count = sum(predictions_df['risk_class'] == 'risk-high')
    moderate_count = sum(predictions_df['risk_class'] == 'risk-moderate')
    
    with col1:
        st.metric(
            get_text('total', lang) + ' ' + get_text('predicted_cases', lang),
            f"{total_predicted:,.0f}"
        )
    
    with col2:
        st.metric(
            f"🔴 {get_text('critical_risk', lang)}",
            critical_count
        )
    
    with col3:
        st.metric(
            f"🟠 {get_text('high_risk', lang)}",
            high_count
        )
    
    with col4:
        st.metric(
            f"🟡 {get_text('moderate_risk', lang)}",
            moderate_count
        )
    
    st.markdown("---")
    
    # ========================================================================
    # PREDICTIONS TABLE
    # ========================================================================
    
    st.subheader(f"📋 {get_text('district_level_predictions', lang)} ({weeks_ahead} {get_text('week', lang) if lang == 'en' else 'semaines'})")
    
    # Sort options
    sort_options = {
        get_text('predicted_cases', lang): get_text('predicted_cases', lang),
        get_text('risk_level', lang): get_text('risk_level', lang),
        get_text('district', lang): get_text('district', lang)
    }
    
    sort_by = st.selectbox(
        f"{get_text('sort_by', lang)}:",
        options=list(sort_options.keys()),
        index=0
    )
    
    # Sort dataframe
    if sort_by == get_text('predicted_cases', lang):
        predictions_display = predictions_df.sort_values(get_text('predicted_cases', lang), ascending=False)
    elif sort_by == get_text('district', lang):
        predictions_display = predictions_df.sort_values(get_text('district', lang))
    else:
        predictions_display = predictions_df.sort_values('risk_class')
    
    # Display columns
    display_cols = [get_text('district', lang), get_text('region', lang), 
                    get_text('predicted_cases', lang), get_text('risk_level', lang)]
    
    # Style the dataframe
    st.dataframe(
        predictions_display[display_cols].style
        .background_gradient(subset=[get_text('predicted_cases', lang)], cmap='YlOrRd')
        .format({get_text('predicted_cases', lang): '{:.1f}'}),
        use_container_width=True,
        height=500
    )
    
    # Download button
    csv_data = predictions_display[display_cols].to_csv(index=False).encode('utf-8')
    st.download_button(
        label=f"📥 {get_text('download', lang)} {get_text('predictions', lang)} (CSV)",
        data=csv_data,
        file_name=f"predictions_{weeks_ahead}weeks_{lang}.csv",
        mime="text/csv"
    )
    
    st.markdown("---")
    
    # ========================================================================
    # TOP RISK DISTRICTS
    # ========================================================================
    
    st.subheader(f"⚠️ {get_text('top_risk_districts', lang)}")
    
    high_risk = predictions_df[predictions_df['risk_class'].isin(['risk-critical', 'risk-high'])]
    
    if not high_risk.empty:
        high_risk_sorted = high_risk.sort_values(get_text('predicted_cases', lang), ascending=False).head(10)
        
        fig = px.bar(
            high_risk_sorted,
            x=get_text('predicted_cases', lang),
            y=get_text('district', lang),
            orientation='h',
            color='risk_color',
            color_discrete_map='identity',
            title=f"<b>{get_text('top_districts', lang)} (10) - {get_text('predicted_cases', lang)}</b>",
            hover_data=[get_text('region', lang), get_text('risk_level', lang)]
        )
        
        fig.update_layout(
            height=400,
            showlegend=False,
            yaxis={'categoryorder': 'total ascending'}
        )
        
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.success(f"✅ {get_text('low_risk', lang) if lang == 'en' else 'Aucun district à haut risque identifié'}")
    
    # ========================================================================
    # REGIONAL SUMMARY
    # ========================================================================
    
    st.markdown("---")
    st.subheader(f"🌍 {get_text('regional_distribution', lang)} - {get_text('predictions', lang)}")
    
    regional_summary = predictions_df.groupby(get_text('region', lang)).agg({
        get_text('predicted_cases', lang): 'sum',
        get_text('district', lang): 'count'
    }).reset_index()
    
    regional_summary.columns = [
        get_text('region', lang),
        get_text('predicted_cases', lang),
        get_text('districts', lang) if lang == 'en' else 'Districts'
    ]
    
    regional_summary = regional_summary.sort_values(get_text('predicted_cases', lang), ascending=False)
    
    # Display regional summary
    st.dataframe(
        regional_summary.style
        .background_gradient(subset=[get_text('predicted_cases', lang)], cmap='YlOrRd')
        .format({get_text('predicted_cases', lang): '{:.1f}'}),
        use_container_width=True
    )
    
    # Regional chart
    fig_regional = px.bar(
        regional_summary,
        x=get_text('predicted_cases', lang),
        y=get_text('region', lang),
        orientation='h',
        color=get_text('predicted_cases', lang),
        color_continuous_scale='YlOrRd',
        title=f"<b>{get_text('predicted_cases', lang)} - {get_text('region', lang)}</b>",
        text=get_text('predicted_cases', lang)
    )
    
    fig_regional.update_traces(texttemplate='%{text:.0f}', textposition='outside')
    fig_regional.update_layout(height=400, showlegend=False)
    
    st.plotly_chart(fig_regional, use_container_width=True)
    
    # ========================================================================
    # FOOTER
    # ========================================================================
    
    st.markdown("---")
    st.caption(f"**{get_text('forecast_horizon', lang)}:** {weeks_ahead} {get_text('week', lang) if lang == 'en' else 'semaines'} | **{get_text('regions', lang)}:** {len(selected_regions)}")
    st.caption(f"**{get_text('total', lang)} {get_text('districts', lang)}:** {len(predictions_df)}")


# ============================================================================
# RUN PAGE
# ============================================================================

if __name__ == "__main__":
    main()
