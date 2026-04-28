#!/usr/bin/env bash

# 🔐 Script d'authentification Docker sécurisé
# Usage: ./scripts/docker-auth.sh [registry]

set -euo pipefail

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

# Fonction pour valider les credentials
validate_credentials() {
    local username="$1"
    local password="$2"
    
    # Vérifier que username n'est pas vide
    if [ -z "$username" ] || [ "$username" = "null" ] || [ "$username" = "undefined" ]; then
        echo "❌ Username Docker invalide ou manquant"
        return 1
    fi
    
    # Vérifier que password n'est pas vide
    if [ -z "$password" ] || [ "$password" = "null" ] || [ "$password" = "undefined" ]; then
        echo "❌ Password Docker invalide ou manquant"
        return 1
    fi
    
    # Vérifier la longueur minimale
    if [ ${#username} -lt 3 ]; then
        echo "❌ Username Docker trop court (minimum 3 caractères)"
        return 1
    fi
    
    if [ ${#password} -lt 6 ]; then
        echo "❌ Password Docker trop court (minimum 6 caractères)"
        return 1
    fi
    
    return 0
}

# Fonction pour lire les credentials de manière sécurisée
read_credentials() {
    local username_var="DOCKER_USERNAME"
    local password_var="DOCKER_PASSWORD"
    
    # Essayer de lire depuis les variables d'environnement
    if [ -n "${!username_var:-}" ] && [ -n "${!password_var:-}" ]; then
        echo "✅ Credentials trouvés dans les variables d'environnement"
        DOCKER_USERNAME="${!username_var}"
        DOCKER_PASSWORD="${!password_var}"
        
        # Valider les credentials
        if validate_credentials "$DOCKER_USERNAME" "$DOCKER_PASSWORD"; then
            return 0
        else
            echo "❌ Credentials des variables d'environnement invalides"
            return 1
        fi
    fi
    
    # Essayer de lire depuis un fichier .env
    if [ -f "$SCRIPT_DIR/../.env" ]; then
        echo "📁 Lecture des credentials depuis .env"
        # shellcheck disable=SC1090
        source "$SCRIPT_DIR/../.env"
        if [ -n "$DOCKER_USERNAME" ] && [ -n "$DOCKER_PASSWORD" ]; then
            echo "✅ Credentials trouvés dans .env"
            if validate_credentials "$DOCKER_USERNAME" "$DOCKER_PASSWORD"; then
                return 0
            else
                echo "❌ Credentials du fichier .env invalides"
                return 1
            fi
        fi
    fi
    
    # Demander interactivement (seulement si TTY disponible)
    if [ -t 0 ]; then
        echo "📝 Saisie interactive des credentials:"
        while true; do
            read -p "Username Docker: " DOCKER_USERNAME
            read -s -p "Password Docker: " DOCKER_PASSWORD
            echo
            
            if validate_credentials "$DOCKER_USERNAME" "$DOCKER_PASSWORD"; then
                echo "✅ Credentials saisis et validés"
                return 0
            else
                echo "❌ Credentials invalides, veuillez réessayer"
            fi
        done
    fi
    
    return 1
}

# Lire les credentials
if ! read_credentials; then
    echo "❌ Impossible de récupérer des credentials Docker valides"
    echo "📋 Solutions:"
    echo "   1. Définir DOCKER_USERNAME et DOCKER_PASSWORD dans l'environnement"
    echo "   2. Créer un fichier .env avec ces variables"
    echo "   3. Exécuter ce script dans un terminal interactif"
    echo ""
    echo "🔍 Vérification des variables d'environnement:"
    echo "   DOCKER_USERNAME: ${DOCKER_USERNAME:-'non défini'}"
    echo "   DOCKER_PASSWORD: ${DOCKER_PASSWORD:+'***défini***'}"
    exit 1
fi

# Affichage des informations de connexion
echo "🔐 Tentative de connexion Docker..."
echo "👤 Utilisateur: $DOCKER_USERNAME"
echo "🏷️ Registry: $REGISTRY"
echo "🔒 Password: ${DOCKER_PASSWORD:0:3}***"

# Authentification Docker avec gestion d'erreur robuste
echo "🔐 Authentification Docker..."
if echo "$DOCKER_PASSWORD" | docker login -u "$DOCKER_USERNAME" --password-stdin "$REGISTRY" 2>/tmp/docker_login_error; then
    echo "✅ Authentification Docker réussie pour $REGISTRY"
    echo "👤 Utilisateur: $DOCKER_USERNAME"
    echo "🏷️ Registry: $REGISTRY"
else
    echo "❌ Échec de l'authentification Docker"
    echo "🔍 Détails de l'erreur:"
    cat /tmp/docker_login_error
    rm -f /tmp/docker_login_error
    
    # Suggestions de résolution
    echo ""
    echo "🚨 Solutions possibles:"
    echo "   1. Vérifier que les credentials sont corrects"
    echo "   2. Vérifier la connectivité réseau"
    echo "   3. Vérifier que le registry est accessible"
    echo "   4. Essayer avec un autre registry (ex: ghcr.io)"
    exit 1
fi

# Nettoyage
rm -f /tmp/docker_login_error

echo ""
echo "🎉 Authentification terminée avec succès !"
echo "📋 Vous pouvez maintenant pousser des images vers $REGISTRY"
