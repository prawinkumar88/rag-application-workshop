import google.generativeai as genai
from config import Config

class GeminiProvider:
    """Gemini API provider for RAG"""
    
    def __init__(self):
        if not Config.GEMINI_API_KEY:
            raise ValueError("GEMINI_API_KEY not configured")
        genai.configure(api_key=Config.GEMINI_API_KEY)
        self.model = genai.GenerativeModel('gemini-3-flash-preview')
    
    def query(self, query: str, system_prompt: str) -> str:
        """Query Gemini with RAG context"""
        try:
            response = self.model.generate_content(
                f"{system_prompt}\n\nQuestion: {query}"
            )
            return response.text
        except Exception as e:
            return f"Error querying Gemini: {str(e)}"
    
    @staticmethod
    def is_available() -> bool:
        """Check if Gemini is available"""
        return bool(Config.GEMINI_API_KEY)
