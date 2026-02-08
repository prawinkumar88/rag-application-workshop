class Prompts:
    """System prompts for RAG assistant"""
    
    @staticmethod
    def get_system_prompt(db_context: str) -> str:
        """Get main system prompt with database context"""
        return f"""You are an intelligent student records and academic advisor AI assistant.
You have access to a complete student database with student information, grades, and course details.

{db_context}

Your role is to:
1. Answer questions about student records accurately
2. Provide academic insights and analysis
3. Help with course information and academic planning
4. Maintain context across conversations

When answering questions:
- Be specific and cite actual data from the database
- Provide helpful academic insights
- Be professional and supportive
- If you don't have specific information, clearly state that"""
    
    @staticmethod
    def get_example_prompts() -> list:
        """Get example prompts for the workshop"""
        return [
            "What is Alice's GPA and major?",
            "Which students are enrolled in CS101?",
            "Tell me about Carol's performance in AI courses",
            "What courses does Bob need for his Data Science major?",
            "Who is the instructor for Machine Learning Fundamentals?",
            "List all A grades in the student database",
            "Compare the academic performance of all students",
            "What are the prerequisites for CS201?"
        ]
