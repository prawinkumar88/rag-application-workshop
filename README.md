# RAG Application

A modular Retrieval-Augmented Generation (RAG) application for student records and academic advising. Supports both Gemini and Ollama LLM providers, with standalone workshop modules and Streamlit integration.

---

## 📋 Prerequisites

### Python Requirements
- **Python 3.9+** (Recommended: Python 3.10 or 3.11)
- pip (Python package manager)

Check your Python version:
```bash
python --version
# or
python3 --version
```

### VS Code Setup (Recommended)
- **Visual Studio Code** - [Download here](https://code.visualstudio.com/)
- **Python Extension** - Install from VS Code Extensions marketplace
- **Recommended Extensions**:
  - Python (Microsoft)
  - Pylance (Microsoft)
  - Python Debugger (Microsoft)
  - Jupyter (Optional, for notebook support)

---

## 🚀 Installation & Setup

### 1. Clone/Download the Project
```bash
cd /root/rag-application
```

### 2. Install Dependencies
```bash
# Install all dependencies from requirements.txt
pip install -r requirements.txt

# Or using pip3
pip3 install -r requirements.txt
```

### 3. Set up Environment Variables
```bash
# Set up environment variables
echo "GEMINI_API_KEY=your-key-here" > .env
echo "OLLAMA_BASE_URL=http://localhost:11434" >> .env
echo "OLLAMA_MODEL=mistral" >> .env
```

### 4. Verify Installation
```bash
# Check if Streamlit is installed
streamlit --version

# Check if packages are available
python -c "import streamlit; import google.generativeai; print('All packages installed successfully!')"
```

---

## 🐳 Docker Installation & Setup

### Quick Start with Docker

```bash
# 1. Clone/navigate to project
cd /root/rag-application

# 2. Create .env file
cat > .env << EOF
GEMINI_API_KEY=your-api-key-here
OLLAMA_BASE_URL=http://ollama:11434
OLLAMA_MODEL=mistral
EOF

# 3. Build and start services
docker-compose up -d

# 4. Access the application
# Main UI: http://localhost:8501
# Vector UI: http://localhost:8502
```

### Docker Commands

```bash
# Build images
make build
# or
docker-compose build

# Start services
make up
# or
docker-compose up -d

# View logs
make logs
# or
docker-compose logs -f

# Stop services
make down
# or
docker-compose down

# Run workshop modules
make workshop
# or
docker exec -it rag-application python workshop_basic_gemini.py

# Open shell in container
make shell
# or
docker exec -it rag-application /bin/bash
```

### Development Mode

```bash
# Start with hot-reload
make dev
# or
docker-compose -f docker-compose.dev.yml up
```

### Pull Ollama Models

```bash
# Pull models inside container
make pull-ollama
# or
docker exec -it ollama-service ollama pull mistral
docker exec -it ollama-service ollama pull llama2
```

### Docker Services

The application runs three services:

1. **rag-app** (Port 8501) - Main Streamlit UI
2. **vector-rag-ui** (Port 8502) - Vector RAG Demo UI
3. **ollama** (Port 11434) - Local LLM service

### GPU Support

For GPU acceleration with Ollama:

```yaml
# In docker-compose.yml, Ollama service already configured for GPU
# Requires: nvidia-docker installed
```

For CPU-only:
```bash
# Remove the 'deploy' section from ollama service in docker-compose.yml
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

# Module 4: Vector-based RAG (NEW!)
python workshop_vector_rag.py

# Bonus: Compare both approaches
python compare_rag_approaches.py
```

### Option 2: Full Streamlit Integration

```bash
# Main UI with all modules
streamlit run ui_streamlit.py

# Vector RAG focused UI (NEW!)
streamlit run ui_streamlit_vector.py
```

---

## 📚 Streamlit Modules

- **Overview**: Workshop introduction & architecture
- **Full RAG Chat**: Complete chat with history, save/load
- **🔍 Vector RAG**: Semantic search with embeddings (NEW!)
- **Gemini Module**: Isolated Gemini testing
- **Ollama Module**: Isolated Ollama testing
- **Prompts Practice**: Learn prompt templates & engineering

---

## ✨ Key Features

- ✅ Modular Design - Each component is independent
- ✅ Standalone Scripts - Run workshops without Streamlit
- ✅ Provider Switching - Switch Gemini/Ollama anytime
- ✅ **Vector Search** - Semantic retrieval with ChromaDB (NEW!)
- ✅ **Embeddings** - Sentence transformers for text similarity (NEW!)
- ✅ **Comparison Tool** - Compare prompt vs vector RAG (NEW!)
- ✅ Chat History - Save & load conversations
- ✅ Prompt Templates - Pre-built query patterns
- ✅ Example Prompts - Learn from 8+ examples
- ✅ Real Database - 3 students, 4 courses with actual data

---

## 🔧 Troubleshooting

### Common Issues

**Issue: `ModuleNotFoundError`**
```bash
# Solution: Reinstall dependencies
pip install -r requirements.txt
```

**Issue: Python version too old**
```bash
# Check version
python --version

# Upgrade Python to 3.9+ from python.org
```

**Issue: Streamlit command not found**
```bash
# Add Python Scripts to PATH or use:
python -m streamlit run ui_streamlit.py
```

---

## 📦 Project Structure

```
rag-application/
├── Dockerfile                   # Docker image definition
├── docker-compose.yml           # Multi-container setup
├── docker-compose.dev.yml       # Development mode
├── docker-entrypoint.sh         # Initialization script
├── Makefile                     # Easy commands
├── .dockerignore               # Files to exclude
├── ui_streamlit.py              # Main Streamlit UI
├── ui_streamlit_vector.py       # Vector RAG focused UI (NEW!)
├── rag_engine.py                # Prompt-based RAG engine
├── vector_rag_engine.py         # Vector-based RAG engine (NEW!)
├── vector_store.py              # ChromaDB vector database (NEW!)
├── embeddings_provider.py       # Text embeddings (NEW!)
├── compare_rag_approaches.py    # Comparison tool (NEW!)
├── prompts.py                   # Prompt templates
├── database.py                  # Student database
├── gemini_provider.py           # Gemini integration
├── ollama_provider.py           # Ollama integration
├── workshop_basic_gemini.py     # Standalone Module 1
├── workshop_basic_ollama.py     # Standalone Module 2
├── workshop_simple_prompts.py   # Standalone Module 3
├── workshop_vector_rag.py       # Standalone Module 4 (NEW!)
├── requirements.txt             # Python dependencies
├── .env                         # Environment variables
├── chroma_db/                   # Vector database storage (NEW!)
└── README.md                    # This file
```
