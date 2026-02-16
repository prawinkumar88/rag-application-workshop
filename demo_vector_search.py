"""
Vector Search Demo - Advanced Examples
Demonstrates various semantic search scenarios
"""

from vector_store import VectorStore
from database import Database
import time

def print_header(title):
    """Print formatted header"""
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70)

def print_results(results, show_full=False):
    """Print formatted search results"""
    for i, result in enumerate(results, 1):
        relevance = (1 - result['distance']) * 100
        print(f"\n{i}. {result['metadata']['name']} ({result['metadata']['type'].upper()})")
        print(f"   Relevance Score: {relevance:.1f}%")
        
        if show_full:
            print(f"   Full Content:\n{result['document']}")
        else:
            print(f"   Preview: {result['document'][:150]}...")

def demo_exact_match():
    """Demo: Exact information retrieval"""
    print_header("Demo 1: Exact Match Queries")
    
    vector_store = VectorStore()
    
    queries = [
        "Alice Johnson",
        "CS101",
        "Computer Science major"
    ]
    
    for query in queries:
        print(f"\n🔍 Query: '{query}'")
        print("-" * 70)
        results = vector_store.search(query, top_k=1)
        print_results(results)

def demo_semantic_search():
    """Demo: Semantic understanding"""
    print_header("Demo 2: Semantic Search")
    
    vector_store = VectorStore()
    
    queries = [
        "top performing student",
        "programming courses",
        "math instructor",
        "struggling student"
    ]
    
    for query in queries:
        print(f"\n🔍 Query: '{query}'")
        print("-" * 70)
        results = vector_store.search(query, top_k=2)
        print_results(results)

def demo_comparison():
    """Demo: Compare different top_k values"""
    print_header("Demo 3: Top-K Comparison")
    
    vector_store = VectorStore()
    query = "student with good grades"
    
    for k in [1, 2, 3, 5]:
        print(f"\n🔍 Query: '{query}' (top_k={k})")
        print("-" * 70)
        
        start = time.time()
        results = vector_store.search(query, top_k=k)
        elapsed = time.time() - start
        
        print_results(results)
        print(f"\n   Search time: {elapsed*1000:.2f}ms")

def demo_context_generation():
    """Demo: Generate formatted context for LLM"""
    print_header("Demo 4: Context Generation for LLM")
    
    vector_store = VectorStore()
    query = "Who is enrolled in CS101?"
    
    print(f"\n🔍 Query: '{query}'")
    print("-" * 70)
    
    results = vector_store.search(query, top_k=3)
    context = vector_store.get_context_from_results(results)
    
    print("\n📄 Generated Context for LLM:\n")
    print(context)

def demo_multi_type_search():
    """Demo: Search across students and courses"""
    print_header("Demo 5: Cross-Type Semantic Search")
    
    vector_store = VectorStore()
    
    queries = [
        "computer science",  # Should match both CS students and CS courses
        "engineering",       # Should match Engineering students and courses
        "high achiever"      # Should match students with high GPA
    ]
    
    for query in queries:
        print(f"\n🔍 Query: '{query}'")
        print("-" * 70)
        results = vector_store.search(query, top_k=3)
        
        # Group by type
        students = [r for r in results if r['metadata']['type'] == 'student']
        courses = [r for r in results if r['metadata']['type'] == 'course']
        
        if students:
            print("\n   📚 Students Found:")
            for r in students:
                relevance = (1 - r['distance']) * 100
                print(f"      • {r['metadata']['name']} ({relevance:.1f}%)")
        
        if courses:
            print("\n   📖 Courses Found:")
            for r in courses:
                relevance = (1 - r['distance']) * 100
                print(f"      • {r['metadata']['name']} ({relevance:.1f}%)")

def demo_performance():
    """Demo: Performance metrics"""
    print_header("Demo 6: Performance Metrics")
    
    vector_store = VectorStore()
    
    test_queries = [
        "Alice Johnson",
        "top student",
        "computer science",
        "calculus course",
        "struggling students"
    ]
    
    print("\n📊 Running performance tests...")
    print("-" * 70)
    
    total_time = 0
    for query in test_queries:
        start = time.time()
        results = vector_store.search(query, top_k=3)
        elapsed = time.time() - start
        total_time += elapsed
        
        print(f"Query: '{query:.<40}' {elapsed*1000:>6.2f}ms")
    
    print("-" * 70)
    print(f"Average search time: {(total_time/len(test_queries))*1000:.2f}ms")
    print(f"Total time: {total_time*1000:.2f}ms")

def main():
    """Run all demos"""
    print("=" * 70)
    print("  Vector Search Comprehensive Demo")
    print("  Demonstrating semantic search capabilities")
    print("=" * 70)
    
    # Initialize and index
    print("\n🔧 Setting up vector store...")
    vector_store = VectorStore()
    db = Database()
    count = vector_store.index_database(db)
    print(f"✅ Indexed {count} documents\n")
    
    # Run demos
    demos = [
        ("1", "Exact Match", demo_exact_match),
        ("2", "Semantic Search", demo_semantic_search),
        ("3", "Top-K Comparison", demo_comparison),
        ("4", "Context Generation", demo_context_generation),
        ("5", "Cross-Type Search", demo_multi_type_search),
        ("6", "Performance", demo_performance)
    ]
    
    print("\nAvailable Demos:")
    for num, name, _ in demos:
        print(f"  {num}. {name}")
    print("  0. Run All Demos")
    
    choice = input("\nSelect demo (0-6): ").strip()
    
    if choice == "0":
        for _, _, demo_func in demos:
            demo_func()
            input("\nPress Enter to continue...")
    else:
        for num, name, demo_func in demos:
            if choice == num:
                demo_func()
                break
        else:
            print("Invalid choice!")
    
    print("\n✅ Demo completed!")

if __name__ == "__main__":
    main()
