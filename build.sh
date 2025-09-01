#!/bin/bash
# 🚀 Script de build personnalisé pour Render
# Force l'utilisation de pip et ignore Poetry

set -e  # Arrêter en cas d'erreur

echo "🚀 DÉBUT DU BUILD ARKALIA QUEST"
echo "================================"

echo "🐍 Vérification de la version Python..."
python --version

echo "📦 Mise à jour de pip..."
pip install --upgrade pip

echo "🔧 Vérification de l'environnement..."
echo "PWD: $(pwd)"
echo "Files: $(ls -la)"

echo "📋 Installation des dépendances depuis requirements.txt..."
if [ -f "requirements.txt" ]; then
    echo "✅ requirements.txt trouvé"
    cat requirements.txt
    pip install -r requirements.txt
else
    echo "❌ requirements.txt non trouvé!"
    exit 1
fi

echo "🧪 Test d'import de l'application..."
python -c "import app; print('✅ App importée avec succès')"

echo "✅ BUILD TERMINÉ AVEC SUCCÈS!"
echo "================================"
