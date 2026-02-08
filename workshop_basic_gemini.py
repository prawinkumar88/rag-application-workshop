"""
WORKSHOP MODULE 1: Basic Gemini Integration
Learn how to use Gemini with simple prompts
"""

from rag_engine import RAGEngine

def main():
    print("=" * 60)
    print("WORKSHOP 1: Basic Gemini Integration")
    print("=" * 60)
    
    # Initialize Gemini provider
    rag = RAGEngine(provider_type="gemini")
    
    # Show example prompts
    print("\nExample Prompts:")
    for i, prompt in enumerate(rag.get_example_prompts(), 1):
        print(f"{i}. {prompt}")
    
    # Interactive query
    print("\n" + "=" * 60)
    print("Ask a question about students or courses:")
    print("=" * 60 + "\n")
    
    while True:
        user_input = input("You: ").strip()
        if user_input.lower() == 'exit':
            break
        
        if not user_input:
            continue
        
        print("\nAssistant: ", end="")
        response = rag.query(user_input)
        print(response)
        print()

if __name__ == "__main__":
    main()
