import requests
from typing import Optional
from config import Config

class OllamaProvider:
    """Ollama API provider for RAG"""
    
    def __init__(self, model: Optional[str] = None):
        self.base_url = Config.OLLAMA_BASE_URL
        self.model = model or Config.OLLAMA_DEFAULT_MODEL
    
    def query(self, query: str, context: str = "") -> str:
        """Query Ollama with optional context"""
        try:
            if context:
                prompt = f"{context}\n\nQuestion: {query}"
            else:
                prompt = query
            
            response = requests.post(
                f"{self.base_url}/api/generate",
                json={
                    "model": self.model,
                    "prompt": prompt,
                    "stream": False
                },
                timeout=300
            )
            
            if response.status_code == 200:
                result = response.json()
                return result.get("response", "No response generated")
            else:
                return f"Error: Ollama returned status {response.status_code}"
        except Exception as e:
            return f"Error querying Ollama: {str(e)}"
    
    @staticmethod
    def is_available() -> bool:
        """Check if Ollama is available"""
        try:
            response = requests.get(
                f"{Config.OLLAMA_BASE_URL}/api/tags",
                timeout=2
            )
            return response.status_code == 200
        except:
            return False
    
    @staticmethod
    def get_available_models() -> list:
        """Get available models from Ollama"""
        try:
            response = requests.get(
                f"{Config.OLLAMA_BASE_URL}/api/tags",
                timeout=2
            )
            if response.status_code == 200:
                models = response.json().get("models", [])
                return [model["name"].split(":")[0] for model in models]
            return []
        except:
            return []
