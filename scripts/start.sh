#!/bin/bash

# 🚀 Script de démarrage Arkalia Quest
# Active l'environnement virtuel et lance l'application

echo "🌟 Démarrage d'Arkalia Quest..."

# Vérifier si l'environnement virtuel existe
if [ ! -d "venv" ]; then
    echo "❌ Environnement virtuel non trouvé. Création..."
    python3 -m venv venv
fi

# Activer l'environnement virtuel
echo "🔧 Activation de l'environnement virtuel..."
source venv/bin/activate

# Installer les dépendances si nécessaire
echo "📦 Vérification des dépendances..."
pip install -r requirements.txt

# Créer le dossier logs s'il n'existe pas
mkdir -p logs

# Lancer l'application
echo "🚀 Lancement d'Arkalia Quest..."
echo "📍 Application accessible sur: http://localhost:5001"
echo "🛑 Appuyez sur Ctrl+C pour arrêter"
echo ""

python app.py
