"""
Streamlit UI for Vector RAG Module
Demonstrates semantic search and vector-based retrieval
"""

import streamlit as st
from datetime import datetime
from vector_rag_engine import VectorRAGEngine
from rag_engine import RAGEngine

st.set_page_config(
    page_title="Vector RAG Demo",
    page_icon="🔍",
    layout="wide"
)

st.title("🔍 Vector-based RAG Workshop")
st.markdown("*Learn semantic search with vector embeddings*")

# Sidebar
with st.sidebar:
    st.header("⚙️ Configuration")
    
    providers = RAGEngine.get_available_providers()
    provider = st.selectbox("Select Provider:", providers)
    
    top_k = st.slider("Documents to Retrieve:", 1, 5, 3)
    show_sources = st.checkbox("Show Sources", value=True)
    
    st.divider()
    
    st.header("📖 How It Works")
    st.markdown("""
    **Vector RAG Steps:**
    1. 📝 Convert query to embedding
    2. 🔍 Find similar documents
    3. 📊 Retrieve top-k results
    4. 🤖 Generate answer
    """)

# Initialize
if "vector_rag" not in st.session_state:
    with st.spinner("Initializing vector store..."):
        ollama_model = None
        if provider == "ollama":
            from ollama_provider import OllamaProvider
            models = OllamaProvider.get_available_models()
            ollama_model = models[0] if models else "mistral"
        
        st.session_state.vector_rag = VectorRAGEngine(
            provider_type=provider,
            ollama_model=ollama_model,
            top_k=top_k
        )

rag = st.session_state.vector_rag

# Main content
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("💬 Ask a Question")
    query = st.text_input("Enter your question:", key="query_input")
    
    if st.button("🔍 Search & Answer", use_container_width=True):
        if query:
            # Show search results
            st.subheader("📊 Retrieved Documents")
            results = rag.get_search_results(query)
            
            for i, result in enumerate(results, 1):
                with st.expander(f"📄 Document {i}: {result['metadata']['name']}"):
                    relevance = (1 - result['distance']) * 100
                    st.metric("Relevance Score", f"{relevance:.1f}%")
                    st.code(result['document'], language=None)
            
            # Get answer
            st.divider()
            st.subheader("💬 Generated Answer")
            with st.spinner("Generating answer..."):
                response = rag.query(query, return_sources=show_sources)
            st.success(response)

with col2:
    st.subheader("📝 Example Queries")
    examples = rag.get_example_prompts()
    
    for example in examples[:5]:
        if st.button(example, key=f"ex_{example[:20]}", use_container_width=True):
            st.session_state.query_input = example
            st.rerun()

# Comparison section
st.divider()
st.header("⚖️ Vector RAG vs Prompt-based RAG")

col1, col2 = st.columns(2)

with col1:
    st.subheader("🔍 Vector RAG")
    st.markdown("""
    **Advantages:**
    - ✅ Scalable to large databases
    - ✅ Semantic understanding
    - ✅ Efficient retrieval
    - ✅ Reduced context size
    
    **Use Cases:**
    - Large document collections
    - Semantic search needed
    - Context window limits
    """)

with col2:
    st.subheader("📝 Prompt-based RAG")
    st.markdown("""
    **Advantages:**
    - ✅ Simple implementation
    - ✅ Complete context available
    - ✅ No indexing needed
    - ✅ Exact matches guaranteed
    
    **Use Cases:**
    - Small databases
    - Exact information needed
    - Simple queries
    """)
