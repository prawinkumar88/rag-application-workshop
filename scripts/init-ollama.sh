#!/bin/bash

echo "🦙 Initializing Ollama models..."

# Wait for Ollama to start
sleep 5

# Pull models
echo "📥 Pulling mistral model..."
ollama pull mistral

echo "📥 Pulling llama2 model..."
ollama pull llama2

echo "✅ Ollama models ready!"

# List available models
ollama list
