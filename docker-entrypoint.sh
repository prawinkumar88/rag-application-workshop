#!/bin/bash
set -e

echo "🚀 Starting RAG Application..."

# Wait for Ollama to be ready
if [ ! -z "$OLLAMA_BASE_URL" ]; then
    echo "⏳ Waiting for Ollama service..."
    until curl -s "$OLLAMA_BASE_URL/api/tags" > /dev/null 2>&1; do
        sleep 2
    done
    echo "✅ Ollama is ready!"
fi

# Initialize vector database if needed
if [ ! -d "/app/chroma_db" ]; then
    echo "📦 Initializing vector database..."
    mkdir -p /app/chroma_db
fi

# Execute the main command
exec "$@"
