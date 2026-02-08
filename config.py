import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Configuration for AI providers and database"""
    
    # AI Provider Settings
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    OLLAMA_DEFAULT_MODEL = os.getenv("OLLAMA_MODEL", "mistral")
    
    # Student Database
    STUDENT_DATABASE = {
        "STU001": {
            "name": "Alice Johnson",
            "email": "alice@university.edu",
            "major": "Computer Science",
            "gpa": 3.8,
            "courses": ["CS101", "CS201", "MATH101", "MATH201"],
            "grades": {"CS101": "A", "CS201": "A-", "MATH101": "A", "MATH201": "B+"}
        },
        "STU002": {
            "name": "Bob Smith",
            "email": "bob@university.edu",
            "major": "Data Science",
            "gpa": 3.6,
            "courses": ["CS101", "STAT101", "STAT201", "MATH101"],
            "grades": {"CS101": "B+", "STAT101": "A", "STAT201": "A-", "MATH101": "A"}
        },
        "STU003": {
            "name": "Carol Davis",
            "email": "carol@university.edu",
            "major": "Artificial Intelligence",
            "gpa": 3.9,
            "courses": ["CS101", "CS201", "AI101", "ML101"],
            "grades": {"CS101": "A", "CS201": "A", "AI101": "A", "ML101": "A-"}
        }
    }
    
    COURSE_DATABASE = {
        "CS101": {
            "name": "Introduction to Computer Science",
            "instructor": "Dr. Smith",
            "credits": 3,
            "description": "Fundamentals of programming and computer science concepts"
        },
        "CS201": {
            "name": "Data Structures",
            "instructor": "Dr. Johnson",
            "credits": 4,
            "description": "Advanced data structures and algorithms"
        },
        "AI101": {
            "name": "Introduction to AI",
            "instructor": "Dr. Lee",
            "credits": 3,
            "description": "Basics of artificial intelligence and machine learning"
        },
        "ML101": {
            "name": "Machine Learning Fundamentals",
            "instructor": "Dr. Brown",
            "credits": 4,
            "description": "Core concepts of machine learning and deep learning"
        }
    }
