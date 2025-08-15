#!/bin/bash
# Script de déploiement pour arkalia-quest
# Généré automatiquement par Athalia

set -e

echo "🚀 Déploiement de arkalia-quest..."

# Variables
PROJECT_NAME="arkalia-quest"
DOCKER_IMAGE="$PROJECT_NAME:latest"
K8S_NAMESPACE="default"

# Build de l'image Docker
echo "📦 Build de l'image Docker..."
docker build -t $DOCKER_IMAGE .

# Push vers le registry (optionnel)
# docker push $DOCKER_IMAGE

# Déploiement Kubernetes
echo "☸️ Déploiement Kubernetes..."
kubectl apply -f k8s-deployment.yaml
kubectl apply -f k8s-service.yaml

# Vérification du déploiement
echo "✅ Vérification du déploiement..."
kubectl rollout status deployment/$PROJECT_NAME

echo "🎉 Déploiement terminé !"
echo "🌐 Service disponible sur: http://localhost:8000"
