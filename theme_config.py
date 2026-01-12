"""
================================================================================
THEME CONFIGURATION MODULE
================================================================================

This module provides theme/color customization for the dashboard.
Users can select from predefined themes or create custom colors.

Themes available:
1. Professional Blue (Default) - Medical/healthcare standard
2. Dark Mode - Low light environments
3. Green Health - Alternative medical theme
4. Warm Sunset - Warm, inviting colors
5. High Contrast - Accessibility-focused
6. Custom - User-defined colors

================================================================================
"""

import streamlit as st

# ============================================================================
# THEME DEFINITIONS
# ============================================================================

THEMES = {
    "Professional Blue (Default)": {
        "name": "Professional Blue",
        "description": "Clean, medical-appropriate design (recommended)",
        "colors": {
            # Backgrounds
            "bg_primary": "#FFFFFF",
            "bg_secondary": "#F8F9FA",
            "bg_sidebar": "#F0F2F6",
            
            # Text
            "text_primary": "#262730",
            "text_secondary": "#6C757D",
            
            # Accent
            "primary": "#1f77b4",
            "secondary": "#2C3E50",
            
            # Status
            "success": "#28A745",
            "warning": "#FFC107",
            "danger": "#DC3545",
            "info": "#17A2B8",
            
            # Charts
            "cases_color": "#1f77b4",
            "deaths_color": "#d62728",
            "cfr_color": "#ff7f0e",
        }
    },
    
    "Dark Mode": {
        "name": "Dark Mode",
        "description": "Dark theme for low-light environments",
        "colors": {
            # Backgrounds
            "bg_primary": "#0E1117",
            "bg_secondary": "#1E2128",
            "bg_sidebar": "#262730",
            
            # Text
            "text_primary": "#FAFAFA",
            "text_secondary": "#B0B0B0",
            
            # Accent
            "primary": "#4A9EFF",
            "secondary": "#3D5A80",
            
            # Status
            "success": "#2ECC71",
            "warning": "#F39C12",
            "danger": "#E74C3C",
            "info": "#3498DB",
            
            # Charts
            "cases_color": "#4A9EFF",
            "deaths_color": "#E74C3C",
            "cfr_color": "#F39C12",
        }
    },
    
    "Green Health": {
        "name": "Green Health",
        "description": "Nature-inspired medical theme",
        "colors": {
            # Backgrounds
            "bg_primary": "#FFFFFF",
            "bg_secondary": "#F0F8F0",
            "bg_sidebar": "#E8F5E8",
            
            # Text
            "text_primary": "#1B5E20",
            "text_secondary": "#558B2F",
            
            # Accent
            "primary": "#2E7D32",
            "secondary": "#388E3C",
            
            # Status
            "success": "#4CAF50",
            "warning": "#FF9800",
            "danger": "#F44336",
            "info": "#00BCD4",
            
            # Charts
            "cases_color": "#2E7D32",
            "deaths_color": "#F44336",
            "cfr_color": "#FF9800",
        }
    },
    
    "Warm Sunset": {
        "name": "Warm Sunset",
        "description": "Warm, inviting color palette",
        "colors": {
            # Backgrounds
            "bg_primary": "#FFFBF5",
            "bg_secondary": "#FFF4E6",
            "bg_sidebar": "#FFE8CC",
            
            # Text
            "text_primary": "#5D4037",
            "text_secondary": "#8D6E63",
            
            # Accent
            "primary": "#E65100",
            "secondary": "#BF360C",
            
            # Status
            "success": "#66BB6A",
            "warning": "#FFA726",
            "danger": "#EF5350",
            "info": "#42A5F5",
            
            # Charts
            "cases_color": "#E65100",
            "deaths_color": "#C62828",
            "cfr_color": "#F57C00",
        }
    },
    
    "High Contrast": {
        "name": "High Contrast",
        "description": "Maximum readability for accessibility",
        "colors": {
            # Backgrounds
            "bg_primary": "#FFFFFF",
            "bg_secondary": "#F0F0F0",
            "bg_sidebar": "#E0E0E0",
            
            # Text
            "text_primary": "#000000",
            "text_secondary": "#333333",
            
            # Accent
            "primary": "#0000FF",
            "secondary": "#000080",
            
            # Status
            "success": "#008000",
            "warning": "#FF8C00",
            "danger": "#FF0000",
            "info": "#0000CD",
            
            # Charts
            "cases_color": "#0000FF",
            "deaths_color": "#FF0000",
            "cfr_color": "#FF8C00",
        }
    },
}


