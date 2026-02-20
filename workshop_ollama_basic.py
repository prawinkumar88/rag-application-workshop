"""Basic Ollama interaction without RAG"""

from ollama_provider import OllamaProvider
from config import Config

def main():
    """Main function for basic Ollama interaction"""
    
    # Check if Ollama is available
    if not OllamaProvider.is_available():
        print("Error: Ollama is not available")
        print("Please ensure Ollama is running on your system")
        print(f"Expected URL: {Config.OLLAMA_URL}")
        return
    
    # Initialize Ollama provider
    print("Initializing Ollama provider...")
    
    # List available models
    print("\nChecking available models...")
    available_models = OllamaProvider.list_models()
    if available_models:
        print(f"Found {len(available_models)} available models:")
        for model in available_models:
            print(f"  - {model}")
    else:
        print("Could not retrieve model list")
    
    # Check if configured model is available
    if not OllamaProvider.check_model_available(Config.OLLAMA_MODEL):
        print(f"\nWarning: Configured model '{Config.OLLAMA_MODEL}' not found!")
        print("Please ensure the model is installed with: ollama pull <model-name>")
        return
    
    ollama = OllamaProvider()
    print(f"\nOllama provider initialized successfully!")
    print(f"Using model: {Config.OLLAMA_MODEL}\n")
    
    # Interactive query loop
    print("=" * 60)
    print("Basic Ollama Chat (without RAG)")
    print("=" * 60)
    print("Type your questions below. Type 'exit' or 'quit' to stop.\n")
    
    while True:
        # Get user input
        user_query = input("You: ").strip()
        
        # Check for exit commands
        if user_query.lower() in ['exit', 'quit', 'q']:
            print("\nGoodbye!")
            break
        
        # Skip empty queries
        if not user_query:
            continue
        
        # Query Ollama
        print("\nOllama: ", end="", flush=True)
        response = ollama.query(user_query, context="")
        print(response)
        print("\n" + "-" * 60 + "\n")

if __name__ == "__main__":
    main()
