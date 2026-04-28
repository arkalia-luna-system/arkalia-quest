# Makefile pour Arkalia Quest
# Version 3.1.0

.PHONY: help install install-dev test test-fast lint format check ci security docs docs-serve build clean run run-dev docker-build docker-run purge-appledouble

PYTHON := python3
PIP := pip
PROJECT_NAME := arkalia-quest
TEST_DIR := tests
SRC := app.py core routes tests

PURGE_APPLEDOUBLE = $(PYTHON) -c "import pathlib; root=pathlib.Path('.'); files=list(root.rglob('._*')); [p.unlink(missing_ok=True) for p in files if p.is_file()]"

help: ## Afficher l'aide
	@echo "Arkalia Quest - commandes maintenues"
	@echo ""
	@echo "  make install-dev  # deps dev/docs/security"
	@echo "  make check        # format + lint + tests"
	@echo "  make ci           # check + docs strict"
	@echo "  make run-dev      # lancement local"

install: ## Installer deps runtime
	$(PIP) install -e .

install-dev: ## Installer deps dev
	$(PIP) install -e .[dev,docs,security]

test: ## Lancer toute la suite de tests
	$(PYTHON) -m pytest $(TEST_DIR) -q

test-fast: ## Lancer les tests coeur
	$(PYTHON) -m pytest tests/test_api_routes.py tests/test_story_engine.py -q

lint: ## Verifier la qualite avec ruff
	ruff check .

format: ## Formater le code Python
	black app.py core routes tests

security: ## Audit securite des dependances
	$(PYTHON) -m pip_audit -r requirements.txt

docs: ## Build docs strict
	$(MAKE) purge-appledouble
	mkdocs build --strict

docs-serve: ## Servir docs en local
	mkdocs serve

build: ## Construire le package Python
	bash scripts/build_package.sh

run: ## Lancer l'app (mode script)
	$(PYTHON) app.py

run-dev: ## Lancer en dev explicite
	FLASK_ENV=development FLASK_DEBUG=1 $(PYTHON) app.py

docker-build: ## Construire image Docker
	docker build -t $(PROJECT_NAME):latest .

docker-run: ## Lancer image Docker
	docker run -p 5001:5001 $(PROJECT_NAME):latest

clean: ## Nettoyer artefacts locaux courants
	$(PYTHON) -c "import pathlib,shutil; root=pathlib.Path('.'); targets=['build','dist','site','__pycache__','.mypy_cache','.pytest_cache','.ruff_cache','.benchmarks','arkalia_quest.egg-info','logs']; [shutil.rmtree(root/t, ignore_errors=True) for t in targets]; [p.unlink() for p in root.rglob('._*') if p.is_file()]; [p.unlink() for p in [root/'.coverage', root/'coverage.xml'] if p.exists()]"

purge-appledouble: ## Supprimer les artefacts macOS ._*
	@$(PURGE_APPLEDOUBLE)

check: ## Verification locale recommandee
	$(MAKE) format
	$(MAKE) lint
	$(MAKE) test

ci: ## Pipeline locale complete maintenue
	$(MAKE) check
	$(MAKE) docs
