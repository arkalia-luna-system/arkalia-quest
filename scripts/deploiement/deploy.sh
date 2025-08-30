#!/bin/bash
# Script de déploiement pour arkalia-quest
# Généré automatiquement par Athalia

set -e

PROJECT_NAME="arkalia-quest"
DOCKER_IMAGE="$PROJECT_NAME:latest"
K8S_NAMESPACE="default"

echo "🚀 Déploiement de arkalia-quest..."

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

# Fonction pour valider les credentials Docker
validate_docker_credentials() {
    local username="$1"
    local password="$2"
    
    if [ -z "$username" ] || [ "$username" = "null" ] || [ "$username" = "undefined" ]; then
        echo "❌ DOCKER_USERNAME invalide ou manquant"
        return 1
    fi
    
    if [ -z "$password" ] || [ "$password" = "null" ] || [ "$password" = "undefined" ]; then
        echo "❌ DOCKER_PASSWORD invalide ou manquant"
        return 1
    fi
    
    return 0
}

# Build de l'image Docker
echo "📦 Build de l'image Docker..."
docker build -t $DOCKER_IMAGE -f config/Dockerfile .

# Vérifier si on a des credentials Docker (pour le push)
if [ -n "$DOCKER_USERNAME" ] && [ -n "$DOCKER_PASSWORD" ]; then
    echo "🔐 Vérification des credentials Docker..."
    
    # Valider les credentials
    if ! validate_docker_credentials "$DOCKER_USERNAME" "$DOCKER_PASSWORD"; then
        echo "❌ Credentials Docker invalides, skip du push"
        echo "📋 Définissez DOCKER_USERNAME et DOCKER_PASSWORD correctement"
    else
        echo "✅ Credentials Docker validés"
        
        # Authentification Docker
        echo "🔐 Authentification Docker..."
        if echo "$DOCKER_PASSWORD" | docker login -u "$DOCKER_USERNAME" --password-stdin "docker.io" 2>/tmp/docker_login_error; then
            echo "✅ Authentification Docker réussie"
            
            # Tag et push vers le registry
            echo "📤 Push vers le registry Docker..."
            docker tag $DOCKER_IMAGE "$DOCKER_USERNAME/$DOCKER_IMAGE"
            if docker push "$DOCKER_USERNAME/$DOCKER_IMAGE"; then
                echo "✅ Image poussée avec succès: $DOCKER_USERNAME/$DOCKER_IMAGE"
            else
                echo "❌ Échec du push de l'image"
                exit 1
            fi
        else
            echo "❌ Échec de l'authentification Docker"
            echo "🔍 Détails de l'erreur:"
            cat /tmp/docker_login_error
            rm -f /tmp/docker_login_error
            echo "❌ Skip du push en raison de l'échec d'authentification"
        fi
    fi
else
    echo "ℹ️ Pas de credentials Docker - skip du push"
    echo "📋 Pour activer le push, définissez DOCKER_USERNAME et DOCKER_PASSWORD"
fi

# Nettoyage des fichiers temporaires
rm -f /tmp/docker_login_error

# Déploiement Kubernetes (si kubectl est disponible)
if command -v kubectl &> /dev/null; then
    echo "☸️ Déploiement Kubernetes..."
    
    # Vérifier que les fichiers K8s existent
    if [ -f "k8s/k8s-deployment.yaml" ] && [ -f "k8s/k8s-service.yaml" ]; then
        kubectl apply -f k8s/k8s-deployment.yaml
        kubectl apply -f k8s/k8s-service.yaml
        
        # Vérification du déploiement
        echo "✅ Vérification du déploiement..."
        kubectl rollout status deployment/$PROJECT_NAME
    else
        echo "⚠️ Fichiers Kubernetes manquants, skip du déploiement K8s"
        echo "📋 Créez k8s/k8s-deployment.yaml et k8s/k8s-service.yaml"
    fi
else
    echo "ℹ️ kubectl non disponible - skip du déploiement K8s"
fi

echo "🎉 Déploiement terminé !"
echo "🐳 Image Docker: $DOCKER_IMAGE"
if [ -n "$DOCKER_USERNAME" ] && [ -n "$DOCKER_PASSWORD" ]; then
    echo "📤 Registry: $DOCKER_USERNAME/$DOCKER_IMAGE"
fi
echo "🌐 Service disponible sur: http://localhost:5001"
