# Makefile pour Arkalia Quest - Jeu Éducatif Intelligent
# Version 3.0.0

.PHONY: help install install-dev test test-cov lint format security clean build run run-dev check ci pylint all

# === VARIABLES ===
PYTHON := python3
PIP := pip
PROJECT_NAME := arkalia-quest
VENV_NAME := venv
SOURCE_DIRS := core engines utils
TEST_DIR := tests
DOCS_DIR := docs
REPORTS_DIR := reports

# === AIDE ===
help: ## Afficher cette aide
	@echo "🎮 Arkalia Quest - Makefile d'aide"
	@echo "=================================="
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'
	@echo ""
	@echo "🚀 Commandes rapides:"
	@echo "  make install-dev  # Installation complète pour développement"
	@echo "  make run-dev      # Lancer en mode développement"
	@echo "  make ci           # Tests complets + qualité"
	@echo "  make check        # Vérification rapide avant commit"

# === INSTALLATION ===
install: ## Installer les dépendances de production
	@echo "📦 Installation des dépendances de production..."
	$(PIP) install -e .

install-dev: ## Installer les dépendances de développement
	@echo "🛠️ Installation complète pour développement..."
	$(PIP) install -e .[dev,docs,security]
	@echo "✅ Installation terminée !"

# === TESTS ===
test: ## Lancer les tests
	@echo "🧪 Lancement des tests..."
	$(PYTHON) -m pytest $(TEST_DIR) -v

test-cov: ## Tests avec couverture de code
	@echo "📊 Tests avec couverture de code..."
	$(PYTHON) -m pytest $(TEST_DIR) --cov=$(SOURCE_DIRS) --cov-report=html --cov-report=xml --cov-report=term-missing
	@echo "📄 Rapport HTML généré: htmlcov/index.html"

test-performance: ## Tests de performance
	@echo "⚡ Tests de performance..."
	$(PYTHON) -m pytest $(TEST_DIR)/performance/ -v --benchmark-only

test-security: ## Tests de sécurité
	@echo "🛡️ Tests de sécurité..."
	$(PYTHON) -m pytest $(TEST_DIR) -v -m security

test-integration: ## Tests d'intégration
	@echo "🔗 Tests d'intégration..."
	$(PYTHON) -m pytest $(TEST_DIR) -v -m integration

test-all: ## Tous les tests (unitaires, intégration, performance, sécurité)
	@echo "🎯 Lancement de tous les tests..."
	$(PYTHON) -m pytest $(TEST_DIR) -v --cov=$(SOURCE_DIRS) --cov-report=html --cov-report=xml

# === QUALITÉ DU CODE ===
lint: ## Vérifier la qualité du code (ruff)
	@echo "🔍 Vérification qualité du code..."
	ruff check $(SOURCE_DIRS) $(TEST_DIR) --fix
	@echo "✅ Linting terminé !"

format: ## Formater le code (black + isort)
	@echo "🎨 Formatage du code..."
	black $(SOURCE_DIRS) $(TEST_DIR) app.py
	isort $(SOURCE_DIRS) $(TEST_DIR) app.py
	@echo "✅ Formatage terminé !"

pylint: ## Analyse approfondie avec pylint
	@echo "🔎 Analyse pylint..."
	pylint $(SOURCE_DIRS) --output-format=text --reports=no --score=no || true
	@echo "📄 Rapport sauvegardé: pylint_report.txt"

mypy: ## Vérification des types avec mypy
	@echo "🔬 Vérification des types..."
	mypy $(SOURCE_DIRS)

security: ## Analyse de sécurité (bandit)
	@echo "🛡️ Analyse de sécurité..."
	bandit -r $(SOURCE_DIRS) -f json -o bandit-report.json || true
	bandit -r $(SOURCE_DIRS) -f txt || true
	@echo "📄 Rapport sécurité: bandit-report.json"

security-deps: ## Vérifier vulnérabilités des dépendances
	@echo "🔒 Vérification sécurité des dépendances..."
	safety check || true

# === NETTOYAGE ===
clean: ## Nettoyer les fichiers temporaires
	@echo "🧹 Nettoyage des fichiers temporaires..."
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".mypy_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".ruff_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -name "*.pyc" -delete 2>/dev/null || true
	find . -name "*.pyo" -delete 2>/dev/null || true
	find . -name "*~" -delete 2>/dev/null || true
	find . -name "._*" -delete 2>/dev/null || true
	rm -rf build/ dist/ htmlcov/ .coverage coverage.xml
	@echo "✅ Nettoyage terminé !"

