from typing import List
from utils.prompts import INTERVIEW_PREP_PROMPT
from utils.gemini_client import query_gemini

class InterviewPreparationAgent:
    """
    Agent responsible for generating a mock interview guide, personalizing baseline questions
    from the offline database using candidate projects and experience details.
    """
    
    def __init__(self):
        self.system_instruction = "You are a senior engineering manager and a professional tech industry interviewer."

    def generate_guide(self, predicted_role: str, skills: List[str], projects: List[str], experience: List[str], baseline_questions: str) -> str:
        """
        Runs the interview guide personalization using Google Gemini.
        
        Args:
            predicted_role (str): The candidate's predicted professional role.
            skills (List[str]): List of candidate skills.
            projects (List[str]): List of candidate projects.
            experience (List[str]): List of candidate experience elements.
            baseline_questions (str): Formatted questions from interview_questions.csv database.
            
        Returns:
            str: Personalized interview guide in Markdown format.
        """
        skills_str = ", ".join(skills) if skills else "None detected"
        projects_str = "; ".join(projects) if projects else "None detected"
        experience_str = "; ".join(experience) if experience else "None detected"
        
        # Populate prompt template
        prompt = INTERVIEW_PREP_PROMPT.format(
            predicted_role=predicted_role,
            skills=skills_str,
            projects=projects_str,
            experience=experience_str,
            baseline_questions=baseline_questions
        )
        
        # Execute query via central gemini client
        response = query_gemini(prompt, system_instruction=self.system_instruction)
        return response
