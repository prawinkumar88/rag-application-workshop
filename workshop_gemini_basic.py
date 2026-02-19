"""Basic Gemini interaction without RAG"""

from gemini_provider import GeminiProvider
from config import Config

def main():
    """Main function for basic Gemini interaction"""
    
    # Check if Gemini is available
    if not GeminiProvider.is_available():
        print("Error: GEMINI_API_KEY not configured")
        print("Please set your Gemini API key in config.py or environment variables")
        return
    
    # Initialize Gemini provider
    print("Initializing Gemini provider...")
    
    # List available models
    print("\nChecking available models...")
    available_models = GeminiProvider.list_models()
    if available_models:
        print(f"Found {len(available_models)} available models:")
        for model in available_models[:5]:  # Show first 5 models
            print(f"  - {model}")
        if len(available_models) > 5:
            print(f"  ... and {len(available_models) - 5} more")
    else:
        print("Could not retrieve model list")
    
    gemini = GeminiProvider()
    print("\nGemini provider initialized successfully!")
    print(f"Using model: gemini-3-flash-preview\n")
    
    # Interactive query loop
    print("=" * 60)
    print("Basic Gemini Chat (without RAG)")
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
        
        # Query Gemini
        print("\nGemini: ", end="", flush=True)
        response = gemini.query(user_query, context="")
        print(response)
        print("\n" + "-" * 60 + "\n")

if __name__ == "__main__":
    main()
