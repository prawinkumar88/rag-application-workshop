import google.generativeai as genai
from config import Config

class GeminiNoRAG:
    """Gemini provider that sends queries WITHOUT database context"""
    
    def __init__(self):
        if not Config.GEMINI_API_KEY:
            raise ValueError("GEMINI_API_KEY not configured")
        genai.configure(api_key=Config.GEMINI_API_KEY)
        self.model = genai.GenerativeModel('gemini-3-flash-preview')
    
    def query(self, user_query: str) -> str:
        """Query Gemini directly with NO context"""
        try:
            # Notice we are NOT passing any system_prompt or database context here
            response = self.model.generate_content(user_query)
            return response.text
        except Exception as e:
            return f"Error: {str(e)}"
