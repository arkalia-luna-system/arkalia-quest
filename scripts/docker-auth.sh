#!/bin/bash

# 🔐 Script d'authentification Docker sécurisé
# Usage: ./scripts/docker-auth.sh [registry]

set -e

REGISTRY=${1:-"docker.io"}
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "🔐 Authentification Docker pour $REGISTRY"
echo "========================================"

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

# Fonction pour lire les credentials de manière sécurisée
read_credentials() {
    local username_var="DOCKER_USERNAME"
    local password_var="DOCKER_PASSWORD"
    
    # Essayer de lire depuis les variables d'environnement
    if [ -n "${!username_var}" ] && [ -n "${!password_var}" ]; then
        echo "✅ Credentials trouvés dans les variables d'environnement"
        DOCKER_USERNAME="${!username_var}"
        DOCKER_PASSWORD="${!password_var}"
        return 0
    fi
    
    # Essayer de lire depuis un fichier .env
    if [ -f "$SCRIPT_DIR/../.env" ]; then
        echo "📁 Lecture des credentials depuis .env"
        source "$SCRIPT_DIR/../.env"
        if [ -n "$DOCKER_USERNAME" ] && [ -n "$DOCKER_PASSWORD" ]; then
            echo "✅ Credentials trouvés dans .env"
            return 0
        fi
    fi
    
    # Demander interactivement (seulement si TTY disponible)
    if [ -t 0 ]; then
        echo "📝 Saisie interactive des credentials:"
        read -p "Username Docker: " DOCKER_USERNAME
        read -s -p "Password Docker: " DOCKER_PASSWORD
        echo
        if [ -n "$DOCKER_USERNAME" ] && [ -n "$DOCKER_PASSWORD" ]; then
            echo "✅ Credentials saisis"
            return 0
        fi
    fi
    
    return 1
}

# Lire les credentials
if ! read_credentials; then
    echo "❌ Impossible de récupérer les credentials Docker"
    echo "📋 Solutions:"
    echo "   1. Définir DOCKER_USERNAME et DOCKER_PASSWORD dans l'environnement"
    echo "   2. Créer un fichier .env avec ces variables"
    echo "   3. Exécuter ce script dans un terminal interactif"
    exit 1
fi

# Authentification Docker
echo "🔐 Authentification Docker..."
if echo "$DOCKER_PASSWORD" | docker login -u "$DOCKER_USERNAME" --password-stdin "$REGISTRY"; then
    echo "✅ Authentification Docker réussie pour $REGISTRY"
    echo "👤 Utilisateur: $DOCKER_USERNAME"
    echo "🏷️ Registry: $REGISTRY"
else
    echo "❌ Échec de l'authentification Docker"
    exit 1
fi

echo ""
echo "🎉 Authentification terminée avec succès !"
echo "📋 Vous pouvez maintenant pousser des images vers $REGISTRY"
