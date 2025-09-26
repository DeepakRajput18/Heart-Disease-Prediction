# Heart Disease Prediction System - Makefile
# Cross-platform commands for easy development

.PHONY: help install setup start dev simple minimal full test clean docker-build docker-run docker-compose-up docker-compose-down

# Default target
help:
	@echo "🫀 Heart Disease Prediction System - Available Commands"
	@echo "=================================================="
	@echo "Setup Commands:"
	@echo "  make install          - Install Python dependencies"
	@echo "  make setup            - Full setup (install + database)"
	@echo ""
	@echo "Server Commands:"
	@echo "  make start            - Start server (auto-detect best option)"
	@echo "  make dev              - Start development server"
	@echo "  make simple           - Start ultra simple server"
	@echo "  make minimal          - Start minimal server"
	@echo "  make full             - Start full server with all features"
	@echo ""
	@echo "Development Commands:"
	@echo "  make test             - Run tests"
	@echo "  make clean            - Clean temporary files"
	@echo ""
	@echo "Docker Commands:"
	@echo "  make docker-build     - Build Docker image"
	@echo "  make docker-run       - Run Docker container"
	@echo "  make docker-compose-up - Start with Docker Compose"
	@echo "  make docker-compose-down - Stop Docker Compose"

# Installation
install:
	@echo "📦 Installing dependencies..."
	@python -m pip install --upgrade pip || pip install --upgrade pip || pip3 install --upgrade pip
	@python -m pip install -r requirements.txt || pip install -r requirements.txt || pip3 install -r requirements.txt

# Setup
setup: install
	@echo "🔧 Setting up database..."
	@python init_db.py || python3 init_db.py || echo "⚠️ Database setup skipped"

# Server commands
start:
	@python run_commands.py start

dev:
	@python run_commands.py dev

simple:
	@python run_commands.py simple

minimal:
	@python run_commands.py minimal

full:
	@python run_commands.py full

# Testing
test:
	@python run_commands.py test

# Database
init-db:
	@python run_commands.py init-db

# Cleanup
clean:
	@echo "🧹 Cleaning temporary files..."
	@find . -type f -name "*.pyc" -delete 2>/dev/null || true
	@find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	@find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	@rm -rf .coverage htmlcov/ 2>/dev/null || true
	@echo "✅ Cleanup completed"

# Docker commands
docker-build:
	@python run_commands.py docker-build

docker-run:
	@python run_commands.py docker-run

docker-compose-up:
	@python run_commands.py docker-compose-up

docker-compose-down:
	@python run_commands.py docker-compose-down

# Windows compatibility
install-windows:
	@echo "📦 Installing dependencies (Windows)..."
	@py -m pip install --upgrade pip
	@py -m pip install -r requirements.txt

start-windows:
	@py ultra_simple.py