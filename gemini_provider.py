import google.generativeai as genai
from config import Config

class GeminiProvider:
    """Gemini API provider for RAG"""
    
    def __init__(self):
        if not Config.GEMINI_API_KEY:
            raise ValueError("GEMINI_API_KEY not configured")
        genai.configure(api_key=Config.GEMINI_API_KEY)
        self.model = genai.GenerativeModel('gemini-3-flash-preview')
    
    def query(self, query: str, context: str = "") -> str:
        """Query Gemini with optional context"""
        try:
            if context:
                prompt = f"{context}\n\nQuestion: {query}"
            else:
                prompt = query
            
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"Error querying Gemini: {str(e)}"
    
    @staticmethod
    def is_available() -> bool:
        """Check if Gemini is available"""
        return bool(Config.GEMINI_API_KEY)
    
    @staticmethod
    def list_models():
        """List available Gemini models"""
        try:
            if not Config.GEMINI_API_KEY:
                return []
            genai.configure(api_key=Config.GEMINI_API_KEY)
            models = genai.list_models()
            return [model.name for model in models if 'generateContent' in model.supported_generation_methods]
        except Exception as e:
            print(f"Error listing models: {str(e)}")
            return []
