import json
from config import Config

class Database:
    """Handle student and course database operations"""
    
    def __init__(self):
        self.students = Config.STUDENT_DATABASE
        self.courses = Config.COURSE_DATABASE
    
    def get_student_info(self, student_id: str) -> dict:
        """Get specific student information"""
        return self.students.get(student_id)
    
    def get_all_students(self) -> dict:
        """Get all students"""
        return self.students
    
    def get_course_info(self, course_id: str) -> dict:
        """Get specific course information"""
        return self.courses.get(course_id)
    
    def get_all_courses(self) -> dict:
        """Get all courses"""
        return self.courses
    
    def format_as_context(self) -> str:
        """Format database as context for RAG"""
        context = "# Student Records and Academics Database\n\n"
        
        context += "## Student Information\n"
        for student_id, info in self.students.items():
            context += f"\n### {info['name']} ({student_id})\n"
            context += f"- Email: {info['email']}\n"
            context += f"- Major: {info['major']}\n"
            context += f"- GPA: {info['gpa']}\n"
            context += f"- Enrolled Courses: {', '.join(info['courses'])}\n"
            context += f"- Grades: {json.dumps(info['grades'], indent=2)}\n"
        
        context += "\n## Course Information\n"
        for course_id, info in self.courses.items():
            context += f"\n### {course_id}: {info['name']}\n"
            context += f"- Instructor: {info['instructor']}\n"
            context += f"- Credits: {info['credits']}\n"
            context += f"- Description: {info['description']}\n"
        
        return context
