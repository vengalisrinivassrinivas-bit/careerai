from typing import List
from utils.prompts import SKILL_RECOMMENDATION_PROMPT
from utils.gemini_client import query_gemini

class SkillRecommendationAgent:
    """
    Agent responsible for recommending technical skills, certifications,
    and online courses to help candidates bridge the gap for their target job role.
    """
    
    def __init__(self):
        self.system_instruction = "You are a career consultant and developer mentor specialized in advising tech professionals on skill acquisition."

    def recommend(self, predicted_role: str, current_skills: List[str], missing_skills: List[str]) -> str:
        """
        Runs the skill recommendation analysis using Google Gemini.
        
        Args:
            predicted_role (str): The candidate's predicted professional role.
            current_skills (List[str]): List of skills currently present on the resume.
            missing_skills (List[str]): List of skills required for the role but missing from the resume.
            
        Returns:
            str: Skill recommendations in Markdown format.
        """
        current_skills_str = ", ".join(current_skills) if current_skills else "None detected"
        missing_skills_str = ", ".join(missing_skills) if missing_skills else "None found"
        
        # Populate prompt template
        prompt = SKILL_RECOMMENDATION_PROMPT.format(
            predicted_role=predicted_role,
            current_skills=current_skills_str,
            missing_skills=missing_skills_str
        )
        
        # Execute query via central gemini client
        response = query_gemini(prompt, system_instruction=self.system_instruction)
        return response
