#!/bin/bash

# 🚀 Script de préparation pour le push - Arkalia Quest
# Version 3.0.0 - Janvier 2025

echo "🌌 Préparation du push pour Arkalia Quest v3.0.0..."
echo "=================================================="

# 1. Vérification de l'environnement Python
echo "🔍 Vérification de l'environnement Python..."
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 n'est pas installé"
    exit 1
fi

# 2. Application de ruff (correction automatique)
echo "🧹 Application de ruff (correction automatique)..."
if command -v ruff &> /dev/null; then
    ruff check --fix core/ app.py arkalia_engine.py
    echo "✅ Ruff appliqué avec succès"
else
    echo "⚠️ Ruff non installé, installation..."
    pip install ruff
    ruff check --fix core/ app.py arkalia_engine.py
fi

# 3. Application de black (formatage)
echo "🎨 Application de black (formatage)..."
if command -v black &> /dev/null; then
    black core/ app.py arkalia_engine.py
    echo "✅ Black appliqué avec succès"
else
    echo "⚠️ Black non installé, installation..."
    pip install black
    black core/ app.py arkalia_engine.py
fi

# 4. Vérification finale avec ruff
echo "🔍 Vérification finale avec ruff..."
if ruff check core/ app.py arkalia_engine.py; then
    echo "✅ Aucune erreur détectée"
else
    echo "❌ Erreurs détectées, correction manuelle requise"
    exit 1
fi

# 5. Test de l'application
echo "🧪 Test de l'application..."
timeout 10s python3 app.py &
APP_PID=$!
sleep 3

if curl -s http://localhost:5001 > /dev/null; then
    echo "✅ Application fonctionne correctement"
    kill $APP_PID 2>/dev/null
else
    echo "❌ Application ne fonctionne pas"
    kill $APP_PID 2>/dev/null
    exit 1
fi

# 6. Test des nouvelles commandes
echo "⌨️ Test des nouvelles commandes d'histoire..."
if curl -s -X POST http://localhost:5001/commande -H "Content-Type: application/json" -d '{"cmd": "prologue"}' | grep -q "PROLOGUE"; then
    echo "✅ Commande prologue fonctionne"
else
    echo "❌ Commande prologue ne fonctionne pas"
    exit 1
fi

# 7. Nettoyage des fichiers temporaires
echo "🧹 Nettoyage des fichiers temporaires..."
find . -name "._*" -delete 2>/dev/null
find . -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null
find . -name "*.pyc" -delete 2>/dev/null

# 8. Vérification de la structure
echo "📁 Vérification de la structure du projet..."
if [ -f "app.py" ] && [ -d "core" ] && [ -d "data" ] && [ -d "static" ] && [ -d "templates" ]; then
    echo "✅ Structure du projet correcte"
else
    echo "❌ Structure du projet incorrecte"
    exit 1
fi

echo ""
echo "🎉 PRÉPARATION TERMINÉE AVEC SUCCÈS !"
echo "======================================"
echo "✅ Code formaté avec black"
echo "✅ Erreurs corrigées avec ruff"
echo "✅ Application testée et fonctionnelle"
echo "✅ Nouvelles commandes d'histoire opérationnelles"
echo "✅ Structure du projet vérifiée"
echo ""
echo "🚀 Prêt pour le push !"
echo "📝 Utilisez : git add . && git commit -m 'feat: Arkalia Quest v3.0.0 - Commandes d'histoire complètes'"
echo "📤 Puis : git push"
