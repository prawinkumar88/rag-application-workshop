import sys
import os

# Add parent directory to path to import gemini_provider
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from gemini_provider import GeminiProvider

def read_emotions_file(file_path: str) -> str:
    """Read the emotions.txt file"""
    with open(file_path, 'r') as f:
        return f.read()

def categorize_emotions_with_gemini(emotions_text: str) -> dict:
    """Use Gemini to categorize emotions into moods"""
    
    system_prompt = """
"""

    try:
        provider = GeminiProvider()
        query = f"Categorize these sentences by mood:\n\n{emotions_text}"
        response = provider.query(query, system_prompt)
        
        return response
    except Exception as e:
        return f"Error: {str(e)}"

def main():
    # Read emotions from file
    emotions_file = os.path.join(os.path.dirname(__file__), 'emotions.txt')
    emotions_text = read_emotions_file(emotions_file)
    
    print("Reading emotions from emotions.txt...")
    print(f"\nText to analyze:\n{emotions_text}\n")
    print("=" * 80)
    print("\nCategorizing emotions using Gemini AI...\n")
    
    # Get mood categorization from Gemini
    result = categorize_emotions_with_gemini(emotions_text)
    
    print("Gemini's Mood Categorization:")
    print("=" * 80)
    print(result)
    print("\n" + "=" * 80)

if __name__ == "__main__":
    main()