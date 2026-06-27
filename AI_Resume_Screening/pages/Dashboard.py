import sys
import os

# Add the project subfolder to python path for streamlit cloud deployments
project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_dir not in sys.path:
    sys.path.append(project_dir)

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

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

def show_dashboard():
    init_session_state()
    st.markdown("<h2 class='section-header'>📊 Analytics & Progress Dashboard</h2>", unsafe_allow_html=True)
    
    # 1. Check if an analysis has been completed
    if "predicted_category" not in st.session_state or st.session_state.predicted_category is None:
        st.warning("⚠️ No active resume analysis found in session. Please navigate to 'Resume Analysis' and upload a resume first!")
        
        # Display dummy cards and sample data for presentation purposes if empty
        st.markdown("<h3 class='section-header'>📉 Demo Visualization Preview</h3>", unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            dummy_df = pd.DataFrame({
                "Score Type": ["Resume Score", "ATS Score"],
                "Score": [85, 78]
            })
            fig = px.bar(dummy_df, x="Score Type", y="Score", range_y=[0, 100], color="Score Type", 
                         title="Example Resume vs ATS Score Comparison", color_discrete_sequence=["#6366f1", "#10b981"])
            st.plotly_chart(fig, use_container_width=True)
        with col2:
            dummy_pie = pd.DataFrame({
                "Status": ["Present Skills", "Missing Skills"],
                "Count": [12, 5]
            })
            fig_pie = px.pie(dummy_pie, names="Status", values="Count", title="Example Skills Coverage Ratio",
                             color_discrete_sequence=["#10b981", "#ef4444"])
            st.plotly_chart(fig_pie, use_container_width=True)
        return
        
    # Retrieve current analysis metrics
    category = st.session_state.predicted_category
    confidence = st.session_state.prediction_confidence
    resume_score = st.session_state.resume_score
    ats_score = st.session_state.ats_score
    skills_found_cnt = len(st.session_state.skills_found)
    missing_skills_cnt = len(st.session_state.missing_skills)
    projects_cnt = len(st.session_state.recommended_projects)
    
    # 2. KPI Cards Section
    st.markdown("### 🔑 Key Performance Indicators (KPIs)")
    
    k_col1, k_col2, k_col3 = st.columns(3)
    with k_col1:
        st.markdown(f"""
        <div class="metric-card" style="text-align: center;">
            <p style="margin: 0; color: #94a3b8; font-size: 14px; font-weight: 600;">RESUME QUALITY SCORE</p>
            <h2 style="margin: 10px 0; color: #6366f1; font-size: 36px; font-weight: 800;">{resume_score}/100</h2>
            <p style="margin: 0; font-size: 12px; color: #cbd5e1;">Rule-based structural completeness</p>
        </div>
        """, unsafe_allow_html=True)
    with k_col2:
        st.markdown(f"""
        <div class="metric-card" style="text-align: center;">
            <p style="margin: 0; color: #94a3b8; font-size: 14px; font-weight: 600;">ATS ALIGNMENT SCORE</p>
            <h2 style="margin: 10px 0; color: #10b981; font-size: 36px; font-weight: 800;">{ats_score}/100</h2>
            <p style="margin: 0; font-size: 12px; color: #cbd5e1;">Keyword overlap match index</p>
        </div>
        """, unsafe_allow_html=True)
    with k_col3:
        st.markdown(f"""
        <div class="metric-card" style="text-align: center;">
            <p style="margin: 0; color: #94a3b8; font-size: 14px; font-weight: 600;">PREDICTION CONFIDENCE</p>
            <h2 style="margin: 10px 0; color: #818cf8; font-size: 36px; font-weight: 800;">{confidence}%</h2>
            <p style="margin: 0; font-size: 12px; color: #cbd5e1;">Logistic Regression classifier</p>
        </div>
        """, unsafe_allow_html=True)
        
    k_col4, k_col5, k_col6 = st.columns(3)
    with k_col4:
        st.markdown(f"""
        <div class="metric-card" style="text-align: center;">
            <p style="margin: 0; color: #94a3b8; font-size: 14px; font-weight: 600;">SKILLS DETECTED</p>
            <h2 style="margin: 10px 0; color: #38bdf8; font-size: 36px; font-weight: 800;">{skills_found_cnt}</h2>
            <p style="margin: 0; font-size: 12px; color: #cbd5e1;">Extracted from PDF content</p>
        </div>
        """, unsafe_allow_html=True)
    with k_col5:
        st.markdown(f"""
        <div class="metric-card" style="text-align: center;">
            <p style="margin: 0; color: #94a3b8; font-size: 14px; font-weight: 600;">MISSING TARGET SKILLS</p>
            <h2 style="margin: 10px 0; color: #f87171; font-size: 36px; font-weight: 800;">{missing_skills_cnt}</h2>
            <p style="margin: 0; font-size: 12px; color: #cbd5e1;">Gaps mapped against required skills</p>
        </div>
        """, unsafe_allow_html=True)
    with k_col6:
        st.markdown(f"""
        <div class="metric-card" style="text-align: center;">
            <p style="margin: 0; color: #94a3b8; font-size: 14px; font-weight: 600;">RECOMMENDED PROJECTS</p>
            <h2 style="margin: 10px 0; color: #fbbf24; font-size: 36px; font-weight: 800;">{projects_cnt}</h2>
            <p style="margin: 0; font-size: 12px; color: #cbd5e1;">Sourced from projects database</p>
        </div>
        """, unsafe_allow_html=True)
        
    st.markdown(f"**Target Candidate Domain:** `{category}`")
    
    # 3. Interactive Roadmap Progress Tracker
    st.markdown("<h3 class='section-header'>📅 Interactive Learning Roadmap Tracker</h3>", unsafe_allow_html=True)
    st.markdown("Track the 30-day curriculum completion progress:")
    
    # Checkboxes for 4 weeks
    prog_col1, prog_col2, prog_col3, prog_col4 = st.columns(4)
    w1 = prog_col1.checkbox("Week 1 Completed (25%)", value=st.session_state.roadmap_progress >= 25)
    w2 = prog_col2.checkbox("Week 2 Completed (50%)", value=st.session_state.roadmap_progress >= 50)
    w3 = prog_col3.checkbox("Week 3 Completed (75%)", value=st.session_state.roadmap_progress >= 75)
    w4 = prog_col4.checkbox("Week 4 Completed (100%)", value=st.session_state.roadmap_progress == 100)
    
    # Compute progress value
    progress_val = sum([w1, w2, w3, w4]) * 25
    st.session_state.roadmap_progress = progress_val
    
    # Display Progress Bar
    st.progress(progress_val / 100)
    st.markdown(f"**Roadmap Progress Status:** `{progress_val}% Completed`")
    
    # 4. Interactive Plotly Charts
    st.markdown("<h3 class='section-header'>📈 Data Visualizations</h3>", unsafe_allow_html=True)
    
    col_chart1, col_chart2 = st.columns(2)
    
    with col_chart1:
        # Chart 1: Bar Chart comparing Scores
        score_df = pd.DataFrame({
            "Metric Type": ["Resume Quality Score", "ATS Alignment Score"],
            "Value": [resume_score, ats_score]
        })
        fig1 = px.bar(
            score_df, 
            x="Metric Type", 
            y="Value", 
            text="Value",
            range_y=[0, 100],
            color="Metric Type",
            color_discrete_map={"Resume Quality Score": "#6366f1", "ATS Alignment Score": "#10b981"},
            title="Resume Quality Score vs ATS Alignment Score"
        )
        fig1.update_traces(textposition='outside')
        fig1.update_layout(showlegend=False, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color="#cbd5e1")
        st.plotly_chart(fig1, use_container_width=True)
        
    with col_chart2:
        # Chart 2: Pie Chart showing Skills Overlap
        skills_pie_df = pd.DataFrame({
            "Skills Status": ["Matched Skills", "Missing Skills"],
            "Count": [skills_found_cnt, missing_skills_cnt]
        })
        fig2 = px.pie(
            skills_pie_df, 
            names="Skills Status", 
            values="Count",
            color="Skills Status",
            color_discrete_map={"Matched Skills": "#10b981", "Missing Skills": "#ef4444"},
            title="Skills Match Coverage (Matched vs Missing)",
            hole=0.4
        )
        fig2.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color="#cbd5e1")
        st.plotly_chart(fig2, use_container_width=True)
        
    col_chart3, col_chart4 = st.columns(2)
    
    with col_chart3:
        # Chart 3: Confidence Gauge Meter
        fig3 = go.Figure(go.Indicator(
            mode = "gauge+number",
            value = confidence,
            domain = {'x': [0, 1], 'y': [0, 1]},
            title = {'text': "ML Prediction Confidence Index", 'font': {'color': "#cbd5e1", 'size': 16}},
            gauge = {
                'axis': {'range': [0, 100], 'tickwidth': 1, 'tickcolor': "#cbd5e1"},
                'bar': {'color': "#6366f1"},
                'bgcolor': "rgba(255,255,255,0.05)",
                'borderwidth': 2,
                'bordercolor': "rgba(255,255,255,0.1)",
                'steps': [
                    {'range': [0, 40], 'color': '#ef4444'},
                    {'range': [40, 75], 'color': '#eab308'},
                    {'range': [75, 100], 'color': '#10b981'}
                ],
            }
        ))
        fig3.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color="#cbd5e1", height=280)
        st.plotly_chart(fig3, use_container_width=True)
        
    with col_chart4:
        # Chart 4: Session History of Classified Roles
        if st.session_state.history:
            history_df = pd.DataFrame(st.session_state.history)
            history_fig = px.histogram(
                history_df, 
                x="predicted_category",
                color="predicted_category",
                title="Classified Job Categories in Current Session",
                labels={"predicted_category": "Job Domain"}
            )
            history_fig.update_layout(showlegend=False, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color="#cbd5e1", height=280)
            st.plotly_chart(history_fig, use_container_width=True)
        else:
            st.markdown("<div class='metric-card' style='height:280px; display:flex; align-items:center; justify-content:center;'><p style='color:#94a3b8;'>Historical charts appear after screening multiple resumes.</p></div>", unsafe_allow_html=True)

if __name__ == "__main__":
    st.set_page_config(page_title="Dashboard - AI Resume Screening", layout="wide")
    from app import inject_custom_css
    inject_custom_css()
    show_dashboard()
