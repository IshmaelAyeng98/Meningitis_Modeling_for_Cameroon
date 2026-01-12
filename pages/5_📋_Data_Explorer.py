"""
================================================================================
PAGE 5: DATA EXPLORER
================================================================================

This page provides flexible data exploration tools:
- Multi-filter system
- Dynamic data table
- Export functionality
- Quick statistics

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

# ============================================================================
# PAGE CONFIGURATION
# ============================================================================

st.set_page_config(
    page_title="Data Explorer - Meningitis Dashboard",
    page_icon="📋",
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


# ============================================================================
# MAIN PAGE FUNCTION
# ============================================================================

def main():
    """Main function for Data Explorer page"""
    
    # ========================================================================
    # HEADER
    # ========================================================================
    
    st.markdown('''
    <div class="dashboard-header">
        <h1>📋 Data Explorer - Custom Queries & Export</h1>
    </div>
    ''', unsafe_allow_html=True)
    
    # ========================================================================
    # LOAD DATA
    # ========================================================================
    
    with st.spinner("Loading data..."):
        df = load_main_dataset()
    
    if df.empty:
        st.error("❌ Failed to load data.")
        st.stop()
    
    # ========================================================================
    # SIDEBAR FILTERS
    # ========================================================================
    
    st.sidebar.header("🔍 Advanced Filters")
    st.sidebar.markdown("---")
    
    # Year filter
    st.sidebar.subheader("📅 Time Period")
    available_years = sorted(df['data_year'].unique())
    selected_years = st.sidebar.multiselect(
        "Years",
        options=available_years,
        default=available_years,
        help="Select one or more years"
    )
    
    # Week range
    week_range = st.sidebar.slider(
        "Week Range",
        min_value=1,
        max_value=53,
        value=(1, 53),
        help="Filter by epidemiological week"
    )
    
    st.sidebar.markdown("---")
    
    # Region filter
    st.sidebar.subheader("🌍 Geographic")
    available_regions = sorted(df['region'].unique())
    selected_regions = st.sidebar.multiselect(
        "Regions",
        options=available_regions,
        default=available_regions,
        help="Select one or more regions"
    )
    
    # District filter (optional - can select specific districts)
    show_district_filter = st.sidebar.checkbox("Filter by specific districts")
    
    if show_district_filter:
        # Only show districts from selected regions
        available_districts = sorted(
            df[df['region'].isin(selected_regions)]['district_clean'].unique()
        )
        selected_districts = st.sidebar.multiselect(
            "Districts",
            options=available_districts,
            default=[],
            help="Leave empty to include all districts"
        )
    else:
        selected_districts = []
    
    st.sidebar.markdown("---")
    
    # Cases filter
    st.sidebar.subheader("📊 Data Range")
    
    cases_filter = st.sidebar.radio(
        "Cases Filter",
        options=["All records", "Only records with cases (>0)", "Custom range"],
        index=0
    )
    
    if cases_filter == "Custom range":
        cases_min = st.sidebar.number_input("Min cases", min_value=0, value=0)
        cases_max = st.sidebar.number_input("Max cases", min_value=0, value=1000)
    
    # ========================================================================
    # APPLY FILTERS
    # ========================================================================
    
    # Start with full dataset
    df_filtered = df.copy()
    
    # Apply year filter
    if selected_years:
        df_filtered = df_filtered[df_filtered['data_year'].isin(selected_years)]
    
    # Apply week range
    df_filtered = df_filtered[
        (df_filtered['week_number'] >= week_range[0]) &
        (df_filtered['week_number'] <= week_range[1])
    ]
    
    # Apply region filter
    if selected_regions:
        df_filtered = df_filtered[df_filtered['region'].isin(selected_regions)]
    
    # Apply district filter (if enabled)
    if show_district_filter and selected_districts:
        df_filtered = df_filtered[df_filtered['district_clean'].isin(selected_districts)]
    
    # Apply cases filter
    if cases_filter == "Only records with cases (>0)":
        df_filtered = df_filtered[df_filtered['cases'] > 0]
    elif cases_filter == "Custom range":
        df_filtered = df_filtered[
            (df_filtered['cases'] >= cases_min) &
            (df_filtered['cases'] <= cases_max)
        ]
    
    # ========================================================================
    # FILTER SUMMARY
    # ========================================================================
    
    st.subheader("📊 Filtered Data Summary")
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric(
            "Total Records",
            f"{len(df_filtered):,}",
            delta=f"{len(df_filtered) - len(df):,}",
            help=f"Original: {len(df):,} records"
        )
    
    with col2:
        st.metric(
            "Total Cases",
            f"{df_filtered['cases'].sum():,.0f}",
            help="Sum of all cases in filtered data"
        )
    
    with col3:
        st.metric(
            "Total Deaths",
            f"{df_filtered['deaths'].sum():,.0f}",
            help="Sum of all deaths in filtered data"
        )
    
    with col4:
        st.metric(
            "Districts",
            df_filtered['district_clean'].nunique(),
            help="Number of unique districts"
        )
    
    with col5:
        st.metric(
            "Date Range",
            f"{df_filtered['data_year'].min()}-{df_filtered['data_year'].max()}",
            help="Year range in filtered data"
        )
    
    st.markdown("---")
    
    # ========================================================================
    # DATA TABLE
    # ========================================================================
    
    st.subheader("📋 Data Table")
    
    # Column selector
    all_columns = df_filtered.columns.tolist()
    
    # Default columns to show
    default_cols = ['region', 'district_clean', 'data_year', 'week_number', 
                    'cases', 'deaths', 'population']
    default_cols = [col for col in default_cols if col in all_columns]
    
    selected_columns = st.multiselect(
        "Select columns to display",
        options=all_columns,
        default=default_cols,
        help="Choose which columns to show in the table"
    )
    
    if not selected_columns:
        st.warning("⚠️ Please select at least one column to display.")
        st.stop()
    
    # Limit rows for performance
    max_rows = st.slider(
        "Maximum rows to display",
        min_value=100,
        max_value=min(10000, len(df_filtered)),
        value=min(1000, len(df_filtered)),
        step=100,
        help="Displaying too many rows may slow down the browser"
    )
    
    # Display table
    df_display = df_filtered[selected_columns].head(max_rows)
    
    st.dataframe(
        df_display,
        use_container_width=True,
        height=500
    )
    
    if len(df_filtered) > max_rows:
        st.info(f"ℹ️ Showing {max_rows:,} of {len(df_filtered):,} records. Adjust slider to show more.")
    
    st.markdown("---")
    
    # ========================================================================
    # QUICK STATISTICS
    # ========================================================================
    
    st.subheader("📈 Quick Statistics")
    
    # Numerical columns for statistics
    numeric_cols = df_filtered.select_dtypes(include=[np.number]).columns.tolist()
    
    if numeric_cols:
        selected_stat_col = st.selectbox(
            "Select column for statistics",
            options=numeric_cols,
            index=numeric_cols.index('cases') if 'cases' in numeric_cols else 0
        )
        
        # Calculate statistics
        stats_data = {
            'Statistic': ['Count', 'Mean', 'Median', 'Std Dev', 'Min', 'Max', 'Sum'],
            'Value': [
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
    
    st.subheader("💾 Export Data")
    
    export_col1, export_col2 = st.columns(2)
    
    with export_col1:
        # Export filtered data
        csv_data = df_filtered[selected_columns].to_csv(index=False).encode('utf-8')
        
        st.download_button(
            label="📥 Download Filtered Data (CSV)",
            data=csv_data,
            file_name=f"meningitis_filtered_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
            mime="text/csv",
            help="Download the current filtered dataset"
        )
    
    with export_col2:
        # Export summary statistics
        if numeric_cols:
            summary_stats = df_filtered[numeric_cols].describe()
            summary_csv = summary_stats.to_csv().encode('utf-8')
            
            st.download_button(
                label="📊 Download Summary Statistics (CSV)",
                data=summary_csv,
                file_name=f"statistics_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
                mime="text/csv",
                help="Download summary statistics for numerical columns"
            )
    
    # ========================================================================
    # SAVED QUERIES (Optional)
    # ========================================================================
    
    st.markdown("---")
    st.subheader("💾 Quick Queries")
    
    st.markdown("""
    Use these pre-defined queries for common analyses:
    """)
    
    query_col1, query_col2, query_col3 = st.columns(3)
    
    with query_col1:
        if st.button("🔴 High CFR Districts (CFR > 10%)"):
            high_cfr = df[df['cfr'] > 10] if 'cfr' in df.columns else pd.DataFrame()
            if not high_cfr.empty:
                st.write(f"Found {len(high_cfr)} records")
                st.dataframe(high_cfr.head(20))
    
    with query_col2:
        if st.button("📈 Recent Outbreaks (Last 4 weeks)"):
            max_year = df['data_year'].max()
            max_week = df[df['data_year'] == max_year]['week_number'].max()
            recent = df[
                (df['data_year'] == max_year) &
                (df['week_number'] > max_week - 4) &
                (df['cases'] > 0)
            ]
            if not recent.empty:
                st.write(f"Found {len(recent)} records")
                st.dataframe(recent.head(20))
    
    with query_col3:
        if st.button("⚠️ Zero-inflation Analysis"):
            zero_count = (df['cases'] == 0).sum()
            total_count = len(df)
            zero_pct = (zero_count / total_count * 100)
            st.metric("Zero-inflation Rate", f"{zero_pct:.1f}%")
            st.write(f"{zero_count:,} of {total_count:,} records have zero cases")
    
    # ========================================================================
    # FOOTER
    # ========================================================================
    
    st.markdown("---")
    st.caption(f"**Filtered Records:** {len(df_filtered):,} of {len(df):,} total")
    st.caption(f"**Displaying:** {len(df_display):,} rows | **Columns:** {len(selected_columns)}")


# ============================================================================
# RUN PAGE
# ============================================================================

if __name__ == "__main__":
    main()
