from fpdf import FPDF
from typing import Dict, Any

class ResumeReportPDF(FPDF):
    """
    Subclass of FPDF to design a structured layout for the PDF report.
    """
    
    def header(self):
        # Draw header band
        self.set_fill_color(26, 54, 93)  # Dark Blue Accent
        self.rect(0, 0, 210, 25, 'F')
        
        # Header Title
        self.set_y(5)
        self.set_font('helvetica', 'B', 16)
        self.set_text_color(255, 255, 255)
        self.cell(0, 15, 'AI RESUME SCREENING & ASSESSMENT REPORT', 0, 1, 'C')
        self.set_text_color(0, 0, 0)
        self.ln(10)

    def footer(self):
        # Set footer position
        self.set_y(-15)
        self.set_font('helvetica', 'I', 8)
        self.set_text_color(128, 128, 128)
        self.cell(0, 10, f'Page {self.page_no()}/{{nb}} | Confidential Talent Assessment', 0, 0, 'C')

def clean_for_pdf(text: str) -> str:
    """
    Cleans string contents, stripping unrecognized characters to prevent Latin-1 encoding errors
    commonly encountered in standard FPDF installations.
    
    Args:
        text (str): Input text string.
        
    Returns:
        str: Latin-1 compatible clean string.
    """
    if not isinstance(text, str):
        return ""
        
    # Replace common markdown/unicode symbols with ASCII representations
    replacements = {
        "•": "-", "✓": "[x]", "✔": "[x]", "★": "*", "▪": "-", "○": "-",
        "“": '"', "”": '"', "‘": "'", "’": "'", "—": "-", "–": "-",
        "\\u2022": "-", "\\u2713": "[x]", "…": "...", "→": "->"
    }
    
    cleaned = text
    for old, new in replacements.items():
        cleaned = cleaned.replace(old, new)
        
    # Remove emojis or other symbols by encoding and ignoring non-latin1 characters
    try:
        cleaned = cleaned.encode("latin-1", errors="ignore").decode("latin-1")
    except Exception:
        # Fallback: strip all non-ASCII
        cleaned = cleaned.encode("ascii", errors="ignore").decode("ascii")
        
    return cleaned

