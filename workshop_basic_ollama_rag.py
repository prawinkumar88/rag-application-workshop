"""
WORKSHOP MODULE 2: Basic Ollama Integration
Learn how to use Ollama with simple prompts
"""

from rag_engine import RAGEngine
from ollama_provider import OllamaProvider

def main():
    print("=" * 60)
    print("WORKSHOP 2: Basic Ollama Integration")
    print("=" * 60)
    
    # Check available models
    models = OllamaProvider.get_available_models()
    if not models:
        print("Error: No Ollama models found!")
        print("Pull a model first: ollama pull mistral")
        return
    
    print(f"\nAvailable models: {', '.join(models)}")
    model = input(f"Select model (default: {models[0]}): ").strip() or models[0]
    
    # Initialize Ollama provider
    rag = RAGEngine(provider_type="ollama", ollama_model=model)
    
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
