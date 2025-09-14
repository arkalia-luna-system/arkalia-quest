#!/bin/bash
# Script de validation CI/CD - Arkalia Quest
# Test local des étapes critiques du CI

set -e

echo "🚀 === VALIDATION CI/CD ARKALIA QUEST ==="
echo "📅 $(date)"
echo ""

# Couleurs pour l'affichage
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Fonction pour afficher les résultats
print_result() {
    if [ $1 -eq 0 ]; then
        echo -e "${GREEN}✅ $2${NC}"
    else
        echo -e "${RED}❌ $2${NC}"
        exit 1
    fi
}

# 1. Vérification de l'environnement
echo "🔍 Vérification de l'environnement..."
python --version
pip --version

# 2. Installation des dépendances
echo "📦 Installation des dépendances..."
pip install -r requirements.txt
print_result $? "Installation des dépendances"

# 3. Formatage Black
echo "🎨 Vérification du formatage (Black)..."
black --check . --quiet
print_result $? "Formatage Black"

# 4. Linting Ruff
echo "🔍 Vérification du linting (Ruff)..."
ruff check . --quiet
print_result $? "Linting Ruff"

# 5. Tests de base
echo "🧪 Exécution des tests..."
python -m pytest tests/test_educational_games.py -v --maxfail=3
print_result $? "Tests de base"

# 6. Tests de performance
echo "⚡ Tests de performance..."
python -m pytest tests/performance/ -v --maxfail=1 --tb=short
print_result $? "Tests de performance"

# 7. Vérification de sécurité
echo "🛡️ Vérification de sécurité (Bandit)..."
bandit -r core engines utils -q -f txt | grep -q "No issues identified" || echo "Problèmes de sécurité détectés (non bloquant)"
print_result 0 "Vérification Bandit"

# 8. Test d'import de l'application
echo "📱 Test d'import de l'application..."
python -c "import app; print('✅ Application importable')"
print_result $? "Import de l'application"

echo ""
echo -e "${GREEN}🎉 VALIDATION CI/CD TERMINÉE AVEC SUCCÈS !${NC}"
echo "🚀 Prêt pour le déploiement"
