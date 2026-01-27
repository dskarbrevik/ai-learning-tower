.PHONY: help lint test setup

.DEFAULT_GOAL := help

##@ Setup

setup: ## Set up development environment
	@echo "Checking for uv..."
	@command -v uv >/dev/null 2>&1 || { echo "Error: uv is not installed. Install it with: curl -LsSf https://astral.sh/uv/install.sh | sh"; exit 1; }
	@echo "✓ uv is installed"
	@echo "Installing dependencies..."
	uv sync --group dev
	@echo "✓ Dependencies installed"
	@echo "\n✅ Setup complete! Run 'make help' to see available commands."

##@ Development

lint: ## Run linting and formatting with ruff
	uv run ruff check --fix
	uv run ruff format

##@ Testing

test: ## Run tests with pytest
	uv run pytest

##@ Help

help: ## Display this help message
	@awk 'BEGIN {FS = ":.*##"; printf "\nUsage:\n  make \033[36m<target>\033[0m\n"} /^[a-zA-Z_-]+:.*?##/ { printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2 } /^##@/ { printf "\n\033[1;33m%s\033[0m\n", substr($$0, 5) } ' $(MAKEFILE_LIST)