# ============================================================================
# THEME FUNCTIONS
# ============================================================================

def get_theme(theme_name):
    """
    Get theme configuration by name
    
    Args:
        theme_name: Name of the theme
        
    Returns:
        Dictionary of theme colors
    """
    if theme_name in THEMES:
        return THEMES[theme_name]["colors"]
    else:
        # Return default theme
        return THEMES["Professional Blue (Default)"]["colors"]


def generate_css(theme_colors):
    """
    Generate CSS based on theme colors
    
    Args:
        theme_colors: Dictionary of color values
        
    Returns:
        String containing CSS styles
    """
    
    css = f"""
    <style>
        /* ===== MAIN LAYOUT ===== */
        
        /* Main background */
        .main {{
            background-color: {theme_colors['bg_primary']};
            color: {theme_colors['text_primary']};
        }}
        
        /* Sidebar styling */
        [data-testid="stSidebar"] {{
            background-color: {theme_colors['bg_sidebar']};
        }}
        
        /* ===== HEADER STYLING ===== */
        
        /* Custom dashboard header with gradient */
        .dashboard-header {{
            background: linear-gradient(135deg, {theme_colors['primary']} 0%, {theme_colors['secondary']} 100%);
            color: white;
            padding: 2rem;
            border-radius: 10px;
            margin-bottom: 2rem;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            text-align: center;
        }}
        
        .dashboard-header h1 {{
            color: white;
            margin: 0;
            font-size: 2.5rem;
            font-weight: 700;
        }}
        
        .dashboard-header p {{
            color: #E8E8E8;
            margin-top: 0.5rem;
            font-size: 1.1rem;
        }}
        
        /* ===== METRIC CARDS ===== */
        
        /* Style metric values */
        [data-testid="stMetricValue"] {{
            color: {theme_colors['primary']};
            font-weight: 600;
            font-size: 2rem;
        }}
        
        /* Style metric labels */
        [data-testid="stMetricLabel"] {{
            color: {theme_colors['text_primary']};
            font-weight: 500;
        }}
        
        /* ===== TEXT COLORS ===== */
        
        h1, h2, h3, h4, h5, h6 {{
            color: {theme_colors['text_primary']};
        }}
        
        p, span, div {{
            color: {theme_colors['text_primary']};
        }}
        
        /* ===== CARDS & CONTAINERS ===== */
        
        /* Card backgrounds */
        .metric-card {{
            background-color: {theme_colors['bg_secondary']};
            border-radius: 10px;
            padding: 1.5rem;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            margin-bottom: 1rem;
        }}
        
        /* Info boxes */
        .info-box {{
            background-color: {theme_colors['info']}22;
            border-left: 5px solid {theme_colors['info']};
            padding: 1rem;
            border-radius: 5px;
            margin: 1rem 0;
        }}
        
        /* Warning boxes */
        .warning-box {{
            background-color: {theme_colors['warning']}22;
            border-left: 5px solid {theme_colors['warning']};
            padding: 1rem;
            border-radius: 5px;
            margin: 1rem 0;
        }}
        
        /* Danger/Alert boxes */
        .alert-box {{
            background-color: {theme_colors['danger']}22;
            border-left: 5px solid {theme_colors['danger']};
            padding: 1rem;
            border-radius: 5px;
            margin: 1rem 0;
        }}
        
        /* Success boxes */
        .success-box {{
            background-color: {theme_colors['success']}22;
            border-left: 5px solid {theme_colors['success']};
            padding: 1rem;
            border-radius: 5px;
            margin: 1rem 0;
        }}
        
        /* ===== BUTTONS ===== */
        
        /* Primary button styling */
        .stButton>button {{
            background-color: {theme_colors['primary']};
            color: white;
            border-radius: 5px;
            padding: 0.5rem 2rem;
            border: none;
            font-weight: 600;
            transition: all 0.3s;
        }}
        
        .stButton>button:hover {{
            background-color: {theme_colors['secondary']};
            box-shadow: 0 4px 8px rgba(0,0,0,0.2);
            transform: translateY(-2px);
        }}
        
        /* Download button */
        .stDownloadButton>button {{
            background-color: {theme_colors['success']};
            color: white;
            border-radius: 5px;
            padding: 0.5rem 2rem;
            border: none;
            font-weight: 600;
        }}
        
        .stDownloadButton>button:hover {{
            background-color: {theme_colors['success']}DD;
            box-shadow: 0 4px 8px rgba(0,0,0,0.2);
        }}
        
        /* ===== DATA TABLES ===== */
        
        /* Dataframe styling */
        .dataframe {{
            font-size: 0.9rem;
            border-radius: 5px;
        }}
        
        /* Table headers */
        .dataframe thead tr th {{
            background-color: {theme_colors['primary']} !important;
            color: white !important;
            font-weight: 600 !important;
        }}
        
        /* ===== ALERTS (STREAMLIT NATIVE) ===== */
        
        /* Success alerts */
        .element-container div[data-testid="stAlert"][data-baseweb="notification"] {{
            background-color: {theme_colors['success']}22;
        }}
        
        /* Info alerts */
        .element-container div[data-testid="stInfo"] {{
            background-color: {theme_colors['info']}22;
        }}
        
        /* Warning alerts */
        .element-container div[data-testid="stWarning"] {{
            background-color: {theme_colors['warning']}22;
        }}
        
        /* Error alerts */
        .element-container div[data-testid="stError"] {{
            background-color: {theme_colors['danger']}22;
        }}
        
        /* ===== SECTION DIVIDERS ===== */
        
        hr {{
            border: none;
            border-top: 2px solid {theme_colors['bg_secondary']};
            margin: 2rem 0;
        }}
        
        /* ===== SIDEBAR ENHANCEMENTS ===== */
        
        /* Sidebar title */
        [data-testid="stSidebar"] h1 {{
            color: {theme_colors['primary']};
            font-size: 1.5rem;
        }}
        
        /* Sidebar section headers */
        [data-testid="stSidebar"] h2,
        [data-testid="stSidebar"] h3 {{
            color: {theme_colors['secondary']};
            font-size: 1.2rem;
            margin-top: 1rem;
        }}
        
        /* Sidebar text */
        [data-testid="stSidebar"] p,
        [data-testid="stSidebar"] span,
        [data-testid="stSidebar"] label {{
            color: {theme_colors['text_primary']};
        }}
        
        /* ===== EXPANDER STYLING ===== */
        
        .streamlit-expanderHeader {{
            background-color: {theme_colors['bg_secondary']};
            border-radius: 5px;
            font-weight: 600;
            color: {theme_colors['text_primary']};
        }}
        
        /* ===== SELECT BOX / INPUT STYLING ===== */
        
        /* Input fields */
        .stTextInput input,
        .stNumberInput input,
        .stSelectbox select {{
            background-color: {theme_colors['bg_secondary']};
            color: {theme_colors['text_primary']};
            border-color: {theme_colors['primary']}44;
        }}
        
        /* ===== SLIDER STYLING ===== */
        
        /* Slider track */
        .stSlider [data-baseweb="slider"] {{
            background-color: {theme_colors['primary']}44;
        }}
        
        /* Slider thumb */
        .stSlider [data-baseweb="slider"] > div > div {{
            background-color: {theme_colors['primary']};
        }}
        
        /* ===== RESPONSIVE DESIGN ===== */
        
        /* Ensure content is readable on smaller screens */
        @media (max-width: 768px) {{
            .dashboard-header h1 {{
                font-size: 1.8rem;
            }}
            
            .dashboard-header p {{
                font-size: 0.9rem;
            }}
        }}
        
    </style>
    """
    
    return css


