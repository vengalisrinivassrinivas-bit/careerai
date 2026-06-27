import sys
import os

# Add the project subfolder to python path for streamlit cloud deployments
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.append(current_dir)

import streamlit as st

# Set page config at the very beginning of app.py
st.set_page_config(
    page_title="AI Resume Screening Assistant",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Premium CSS Injection for Dark Mode & Glassmorphic Look
def inject_custom_css():
    st.markdown("""
    <style>
    /* Main Background and text colors */
    .stApp {
        background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 100%);
        color: #f1f5f9;
    }
    
    /* Sidebar styling */
    section[data-testid="stSidebar"] {
        background-color: rgba(15, 23, 42, 0.9) !important;
        border-right: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    /* Card design for metrics and sections */
    .metric-card {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 20px;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
        transition: transform 0.2s ease, border-color 0.2s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-2px);
        border-color: rgba(255, 255, 255, 0.2);
    }
    
    /* Section headers */
    .section-header {
        color: #6366f1;
        font-weight: 700;
        border-bottom: 2px solid rgba(99, 102, 241, 0.3);
        padding-bottom: 8px;
        margin-top: 25px;
        margin-bottom: 15px;
    }
    
    /* Keywords badge layout */
    .keyword-badge {
        display: inline-block;
        background: rgba(99, 102, 241, 0.2);
        color: #a5b4fc;
        padding: 4px 10px;
        margin: 4px;
        border-radius: 20px;
        border: 1px solid rgba(99, 102, 241, 0.4);
        font-size: 13px;
        font-weight: 600;
    }
    
    /* Info badge layout */
    .info-badge {
        display: inline-block;
        background: rgba(16, 185, 129, 0.2);
        color: #a7f3d0;
        padding: 4px 10px;
        margin: 4px;
        border-radius: 20px;
        border: 1px solid rgba(16, 185, 129, 0.4);
        font-size: 13px;
    }
    
    /* Missing badge layout */
    .missing-badge {
        display: inline-block;
        background: rgba(239, 68, 68, 0.2);
        color: #fca5a5;
        padding: 4px 10px;
        margin: 4px;
        border-radius: 20px;
        border: 1px solid rgba(239, 68, 68, 0.4);
        font-size: 13px;
    }
    
    /* Buttons */
    .stButton>button {
        background: linear-gradient(90deg, #4f46e5 0%, #7c3aed 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 10px 24px !important;
        font-weight: 600 !important;
        box-shadow: 0 4px 14px 0 rgba(79, 70, 229, 0.4) !important;
        transition: all 0.3s ease !important;
    }
    
    .stButton>button:hover {
        transform: scale(1.02) !important;
        box-shadow: 0 6px 20px 0 rgba(79, 70, 229, 0.6) !important;
    }
    </style>
    """, unsafe_allow_html=True)

def init_session_state():
    """Initializes session state variables for storage cache."""
    keys = {
        "resume_text": None,
        "parsed_data": None,
        "predicted_category": None,
        "prediction_confidence": 0.0,
        "resume_score": 0,
        "ats_score": 0,
        "skills_found": [],
        "missing_skills": [],
        "recommended_projects": [],
        "xai_keywords": [],
        "reviewer_analysis": None,
        "skills_analysis": None,
        "roadmap_plan": None,
        "interview_prep": None,
        "history": [],
        "roadmap_progress": 0
    }
    for key, default in keys.items():
        if key not in st.session_state:
            st.session_state[key] = default

def main():
    inject_custom_css()
    init_session_state()
    
    # Render Home page content directly on app.py or fallback
    from pages.Home import show_home
    show_home()

if __name__ == "__main__":
    main()
