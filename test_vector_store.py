"""
Test script to verify ChromaDB configuration
"""

def test_chroma_client():
    """Test new ChromaDB client configuration"""
    import chromadb
    
    print("Testing ChromaDB configuration...")
    
    # Test 1: Create client
    print("\n1. Creating PersistentClient...")
    client = chromadb.PersistentClient(path="./test_chroma_db")
    print("✅ Client created successfully")
    
    # Test 2: Create collection
    print("\n2. Creating collection...")
    try:
        collection = client.get_or_create_collection(
            name="test_collection",
            metadata={"description": "Test collection"}
        )
        print("✅ Collection created successfully")
    except Exception as e:
        print(f"❌ Error: {e}")
        return False
    
    # Test 3: Add documents
    print("\n3. Adding test documents...")
    try:
        collection.add(
            documents=["This is a test document", "Another test"],
            metadatas=[{"source": "test1"}, {"source": "test2"}],
            ids=["id1", "id2"]
        )
        print("✅ Documents added successfully")
    except Exception as e:
        print(f"❌ Error: {e}")
        return False
    
    # Test 4: Query
    print("\n4. Testing query...")
    try:
        results = collection.query(
            query_texts=["test"],
            n_results=2
        )
        print(f"✅ Query successful, found {len(results['ids'][0])} results")
    except Exception as e:
        print(f"❌ Error: {e}")
        return False
    
    # Cleanup
    print("\n5. Cleaning up...")
    client.delete_collection("test_collection")
    print("✅ Cleanup complete")
    
    return True

def test_vector_store():
    """Test VectorStore class"""
    from vector_store import VectorStore
    from database import Database
    
    print("\n" + "="*70)
    print("Testing VectorStore Class")
    print("="*70)
    
    try:
        print("\n1. Initializing VectorStore...")
        vs = VectorStore()
        print("✅ VectorStore initialized")
        
        print("\n2. Indexing database...")
        db = Database()
        count = vs.index_database(db)
        print(f"✅ Indexed {count} documents")
        
        print("\n3. Testing search...")
        results = vs.search("computer science", top_k=2)
        print(f"✅ Search returned {len(results)} results")
        
        for i, result in enumerate(results, 1):
            print(f"\n   Result {i}: {result['metadata']['name']}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("="*70)
    print("ChromaDB Configuration Test Suite")
    print("="*70)
    
    # Test 1: Basic ChromaDB
    if test_chroma_client():
        print("\n✅ ChromaDB client test PASSED")
    else:
        print("\n❌ ChromaDB client test FAILED")
        exit(1)
    
    # Test 2: VectorStore
    if test_vector_store():
        print("\n✅ VectorStore test PASSED")
    else:
        print("\n❌ VectorStore test FAILED")
        exit(1)
    
    print("\n" + "="*70)
    print("All tests PASSED! ✅")
    print("="*70)
