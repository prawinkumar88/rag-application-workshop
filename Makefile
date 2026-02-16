.PHONY: help build up down logs shell test workshop clean

help:
	@echo "RAG Application Docker Commands"
	@echo "================================"
	@echo "build         - Build Docker images"
	@echo "up            - Start all services"
	@echo "down          - Stop all services"
	@echo "logs          - View logs"
	@echo "shell         - Open shell in container"
	@echo "workshop      - Run workshop module"
	@echo "vector-demo   - Run vector store demo"
	@echo "dev           - Start development mode"
	@echo "clean         - Clean up containers and volumes"
	@echo "pull-ollama   - Pull Ollama models"

build:
	docker-compose build

up:
	docker-compose up -d
	@echo "Services started!"
	@echo "Main UI: http://localhost:8501"
	@echo "Vector UI: http://localhost:8502"
	@echo "Ollama: http://localhost:11434"

down:
	docker-compose down

logs:
	docker-compose logs -f

logs-app:
	docker-compose logs -f rag-app

logs-ollama:
	docker-compose logs -f ollama

shell:
	docker exec -it rag-application /bin/bash

shell-ollama:
	docker exec -it ollama-service /bin/bash

workshop:
	docker exec -it rag-application python workshop_basic_gemini.py

vector-demo:
	docker exec -it rag-application python demo_vector_search.py

dev:
	docker-compose -f docker-compose.dev.yml up

clean:
	docker-compose down -v
	docker system prune -f

pull-ollama:
	docker exec -it ollama-service ollama pull mistral
	docker exec -it ollama-service ollama pull llama2

restart:
	docker-compose restart

status:
	docker-compose ps
