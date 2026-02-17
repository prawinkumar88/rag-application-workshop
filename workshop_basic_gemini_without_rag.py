"""
WORKSHOP MODULE 1 (Comparison): Basic Gemini WITHOUT RAG
This script shows how the AI behaves when it lacks access to your student database.
"""
from gemini_no_rag import GeminiNoRAG

def main():
    print("=" * 60)
    print("WORKSHOP: Gemini WITHOUT RAG (The 'Blind' Model)")
    print("=" * 60)
    print("Notice: This model has NO access to your student or course database.")
    
    # Initialize the No-RAG provider
    ai = GeminiNoRAG()
    
    # Example prompts that require your data
    test_prompts = [
        "What is Alice Johnson's GPA?",
        "Who is the instructor for CS101?",
        "List all students enrolled in Data Science."
    ]
    
    print("\nTry these specific questions to see it fail/hallucinate:")
    for i, prompt in enumerate(test_prompts, 1):
        print(f"{i}. {prompt}")
    
    print("\n" + "=" * 60)
    print("Type your question (or 'exit' to quit):")
    print("=" * 60 + "\n")
    
    while True:
        user_input = input("You (No RAG): ").strip()
        if user_input.lower() == 'exit':
            break
        
        if not user_input:
            continue
        
        print("\nAssistant (Thinking without context...):")
        response = ai.query(user_input)
        print(response)
        print("-" * 60)

if __name__ == "__main__":
    main()
