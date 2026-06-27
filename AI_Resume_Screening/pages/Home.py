import streamlit as st

def show_home():
    # Title Hero
    st.markdown("""
    <div style="text-align: center; padding: 20px 0px 40px 0px;">
        <h1 style="font-size: 3rem; font-weight: 800; background: linear-gradient(90deg, #818cf8, #c084fc); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
            AI Resume Screening Assistant
        </h1>
        <p style="font-size: 1.25rem; color: #94a3b8; max-width: 800px; margin: 0 auto; line-height: 1.6;">
            A hybrid Intelligent Talent Assessment platform merging traditional <b>Supervised Machine Learning</b> with <b>Agentic Generative AI</b> to screen resumes, evaluate suitability, recommend skill paths, and prep candidate interviews.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # 2 Column Layout for Objectives & Overview
    col1, col2 = st.columns(2, gap="large")
    
    with col1:
        st.markdown("<h3 class='section-header'>🎓 Project Objectives</h3>", unsafe_allow_html=True)
        st.markdown("""
        * **Supervised Machine Learning Ingestion**: Classify the candidate's professional domain using a TF-IDF text representation matched against a Logistic Regression model trained on standard Kaggle resume corpora.
        * **Advanced Text Extraction**: Parse raw resumes to capture contact details (name, email, phone) and partition text sections (skills, projects, certifications, work experience, education) via pattern heuristics.
        * **Dual Metric Ingestion**: Compute rule-based scores measuring general completion quality alongside a specialized ATS keyword matching density against target requirements.
        * **Sequential AI Multi-Agents**: Coordinate four specialized LLM agents (Reviewer, Skill Gaps, Learning Roadmap, Mock Interview) to explain classification choices, customize learning modules, and draft interview guides.
        * **Interactive Business Intelligence**: Display metrics and progress trackers in a central dashboard and export talent dossiers into professional PDFs.
        """)
        
    with col2:
        st.markdown("<h3 class='section-header'>🛠️ System Technology Stack</h3>", unsafe_allow_html=True)
        # Display cards
        st.markdown("""
        <div class="metric-card">
            <h4 style="margin:0 0 8px 0; color:#818cf8;">🧠 Machine Learning Pipeline</h4>
            <ul style="margin:0; padding-left:20px; font-size:14px; color:#cbd5e1;">
                <li>TF-IDF Vectorizer (5,000 max features)</li>
                <li>Logistic Regression Classifier (Primary)</li>
                <li>Multinomial Naive Bayes Model (Baseline)</li>
                <li>Accuracy: <b>99.48%</b> | Weighted F1: <b>99.47%</b></li>
            </ul>
        </div>
        <div class="metric-card" style="margin-top:15px;">
            <h4 style="margin:0 0 8px 0; color:#c084fc;">🤖 Agentic AI Module</h4>
            <ul style="margin:0; padding-left:20px; font-size:14px; color:#cbd5e1;">
                <li>Google Gemini API client (gemini-2.5-flash)</li>
                <li>Specialized prompt engineering templates</li>
                <li>Sequential coordinate execution logic</li>
                <li>Hybrid pre-seeded datasets (Skills, Projects, QA)</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    # Architectural block
    st.markdown("<h3 class='section-header'>⚙️ System & Data Pipeline</h3>", unsafe_allow_html=True)
    st.markdown("""
    ```
    Upload Resume PDF  ──►  Extract Raw Text  ──►  Heuristic Section Parsing
                                                             │
    📊 Display Dashboard  ◄──  AI Agents  ◄──  Rule-Based   ◄─┴──  ML Prediction
       & PDF Reports          (LLM reasoning)  Scoring (ATS)      (Logistic Regression)
    ```
    """)
    
    st.info("💡 **Quick Start Guide:** Navigate to the sidebar and click on **Resume Analysis** to upload a PDF resume and start the assessment pipeline!")

if __name__ == "__main__":
    # If run as entry directly
    st.set_page_config(page_title="Home - AI Resume Screening", layout="wide")
    from app import inject_custom_css
    inject_custom_css()
    show_home()
