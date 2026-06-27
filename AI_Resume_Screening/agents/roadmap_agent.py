from typing import List
from utils.prompts import ROADMAP_GENERATOR_PROMPT
from utils.gemini_client import query_gemini

class RoadmapGeneratorAgent:
    """
    Agent responsible for generating a detailed, structured 30-day learning plan (roadmap)
    incorporating weekly modules, mini-projects, practice challenges, and resources.
    """
    
    def __init__(self):
        self.system_instruction = "You are an expert technical curriculum designer and coding bootcamp manager."

    def generate_roadmap(self, predicted_role: str, missing_skills: List[str], suggested_projects: List[str]) -> str:
        """
        Runs the roadmap generation analysis using Google Gemini.
        
        Args:
            predicted_role (str): The candidate's predicted professional role.
            missing_skills (List[str]): List of missing skills.
            suggested_projects (List[str]): Titles/descriptions of recommended projects.
            
        Returns:
            str: 30-day learning roadmap in Markdown format.
        """
        missing_skills_str = ", ".join(missing_skills) if missing_skills else "None"
        projects_str = "; ".join(suggested_projects) if suggested_projects else "None"
        
        # Populate prompt template
        prompt = ROADMAP_GENERATOR_PROMPT.format(
            predicted_role=predicted_role,
            missing_skills=missing_skills_str,
            suggested_projects=projects_str
        )
        
        # Execute query via central gemini client
        response = query_gemini(prompt, system_instruction=self.system_instruction)
        return response
