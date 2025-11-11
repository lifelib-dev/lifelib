# Makefile pour le projet lifelib
# Automatisation de l'environnement de développement et des tâches courantes

.PHONY: help venv install install-dev install-test clean clean-all test test-cov lint format check build dist

# Variables
PYTHON := python3
VENV := venv_lifelib
BIN := $(VENV)/bin
PYTHON_VENV := $(BIN)/python
PIP := $(BIN)/pip

# Détection de l'OS pour activation
ifeq ($(OS),Windows_NT)
	ACTIVATE := $(VENV)/Scripts/activate
else
	ACTIVATE := $(BIN)/activate
endif

# Couleurs pour l'affichage
BLUE := \033[0;34m
GREEN := \033[0;32m
YELLOW := \033[0;33m
RED := \033[0;31m
NC := \033[0m # No Color

# Cible par défaut
.DEFAULT_GOAL := help

help: ## Afficher cette aide
	@echo "$(BLUE)═══════════════════════════════════════════════════════════$(NC)"
	@echo "$(BLUE)  Makefile pour lifelib - Gestion de l'environnement$(NC)"
	@echo "$(BLUE)═══════════════════════════════════════════════════════════$(NC)"
	@echo ""
	@echo "$(GREEN)Commandes disponibles :$(NC)"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  $(YELLOW)%-20s$(NC) %s\n", $$1, $$2}'
	@echo ""
	@echo "$(BLUE)Exemples d'utilisation :$(NC)"
	@echo "  make venv          # Créer l'environnement virtuel"
	@echo "  make install-dev   # Installer en mode développement"
	@echo "  make test          # Lancer les tests"
	@echo "  make format        # Formater le code"
	@echo ""

venv: ## Créer l'environnement virtuel Python
	@echo "$(BLUE)Création de l'environnement virtuel...$(NC)"
	@if [ ! -d "$(VENV)" ]; then \
		$(PYTHON) -m venv $(VENV); \
		echo "$(GREEN)✓ Environnement virtuel créé dans $(VENV)$(NC)"; \
	else \
		echo "$(YELLOW)⚠ L'environnement virtuel existe déjà$(NC)"; \
	fi
	@echo ""
	@echo "$(GREEN)Pour activer l'environnement virtuel :$(NC)"
	@echo "  source $(ACTIVATE)"

install: venv ## Installer le package en mode production
	@echo "$(BLUE)Installation du package en mode production...$(NC)"
	@$(PIP) install --upgrade pip setuptools wheel
	@$(PIP) install -e .
	@echo "$(GREEN)✓ Installation terminée$(NC)"

install-dev: venv ## Installer le package en mode développement (avec dépendances dev)
	@echo "$(BLUE)Installation du package en mode développement...$(NC)"
	@$(PIP) install --upgrade pip setuptools wheel
	@$(PIP) install -e ".[dev]"
	@echo "$(GREEN)✓ Installation développement terminée$(NC)"
	@echo ""
	@echo "$(GREEN)Dépendances installées :$(NC)"
	@echo "  - modelx (runtime)"
	@echo "  - pytest, pytest-cov, pytest-xdist (tests)"
	@echo "  - pandas, numpy, openpyxl (tests)"
	@echo "  - flake8, black, isort (dev)"

install-test: venv ## Installer le package en mode test uniquement
	@echo "$(BLUE)Installation du package en mode test...$(NC)"
	@$(PIP) install --upgrade pip setuptools wheel
	@$(PIP) install -e ".[test]"
	@echo "$(GREEN)✓ Installation test terminée$(NC)"

upgrade: venv ## Mettre à jour toutes les dépendances
	@echo "$(BLUE)Mise à jour des dépendances...$(NC)"
	@$(PIP) install --upgrade pip setuptools wheel
	@$(PIP) install --upgrade -e ".[dev]"
	@echo "$(GREEN)✓ Dépendances mises à jour$(NC)"

test: ## Lancer les tests avec pytest
	@echo "$(BLUE)Lancement des tests...$(NC)"
	@$(BIN)/pytest -v --cov=lifelib --cov-report=term-missing
	@echo "$(GREEN)✓ Tests terminés$(NC)"

test-cov: ## Lancer les tests avec rapport de couverture HTML
	@echo "$(BLUE)Lancement des tests avec rapport de couverture...$(NC)"
	@$(BIN)/pytest --cov=lifelib --cov-report=html --cov-report=term --cov-report=xml
	@echo "$(GREEN)✓ Rapport de couverture généré dans htmlcov/index.html$(NC)"

test-fast: ## Lancer les tests en parallèle (rapide)
	@echo "$(BLUE)Lancement des tests en parallèle...$(NC)"
	@$(BIN)/pytest -n auto -v
	@echo "$(GREEN)✓ Tests terminés$(NC)"

lint: ## Vérifier le code avec flake8
	@echo "$(BLUE)Vérification du code avec flake8...$(NC)"
	@$(BIN)/flake8 lifelib --count --select=E9,F63,F7,F82 --show-source --statistics
	@$(BIN)/flake8 lifelib --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics
	@echo "$(GREEN)✓ Vérification terminée$(NC)"

format: ## Formater le code avec black et isort
	@echo "$(BLUE)Formatage du code avec black et isort...$(NC)"
	@$(BIN)/black lifelib
	@$(BIN)/isort lifelib
	@echo "$(GREEN)✓ Code formaté$(NC)"

check: ## Vérifier le formatage sans modifier les fichiers
	@echo "$(BLUE)Vérification du formatage...$(NC)"
	@$(BIN)/black --check lifelib
	@$(BIN)/isort --check-only lifelib
	@echo "$(GREEN)✓ Vérification terminée$(NC)"

check-all: lint check ## Vérifier le code et le formatage (lint + check)
	@echo "$(GREEN)✓ Toutes les vérifications sont terminées$(NC)"

build: ## Construire le package (sdist et wheel)
	@echo "$(BLUE)Construction du package...$(NC)"
	@$(PYTHON_VENV) -m pip install --upgrade build
	@$(PYTHON_VENV) -m build
	@echo "$(GREEN)✓ Package construit dans dist/$(NC)"

dist: clean build ## Nettoyer et construire le package pour distribution

clean: ## Nettoyer les fichiers générés (cache, build, etc.)
	@echo "$(BLUE)Nettoyage des fichiers générés...$(NC)"
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
	@echo "$(GREEN)✓ Nettoyage terminé$(NC)"

clean-all: clean ## Nettoyer tout y compris l'environnement virtuel
	@echo "$(BLUE)Suppression de l'environnement virtuel...$(NC)"
	@rm -rf $(VENV)
	@echo "$(GREEN)✓ Environnement virtuel supprimé$(NC)"

info: ## Afficher les informations sur l'environnement
	@echo "$(BLUE)═══════════════════════════════════════════════════════════$(NC)"
	@echo "$(BLUE)  Informations sur l'environnement$(NC)"
	@echo "$(BLUE)═══════════════════════════════════════════════════════════$(NC)"
	@echo ""
	@echo "$(GREEN)Python :$(NC)"
	@which $(PYTHON) && $(PYTHON) --version || echo "Python non trouvé"
	@echo ""
	@if [ -d "$(VENV)" ]; then \
		echo "$(GREEN)Environnement virtuel :$(NC) $(VENV) (actif)"; \
		echo "$(GREEN)Version Python :$(NC)"; \
		$(PYTHON_VENV) --version; \
		echo ""; \
		echo "$(GREEN)Packages installés :$(NC)"; \
		$(PIP) list; \
	else \
		echo "$(YELLOW)Environnement virtuel non créé$(NC)"; \
		echo "Lancez 'make venv' pour le créer"; \
	fi

shell: ## Ouvrir un shell dans l'environnement virtuel
	@echo "$(BLUE)Ouverture d'un shell dans l'environnement virtuel...$(NC)"
	@echo "$(YELLOW)Pour quitter : tapez 'exit'$(NC)"
	@. $(ACTIVATE) && exec $(SHELL)

tox: venv ## Lancer les tests avec tox (tous les environnements)
	@echo "$(BLUE)Installation et lancement de tox...$(NC)"
	@$(PIP) install tox
	@$(BIN)/tox

tox-lint: venv ## Lancer uniquement le linting avec tox
	@echo "$(BLUE)Lancement du linting avec tox...$(NC)"
	@$(PIP) install tox
	@$(BIN)/tox -e lint

init: install-dev ## Initialiser complètement l'environnement de développement
	@echo ""
	@echo "$(GREEN)═══════════════════════════════════════════════════════════$(NC)"
	@echo "$(GREEN)  Environnement de développement prêt !$(NC)"
	@echo "$(GREEN)═══════════════════════════════════════════════════════════$(NC)"
	@echo ""
	@echo "$(YELLOW)Pour activer l'environnement virtuel :$(NC)"
	@echo "  source $(ACTIVATE)"
	@echo ""
	@echo "$(YELLOW)Commandes utiles :$(NC)"
	@echo "  make test       # Lancer les tests"
	@echo "  make format     # Formater le code"
	@echo "  make lint       # Vérifier le code"
	@echo "  make help       # Voir toutes les commandes"
	@echo ""