clean-logs: ## Nettoyer les logs
	@echo "📝 Nettoyage des logs..."
	rm -rf logs/*.log 2>/dev/null || true
	touch logs/arkalia.log logs/error.log logs/security.log
	@echo "✅ Logs nettoyés !"

# === BUILD ET PACKAGING ===
build: ## Construire le package
	@echo "📦 Construction du package..."
	$(PYTHON) -m build
	@echo "✅ Package construit dans dist/"

version: ## Afficher la version
	@$(PYTHON) -c "try: import tomllib; except ImportError: import tomli as tomllib; print(tomllib.load(open('pyproject.toml', 'rb'))['project']['version'])"

release: ## Créer une release (version + tag + build)
	@echo "🚀 Création de la release..."
	@$(MAKE) version
	@$(MAKE) clean
	@$(MAKE) test-all
	@$(MAKE) build
	@echo "✅ Release prête dans dist/"

# === DÉMARRAGE ===
run: ## Lancer l'application en mode production
	@echo "🚀 Lancement Arkalia Quest (production)..."
	$(PYTHON) app.py

run-dev: ## Lancer l'application en mode développement
	@echo "🛠️ Lancement Arkalia Quest (développement)..."
	FLASK_ENV=development FLASK_DEBUG=1 $(PYTHON) app.py

run-gunicorn: ## Lancer avec Gunicorn (production)
	@echo "🚀 Lancement avec Gunicorn..."
	gunicorn --bind 0.0.0.0:5001 --workers 4 app:app

start: ## Script de démarrage automatique
	@echo "🎯 Lancement automatique..."
	chmod +x start.sh
	./start.sh

# === DOCKER ===
docker-build: ## Construire l'image Docker
	@echo "🐳 Construction image Docker..."
	docker build -t $(PROJECT_NAME):latest .

docker-run: ## Lancer le conteneur Docker
	@echo "🐳 Lancement conteneur Docker..."
	docker run -p 5001:5001 $(PROJECT_NAME):latest

docker-compose: ## Lancer avec Docker Compose
	@echo "🐳 Lancement Docker Compose..."
	docker-compose up -d

# === DÉVELOPPEMENT ===
dev-setup: ## Configuration complète environnement de développement
	@echo "🛠️ Configuration développement..."
	@$(MAKE) install-dev
	@$(MAKE) clean
	@echo "✅ Environnement prêt !"

check: ## Vérification rapide avant commit
	@echo "🔍 Vérification rapide..."
	@$(MAKE) format
	@$(MAKE) lint
	@$(MAKE) test
	@echo "✅ Vérification réussie !"

# === CI/CD ===
ci: ## Pipeline CI complète (format + lint + test + sécurité)
	@echo "🎯 Pipeline CI complète..."
	@$(MAKE) format
	@$(MAKE) lint
	@$(MAKE) mypy
	@$(MAKE) security
	@$(MAKE) test-all
	@echo "🎉 Pipeline CI réussie !"

ci-fast: ## Pipeline CI rapide (pas de tests longs)
	@echo "⚡ Pipeline CI rapide..."
	@$(MAKE) format
	@$(MAKE) lint
	@$(MAKE) test
	@echo "✅ Pipeline CI rapide réussie !"

# === DOCUMENTATION ===
docs: ## Générer la documentation
	@echo "📚 Génération documentation..."
	mkdocs build
	@echo "📄 Documentation: site/index.html"

docs-serve: ## Servir la documentation en local
	@echo "📚 Service documentation (http://localhost:8000)..."
	mkdocs serve

# === MÉTRIQUES ET MONITORING ===
metrics: ## Afficher métriques du projet
	@echo "📊 Métriques Arkalia Quest"
	@echo "========================="
	@echo "📁 Lignes de code:"
	@find $(SOURCE_DIRS) -name "*.py" -exec wc -l {} + | tail -1
	@echo "🧪 Tests:"
	@find $(TEST_DIR) -name "test_*.py" | wc -l | awk '{print $$1 " fichiers de test"}'
	@echo "📄 Documentation:"
	@find $(DOCS_DIR) -name "*.md" | wc -l | awk '{print $$1 " fichiers markdown"}'
	@echo "🔧 Configuration:"
	@ls -la | grep -E '\.(toml|yml|yaml|json|ini)$$' | wc -l | awk '{print $$1 " fichiers de config"}'

status: ## Afficher le statut complet du projet
	@echo "🎮 Statut Arkalia Quest"
	@echo "======================"
	@echo "📦 Version: $(shell $(MAKE) version)"
	@echo "🐍 Python: $(shell $(PYTHON) --version)"
	@echo "📁 Répertoire: $(shell pwd)"
	@echo "🌿 Branche Git: $(shell git branch --show-current 2>/dev/null || echo 'Non Git')"
	@echo "💾 Espace disque: $(shell df -h . | tail -1 | awk '{print $$4 " libre"}')"
	@$(MAKE) metrics

# === UTILS ===
requirements: ## Mettre à jour requirements.txt depuis pyproject.toml
	@echo "📋 Mise à jour requirements.txt..."
	pip-compile pyproject.toml --output-file requirements.txt || true

upgrade-deps: ## Mettre à jour toutes les dépendances
	@echo "⬆️ Mise à jour des dépendances..."
	$(PIP) install --upgrade pip setuptools wheel
	pip-compile --upgrade pyproject.toml || true

# === COMMANDES COMBINÉES ===
all: ## Tout faire (clean + install + check + test + build)
	@echo "🎯 Exécution complète..."
	@$(MAKE) clean
	@$(MAKE) install-dev
	@$(MAKE) check
	@$(MAKE) test-all
	@$(MAKE) build
	@echo "🎉 Exécution complète réussie !"

fresh: ## Reset complet + installation + tests
	@echo "🔄 Reset complet..."
	@$(MAKE) clean
	@$(MAKE) dev-setup
	@$(MAKE) test
	@echo "✅ Reset terminé !"
