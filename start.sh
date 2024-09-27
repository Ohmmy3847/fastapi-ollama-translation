#!/bin/bash

# Start Ollama in the background
ollama serve &

# Wait for Ollama to start
echo "Waiting for Ollama to start..."
while ! curl -s http://localhost:11434/api/tags >/dev/null; do
    sleep 1
done

# Pull the Qwen2 model
echo "Pulling Qwen2 model..."
ollama pull qwen2

# Start the FastAPI application
echo "Starting FastAPI application..."
uvicorn app:app --host 0.0.0.0 --port 8000