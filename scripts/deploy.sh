#!/bin/bash

# 🚀 Script de déploiement Arkalia Quest
# Usage: ./scripts/deploy.sh [platform]

set -e

PLATFORM=${1:-"local"}
VERSION="3.0.0"

echo "🚀 Déploiement Arkalia Quest v$VERSION sur $PLATFORM"
echo "=================================================="

# Vérifications pré-déploiement
echo "🔍 Vérifications pré-déploiement..."

# Tests
echo "🧪 Exécution des tests..."
python -m pytest tests/ --tb=no -q | tail -1

# Qualité du code
echo "🎨 Vérification de la qualité..."
black --check . --quiet && echo "✅ Black: PASS"
ruff check . --quiet && echo "✅ Ruff: PASS"

# Construction
echo "🔨 Construction de l'application..."

case $PLATFORM in
    "local")
        echo "🏠 Déploiement local..."
        python app.py
        ;;
    "docker")
        echo "🐳 Déploiement Docker..."
        docker build -f config/Dockerfile -t arkalia-quest:$VERSION .
        docker run -d -p 5000:5000 --name arkalia-quest arkalia-quest:$VERSION
        echo "✅ Déployé sur http://localhost:5000"
        ;;
    "heroku")
        echo "🎯 Déploiement Heroku..."
        if command -v heroku &> /dev/null; then
            heroku container:push web
            heroku container:release web
            echo "✅ Déployé sur Heroku"
        else
            echo "❌ Heroku CLI non installé"
            exit 1
        fi
        ;;
    "render")
        echo "🌐 Déploiement Render..."
        echo "✅ Configuration Render prête - déployez via le dashboard"
        ;;
    "railway")
        echo "🚂 Déploiement Railway..."
        if command -v railway &> /dev/null; then
            railway up
            echo "✅ Déployé sur Railway"
        else
            echo "❌ Railway CLI non installé"
            exit 1
        fi
        ;;
    "vps")
        echo "🖥️ Déploiement VPS..."
        echo "✅ Configuration systemd prête dans config/systemd/"
        echo "📋 Commandes à exécuter sur le serveur:"
        echo "   sudo cp config/systemd/arkalia-quest.service /etc/systemd/system/"
        echo "   sudo systemctl daemon-reload"
        echo "   sudo systemctl enable arkalia-quest"
        echo "   sudo systemctl start arkalia-quest"
        ;;
    *)
        echo "❌ Plateforme non reconnue: $PLATFORM"
        echo "📋 Plateformes supportées: local, docker, heroku, render, railway, vps"
        exit 1
        ;;
esac

echo ""
echo "🎉 Déploiement terminé avec succès !"
echo "🌍 Vérifiez l'endpoint de santé: /health"
echo "📊 Vérifiez les métriques: /metrics"
