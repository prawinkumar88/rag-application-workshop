from database import Database
from prompts import Prompts
from gemini_provider import GeminiProvider
from ollama_provider import OllamaProvider

class RAGEngine:
    """Main RAG engine that coordinates providers and database"""
    
    def __init__(self, provider_type: str = "gemini", ollama_model: str = None):
        self.db = Database()
        self.db_context = self.db.format_as_context()
        self.system_prompt = Prompts.get_system_prompt(self.db_context)
        self.provider_type = provider_type
        
        if provider_type == "gemini":
            self.provider = GeminiProvider()
        elif provider_type == "ollama":
            self.provider = OllamaProvider(ollama_model)
        else:
            raise ValueError(f"Unknown provider: {provider_type}")
    
    def query(self, question: str) -> str:
        """Query the RAG system"""
        return self.provider.query(question, self.system_prompt)
    
    def get_example_prompts(self) -> list:
        """Get example prompts for workshop"""
        return Prompts.get_example_prompts()
    
    @staticmethod
    def get_available_providers() -> list:
        """Get list of available providers"""
        providers = []
        if GeminiProvider.is_available():
            providers.append("gemini")
        if OllamaProvider.is_available():
            providers.append("ollama")
        return providers
