#!/bin/bash

# Script de démarrage optimisé pour Arkalia Quest V3.2.0
# Évite les fuites de ressources et optimise les performances

echo "🚀 Démarrage optimisé d'Arkalia Quest V3.2.0..."

# Activer l'environnement virtuel
source venv/bin/activate

# Arrêter les processus existants
pkill -f "python.*app.py" 2>/dev/null
pkill -f "gunicorn.*app:app" 2>/dev/null

# Attendre que les processus se terminent
sleep 2

# Vérifier si Gunicorn est disponible
if command -v gunicorn &> /dev/null; then
    echo "✅ Démarrage avec Gunicorn (production optimisée)"
    gunicorn -c gunicorn.conf.py app:app
else
    echo "⚠️  Gunicorn non trouvé, démarrage avec Flask (développement)"
    echo "   Installez Gunicorn : pip install gunicorn"
    echo ""
    export FLASK_APP=app.py
    export FLASK_ENV=production
    python -m flask run --host=0.0.0.0 --port=5001
fi
