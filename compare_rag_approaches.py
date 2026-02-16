"""
Utility to compare Prompt-based RAG vs Vector-based RAG
"""

from rag_engine import RAGEngine
from vector_rag_engine import VectorRAGEngine
import time

def compare_approaches(query: str):
    """Compare both RAG approaches for the same query"""
    
    print("=" * 80)
    print(f"Query: {query}")
    print("=" * 80)
    
    # Prompt-based RAG
    print("\n📝 PROMPT-BASED RAG")
    print("-" * 80)
    prompt_rag = RAGEngine(provider_type="gemini")
    
    start = time.time()
    prompt_response = prompt_rag.query(query)
    prompt_time = time.time() - start
    
    print(f"Response: {prompt_response}")
    print(f"Time: {prompt_time:.2f}s")
    
    # Vector-based RAG
    print("\n🔍 VECTOR-BASED RAG")
    print("-" * 80)
    vector_rag = VectorRAGEngine(provider_type="gemini", top_k=3)
    
    # Show retrieved documents
    results = vector_rag.get_search_results(query)
    print("Retrieved Documents:")
    for i, result in enumerate(results, 1):
        relevance = (1 - result['distance']) * 100
        print(f"  {i}. {result['metadata']['name']} (Relevance: {relevance:.1f}%)")
    
    start = time.time()
    vector_response = vector_rag.query(query, return_sources=True)
    vector_time = time.time() - start
    
    print(f"\nResponse: {vector_response}")
    print(f"Time: {vector_time:.2f}s")
    
    # Comparison
    print("\n" + "=" * 80)
    print("COMPARISON")
    print("=" * 80)
    print(f"Prompt-based time: {prompt_time:.2f}s")
    print(f"Vector-based time: {vector_time:.2f}s")
    print(f"Speed difference: {abs(prompt_time - vector_time):.2f}s")

def main():
    print("RAG Approaches Comparison Tool\n")
    
    queries = [
        "What is Alice Johnson's GPA?",
        "Which student has the highest GPA?",
        "Tell me about CS101",
        "What courses is Bob Smith taking?"
    ]
    
    print("Select a query to compare:")
    for i, q in enumerate(queries, 1):
        print(f"{i}. {q}")
    print(f"{len(queries) + 1}. Custom query")
    
    choice = input("\nEnter choice (1-5): ").strip()
    
    if choice.isdigit() and 1 <= int(choice) <= len(queries):
        query = queries[int(choice) - 1]
    else:
        query = input("Enter your custom query: ").strip()
    
    compare_approaches(query)

if __name__ == "__main__":
    main()