def generate_resume_report_pdf(data: Dict[str, Any]) -> bytes:
    """
    Assembles structural candidate data, ML predictions, scores, and Gemini output,
    compiling it into a professional, printable PDF document.
    
    Args:
        data (Dict[str, Any]): Dictionary containing candidate profile, scores, predictions,
                               and agent analysis texts.
                               
    Returns:
        bytes: Compiled PDF byte buffer.
    """
    # Create PDF instance (Portrait, mm, A4 size)
    pdf = ResumeReportPDF(orientation='P', unit='mm', format='A4')
    pdf.alias_nb_pages()
    pdf.add_page()
    
    # --- CANDIDATE DETAIL CARD ---
    pdf.set_font('helvetica', 'B', 12)
    pdf.set_text_color(26, 54, 93)  # Primary Color
    pdf.cell(0, 8, "CANDIDATE INFORMATION", 0, 1, 'L')
    pdf.set_text_color(0, 0, 0)
    pdf.set_draw_color(26, 54, 93)
    pdf.line(pdf.get_x(), pdf.get_y(), pdf.get_x() + 190, pdf.get_y())
    pdf.ln(3)
    
    pdf.set_font('helvetica', '', 10)
    # Get values
    name = clean_for_pdf(data.get("name", "N/A"))
    email = clean_for_pdf(data.get("email", "N/A"))
    phone = clean_for_pdf(data.get("phone", "N/A"))
    
    pdf.cell(95, 6, f"Name: {name}", 0, 0)
    pdf.cell(95, 6, f"Email: {email}", 0, 1)
    pdf.cell(95, 6, f"Phone: {phone}", 0, 1)
    pdf.ln(5)
    
    # --- ASSESSMENT SCORES & PREDICTIONS ---
    pdf.set_font('helvetica', 'B', 12)
    pdf.set_text_color(26, 54, 93)
    pdf.cell(0, 8, "PREDICTION & SCREENING METRICS", 0, 1, 'L')
    pdf.set_text_color(0, 0, 0)
    pdf.line(pdf.get_x(), pdf.get_y(), pdf.get_x() + 190, pdf.get_y())
    pdf.ln(3)
    
    category = clean_for_pdf(data.get("predicted_category", "N/A"))
    confidence = data.get("prediction_confidence", 0.0)
    resume_score = data.get("resume_score", 0)
    ats_score = data.get("ats_score", 0)
    
    pdf.set_font('helvetica', 'B', 10)
    pdf.cell(95, 6, f"Predicted Domain: {category}", 0, 0)
    pdf.cell(95, 6, f"Classifier Confidence: {confidence}%", 0, 1)
    
    pdf.set_font('helvetica', '', 10)
    pdf.cell(95, 6, f"Programmatic Resume Score: {resume_score}/100", 0, 0)
    pdf.cell(95, 6, f"ATS Friendliness Index: {ats_score}/100", 0, 1)
    
    # Clean up XAI keywords
    xai_keywords = [f"{clean_for_pdf(kw)} ({round(wt, 2)})" for kw, wt in data.get("xai_keywords", [])]
    xai_str = ", ".join(xai_keywords) if xai_keywords else "N/A"
    pdf.set_font('helvetica', 'I', 9)
    pdf.multi_cell(0, 5, f"Explainable AI (XAI) Influential Keywords: {xai_str}")
    pdf.ln(5)
    
    # --- SKILLS MATRIX ---
    pdf.set_font('helvetica', 'B', 12)
    pdf.set_text_color(26, 54, 93)
    pdf.cell(0, 8, "SKILLS ASSESSMENT", 0, 1, 'L')
    pdf.set_text_color(0, 0, 0)
    pdf.line(pdf.get_x(), pdf.get_y(), pdf.get_x() + 190, pdf.get_y())
    pdf.ln(3)
    
    parsed_skills = [clean_for_pdf(sk) for sk in data.get("skills_found", [])]
    missing_skills = [clean_for_pdf(sk) for sk in data.get("missing_skills", [])]
    
    pdf.set_font('helvetica', 'B', 10)
    pdf.cell(0, 5, "Extracted Profile Skills:", 0, 1)
    pdf.set_font('helvetica', '', 9)
    pdf.multi_cell(0, 5, ", ".join(parsed_skills) if parsed_skills else "None found")
    pdf.ln(2)
    
    pdf.set_font('helvetica', 'B', 10)
    pdf.cell(0, 5, "Target Role Gap (Missing Skills):", 0, 1)
    pdf.set_font('helvetica', '', 9)
    pdf.multi_cell(0, 5, ", ".join(missing_skills) if missing_skills else "None! Profile matches role standards.")
    pdf.ln(5)
    
    # --- RECOMMENDED PROJECTS ---
    pdf.set_font('helvetica', 'B', 12)
    pdf.set_text_color(26, 54, 93)
    pdf.cell(0, 8, "RECOMMENDED PROJECTS", 0, 1, 'L')
    pdf.set_text_color(0, 0, 0)
    pdf.line(pdf.get_x(), pdf.get_y(), pdf.get_x() + 190, pdf.get_y())
    pdf.ln(3)
    
    recommended_projects = data.get("recommended_projects", [])
    if recommended_projects:
        pdf.set_font('helvetica', '', 9)
        for proj in recommended_projects:
            title = clean_for_pdf(proj.get("Project_Name", "Project"))
            desc = clean_for_pdf(proj.get("Description", ""))
            diff = clean_for_pdf(proj.get("Difficulty", "Medium"))
            pdf.set_font('helvetica', 'B', 9)
            pdf.cell(0, 5, f"- {title} ({diff})", 0, 1)
            pdf.set_font('helvetica', '', 9)
            pdf.multi_cell(0, 4, desc)
            pdf.ln(1)
    else:
        pdf.set_font('helvetica', '', 9)
        pdf.cell(0, 5, "No specific project recommendations available.", 0, 1)
    pdf.ln(5)
    
    # --- AGENT REPORTS (Starts on new page for clean spacing) ---
    pdf.add_page()
    
    # 1. Resume Review Agent Output
    pdf.set_font('helvetica', 'B', 12)
    pdf.set_text_color(26, 54, 93)
    pdf.cell(0, 8, "EXPERT RESUME REVIEW (AI Reviewer Agent)", 0, 1, 'L')
    pdf.set_text_color(0, 0, 0)
    pdf.line(pdf.get_x(), pdf.get_y(), pdf.get_x() + 190, pdf.get_y())
    pdf.ln(3)
    
    pdf.set_font('helvetica', '', 9.5)
    review_text = clean_for_pdf(data.get("reviewer_analysis", "Review analysis not completed."))
    pdf.multi_cell(0, 5, review_text)
    pdf.ln(5)
    
    # 2. Skill Recommendation Agent Output
    pdf.set_font('helvetica', 'B', 12)
    pdf.set_text_color(26, 54, 93)
    pdf.cell(0, 8, "SKILLS RECOMMENDATION DETAILS (AI Skills Agent)", 0, 1, 'L')
    pdf.set_text_color(0, 0, 0)
    pdf.line(pdf.get_x(), pdf.get_y(), pdf.get_x() + 190, pdf.get_y())
    pdf.ln(3)
    
    pdf.set_font('helvetica', '', 9.5)
    skills_recom_text = clean_for_pdf(data.get("skills_analysis", "Skills recommendations not completed."))
    pdf.multi_cell(0, 5, skills_recom_text)
    pdf.ln(5)
    
    # --- ROADMAP & INTERVIEW (New page) ---
    pdf.add_page()
    
    # 3. 30-Day Learning Plan
    pdf.set_font('helvetica', 'B', 12)
    pdf.set_text_color(26, 54, 93)
    pdf.cell(0, 8, "30-DAY LEARNING ROADMAP (AI Roadmap Agent)", 0, 1, 'L')
    pdf.set_text_color(0, 0, 0)
    pdf.line(pdf.get_x(), pdf.get_y(), pdf.get_x() + 190, pdf.get_y())
    pdf.ln(3)
    
    pdf.set_font('helvetica', '', 9)
    roadmap_text = clean_for_pdf(data.get("roadmap_plan", "Roadmap plan not completed."))
    pdf.multi_cell(0, 4.5, roadmap_text)
    pdf.ln(5)
    
    # 4. Interview Preparation Guide
    pdf.add_page()
    pdf.set_font('helvetica', 'B', 12)
    pdf.set_text_color(26, 54, 93)
    pdf.cell(0, 8, "INTERVIEW PREPARATION GUIDE (AI Interview Agent)", 0, 1, 'L')
    pdf.set_text_color(0, 0, 0)
    pdf.line(pdf.get_x(), pdf.get_y(), pdf.get_x() + 190, pdf.get_y())
    pdf.ln(3)
    
    pdf.set_font('helvetica', '', 9)
    interview_text = clean_for_pdf(data.get("interview_prep", "Interview prep questions not completed."))
    pdf.multi_cell(0, 4.5, interview_text)
    
    # Output PDF as byte string
    pdf_bytes = pdf.output()
    # In newer fpdf2 versions, output() returns bytes if no dest is set.
    # To ensure it is returned as bytes, let's cast or return appropriately.
    if isinstance(pdf_bytes, str):
        return pdf_bytes.encode('latin-1')
    return bytes(pdf_bytes)
