#!/bin/bash
# 🚀 Script de démarrage unifié Arkalia Quest
# Usage: ./start.sh [dev|prod|eval]  (défaut: dev)
#   dev  = Flask seul (port 5001)
#   prod = Gunicorn si dispo, sinon Flask
#   eval = Lancement + vérification curl pour évaluation

set -e
MODE="${1:-dev}"

echo "🌟 Arkalia Quest — mode: $MODE"

# Environnement virtuel
if [ ! -d "venv" ]; then
    echo "❌ Environnement virtuel non trouvé. Création..."
    python3 -m venv venv
fi
echo "🔧 Activation du venv..."
source venv/bin/activate

# Dépendances
echo "📦 Vérification des dépendances..."
pip install -q -r requirements.txt

mkdir -p logs

case "$MODE" in
prod)
    pkill -f "python.*app.py" 2>/dev/null || true
    pkill -f "gunicorn.*app:app" 2>/dev/null || true
    sleep 2
    if command -v gunicorn &>/dev/null; then
        echo "✅ Démarrage avec Gunicorn (production)"
        exec gunicorn -c gunicorn.conf.py app:app
    else
        echo "⚠️  Gunicorn non trouvé, démarrage Flask (production)"
        export FLASK_APP=app.py
        export FLASK_ENV=production
        exec python -m flask run --host=0.0.0.0 --port=5001
    fi
    ;;
eval)
    if pgrep -f "flask run" >/dev/null 2>&1; then
        echo "✅ Application déjà en cours"
    else
        echo "🚀 Lancement de l'application..."
        python -m flask run --host=0.0.0.0 --port=5001 &
        sleep 3
    fi
    echo "🔍 Vérification..."
    if curl -s http://localhost:5001/ >/dev/null; then
        echo "✅ Application accessible sur http://localhost:5001/"
    else
        echo "❌ L'application ne répond pas."
        exit 1
    fi
    echo "🎯 Prêt pour l'évaluation."
    exit 0
    ;;
dev|*)
    echo "📍 http://localhost:5001 — Ctrl+C pour arrêter"
    export FLASK_APP=app.py
    exec python app.py
    ;;
esac
