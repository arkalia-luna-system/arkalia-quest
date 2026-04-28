#!/usr/bin/env bash
# 🚀 Script de démarrage unifié Arkalia Quest
# Usage: ./start.sh [dev|prod|eval]  (défaut: dev)
#   dev  = Flask seul (port 5001)
#   prod = Gunicorn si dispo, sinon Flask
#   eval = Lancement + vérification curl pour évaluation

set -euo pipefail
cd "$(dirname "$0")"

MODE="${1:-dev}"
HOST="${HOST:-0.0.0.0}"
PORT="${PORT:-5001}"
PYTHON_BIN="${PYTHON_BIN:-python3}"

echo "🌟 Arkalia Quest — mode: $MODE"

# Environnement virtuel
if [ ! -d "venv" ]; then
    echo "❌ Environnement virtuel non trouvé. Création..."
    "$PYTHON_BIN" -m venv venv
fi
echo "🔧 Activation du venv..."
# shellcheck disable=SC1091
source venv/bin/activate

# Dépendances
echo "📦 Vérification des dépendances..."
python -m pip install -q -r requirements.txt

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
        exec python -m flask run --host="$HOST" --port="$PORT"
    fi
    ;;
eval)
    export FLASK_APP=app.py
    if pgrep -f "flask run" >/dev/null 2>&1; then
        echo "✅ Application déjà en cours"
    else
        echo "🚀 Lancement de l'application..."
        python -m flask run --host="$HOST" --port="$PORT" &
        sleep 3
    fi
    echo "🔍 Vérification..."
    if ! command -v curl >/dev/null 2>&1; then
        echo "❌ curl est requis en mode eval."
        exit 1
    fi
    if curl -fsS "http://localhost:${PORT}/health" >/dev/null; then
        echo "✅ Application accessible sur http://localhost:${PORT}/"
    else
        echo "❌ L'application ne répond pas."
        exit 1
    fi
    echo "🎯 Prêt pour l'évaluation."
    exit 0
    ;;
dev|*)
    echo "📍 http://localhost:${PORT} — Ctrl+C pour arrêter"
    export FLASK_APP=app.py
    export HOST PORT
    exec python app.py
    ;;
esac
