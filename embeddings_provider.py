from sentence_transformers import SentenceTransformer
import numpy as np
from typing import List, Union
import os

class EmbeddingsProvider:
    """Handle text embeddings generation"""
    
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        """
        Initialize embeddings provider
        Args:
            model_name: HuggingFace model name for embeddings
                       Options: 'all-MiniLM-L6-v2', 'all-mpnet-base-v2'
        """
        self.model_name = model_name
        self.model = SentenceTransformer(model_name)
        self.embedding_dim = self.model.get_sentence_embedding_dimension()
    
    def embed_text(self, text: str) -> np.ndarray:
        """Generate embedding for single text"""
        return self.model.encode(text, convert_to_numpy=True)
    
    def embed_texts(self, texts: List[str]) -> np.ndarray:
        """Generate embeddings for multiple texts"""
        return self.model.encode(texts, convert_to_numpy=True)
    
    def cosine_similarity(self, embedding1: np.ndarray, embedding2: np.ndarray) -> float:
        """Calculate cosine similarity between two embeddings"""
        return np.dot(embedding1, embedding2) / (
            np.linalg.norm(embedding1) * np.linalg.norm(embedding2)
        )
    
    @staticmethod
    def get_available_models() -> List[str]:
        """Get list of recommended embedding models"""
        return [
            "all-MiniLM-L6-v2",  # Fast, 384 dim
            "all-mpnet-base-v2",  # Better quality, 768 dim
            "paraphrase-MiniLM-L6-v2",  # Paraphrase detection
        ]
