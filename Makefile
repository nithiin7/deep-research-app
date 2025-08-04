.PHONY: help install install-dev test test-cov lint format type-check clean run setup

help: ## Show this help message
	@echo "Deep Research App - Development Commands"
	@echo "========================================"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

setup: ## Initial setup of the project
	@echo "Setting up Deep Research App..."
	@if [ ! -f .env ]; then \
		echo "Creating .env file from template..."; \
		cp .env.example .env; \
		echo "Please edit .env file with your API keys and email addresses"; \
	else \
		echo ".env file already exists"; \
	fi

install: ## Install production dependencies
	uv pip install -r requirements.txt

install-dev: ## Install development dependencies
	uv pip install -r requirements.txt
	uv pip install pytest pytest-asyncio pytest-cov black flake8 mypy pre-commit

test: ## Run tests
	pytest

test-cov: ## Run tests with coverage
	pytest --cov=src/deep_research --cov-report=html --cov-report=term

lint: ## Run linting checks
	flake8 src/ tests/

format: ## Format code with black
	black src/ tests/

format-check: ## Check if code is formatted correctly
	black --check src/ tests/

type-check: ## Run type checking
	mypy src/

check: format-check lint type-check ## Run all code quality checks

clean: ## Clean up generated files
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	rm -rf build/
	rm -rf dist/
	rm -rf .pytest_cache/
	rm -rf .mypy_cache/
	rm -rf htmlcov/
	rm -rf .coverage

run: ## Run the application
	python -m src.deep_research.main

run-dev: ## Run the application in development mode
	LOG_LEVEL=DEBUG python -m src.deep_research.main

docker-build: ## Build Docker image
	docker build -t deep-research-app .

docker-run: ## Run Docker container
	docker run -p 7860:7860 --env-file .env deep-research-app

pre-commit-install: ## Install pre-commit hooks
	pre-commit install

pre-commit-run: ## Run pre-commit on all files
	pre-commit run --all-files

docs: ## Generate documentation
	@echo "Documentation generation not yet implemented"

package: ## Create distribution package
	python -m build

publish: ## Publish to PyPI (requires authentication)
	python -m twine upload dist/*

# Development workflow
dev-setup: setup install-dev pre-commit-install ## Complete development setup
	@echo "Development environment setup complete!"

# Quick development cycle
dev: format lint type-check test ## Run full development cycle 