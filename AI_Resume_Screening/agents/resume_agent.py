from typing import Dict, Any
from utils.prompts import RESUME_REVIEWER_PROMPT
from utils.gemini_client import query_gemini

class ResumeReviewerAgent:
    """
    Agent responsible for reviewing the resume content, identifying strengths,
    weaknesses, formatting suggestions, grammar, and ATS optimization tips.
    It explains the rule-based scores qualitatively.
    """
    
    def __init__(self):
        self.system_instruction = "You are a professional resume writer and recruitment specialist helping candidates improve their job prospects."

    def analyze(self, parsed_resume: Dict[str, Any], resume_score: int, ats_score: int) -> str:
        """
        Runs the resume reviewer analysis using Google Gemini.
        
        Args:
            parsed_resume (Dict[str, Any]): Dictionary of candidate resume attributes.
            resume_score (int): Programmatic Resume Score.
            ats_score (int): Programmatic ATS Score.
            
        Returns:
            str: Review feedback in Markdown format.
        """
        # Format list variables for prompt injection
        skills_str = ", ".join(parsed_resume.get("all_skills", [])) if parsed_resume.get("all_skills") else "None detected"
        education_str = "; ".join(parsed_resume.get("education", [])) if parsed_resume.get("education") else "None detected"
        experience_str = "; ".join(parsed_resume.get("experience", [])) if parsed_resume.get("experience") else "None detected"
        projects_str = "; ".join(parsed_resume.get("projects", [])) if parsed_resume.get("projects") else "None detected"
        certs_str = ", ".join(parsed_resume.get("certifications", [])) if parsed_resume.get("certifications") else "None detected"
        
        # Populate prompt template
        prompt = RESUME_REVIEWER_PROMPT.format(
            name=parsed_resume.get("name", "Candidate"),
            email=parsed_resume.get("email", "N/A"),
            phone=parsed_resume.get("phone", "N/A"),
            skills=skills_str,
            education=education_str,
            experience=experience_str,
            projects=projects_str,
            certifications=certs_str,
            resume_score=resume_score,
            ats_score=ats_score
        )
        
        # Execute query via central gemini client
        response = query_gemini(prompt, system_instruction=self.system_instruction)
        return response
