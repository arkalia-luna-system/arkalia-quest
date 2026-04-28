#!/usr/bin/env bash

# 🚀 Script de déploiement Arkalia Quest
# Usage: ./scripts/deploy.sh [platform]

set -euo pipefail

PLATFORM=${1:-"local"}
VERSION="${VERSION:-3.1.0}"

echo "🚀 Déploiement Arkalia Quest v$VERSION sur $PLATFORM"
echo "=================================================="

# Vérifications pré-déploiement
echo "🔍 Vérifications pré-déploiement..."

# Tests
echo "🧪 Exécution des tests..."
python -m pytest tests/ --tb=no -q

# Qualité du code
echo "🎨 Vérification de la qualité..."
black --check . --quiet && echo "✅ Black: PASS"
ruff check . --quiet && echo "✅ Ruff: PASS"

# Construction
echo "🔨 Construction de l'application..."

case "$PLATFORM" in
    "local")
        echo "🏠 Déploiement local..."
        python app.py
        ;;
    "docker")
        echo "🐳 Déploiement Docker..."
        
        # Vérifier que Docker est disponible
        if ! command -v docker &> /dev/null; then
            echo "❌ Docker n'est pas installé"
            exit 1
        fi
        
        # Vérifier que Docker daemon est en cours d'exécution
        if ! docker info &> /dev/null; then
            echo "❌ Docker daemon n'est pas en cours d'exécution"
            exit 1
        fi
        
        # Arrêter et supprimer le conteneur existant s'il existe
        if docker ps -a --format "table {{.Names}}" | grep -q "arkalia-quest"; then
            echo "🔄 Arrêt du conteneur existant..."
            docker stop arkalia-quest || true
            docker rm arkalia-quest || true
        fi
        
        # Construire l'image
        echo "🔨 Construction de l'image Docker..."
        docker build -t "arkalia-quest:$VERSION" .
        
        # Lancer le conteneur
        echo "🚀 Lancement du conteneur..."
        docker run -d \
            -p 5001:5001 \
            --name arkalia-quest \
            --restart unless-stopped \
            "arkalia-quest:$VERSION"
        
        echo "✅ Déployé sur http://localhost:5001"
        echo "📋 Commandes utiles:"
        echo "   docker logs arkalia-quest          # Voir les logs"
        echo "   docker stop arkalia-quest          # Arrêter"
        echo "   docker start arkalia-quest         # Redémarrer"
        ;;
    "docker-build")
        echo "🐳 Construction Docker uniquement..."
        
        if ! command -v docker &> /dev/null; then
            echo "❌ Docker n'est pas installé"
            exit 1
        fi
        
        echo "🔨 Construction de l'image Docker..."
        docker build -t "arkalia-quest:$VERSION" .
        echo "✅ Image construite: arkalia-quest:$VERSION"
        ;;
    "render")
        echo "🌐 Déploiement Render..."
        echo "✅ Configuration Render prête - déployez via le dashboard"
        ;;
    *)
        echo "❌ Plateforme non reconnue: $PLATFORM"
        echo "📋 Plateformes supportées: local, docker, docker-build, render"
        exit 1
        ;;
esac

echo ""
echo "🎉 Déploiement terminé avec succès !"
echo "🌍 Vérifiez l'endpoint de santé: /health"
