import sys
import os

# Add the project subfolder to python path for streamlit cloud deployments
project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_dir not in sys.path:
    sys.path.append(project_dir)

import streamlit as st
import pandas as pd
from typing import Dict, List, Any

# Import utilities and agents
from utils.pdf_reader import extract_text_from_pdf, PDFReaderError
from utils.resume_parser import parse_resume
from utils.category_mapper import get_clean_category
from ml.predictor import ResumePredictor
from utils.pdf_report_generator import generate_resume_report_pdf
from utils.gemini_client import query_gemini, GeminiAPIError, MissingAPIKeyError

# Import Agent Classes
from agents.resume_agent import ResumeReviewerAgent
from agents.skill_agent import SkillRecommendationAgent
from agents.roadmap_agent import RoadmapGeneratorAgent
from agents.interview_agent import InterviewPreparationAgent

def calculate_resume_score(parsed_data: Dict[str, Any]) -> int:
    """
    Calculates programmatic Resume Score based on completeness weights:
    Contact Details (Email/Phone) = 15 (5 each for Name, Email, Phone)
    Education = 15
    Experience = 20
    Projects = 20
    Skills = 20
    Certifications = 10
    Total = 100
    """
    score = 0
    # Contact Info (max 15)
    if parsed_data.get("name") and parsed_data.get("name") != "Not Found":
        score += 5
    if parsed_data.get("email") and parsed_data.get("email") != "Not Found":
        score += 5
    if parsed_data.get("phone") and parsed_data.get("phone") != "Not Found":
        score += 5
        
    # Education (max 15)
    if parsed_data.get("education"):
        score += 15
        
    # Experience (max 20)
    if parsed_data.get("experience"):
        score += 20
        
    # Projects (max 20)
    if parsed_data.get("projects"):
        score += 20
        
    # Skills (max 20)
    if parsed_data.get("all_skills"):
        score += 20
        
    # Certifications (max 10)
    if parsed_data.get("certifications"):
        score += 10
        
    return score

def calculate_ats_score(parsed_data: Dict[str, Any], required_skills: List[str]) -> int:
    """
    Calculates programmatic ATS Score based on section presence and skill matches:
    Contact completeness = 10 (5 each for email and phone)
    Experience present = 20
    Education present = 10
    Projects present = 10
    Certifications present = 10
    Required Skill overlap density = 40 (ratio of match vs required skills)
    Total = 100
    """
    score = 0
    # Contact info (max 10)
    if parsed_data.get("email") and parsed_data.get("email") != "Not Found":
        score += 5
    if parsed_data.get("phone") and parsed_data.get("phone") != "Not Found":
        score += 5
        
    # Section markers (max 50)
    if parsed_data.get("experience"):
        score += 20
    if parsed_data.get("education"):
        score += 10
    if parsed_data.get("projects"):
        score += 10
    if parsed_data.get("certifications"):
        score += 10
        
    # Skill overlap (max 40)
    if required_skills:
        candidate_skills_lower = [s.lower() for s in parsed_data.get("all_skills", [])]
        matched_skills = [s for s in required_skills if s.lower() in candidate_skills_lower]
        match_ratio = len(matched_skills) / len(required_skills)
        score += int(match_ratio * 40)
    else:
        # Fallback if no required skills defined
        score += 20
        
    return min(100, score)

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

