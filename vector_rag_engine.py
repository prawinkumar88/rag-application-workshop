from database import Database
from prompts import Prompts
from gemini_provider import GeminiProvider
from ollama_provider import OllamaProvider
from vector_store import VectorStore

class VectorRAGEngine:
    """Vector-based RAG engine using semantic search"""
    
    def __init__(self, provider_type: str = "gemini", ollama_model: str = None, top_k: int = 3):
        """
        Initialize Vector RAG Engine
        Args:
            provider_type: 'gemini' or 'ollama'
            ollama_model: Model name if using Ollama
            top_k: Number of relevant documents to retrieve
        """
        self.db = Database()
        self.vector_store = VectorStore()
        self.top_k = top_k
        self.provider_type = provider_type
        
        # Initialize LLM provider
        if provider_type == "gemini":
            self.provider = GeminiProvider()
        elif provider_type == "ollama":
            self.provider = OllamaProvider(ollama_model)
        else:
            raise ValueError(f"Unknown provider: {provider_type}")
        
        # Index database if not already indexed
        self._ensure_indexed()
    
    def _ensure_indexed(self):
        """Ensure database is indexed in vector store"""
        try:
            # Try a test search
            self.vector_store.search("test", top_k=1)
        except:
            # If fails, index the database
            print("Indexing database into vector store...")
            count = self.vector_store.index_database(self.db)
            print(f"Indexed {count} documents")
    
    def query(self, question: str, return_sources: bool = False) -> str:
        """
        Query using vector-based retrieval
        Args:
            question: User's question
            return_sources: If True, return sources with answer
        """
        # 1. Retrieve relevant documents
        results = self.vector_store.search(question, top_k=self.top_k)
        
        # 2. Build context from results
        retrieved_context = self.vector_store.get_context_from_results(results)
        
        # 3. Create system prompt with retrieved context
        system_prompt = f"""You are an academic advisor assistant with access to student records.

{retrieved_context}

Answer questions based ONLY on the information provided above.
If the information is not available, say so clearly.
Be concise and accurate."""
        
        # 4. Query LLM
        response = self.provider.query(question, system_prompt)
        
        if return_sources:
            sources = "\n\n---\n**Sources Used:**\n"
            for i, result in enumerate(results, 1):
                sources += f"{i}. {result['metadata'].get('type', 'unknown').title()}: {result['metadata'].get('name', result['id'])}\n"
            return response + sources
        
        return response
    
    def get_example_prompts(self) -> list:
        """Get example prompts for workshop"""
        return Prompts.get_example_prompts()
    
    def get_search_results(self, query: str) -> list:
        """Get raw search results for debugging/visualization"""
        return self.vector_store.search(query, top_k=self.top_k)
    
    def reindex(self):
        """Force reindex of database"""
        self.vector_store.reset()
        count = self.vector_store.index_database(self.db)
        return count
