import os
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables relative to the project directory
current_dir = os.path.dirname(os.path.abspath(__file__))
project_dir = os.path.dirname(current_dir)
load_dotenv(os.path.join(project_dir, '.env'))
# Also fallback to default load_dotenv for global environment variables
load_dotenv()

class GeminiAPIError(Exception):
    """Exception raised for errors in calling the Google Gemini API."""
    pass

class MissingAPIKeyError(GeminiAPIError):
    """Exception raised when the GEMINI_API_KEY environment variable is missing."""
    pass

def init_gemini_client():
    """
    Checks for the existence of GEMINI_API_KEY and configures the google-generativeai package.
    
    Raises:
        MissingAPIKeyError: If API key is not set.
    """
    # Fetch key from environment or streamlit secrets (as fallback)
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        try:
            import streamlit as st
            if "GEMINI_API_KEY" in st.secrets:
                api_key = st.secrets["GEMINI_API_KEY"]
        except Exception:
            pass
            
    # If not in env or secrets, check if it's set in streamlit session or local config (handled dynamically by calling app)
    if not api_key:
        raise MissingAPIKeyError(
            "GEMINI_API_KEY is not configured. Please create a `.env` file in the "
            "project directory and add: GEMINI_API_KEY=your_key_here, or set it as an "
            "environment variable."
        )
        
    genai.configure(api_key=api_key)

def query_gemini(prompt: str, system_instruction: str = None) -> str:
    """
    Sends a query prompt to Google Gemini API using gemini-2.5-flash model.
    
    Args:
        prompt (str): The prompt text containing details for the agent.
        system_instruction (str, optional): System instructions for model behavior.
        
    Returns:
        str: Response text from the model.
        
    Raises:
        GeminiAPIError: If the API fails.
    """
    # Ensure client is initialized
    init_gemini_client()
    
    try:
        # Create model configuration
        model_name = "gemini-2.5-flash"
        
        # Configure model with system instruction if provided
        if system_instruction:
            model = genai.GenerativeModel(
                model_name=model_name,
                system_instruction=system_instruction
            )
        else:
            model = genai.GenerativeModel(model_name=model_name)
            
        # Set basic parameters
        generation_config = genai.types.GenerationConfig(
            temperature=0.7,
            max_output_tokens=2048,
        )
        
        response = model.generate_content(prompt, generation_config=generation_config)
        
        if not response.text:
            raise GeminiAPIError("Gemini API returned an empty response. The content might have been flagged by safety filters.")
            
        return response.text
        
    except genai.types.BlockedPromptException as block_err:
        raise GeminiAPIError(f"Prompt was blocked by Gemini safety settings: {block_err}")
    except Exception as e:
        if isinstance(e, MissingAPIKeyError):
            raise e
        raise GeminiAPIError(f"Google Gemini API error: {str(e)}")
