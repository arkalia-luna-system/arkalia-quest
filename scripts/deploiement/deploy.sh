#!/bin/bash
# Script de déploiement pour arkalia-quest
# Généré automatiquement par Athalia

set -e

echo "🚀 Déploiement de arkalia-quest..."

# Variables
PROJECT_NAME="arkalia-quest"
DOCKER_IMAGE="$PROJECT_NAME:latest"
K8S_NAMESPACE="default"

# Vérifier que Docker est disponible
if ! command -v docker &> /dev/null; then
    echo "❌ Docker n'est pas installé ou n'est pas dans le PATH"
    exit 1
fi

# Vérifier que Docker daemon est en cours d'exécution
if ! docker info &> /dev/null; then
    echo "❌ Docker daemon n'est pas en cours d'exécution"
    exit 1
fi

# Build de l'image Docker
echo "📦 Build de l'image Docker..."
docker build -t $DOCKER_IMAGE -f config/Dockerfile .

# Vérifier si on a des credentials Docker (pour le push)
if [ -n "$DOCKER_USERNAME" ] && [ -n "$DOCKER_PASSWORD" ]; then
    echo "🔐 Authentification Docker..."
    # Utiliser --password-stdin pour éviter les problèmes de TTY
    echo "$DOCKER_PASSWORD" | docker login -u "$DOCKER_USERNAME" --password-stdin
    
    # Tag et push vers le registry
    echo "📤 Push vers le registry Docker..."
    docker tag $DOCKER_IMAGE "$DOCKER_USERNAME/$DOCKER_IMAGE"
    docker push "$DOCKER_USERNAME/$DOCKER_IMAGE"
else
    echo "ℹ️ Pas de credentials Docker - skip du push"
fi

# Déploiement Kubernetes (si kubectl est disponible)
if command -v kubectl &> /dev/null; then
    echo "☸️ Déploiement Kubernetes..."
    kubectl apply -f k8s/k8s-deployment.yaml
    kubectl apply -f k8s/k8s-service.yaml
    
    # Vérification du déploiement
    echo "✅ Vérification du déploiement..."
    kubectl rollout status deployment/$PROJECT_NAME
else
    echo "ℹ️ kubectl non disponible - skip du déploiement K8s"
fi

echo "🎉 Déploiement terminé !"
echo "🐳 Image Docker: $DOCKER_IMAGE"
if [ -n "$DOCKER_USERNAME" ]; then
    echo "📤 Registry: $DOCKER_USERNAME/$DOCKER_IMAGE"
fi
echo "🌐 Service disponible sur: http://localhost:5000"
