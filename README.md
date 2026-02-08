# RAG Application

A modular Retrieval-Augmented Generation (RAG) application for student records and academic advising. Supports both Gemini and Ollama LLM providers, with standalone workshop modules and Streamlit integration.

---

## 🚀 Installation & Setup

```bash
# Install dependencies
pip install streamlit google-generativeai requests python-dotenv

# Set up environment variables
echo "GEMINI_API_KEY=your-key-here" > .env
echo "OLLAMA_BASE_URL=http://localhost:11434" >> .env
echo "OLLAMA_MODEL=mistral" >> .env
```

---

## 🎓 How to Run Each Module

### Option 1: Standalone Modules (Workshop)

```bash
# Module 1: Gemini only
python workshop_basic_gemini.py

# Module 2: Ollama only
python workshop_basic_ollama.py

# Module 3: Prompt Practice
python workshop_simple_prompts.py
```

### Option 2: Full Streamlit Integration

```bash
streamlit run app.py
```

---

## 📚 Streamlit Modules

- **Overview**: Workshop introduction & architecture
- **Full RAG Chat**: Complete chat with history, save/load
- **Gemini Module**: Isolated Gemini testing
- **Ollama Module**: Isolated Ollama testing
- **Prompts Practice**: Learn prompt templates & engineering

---

## ✨ Key Features

- ✅ Modular Design - Each component is independent
- ✅ Standalone Scripts - Run workshops without Streamlit
- ✅ Provider Switching - Switch Gemini/Ollama anytime
- ✅ Chat History - Save & load conversations
- ✅ Prompt Templates - Pre-built query patterns
- ✅ Example Prompts - Learn from 8+ examples
- ✅ Real Database - 3 students, 4 courses with actual data
