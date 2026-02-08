# app.py (Streamlit Integration)
import streamlit as st
from datetime import datetime
import json
import os
from rag_engine import RAGEngine
from prompts import Prompts

st.set_page_config(
    page_title="Student RAG Workshop",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .module-box {
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
    }
    .gemini-box {
        background-color: #f0f8ff;
        border-left: 4px solid #1f76d2;
    }
    .ollama-box {
        background-color: #f0fff4;
        border-left: 4px solid #22c55e;
    }
    .prompt-box {
        background-color: #fef3c7;
        border-left: 4px solid #f59e0b;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "current_provider" not in st.session_state:
    providers = RAGEngine.get_available_providers()
    st.session_state.current_provider = providers[0] if providers else None

if "current_model" not in st.session_state:
    st.session_state.current_model = "mistral"

if "rag_engine" not in st.session_state:
    st.session_state.rag_engine = None

# Sidebar Navigation
with st.sidebar:
    st.title("🎓 RAG Workshop Menu")
    st.divider()
    
    page = st.radio(
        "Select Workshop Module:",
        ["📚 Overview", "💬 Full RAG Chat", "🔧 Gemini Module", "🦙 Ollama Module", "✍️ Prompts Practice"],
        help="Choose a workshop module to explore"
    )

# PAGE 1: Overview
if page == "📚 Overview":
    st.title("🎓 Student Records RAG Workshop")
    st.markdown("*Generative AI Fundamentals & Retrieval-Augmented Generation*")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### 📖 What You'll Learn
        
        - **Generative AI Fundamentals** - Understanding LLMs
        - **RAG Concept** - Retrieval-Augmented Generation
        - **Provider Integration** - Gemini & Ollama
        - **Prompt Engineering** - Effective query crafting
        - **Context Management** - Database as context
        """)
    
    with col2:
        st.markdown("""
        ### 🎯 Workshop Modules
        
        1. **💬 Full RAG Chat** - Complete chat with history
        2. **🔧 Gemini Module** - Pure Gemini integration
        3. **🦙 Ollama Module** - Pure Ollama integration
        4. **✍️ Prompts Practice** - Learn prompt engineering
        """)
    
    st.divider()
    
    # Show example prompts
    st.subheader("📝 Example Questions")
    col1, col2 = st.columns(2)
    
    examples = Prompts.get_example_prompts()
    with col1:
        for example in examples[:4]:
            st.write(f"• {example}")
    
    with col2:
        for example in examples[4:]:
            st.write(f"• {example}")
    
    st.divider()
    
    # Architecture
    st.subheader("🏗️ System Architecture")
    st.markdown("""
    ```
    User Query
        ↓
    RAG Engine
        ├── Database (Students & Courses)
        ├── Prompts (System & Templates)
        └── Provider (Gemini or Ollama)
        ↓
    Response with Context
    ```
    """)

# PAGE 2: Full RAG Chat
elif page == "💬 Full RAG Chat":
    st.title("💬 Student Records AI Assistant")
    
    # Sidebar settings for this page
    with st.sidebar:
        st.subheader("⚙️ Settings")
        
        providers = RAGEngine.get_available_providers()
        
        if providers:
            provider = st.selectbox(
                "Select Provider:",
                providers,
                index=providers.index(st.session_state.current_provider) if st.session_state.current_provider in providers else 0
            )
            st.session_state.current_provider = provider
            
            # Model selection for Ollama
            if provider == "ollama":
                from ollama_provider import OllamaProvider
                models = OllamaProvider.get_available_models()
                if models:
                    model = st.selectbox(
                        "Select Model:",
                        models,
                        index=models.index(st.session_state.current_model) if st.session_state.current_model in models else 0
                    )
                    st.session_state.current_model = model
            
            st.divider()
            
            # Initialize RAG engine if needed
            if st.session_state.rag_engine is None or st.session_state.rag_engine.provider_type != provider:
                ollama_model = st.session_state.current_model if provider == "ollama" else None
                st.session_state.rag_engine = RAGEngine(provider_type=provider, ollama_model=ollama_model)
            
            # Chat controls
            col1, col2 = st.columns(2)
            with col1:
                if st.button("💾 Save Chat", use_container_width=True):
                    filename = f"chat_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
                    with open(filename, 'w') as f:
                        json.dump(st.session_state.chat_history, f, indent=2)
                    st.success(f"Saved to {filename}")
            
            with col2:
                if st.button("🔄 Clear Chat", use_container_width=True):
                    st.session_state.chat_history = []
                    st.rerun()
        else:
            st.error("❌ No providers available!")
    
    # Display chat history
    chat_container = st.container()
    with chat_container:
        for msg in st.session_state.chat_history:
            if msg["role"] == "user":
                with st.chat_message("user"):
                    st.write(msg["content"])
            else:
                with st.chat_message("assistant"):
                    st.write(msg["content"])
                    st.caption(f"Provider: {msg.get('provider', 'unknown')} • {msg.get('timestamp', '')}")
    
    st.divider()
    
    # Input area
    user_input = st.chat_input("Ask about students, courses, or academics...")
    
    if user_input and st.session_state.rag_engine:
        st.session_state.chat_history.append({
            "role": "user",
            "content": user_input
        })
        
        with st.chat_message("user"):
            st.write(user_input)
        
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = st.session_state.rag_engine.query(user_input)
            st.write(response)
            st.caption(f"Provider: {st.session_state.current_provider.upper()} • {datetime.now().strftime('%H:%M:%S')}")
        
        st.session_state.chat_history.append({
            "role": "assistant",
            "content": response,
            "provider": st.session_state.current_provider,
            "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        })

# PAGE 3: Gemini Module
elif page == "🔧 Gemini Module":
    st.title("🔧 Workshop Module 1: Gemini Integration")
    
    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown("Learn how to integrate Google Gemini for student queries")
    with col2:
        if st.button("📖 View Code"):
            st.info("Run: `python workshop_basic_gemini.py`")
    
    try:
        rag = RAGEngine(provider_type="gemini")
        
        st.subheader("📝 Example Prompts")
        examples = rag.get_example_prompts()
        for i, example in enumerate(examples, 1):
            st.write(f"{i}. {example}")
        
        st.divider()
        st.subheader("🧪 Try Gemini")
        
        user_query = st.text_area("Enter your question:")
        
        if st.button("Query Gemini", use_container_width=True):
            with st.spinner("Querying Gemini..."):
                response = rag.query(user_query)
            
            st.success("Response:")
            st.write(response)
    
    except Exception as e:
        st.error(f"❌ Gemini not available: {str(e)}")
        st.info("Set GEMINI_API_KEY environment variable")

# PAGE 4: Ollama Module
elif page == "🦙 Ollama Module":
    st.title("🦙 Workshop Module 2: Ollama Integration")
    
    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown("Learn how to integrate local Ollama models for student queries")
    with col2:
        if st.button("📖 View Code"):
            st.info("Run: `python workshop_basic_ollama.py`")
    
    try:
        from ollama_provider import OllamaProvider
        
        if not OllamaProvider.is_available():
            st.error("❌ Ollama not running")
            st.info("Start Ollama: `ollama serve`")
            st.stop()
        
        models = OllamaProvider.get_available_models()
        
        st.subheader("📦 Available Models")
        st.write(", ".join(models) if models else "No models found")
        
        selected_model = st.selectbox("Select Model:", models)
        
        st.divider()
        
        rag = RAGEngine(provider_type="ollama", ollama_model=selected_model)
        
        st.subheader("📝 Example Prompts")
        examples = rag.get_example_prompts()
        for i, example in enumerate(examples, 1):
            st.write(f"{i}. {example}")
        
        st.divider()
        st.subheader("🧪 Try Ollama")
        
        user_query = st.text_area("Enter your question:")
        
        if st.button("Query Ollama", use_container_width=True):
            with st.spinner(f"Querying {selected_model}..."):
                response = rag.query(user_query)
            
            st.success("Response:")
            st.write(response)
    
    except Exception as e:
        st.error(f"❌ Error: {str(e)}")

# PAGE 5: Prompts Practice
elif page == "✍️ Prompts Practice":
    st.title("✍️ Workshop Module 3: Prompt Engineering")
    
    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown("Learn how to write effective prompts for student database queries")
    with col2:
        if st.button("📖 View Code"):
            st.info("Run: `python workshop_simple_prompts.py`")
    
    providers = RAGEngine.get_available_providers()
    
    if not providers:
        st.error("❌ No providers available")
        st.stop()
    
    col1, col2 = st.columns(2)
    with col1:
        provider = st.selectbox("Select Provider:", providers)
    with col2:
        if provider == "ollama":
            from ollama_provider import OllamaProvider
            models = OllamaProvider.get_available_models()
            model = st.selectbox("Select Model:", models) if models else None
        else:
            model = None
    
    st.divider()
    
    # Prompt templates
    templates = {
        "Student GPA": "What is {name}'s GPA?",
        "Student Major": "What is {name}'s major?",
        "Enrolled Courses": "What courses is {name} enrolled in?",
        "Course Info": "Tell me about {course_id}",
        "Highest GPA": "Which student has the highest GPA?",
        "Course Enrollment": "How many students are enrolled in {course_id}?",
    }
    
    st.subheader("📋 Prompt Templates")
    
    col1, col2 = st.columns(2)
    
    with col1:
        template_choice = st.selectbox("Select a template:", list(templates.keys()))
        template = templates[template_choice]
        st.write(f"Template: `{template}`")
    
    with col2:
        st.write("**Fill in the variables:**")
        import re
        var_names = re.findall(r'\{(\w+)\}', template)
        variables = {}
        for var in var_names:
            variables[var] = st.text_input(f"{var}:")
    
    st.divider()
    
    # Custom prompt option
    st.subheader("✏️ Or Write Custom Prompt")
    custom_prompt = st.text_area("Enter your custom prompt:")
    
    st.divider()
    
    # Execute
    if st.button("Execute Prompt", use_container_width=True):
        # Build final prompt
        if custom_prompt:
            final_prompt = custom_prompt
        else:
            try:
                final_prompt = template.format(**variables)
            except KeyError as e:
                st.error(f"Missing variable: {e}")
                st.stop()
        
        st.info(f"**Final Prompt:** {final_prompt}")
        
        # Query
        rag = RAGEngine(provider_type=provider, ollama_model=model)
        
        with st.spinner("Processing..."):
            response = rag.query(final_prompt)
        
        st.success("Response:")
        st.write(response)
        
        # Show statistics
        st.divider()
        st.subheader("📊 Prompt Statistics")
        col1, col2, col3 = st.columns(3)
        col1.metric("Prompt Length", len(final_prompt))
        col2.metric("Response Length", len(response))
        col3.metric("Provider", provider.upper())

# Footer
st.divider()
st.markdown("""
---
**🎓 Student Records RAG Workshop**
- Learn Generative AI & RAG concepts
- Practice with real student database
- Master prompt engineering
""")