def apply_theme(theme_name):
    """
    Apply selected theme to the dashboard
    
    Args:
        theme_name: Name of theme to apply
    """
    theme_colors = get_theme(theme_name)
    css = generate_css(theme_colors)
    st.markdown(css, unsafe_allow_html=True)
    
    # Store theme colors in session state for access by charts
    st.session_state['theme_colors'] = theme_colors


def get_chart_colors():
    """
    Get current theme colors for charts
    
    Returns:
        Dictionary of chart colors, or defaults if no theme selected
    """
    if 'theme_colors' in st.session_state:
        return st.session_state['theme_colors']
    else:
        # Return default theme colors
        return THEMES["Professional Blue (Default)"]["colors"]


def theme_selector_sidebar():
    """
    Add theme selector to sidebar
    
    This function should be called in the sidebar of each page
    """
    st.sidebar.markdown("---")
    st.sidebar.subheader("🎨 Theme Settings")
    
    # Theme selector
    theme_options = list(THEMES.keys())
    
    # Get current theme from session state, or use default
    if 'selected_theme' not in st.session_state:
        st.session_state['selected_theme'] = "Professional Blue (Default)"
    
    selected_theme = st.sidebar.selectbox(
        "Select Theme",
        options=theme_options,
        index=theme_options.index(st.session_state['selected_theme']),
        help="Choose a color theme for the dashboard",
        key='theme_selector'
    )
    
    # Update session state
    st.session_state['selected_theme'] = selected_theme
    
    # Show theme description
    theme_desc = THEMES[selected_theme]["description"]
    st.sidebar.caption(f"*{theme_desc}*")
    
    # Preview colors
    with st.sidebar.expander("🎨 Preview Colors"):
        theme_colors = get_theme(selected_theme)
        
        st.markdown("**Primary Colors:**")
        st.markdown(f"""
        <div style="background-color: {theme_colors['primary']}; color: white; padding: 0.5rem; border-radius: 5px; margin: 0.25rem 0;">
            Primary: {theme_colors['primary']}
        </div>
        <div style="background-color: {theme_colors['secondary']}; color: white; padding: 0.5rem; border-radius: 5px; margin: 0.25rem 0;">
            Secondary: {theme_colors['secondary']}
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("**Status Colors:**")
        st.markdown(f"""
        <div style="background-color: {theme_colors['success']}; color: white; padding: 0.5rem; border-radius: 5px; margin: 0.25rem 0;">
            Success: {theme_colors['success']}
        </div>
        <div style="background-color: {theme_colors['warning']}; color: white; padding: 0.5rem; border-radius: 5px; margin: 0.25rem 0;">
            Warning: {theme_colors['warning']}
        </div>
        <div style="background-color: {theme_colors['danger']}; color: white; padding: 0.5rem; border-radius: 5px; margin: 0.25rem 0;">
            Danger: {theme_colors['danger']}
        </div>
        """, unsafe_allow_html=True)
    
    # Apply the selected theme
    apply_theme(selected_theme)
    
    return selected_theme


# ============================================================================
# EXAMPLE USAGE
# ============================================================================

if __name__ == "__main__":
    st.set_page_config(page_title="Theme Demo", layout="wide")
    
    # Add theme selector to sidebar
    selected_theme = theme_selector_sidebar()
    
    # Demo content
    st.title("🎨 Theme Demonstration")
    
    st.info(f"Current theme: **{selected_theme}**")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Cases", "10,485", "+5%")
    
    with col2:
        st.metric("Total Deaths", "436", "-2%")
    
    with col3:
        st.metric("CFR", "4.16%", "-0.3%")
    
    st.success("✅ This is a success message")
    st.warning("⚠️ This is a warning message")
    st.error("❌ This is an error message")
    st.info("ℹ️ This is an info message")
    
    st.button("Click Me")
    st.download_button("Download", data="test", file_name="test.txt")
