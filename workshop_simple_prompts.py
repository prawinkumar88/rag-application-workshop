"""
WORKSHOP MODULE 3: Simple Prompts Exercise
Practice writing effective prompts for student queries
"""

from rag_engine import RAGEngine

SIMPLE_PROMPTS = {
    "student_gpa": "What is {student_name}'s GPA?",
    "student_major": "What is {student_name}'s major?",
    "student_courses": "What courses is {student_name} enrolled in?",
    "course_info": "Tell me about {course_id}",
    "highest_gpa": "Which student has the highest GPA?",
    "course_enrollment": "How many students are enrolled in {course_id}?",
}

def main():
    print("=" * 60)
    print("WORKSHOP 3: Simple Prompts Exercise")
    print("=" * 60)
    
    # Get available providers
    providers = RAGEngine.get_available_providers()
    if not providers:
        print("Error: No AI providers available!")
        return
    
    print(f"\nAvailable providers: {', '.join(providers)}")
    provider = input(f"Select provider (default: {providers[0]}): ").strip() or providers[0]
    
    ollama_model = None
    if provider == "ollama":
        from ollama_provider import OllamaProvider
        models = OllamaProvider.get_available_models()
        ollama_model = input(f"Select model (default: {models[0]}): ").strip() or models[0]
    
    # Initialize RAG
    rag = RAGEngine(provider_type=provider, ollama_model=ollama_model)
    
    # Show prompt templates
    print("\nAvailable Prompt Templates:")
    for key, template in SIMPLE_PROMPTS.items():
        print(f"- {key}: {template}")
    
    # Practice prompts
    print("\n" + "=" * 60)
    print("Practice with templates or write your own:")
    print("=" * 60 + "\n")
    
    while True:
        print("\nOptions:")
        print("1. Use a template")
        print("2. Write custom prompt")
        print("3. Exit")
        
        choice = input("\nSelect option: ").strip()
        
        if choice == "1":
            print("\nAvailable templates:")
            for i, key in enumerate(SIMPLE_PROMPTS.keys(), 1):
                print(f"{i}. {key}")
            
            template_choice = input("Select template number: ").strip()
            try:
                template_key = list(SIMPLE_PROMPTS.keys())[int(template_choice) - 1]
                template = SIMPLE_PROMPTS[template_key]
                
                variables = {}
                import re
                var_names = re.findall(r'\{(\w+)\}', template)
                for var in var_names:
                    variables[var] = input(f"Enter {var}: ").strip()
                
                prompt = template.format(**variables)
                print(f"\nPrompt: {prompt}")
                response = rag.query(prompt)
                print(f"\nResponse: {response}")
            except (ValueError, IndexError):
                print("Invalid selection")
        
        elif choice == "2":
            prompt = input("\nEnter your prompt: ").strip()
            if prompt:
                response = rag.query(prompt)
                print(f"\nResponse: {response}")
        
        elif choice == "3":
            break

if __name__ == "__main__":
    main()
