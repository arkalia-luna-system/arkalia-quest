#!/bin/bash

# 🚀 Script de démarrage optimisé - Arkalia Quest
# Version 3.0.0 - Janvier 2025

echo "🌌 Démarrage d'Arkalia Quest v3.0.0..."
echo "========================================"

# Vérification de l'environnement Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 n'est pas installé"
    exit 1
fi

# Vérification des dépendances
echo "🔍 Vérification des dépendances..."
python3 -c "import flask, sqlite3, json" 2>/dev/null || {
    echo "❌ Dépendances manquantes. Installez avec: pip install -r requirements.txt"
    exit 1
}

# Vérification de la base de données
echo "🗄️ Vérification de la base de données..."
if [ ! -f "arkalia.db" ]; then
    echo "📊 Initialisation de la base de données..."
    python3 -c "from core.database import DatabaseManager; db = DatabaseManager(); print('✅ Base de données initialisée')"
fi

# Vérification des fichiers de données
echo "📁 Vérification des fichiers de données..."
[ -f "data/profiles/main_profile.json" ] || echo "⚠️ Profil principal manquant"
[ -d "data/missions" ] || echo "⚠️ Dossier missions manquant"
[ -d "logs" ] || echo "⚠️ Dossier logs manquant"

# Démarrage de l'application
echo "🚀 Lancement d'Arkalia Quest..."
echo "🌐 Interface disponible sur: http://localhost:5001"
echo "💻 Terminal immersif: http://localhost:5001/terminal"
echo "🌍 Monde Arkalia: http://localhost:5001/monde"
echo ""
echo "🛑 Appuyez sur Ctrl+C pour arrêter"
echo "========================================"

# Lancement avec gestion d'erreurs
python3 app.py
