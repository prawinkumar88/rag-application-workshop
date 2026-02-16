import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Configuration and database for RAG application"""
    
    # AI Provider Settings
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    OLLAMA_DEFAULT_MODEL = os.getenv("OLLAMA_MODEL", "mistral")
    
    # Student Database
    STUDENT_DATABASE = {
        "S001": {
            "name": "Alice Johnson",
            "email": "alice.j@university.edu",
            "major": "Computer Science",
            "gpa": 3.8,
            "courses": ["CS101", "MATH201", "PHYS101"],
            "grades": {
                "CS101": "A",
                "MATH201": "A-",
                "PHYS101": "B+"
            }
        },
        "S002": {
            "name": "Bob Smith",
            "email": "bob.smith@university.edu",
            "major": "Engineering",
            "gpa": 3.5,
            "courses": ["CS101", "MATH201", "ENG301"],
            "grades": {
                "CS101": "B+",
                "MATH201": "B",
                "ENG301": "A-"
            }
        },
        "S003": {
            "name": "Carol White",
            "email": "carol.w@university.edu",
            "major": "Mathematics",
            "gpa": 3.9,
            "courses": ["MATH201", "PHYS101", "CS201"],
            "grades": {
                "MATH201": "A",
                "PHYS101": "A",
                "CS201": "A-"
            }
        }
    }
    
    COURSE_DATABASE = {
        "CS101": {
            "name": "Introduction to Programming",
            "instructor": "Dr. Smith",
            "credits": 3,
            "description": "Fundamentals of programming using Python"
        },
        "MATH201": {
            "name": "Calculus II",
            "instructor": "Prof. Johnson",
            "credits": 4,
            "description": "Integral calculus and series"
        },
        "PHYS101": {
            "name": "Physics I",
            "instructor": "Dr. Brown",
            "credits": 4,
            "description": "Mechanics and thermodynamics"
        },
        "ENG301": {
            "name": "Engineering Design",
            "instructor": "Prof. Davis",
            "credits": 3,
            "description": "Introduction to engineering design principles"
        },
        "CS201": {
            "name": "Data Structures",
            "instructor": "Dr. Smith",
            "credits": 3,
            "description": "Advanced data structures and algorithms"
        }
    }
