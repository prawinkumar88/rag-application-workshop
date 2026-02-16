import chromadb
from chromadb.config import Settings
import numpy as np
from typing import List, Dict, Tuple
from embeddings_provider import EmbeddingsProvider
from database import Database
import json

class VectorStore:
    """Vector database for semantic search"""
    
    def __init__(self, collection_name: str = "student_records", persist_directory: str = "./chroma_db"):
        """Initialize vector store with ChromaDB"""
        self.embeddings = EmbeddingsProvider()
        
        # Initialize ChromaDB client (new configuration)
        self.client = chromadb.PersistentClient(path=persist_directory)
        
        # Get or create collection
        try:
            self.collection = self.client.get_collection(collection_name)
        except:
            self.collection = self.client.create_collection(
                name=collection_name,
                metadata={"description": "Student records and course information"}
            )
    
    def index_database(self, db: Database):
        """Index all students and courses into vector store"""
        documents = []
        metadatas = []
        ids = []
        
        # Index students
        for student_id, info in db.get_all_students().items():
            # Create rich text representation
            doc_text = f"""
            Student: {info['name']}
            ID: {student_id}
            Email: {info['email']}
            Major: {info['major']}
            GPA: {info['gpa']}
            Enrolled Courses: {', '.join(info['courses'])}
            Grades: {json.dumps(info['grades'])}
            """
            
            documents.append(doc_text.strip())
            metadatas.append({
                "type": "student",
                "id": student_id,
                "name": info['name'],
                "major": info['major'],
                "gpa": str(info['gpa'])
            })
            ids.append(f"student_{student_id}")
        
        # Index courses
        for course_id, info in db.get_all_courses().items():
            doc_text = f"""
            Course: {info['name']}
            Course ID: {course_id}
            Instructor: {info['instructor']}
            Credits: {info['credits']}
            Description: {info['description']}
            """
            
            documents.append(doc_text.strip())
            metadatas.append({
                "type": "course",
                "id": course_id,
                "name": info['name'],
                "instructor": info['instructor']
            })
            ids.append(f"course_{course_id}")
        
        # Add to collection
        self.collection.add(
            documents=documents,
            metadatas=metadatas,
            ids=ids
        )
        
        return len(documents)
    
    def search(self, query: str, top_k: int = 3) -> List[Dict]:
        """
        Semantic search in vector store
        Returns top_k most relevant documents
        """
        results = self.collection.query(
            query_texts=[query],
            n_results=top_k
        )
        
        # Format results
        formatted_results = []
        for i in range(len(results['ids'][0])):
            formatted_results.append({
                'id': results['ids'][0][i],
                'document': results['documents'][0][i],
                'metadata': results['metadatas'][0][i],
                'distance': results['distances'][0][i] if 'distances' in results else None
            })
        
        return formatted_results
    
    def get_context_from_results(self, results: List[Dict]) -> str:
        """Convert search results to context string"""
        context = "# Relevant Information Retrieved:\n\n"
        
        for i, result in enumerate(results, 1):
            context += f"## Result {i} (Relevance: {1 - result.get('distance', 0):.2%})\n"
            context += result['document'] + "\n\n"
        
        return context
    
    def reset(self):
        """Clear all data from collection"""
        self.client.delete_collection(self.collection.name)
        self.collection = self.client.create_collection(
            name=self.collection.name,
            metadata={"description": "Student records and course information"}
        )

def main():
    """
    Demonstration of VectorStore functionality
    Shows indexing, searching, and retrieval examples
    """
    print("=" * 70)
    print("VectorStore Demo - Semantic Search for Student Records")
    print("=" * 70)
    
    # Initialize
    print("\n1️⃣  Initializing Vector Store...")
    vector_store = VectorStore()
    db = Database()
    
    # Index database
    print("\n2️⃣  Indexing Database...")
    count = vector_store.index_database(db)
    print(f"   ✅ Indexed {count} documents (students + courses)")
    
    # Example queries
    example_queries = [
        "student with highest GPA",
        "computer science courses",
        "who teaches mathematics",
        "student grades in CS101",
        "engineering major students"
    ]
    
    print("\n3️⃣  Running Example Searches:")
    print("-" * 70)
    
    for query in example_queries:
        print(f"\n🔍 Query: '{query}'")
        print("-" * 70)
        
        results = vector_store.search(query, top_k=2)
        
        for i, result in enumerate(results, 1):
            relevance = (1 - result['distance']) * 100
            print(f"\n   Result {i}: {result['metadata']['name']} ({result['metadata']['type']})")
            print(f"   Relevance: {relevance:.1f}%")
            print(f"   Preview: {result['document'][:150]}...")
    
    # Interactive mode
    print("\n" + "=" * 70)
    print("4️⃣  Interactive Search Mode")
    print("=" * 70)
    print("   Type your search query (or 'quit' to exit)")
    print()
    
    while True:
        query = input("🔍 Search: ").strip()
        
        if query.lower() in ['quit', 'exit', 'q']:
            break
        
        if not query:
            continue
        
        print()
        results = vector_store.search(query, top_k=3)
        
        for i, result in enumerate(results, 1):
            relevance = (1 - result['distance']) * 100
            print(f"{i}. [{relevance:.1f}%] {result['metadata']['type'].upper()}: {result['metadata']['name']}")
            print(f"   {result['document'][:200]}...")
            print()
        
        # Show formatted context
        if input("Show formatted context? (y/n): ").lower() == 'y':
            context = vector_store.get_context_from_results(results)
            print("\n" + "=" * 70)
            print(context)
            print("=" * 70 + "\n")
    
    print("\n✅ Demo completed!")

if __name__ == "__main__":
    main()
