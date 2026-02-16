"""
Workshop Module 4: Vector-based RAG
Learn semantic search and vector embeddings
"""

from vector_rag_engine import VectorRAGEngine
from database import Database

def main():
    print("=" * 60)
    print("Workshop Module 4: Vector-based RAG")
    print("=" * 60)
    
    # Initialize
    print("\n1. Initializing Vector RAG Engine...")
    print("   - Loading database")
    print("   - Creating vector embeddings")
    print("   - Indexing into vector store")
    
    rag = VectorRAGEngine(provider_type="gemini", top_k=2)
    
    print("✅ Vector RAG Engine ready!")
    
    # Show example prompts
    print("\n2. Example Questions:")
    examples = rag.get_example_prompts()
    for i, example in enumerate(examples[:5], 1):
        print(f"   {i}. {example}")
    
    # Interactive loop
    print("\n3. Try Vector-based Retrieval:")
    print("   (Type 'quit' to exit, 'search:query' to see search results)\n")
    
    while True:
        question = input("Your question: ").strip()
        
        if question.lower() == 'quit':
            break
        
        if question.startswith('search:'):
            # Show search results
            query = question[7:].strip()
            print("\n📊 Search Results:")
            results = rag.get_search_results(query)
            for i, result in enumerate(results, 1):
                print(f"\n{i}. {result['metadata']['type'].title()}: {result['metadata']['name']}")
                print(f"   Relevance: {(1 - result['distance']) * 100:.1f}%")
                print(f"   Preview: {result['document'][:200]}...")
            print()
        else:
            print("\n🤖 Answer:")
            response = rag.query(question, return_sources=True)
            print(response)
            print()

if __name__ == "__main__":
    main()
