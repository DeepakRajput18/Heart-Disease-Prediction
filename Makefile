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
	@python3 -m pip install -r requirements.txt 2>/dev/null || \
	 pip3 install -r requirements.txt 2>/dev/null || \
	 pip install -r requirements.txt 2>/dev/null || \
	 echo "⚠️ Could not install dependencies. Please install pip first or use Docker."

# Setup
setup: install
	@echo "🔧 Setting up database..."
	@python3 init_db.py || echo "⚠️ Database setup skipped"

# Server commands
start:
	@python3 run_commands.py start

dev:
	@python3 run_commands.py dev

simple:
	@python3 run_commands.py simple

minimal:
	@python3 run_commands.py minimal

full:
	@python3 run_commands.py full

# Testing
test:
	@python3 run_commands.py test

# Database
init-db:
	@python3 run_commands.py init-db

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
	@python3 run_commands.py docker-build

docker-run:
	@python3 run_commands.py docker-run

docker-compose-up:
	@python3 run_commands.py docker-compose-up

docker-compose-down:
	@python3 run_commands.py docker-compose-down

# Windows compatibility
install-windows:
	@echo "📦 Installing dependencies (Windows)..."
	@py -m pip install --upgrade pip
	@py -m pip install -r requirements.txt

start-windows:
	@py ultra_simple.py