def show_analysis():
    init_session_state()
    st.markdown("<h2 class='section-header'>🔬 Resume Screening & Assessment</h2>", unsafe_allow_html=True)
    
    # 1. API Key Config in Sidebar
    st.sidebar.markdown("### 🔑 API Authentication")
    gemini_key = st.sidebar.text_input(
        "Google Gemini API Key", 
        type="password", 
        value=os.getenv("GEMINI_API_KEY", ""),
        help="Supply your Gemini API key to run Agentic AI analyses."
    )
    
    if gemini_key:
        os.environ["GEMINI_API_KEY"] = gemini_key
    
    # File Uploader
    uploaded_file = st.file_uploader("Upload Candidate Resume (PDF format)", type=["pdf"])
    
    if uploaded_file is not None:
        try:
            # Check if we need to parse a new file
            file_changed = False
            if "last_uploaded_name" not in st.session_state or st.session_state["last_uploaded_name"] != uploaded_file.name:
                st.session_state["last_uploaded_name"] = uploaded_file.name
                file_changed = True
            
            # Read Text if changed
            if file_changed or st.session_state.resume_text is None:
                with st.spinner("Reading PDF resume content..."):
                    resume_text = extract_text_from_pdf(uploaded_file)
                    st.session_state.resume_text = resume_text
                    
                    # Parse elements
                    parsed_data = parse_resume(resume_text)
                    st.session_state.parsed_data = parsed_data
                    
                    # Clear previous analysis states
                    st.session_state.predicted_category = None
                    st.session_state.reviewer_analysis = None
                    st.session_state.skills_analysis = None
                    st.session_state.roadmap_plan = None
                    st.session_state.interview_prep = None
                    st.session_state.roadmap_progress = 0
            
            # Retrieve cached details
            parsed_data = st.session_state.parsed_data
            
            # 2. Render Parsed Candidate Profile Details (Name, Email, Phone, Sections)
            st.markdown("<h3 class='section-header'>👤 Parsed Profile Details</h3>", unsafe_allow_html=True)
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.markdown(f"**Name:** {parsed_data.get('name')}")
            with col2:
                st.markdown(f"**Email:** {parsed_data.get('email')}")
            with col3:
                st.markdown(f"**Phone:** {parsed_data.get('phone')}")
                
            # Displays extracted sections
            col_left, col_right = st.columns(2)
            with col_left:
                st.markdown("**Education Details:**")
                if parsed_data.get("education"):
                    for edu in parsed_data.get("education")[:3]:
                        st.markdown(f"- {edu}")
                else:
                    st.markdown("*No education details explicitly parsed.*")
                    
                st.markdown("**Projects Listed:**")
                if parsed_data.get("projects"):
                    for proj in parsed_data.get("projects")[:3]:
                        st.markdown(f"- {proj}")
                else:
                    st.markdown("*No projects section explicitly parsed.*")
            
            with col_right:
                st.markdown("**Work Experience:**")
                if parsed_data.get("experience"):
                    for exp in parsed_data.get("experience")[:3]:
                        st.markdown(f"- {exp}")
                else:
                    st.markdown("*No experience section explicitly parsed.*")
                    
                st.markdown("**Certifications:**")
                if parsed_data.get("certifications"):
                    for cert in parsed_data.get("certifications")[:3]:
                        st.markdown(f"- {cert}")
                else:
                    st.markdown("*No certifications explicitly parsed.*")
            
            # Skills Found badges
            st.markdown("**Extracted Skills:**")
            if parsed_data.get("all_skills"):
                badges_html = "".join([f"<span class='keyword-badge'>{s}</span>" for s in parsed_data.get("all_skills")])
                st.markdown(badges_html, unsafe_allow_html=True)
            else:
                st.markdown("*No technology or soft skills parsed.*")
                
            # Trigger Button
            analyze_button = st.button("🚀 Run AI Resume Screening Pipeline")
            
            # If clicked, execute ML prediction & sequential Agents
            if analyze_button:
                if not os.getenv("GEMINI_API_KEY"):
                    st.error("❌ Gemini API Key is missing! Please configure it in the sidebar to run agent assessments.")
                    return
                    
                try:
                    # 1. ML Model Prediction
                    with st.spinner("ML Model: Vectorizing text and predicting domain..."):
                        predictor = ResumePredictor("AI_Resume_Screening/models")
                        prediction_res = predictor.predict(st.session_state.resume_text)
                        
                        raw_category = prediction_res["category"]
                        st.session_state.predicted_category = get_clean_category(raw_category)
                        st.session_state.prediction_confidence = prediction_res["confidence"]
                        st.session_state.xai_keywords = prediction_res["top_keywords"]
                        
                    # Load datasets for mapping
                    skills_df = pd.read_csv("AI_Resume_Screening/data/skills_dataset.csv")
                    projects_df = pd.read_csv("AI_Resume_Screening/data/projects_dataset.csv")
                    questions_df = pd.read_csv("AI_Resume_Screening/data/interview_questions.csv")
                    
                    # 2. Extract required skills and compare
                    row_skills = skills_df[skills_df["Category"] == raw_category]
                    required_skills_list = []
                    if not row_skills.empty:
                        required_skills_list = [s.strip() for s in row_skills.iloc[0]["Skills"].split(",")]
                    
                    candidate_skills_lower = [s.lower() for s in parsed_data.get("all_skills", [])]
                    st.session_state.skills_found = [s for s in parsed_data.get("all_skills", [])]
                    
                    missing = [s for s in required_skills_list if s.lower() not in candidate_skills_lower]
                    st.session_state.missing_skills = missing
                    
                    # 3. Recommended projects
                    rec_projects_rows = projects_df[projects_df["Category"] == raw_category]
                    st.session_state.recommended_projects = rec_projects_rows.to_dict('records')
                    
                    # 4. Programmatic Scores
                    st.session_state.resume_score = calculate_resume_score(parsed_data)
                    st.session_state.ats_score = calculate_ats_score(parsed_data, required_skills_list)
                    
                    # 5. Execute Gemini Agents sequentially
                    # Agent 1: Resume Reviewer
                    with st.spinner("Agent 1: Analyzing resume layout, grammar & ATS friendliness..."):
                        reviewer = ResumeReviewerAgent()
                        review_feedback = reviewer.analyze(
                            parsed_data, 
                            st.session_state.resume_score, 
                            st.session_state.ats_score
                        )
                        st.session_state.reviewer_analysis = review_feedback
                        
                    # Agent 2: Skill gap recommender
                    with st.spinner("Agent 2: Formulating skill acquisition & course pathway..."):
                        skill_agent = SkillRecommendationAgent()
                        skills_feedback = skill_agent.recommend(
                            st.session_state.predicted_category, 
                            st.session_state.skills_found, 
                            st.session_state.missing_skills
                        )
                        st.session_state.skills_analysis = skills_feedback
                        
                    # Agent 3: Roadmap Generator
                    with st.spinner("Agent 3: Constructing 30-day structural calendar roadmap..."):
                        roadmap_agent = RoadmapGeneratorAgent()
                        suggested_proj_titles = [p.get("Project_Name", "") for p in st.session_state.recommended_projects]
                        roadmap_feedback = roadmap_agent.generate_roadmap(
                            st.session_state.predicted_category, 
                            st.session_state.missing_skills, 
                            suggested_proj_titles
                        )
                        st.session_state.roadmap_plan = roadmap_feedback
                        
                    # Agent 4: Interview Preparation Agent
                    with st.spinner("Agent 4: Compiling customized mock technical interview dossier..."):
                        interview_agent = InterviewPreparationAgent()
                        # Extract baseline questions from csv for category
                        cat_questions = questions_df[questions_df["Category"] == raw_category]
                        if cat_questions.empty:
                            # fallback if category mismatch
                            cat_questions = questions_df[questions_df["Category"] == "Python Developer"]
                            
                        baseline_qs_str = ""
                        for idx, q_row in cat_questions.iterrows():
                            baseline_qs_str += f"- [{q_row['Question_Type']} - {q_row['Difficulty']}]: {q_row['Question']}\n"
                            
                        interview_feedback = interview_agent.generate_guide(
                            st.session_state.predicted_role if "predicted_role" in st.session_state else st.session_state.predicted_category,
                            st.session_state.skills_found,
                            parsed_data.get("projects", []),
                            parsed_data.get("experience", []),
                            baseline_qs_str
                        )
                        st.session_state.interview_prep = interview_feedback
                        
                    # Append history record for Dashboard analytics
                    history_entry = {
                        "name": parsed_data.get("name", "Candidate"),
                        "predicted_category": st.session_state.predicted_category,
                        "confidence": st.session_state.prediction_confidence,
                        "resume_score": st.session_state.resume_score,
                        "ats_score": st.session_state.ats_score,
                        "skills_found_count": len(st.session_state.skills_found),
                        "missing_skills_count": len(st.session_state.missing_skills),
                        "projects_count": len(st.session_state.recommended_projects)
                    }
                    st.session_state.history.append(history_entry)
                    st.success("✅ Complete analysis executed successfully!")
                    
                except MissingAPIKeyError as key_err:
                    st.error(f"❌ Gemini API Auth Error: {key_err}")
                except GeminiAPIError as api_err:
                    st.error(f"❌ Agent execution failed: {api_err}")
                except Exception as eval_err:
                    st.error(f"❌ Evaluation Pipeline Error: {eval_err}")
                    
            # 3. Display Analysis Results if session variables exist
            if st.session_state.predicted_category is not None:
                st.markdown("<h3 class='section-header'>📊 Evaluation Summary Dashboard</h3>", unsafe_allow_html=True)
                
                # Metric display
                m_col1, m_col2, m_col3, m_col4 = st.columns(4)
                with m_col1:
                    st.metric(label="Predicted Role Domain", value=st.session_state.predicted_category)
                with m_col2:
                    st.metric(label="Prediction Confidence", value=f"{st.session_state.prediction_confidence}%")
                with m_col3:
                    st.metric(label="Programmatic Resume Score", value=f"{st.session_state.resume_score}/100")
                with m_col4:
                    st.metric(label="ATS Friendliness Score", value=f"{st.session_state.ats_score}/100")
                
                # Tabbed outputs
                tab1, tab2, tab3, tab4, tab5 = st.tabs([
                    "🧠 ML prediction & XAI", 
                    "📝 Resume review", 
                    "🎯 Skill gaps & Projects", 
                    "📅 30-Day learning plan", 
                    "💬 Interview preparation"
                ])
                
                with tab1:
                    st.markdown("#### Classifier Explainable AI (XAI) Keywords")
                    st.markdown("The following keywords from the resume contributed most heavily to the Logistic Regression domain prediction:")
                    
                    if st.session_state.xai_keywords:
                        xai_df = pd.DataFrame(st.session_state.xai_keywords, columns=["Keyword", "Influence Weight"])
                        xai_df = xai_df.sort_values(by="Influence Weight", ascending=False)
                        st.dataframe(xai_df, use_container_width=True)
                        
                        # Display badges in sorted order
                        badges = "".join([f"<span class='keyword-badge'>✓ {kw}</span>" for kw, _ in st.session_state.xai_keywords])
                        st.markdown(badges, unsafe_allow_html=True)
                    else:
                        st.markdown("*No keywords extracted.*")
                        
                with tab2:
                    st.markdown("#### Detailed Resume review")
                    if st.session_state.reviewer_analysis:
                        st.markdown(st.session_state.reviewer_analysis)
                    else:
                        st.markdown("*Review not compiled.*")
                        
                with tab3:
                    st.markdown("#### Skill Gap Analysis & Projects")
                    
                    col_gap1, col_gap2 = st.columns(2)
                    with col_gap1:
                        st.markdown("**Skills Present on Resume:**")
                        if st.session_state.skills_found:
                            badges_found = "".join([f"<span class='info-badge'>{s}</span>" for s in st.session_state.skills_found])
                            st.markdown(badges_found, unsafe_allow_html=True)
                        else:
                            st.markdown("*None identified.*")
                            
                    with col_gap2:
                        st.markdown("**Missing Required Skills:**")
                        if st.session_state.missing_skills:
                            badges_missing = "".join([f"<span class='missing-badge'>{s}</span>" for s in st.session_state.missing_skills])
                            st.markdown(badges_missing, unsafe_allow_html=True)
                        else:
                            st.success("🎉 Excellent! Your profile contains all standard required skills for this domain.")
                            
                    st.markdown("---")
                    st.markdown("#### Recommended Projects (from Projects Database)")
                    if st.session_state.recommended_projects:
                        for idx, proj in enumerate(st.session_state.recommended_projects):
                            st.markdown(f"##### {idx+1}. {proj.get('Project_Name')} (Difficulty: `{proj.get('Difficulty')}`)")
                            st.markdown(f"*{proj.get('Description')}*")
                    else:
                        st.markdown("*No project recommendations cached.*")
                        
                    st.markdown("---")
                    st.markdown("#### Skills Agent Suggestions")
                    if st.session_state.skills_analysis:
                        st.markdown(st.session_state.skills_analysis)
                        
                with tab4:
                    st.markdown("#### Structured 30-Day Learning Plan")
                    if st.session_state.roadmap_plan:
                        st.markdown(st.session_state.roadmap_plan)
                    else:
                        st.markdown("*Roadmap not compiled.*")
                        
                with tab5:
                    st.markdown("#### Mock Interview Preparation Dossier")
                    if st.session_state.interview_prep:
                        st.markdown(st.session_state.interview_prep)
                    else:
                        st.markdown("*Interview guide not compiled.*")
                        
                # Download PDF Report Section
                st.markdown("---")
                st.markdown("### 📥 Export Assessment Dossier")
                st.markdown("Export a comprehensive PDF dossier containing all evaluation metrics, keyword charts, and AI agent roadmaps.")
                
                try:
                    # Package report data
                    report_data = {
                        "name": parsed_data.get("name", "Candidate"),
                        "email": parsed_data.get("email", "N/A"),
                        "phone": parsed_data.get("phone", "N/A"),
                        "predicted_category": st.session_state.predicted_category,
                        "prediction_confidence": st.session_state.prediction_confidence,
                        "resume_score": st.session_state.resume_score,
                        "ats_score": st.session_state.ats_score,
                        "skills_found": st.session_state.skills_found,
                        "missing_skills": st.session_state.missing_skills,
                        "recommended_projects": st.session_state.recommended_projects,
                        "xai_keywords": st.session_state.xai_keywords,
                        "reviewer_analysis": st.session_state.reviewer_analysis,
                        "skills_analysis": st.session_state.skills_analysis,
                        "roadmap_plan": st.session_state.roadmap_plan,
                        "interview_prep": st.session_state.interview_prep
                    }
                    
                    pdf_bytes = generate_resume_report_pdf(report_data)
                    
                    st.download_button(
                        label="📥 Download Candidate Assessment PDF Report",
                        data=pdf_bytes,
                        file_name=f"Resume_Assessment_{parsed_data.get('name', 'Candidate').replace(' ', '_')}.pdf",
                        mime="application/pdf"
                    )
                except Exception as report_err:
                    st.warning(f"Unable to generate downloadable PDF report buffer: {report_err}")
                    
        except PDFReaderError as pdf_err:
            st.error(f"❌ PDF Parser Error: {pdf_err}")
        except Exception as e:
            st.error(f"❌ An unexpected error occurred: {str(e)}")

if __name__ == "__main__":
    st.set_page_config(page_title="Resume Analysis - AI Resume Screening", layout="wide")
    from app import inject_custom_css
    inject_custom_css()
    show_analysis()
