#!/bin/bash

echo "🚀 Démarrage d'Arkalia Quest avec Gunicorn (mode production)"
echo "=========================================================="

# Vérification de l'environnement virtuel
if [ ! -d ".venv-quest" ]; then
    echo "❌ Environnement virtuel non trouvé"
    echo "💡 Lancez: source activate-quest.sh"
    exit 1
fi

# Activation de l'environnement virtuel
source .venv-quest/bin/activate

# Installation des dépendances si nécessaire
echo "📦 Vérification des dépendances..."
pip install -r requirements.txt

# Démarrage avec gunicorn
echo "🌐 Démarrage du serveur sur http://localhost:5001"
echo "💡 Appuyez sur Ctrl+C pour arrêter"
echo ""

gunicorn app:app \
    --bind 0.0.0.0:5001 \
    --workers 2 \
    --timeout 120 \
    --access-logfile - \
    --error-logfile - \
    --log-level info 