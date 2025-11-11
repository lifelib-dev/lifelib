# Makefile for lifelib project
# Automation of development environment and common tasks

.PHONY: help venv install install-dev install-test clean clean-all test test-cov lint format check build dist

# Variables
PYTHON := python3
VENV := venv_lifelib
BIN := $(VENV)/bin
PYTHON_VENV := $(BIN)/python
PIP := $(BIN)/pip

# OS detection for activation
ifeq ($(OS),Windows_NT)
	ACTIVATE := $(VENV)/Scripts/activate
else
	ACTIVATE := $(BIN)/activate
endif

# Colors for display
BLUE := \033[0;34m
GREEN := \033[0;32m
YELLOW := \033[0;33m
RED := \033[0;31m
NC := \033[0m # No Color

# Default target
.DEFAULT_GOAL := help

help: ## Display this help message
	@echo "$(BLUE)═══════════════════════════════════════════════════════════$(NC)"
	@echo "$(BLUE)  Makefile for lifelib - Environment Management$(NC)"
	@echo "$(BLUE)═══════════════════════════════════════════════════════════$(NC)"
	@echo ""
	@echo "$(GREEN)Available commands:$(NC)"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  $(YELLOW)%-20s$(NC) %s\n", $$1, $$2}'
	@echo ""
	@echo "$(BLUE)Usage examples:$(NC)"
	@echo "  make venv          # Create virtual environment"
	@echo "  make install-dev   # Install in development mode"
	@echo "  make test          # Run tests"
	@echo "  make format        # Format code"
	@echo ""

venv: ## Create Python virtual environment
	@echo "$(BLUE)Creating virtual environment...$(NC)"
	@if [ ! -d "$(VENV)" ]; then \
		$(PYTHON) -m venv $(VENV); \
		echo "$(GREEN)✓ Virtual environment created in $(VENV)$(NC)"; \
	else \
		echo "$(YELLOW)⚠ Virtual environment already exists$(NC)"; \
	fi
	@echo ""
	@echo "$(GREEN)To activate the virtual environment:$(NC)"
	@echo "  source $(ACTIVATE)"

install: venv ## Install package in production mode
	@echo "$(BLUE)Installing package in production mode...$(NC)"
	@$(PIP) install --upgrade pip setuptools wheel
	@$(PIP) install -e .
	@echo "$(GREEN)✓ Installation complete$(NC)"

install-dev: venv ## Install package in development mode (with dev dependencies)
	@echo "$(BLUE)Installing package in development mode...$(NC)"
	@$(PIP) install --upgrade pip setuptools wheel
	@$(PIP) install -e ".[dev]"
	@echo "$(GREEN)✓ Development installation complete$(NC)"
	@echo ""
	@echo "$(GREEN)Installed dependencies:$(NC)"
	@echo "  - modelx (runtime)"
	@echo "  - pytest, pytest-cov, pytest-xdist (tests)"
	@echo "  - pandas, numpy, openpyxl (tests)"
	@echo "  - flake8, black, isort (dev)"

install-test: venv ## Install package in test mode only
	@echo "$(BLUE)Installing package in test mode...$(NC)"
	@$(PIP) install --upgrade pip setuptools wheel
	@$(PIP) install -e ".[test]"
	@echo "$(GREEN)✓ Test installation complete$(NC)"

upgrade: venv ## Upgrade all dependencies
	@echo "$(BLUE)Upgrading dependencies...$(NC)"
	@$(PIP) install --upgrade pip setuptools wheel
	@$(PIP) install --upgrade -e ".[dev]"
	@echo "$(GREEN)✓ Dependencies upgraded$(NC)"

test: ## Run tests with pytest
	@echo "$(BLUE)Running tests...$(NC)"
	@$(BIN)/pytest -v --cov=lifelib --cov-report=term-missing
	@echo "$(GREEN)✓ Tests completed$(NC)"

test-cov: ## Run tests with HTML coverage report
	@echo "$(BLUE)Running tests with coverage report...$(NC)"
	@$(BIN)/pytest --cov=lifelib --cov-report=html --cov-report=term --cov-report=xml
	@echo "$(GREEN)✓ Coverage report generated in htmlcov/index.html$(NC)"

test-fast: ## Run tests in parallel (fast)
	@echo "$(BLUE)Running tests in parallel...$(NC)"
	@$(BIN)/pytest -n auto -v
	@echo "$(GREEN)✓ Tests completed$(NC)"

lint: ## Check code with flake8
	@echo "$(BLUE)Checking code with flake8...$(NC)"
	@$(BIN)/flake8 lifelib --count --select=E9,F63,F7,F82 --show-source --statistics
	@$(BIN)/flake8 lifelib --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics
	@echo "$(GREEN)✓ Check complete$(NC)"

format: ## Format code with black and isort
	@echo "$(BLUE)Formatting code with black and isort...$(NC)"
	@$(BIN)/black lifelib
	@$(BIN)/isort lifelib
	@echo "$(GREEN)✓ Code formatted$(NC)"

check: ## Check formatting without modifying files
	@echo "$(BLUE)Checking formatting...$(NC)"
	@$(BIN)/black --check lifelib
	@$(BIN)/isort --check-only lifelib
	@echo "$(GREEN)✓ Check complete$(NC)"

check-all: lint check ## Check code and formatting (lint + check)
	@echo "$(GREEN)✓ All checks completed$(NC)"

build: ## Build package (sdist and wheel)
	@echo "$(BLUE)Building package...$(NC)"
	@$(PYTHON_VENV) -m pip install --upgrade build
	@$(PYTHON_VENV) -m build
	@echo "$(GREEN)✓ Package built in dist/$(NC)"

dist: clean build ## Clean and build package for distribution

clean: ## Clean generated files (cache, build, etc.)
	@echo "$(BLUE)Cleaning generated files...$(NC)"
	@rm -rf build/
	@rm -rf dist/
	@rm -rf *.egg-info
	@rm -rf .pytest_cache/
	@rm -rf .coverage
	@rm -rf htmlcov/
	@rm -rf .tox/
	@find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	@find . -type f -name "*.pyc" -delete
	@find . -type f -name "*.pyo" -delete
	@find . -type f -name "*.pyd" -delete
	@find . -type f -name ".coverage.*" -delete
	@echo "$(GREEN)✓ Cleaning complete$(NC)"

clean-all: clean ## Clean everything including virtual environment
	@echo "$(BLUE)Removing virtual environment...$(NC)"
	@rm -rf $(VENV)
	@echo "$(GREEN)✓ Virtual environment removed$(NC)"

info: ## Display environment information
	@echo "$(BLUE)═══════════════════════════════════════════════════════════$(NC)"
	@echo "$(BLUE)  Environment Information$(NC)"
	@echo "$(BLUE)═══════════════════════════════════════════════════════════$(NC)"
	@echo ""
	@echo "$(GREEN)Python:$(NC)"
	@which $(PYTHON) && $(PYTHON) --version || echo "Python not found"
	@echo ""
	@if [ -d "$(VENV)" ]; then \
		echo "$(GREEN)Virtual environment:$(NC) $(VENV) (active)"; \
		echo "$(GREEN)Python version:$(NC)"; \
		$(PYTHON_VENV) --version; \
		echo ""; \
		echo "$(GREEN)Installed packages:$(NC)"; \
		$(PIP) list; \
	else \
		echo "$(YELLOW)Virtual environment not created$(NC)"; \
		echo "Run 'make venv' to create it"; \
	fi

shell: ## Open shell in virtual environment
	@echo "$(BLUE)Opening shell in virtual environment...$(NC)"
	@echo "$(YELLOW)To exit: type 'exit'$(NC)"
	@. $(ACTIVATE) && exec $(SHELL)

tox: venv ## Run tests with tox (all environments)
	@echo "$(BLUE)Installing and running tox...$(NC)"
	@$(PIP) install tox
	@$(BIN)/tox

tox-lint: venv ## Run linting only with tox
	@echo "$(BLUE)Running linting with tox...$(NC)"
	@$(PIP) install tox
	@$(BIN)/tox -e lint

init: install-dev ## Fully initialize development environment
	@echo ""
	@echo "$(GREEN)═══════════════════════════════════════════════════════════$(NC)"
	@echo "$(GREEN)  Development environment ready!$(NC)"
	@echo "$(GREEN)═══════════════════════════════════════════════════════════$(NC)"
	@echo ""
	@echo "$(YELLOW)To activate the virtual environment:$(NC)"
	@echo "  source $(ACTIVATE)"
	@echo ""
	@echo "$(YELLOW)Useful commands:$(NC)"
	@echo "  make test       # Run tests"
	@echo "  make format     # Format code"
	@echo "  make lint       # Check code"
	@echo "  make help       # See all commands"
	@echo ""
