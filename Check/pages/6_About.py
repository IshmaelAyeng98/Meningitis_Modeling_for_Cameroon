"""
================================================================================
PAGE 6: ABOUT & METHODOLOGY
================================================================================

This page provides documentation about:
- Data sources
- Methodology
- Project information
- Contact details

================================================================================
"""

# ============================================================================
# IMPORTS
# ============================================================================

import streamlit as st

# ============================================================================
# PAGE CONFIGURATION
# ============================================================================

st.set_page_config(
    page_title="About - Meningitis Dashboard",
    page_icon="ℹ️",
    layout="wide"
)

# ============================================================================
# MAIN PAGE
# ============================================================================

st.markdown('''
<div style="background: linear-gradient(135deg, #1f77b4 0%, #2C3E50 100%); color: white; padding: 2rem; border-radius: 10px; margin-bottom: 2rem;">
    <h1 style="color: white; margin: 0;">ℹ️ About This Dashboard</h1>
</div>
''', unsafe_allow_html=True)

# ============================================================================
# PROJECT OVERVIEW
# ============================================================================

st.header("📋 Project Overview")

st.markdown("""
This dashboard provides **real-time surveillance and analysis** of meningitis outbreaks 
across health districts in Cameroon, supporting evidence-based decision-making for 
DLMEP/MINSANTE.

### 🎯 Objectives

1. **Monitor** meningitis trends across districts and regions
2. **Identify** geographic and temporal hotspots
3. **Predict** outbreak risk using machine learning
4. **Guide** vaccination strategies and resource allocation
5. **Support** public health decision-making
""")

st.markdown("---")

# ============================================================================
# DATA SOURCES
# ============================================================================

st.header("📊 Data Sources")

st.markdown("""
### Primary Data Source

- **Organization:** DLMEP/MINSANTE (Direction de la Lutte contre la Maladie, les Epidémies et les Pandémies)
- **Country:** Cameroon Ministry of Public Health
- **System:** Weekly surveillance reporting from health districts
- **Period:** 2017-2025 (9 years)
- **Coverage:** 197 health districts (96.6% of total)
- **Records:** ~91,000+ district-week observations

### Data Structure

| Variable | Description | Type |
|----------|-------------|------|
| **Region** | Administrative region | Categorical (10 regions) |
| **District** | Health district | Categorical (197 districts) |
| **Year** | Surveillance year | Numerical (2017-2025) |
| **Week** | Epidemiological week | Numerical (1-53) |
| **Cases** | Confirmed meningitis cases | Numerical |
| **Deaths** | Deaths from meningitis | Numerical |
| **Population** | District population | Numerical |

### Geographic Coverage

- **Regions Covered:** 10/10 (100%)
- **Districts Covered:** 197/204 (96.6%)
- **Excluded Districts:** 7 districts without geographic boundaries
""")

st.markdown("---")

# ============================================================================
# METHODOLOGY
# ============================================================================

st.header("🔬 Methodology")

st.markdown("""
### Data Processing Pipeline

1. **Data Cleaning**
   - Standardized district names across years
   - Handled missing values appropriately
   - Validated data quality and consistency
   - Removed duplicate records

2. **Feature Engineering**
   - Temporal lag features (1, 2, 4 weeks)
   - Rolling averages (2, 4, 8 weeks)
   - Spatial features (region encoding)
   - Epidemiological rates (incidence, CFR, attack rate)

3. **Geospatial Matching**
   - 100% geometry matching achieved
   - District boundaries from official shapefiles
   - Spatial adjacency matrices computed

### Key Metrics Calculated

- **Case Fatality Rate (CFR):** `(Deaths / Cases) × 100`
- **Incidence Rate:** `(Cases / Population) × 100,000`
- **Attack Rate:** `(Cases / Population) × 100`
- **Epidemic Threshold:** 90th percentile of weekly cases

### Analysis Methods

- **Temporal Analysis:** Seasonal decomposition, trend detection
- **Spatial Analysis:** Choropleth mapping, hotspot identification
- **Statistical Methods:** Descriptive statistics, correlation analysis
- **Machine Learning:** XGBoost, LightGBM, Random Forest (for predictions)
""")

st.markdown("---")

# ============================================================================
# MACHINE LEARNING MODELS
# ============================================================================

st.header("🤖 Machine Learning Models")

st.markdown("""
### Models Implemented

1. **XGBoost Regressor**
   - Purpose: Predict weekly case counts
   - Performance: RMSE ~12-15 cases
   - Features: 25+ temporal and spatial features

2. **LightGBM Regressor**
   - Purpose: Alternative forecasting model
   - Advantage: Faster training on large datasets

3. **Random Forest Classifier**
   - Purpose: Outbreak detection (binary classification)
   - Threshold: 90th percentile of cases

### Model Training

- **Training Period:** 2017-2023 (7 years)
- **Testing Period:** 2024-2025 (2 years)
- **Validation Method:** Temporal split (preserves time order)
- **Optimization:** Hyperparameter tuning via grid search

### Challenges Addressed

- **Zero-Inflation:** 77%+ of weeks have zero cases
  - Solution: Zero-inflated models (ZIP, ZINB)
- **Spatial Correlation:** Cases cluster geographically
  - Solution: Spatial lag features
- **Seasonality:** Strong weekly patterns
  - Solution: Week-of-year encoding
""")

