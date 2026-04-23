# Smart Lobster - Development Makefile

.PHONY: help install format lint test clean run docker-build docker-run

help:
	@echo "Smart Lobster Development Commands:"
	@echo "  make install      - Install dependencies"
	@echo "  make format       - Format code with black"
	@echo "  make lint         - Run flake8 linting"
	@echo "  make test         - Run pytest"
	@echo "  make check        - Run format + lint + test"
	@echo "  make clean        - Clean cache files"
	@echo "  make run          - Start development server"
	@echo "  make docker-build - Build Docker image"
	@echo "  make docker-run   - Run Docker container"

install:
	pip install -r requirements.txt

format:
	black . --line-length 100

lint:
	flake8 . --max-line-length 100 --extend-ignore=E203,W503

test:
	pytest tests/ -v --tb=short

check: format lint test
	@echo "✅ All checks passed!"

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type f -name ".coverage" -delete
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name "htmlcov" -exec rm -rf {} + 2>/dev/null || true

run:
	python -m core.fraud_detector

docker-build:
	docker build -t smart-lobster:latest .

docker-run:
	docker run -p 8000:8000 --env-file .env smart-lobster:latest