#!/bin/bash
# 🚀 Script de build personnalisé pour Render
# Force l'utilisation de pip et ignore Poetry

set -e  # Arrêter en cas d'erreur
set -u  # Arrêter si variable non définie

echo "🚀 DÉBUT DU BUILD ARKALIA QUEST"
echo "================================"

# Vérification de l'environnement Python
echo "🐍 Vérification de la version Python..."
python --version
python -c "import sys; print(f'Python path: {sys.executable}')"

# Mise à jour de pip
echo "📦 Mise à jour de pip..."
pip install --upgrade pip

# Vérification de l'environnement
echo "🔧 Vérification de l'environnement..."
echo "PWD: $(pwd)"
echo "Files: $(ls -la)"

# Installation des dépendances
echo "📋 Installation des dépendances depuis requirements.txt..."
if [ -f "requirements.txt" ]; then
    echo "✅ requirements.txt trouvé"
    echo "📄 Contenu de requirements.txt:"
    cat requirements.txt
    echo ""
    echo "🔧 Installation en cours..."
    pip install -r requirements.txt --no-cache-dir
else
    echo "❌ requirements.txt non trouvé!"
    exit 1
fi

# Test d'import de l'application
echo "🧪 Test d'import de l'application..."
python -c "import app; print('✅ App importée avec succès')"

# Vérification finale
echo "🔍 Vérification des modules installés..."
python -c "
import sys
required_modules = ['flask', 'gunicorn', 'flask_compress']
for module in required_modules:
    try:
        __import__(module)
        print(f'✅ {module} disponible')
    except ImportError as e:
        print(f'❌ {module} manquant: {e}')
        sys.exit(1)
"

echo "✅ BUILD TERMINÉ AVEC SUCCÈS!"
echo "================================"