st.markdown("---")

# ============================================================================
# LIMITATIONS
# ============================================================================

st.header("⚠️ Limitations & Caveats")

st.markdown("""
### Data Limitations

1. **Climate Data Unavailable**
   - Temperature, rainfall, humidity not included
   - Limits model accuracy for seasonal prediction

2. **Intervention Data Incomplete**
   - Vaccination campaigns not fully documented
   - Cannot assess intervention impact directly

3. **Under-Reporting Possible**
   - Some districts may have incomplete reporting
   - CFR variations may reflect data quality differences

4. **Geographic Exclusions**
   - 7 districts excluded due to missing boundaries
   - Represents ~3.4% of districts

### Model Limitations

1. **Prediction Horizon:** Limited to 4-12 weeks ahead
2. **Data Requirements:** Requires recent data for accurate forecasting
3. **Outbreak Definition:** Based on statistical threshold (90th percentile)

### Recommendations

- Interpret predictions as **decision support tools**, not definitive forecasts
- Combine with local epidemiological knowledge
- Update models regularly with new data
- Validate predictions against ground truth
""")

st.markdown("---")

# ============================================================================
# TECHNICAL SPECIFICATIONS
# ============================================================================

st.header("💻 Technical Specifications")

st.markdown("""
### Dashboard Technology

- **Framework:** Streamlit 1.20+
- **Language:** Python 3.9+
- **Visualization:** Plotly, Matplotlib
- **Geospatial:** GeoPandas, Folium

### Key Libraries

```python
streamlit          # Dashboard framework
pandas, numpy      # Data processing
plotly             # Interactive charts
geopandas          # Spatial analysis
scikit-learn       # ML utilities
xgboost, lightgbm  # Gradient boosting models
```

### Performance

- **Data Size:** ~20 MB
- **Load Time:** 2-3 seconds
- **Memory Usage:** ~150 MB (including Streamlit)
- **Caching:** Aggressive data and computation caching
""")

st.markdown("---")

# ============================================================================
# PROJECT TEAM
# ============================================================================

st.header("👥 Project Team")

st.markdown("""
### Developer

**Ishmael Bakpianefene Ayeng (Sire Ayenbi)**
- Institution: African Institute for Mathematical Sciences (AIMS) Cameroon
- Degree: MSc Mathematical Sciences (Data Science specialization)
- Project Duration: 5 months (July - December 2024)

### Partner Organization

**DLMEP/MINSANTE**
- Full Name: Direction de la Lutte contre la Maladie, les Epidémies et les Pandémies
- Ministry: Cameroon Ministry of Public Health
- Role: Data provider, project partner

### Acknowledgments

Special thanks to:
- AIMS Cameroon faculty and staff
- DLMEP/MINSANTE surveillance team
- Cameroon Ministry of Public Health
""")

st.markdown("---")

# ============================================================================
# CONTACT & FEEDBACK
# ============================================================================

st.header("📧 Contact & Feedback")

st.markdown("""
### Report Issues

If you encounter any issues or have suggestions:

1. **Dashboard Bugs:** Report technical issues
2. **Data Questions:** Clarify data interpretation
3. **Feature Requests:** Suggest new analyses or visualizations

### Future Enhancements

Planned improvements include:
- ✅ Climate data integration (when available)
- ✅ Vaccination coverage tracking
- ✅ Mobile-responsive design
- ✅ Real-time data updates
- ✅ Multi-language support (French/English)
""")

st.markdown("---")

# ============================================================================
# VERSION HISTORY
# ============================================================================

st.header("📝 Version History")

st.markdown("""
### Version 1.0 (December 2024)

**Initial Release**
- ✅ Overview page with KPIs
- ✅ Spatial analysis with choropleth maps
- ✅ Temporal analysis with seasonal patterns
- ✅ Data explorer with filters and export
- ✅ Documentation and methodology

**Features:**
- 6 interactive pages
- 20+ visualizations
- Multiple export formats
- Responsive design
""")

st.markdown("---")

# ============================================================================
# REFERENCES
# ============================================================================

st.header("📚 References & Resources")

st.markdown("""
### Key References

1. **WHO Meningitis Guidelines**
   - World Health Organization meningitis control strategies

2. **Spatial Epidemiology**
   - Methods for spatial analysis and hotspot detection

3. **Machine Learning in Public Health**
   - Applications of ML to disease forecasting

4. **Streamlit Documentation**
   - https://docs.streamlit.io

### Learn More

- **AIMS Cameroon:** https://aims-cameroon.org
- **WHO Africa:** https://www.afro.who.int
- **Plotly:** https://plotly.com/python
""")

st.markdown("---")

# ============================================================================
# FOOTER
# ============================================================================

st.info("""
**Disclaimer:** This dashboard is for decision support purposes. All predictions and 
analyses should be interpreted by qualified public health professionals in conjunction 
with local epidemiological knowledge and current field conditions.
""")

st.caption("**Dashboard Version:** 1.0 | **Last Updated:** December 2024")
st.caption("**Developed by:** Sire Ayenbi, AIMS Cameroon | **Partner:** DLMEP/MINSANTE")
