#!/bin/bash

# 🧪 Script de test Docker pour Arkalia Quest
# Usage: ./scripts/test-docker.sh

set -e

echo "🧪 Test de la configuration Docker"
echo "================================="

# Couleurs pour les messages
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Fonction pour afficher les résultats
print_result() {
    local status=$1
    local message=$2
    
    if [ $status -eq 0 ]; then
        echo -e "${GREEN}✅ $message${NC}"
    else
        echo -e "${RED}❌ $message${NC}"
    fi
}

print_warning() {
    local message=$1
    echo -e "${YELLOW}⚠️ $message${NC}"
}

print_info() {
    local message=$1
    echo -e "${BLUE}ℹ️ $message${NC}"
}

# Tests de base
echo ""
echo "🔍 Tests de base..."

# Test 1: Docker installé
if command -v docker &> /dev/null; then
    DOCKER_VERSION=$(docker --version)
    print_result 0 "Docker installé: $DOCKER_VERSION"
else
    print_result 1 "Docker non installé"
    exit 1
fi

# Test 2: Docker daemon en cours d'exécution
if docker info &> /dev/null; then
    print_result 0 "Docker daemon en cours d'exécution"
else
    print_result 1 "Docker daemon non accessible"
    echo "💡 Solution: sudo systemctl start docker"
    exit 1
fi

# Test 3: Permissions Docker
if docker ps &> /dev/null; then
    print_result 0 "Permissions Docker OK"
else
    print_result 1 "Permissions Docker insuffisantes"
    echo "💡 Solution: sudo usermod -aG docker $USER"
    exit 1
fi

# Tests de configuration
echo ""
echo "🔧 Tests de configuration..."

# Test 4: Variables d'environnement Docker
if [ -n "$DOCKER_USERNAME" ]; then
    print_result 0 "DOCKER_USERNAME défini: $DOCKER_USERNAME"
else
    print_warning "DOCKER_USERNAME non défini"
fi

if [ -n "$DOCKER_PASSWORD" ]; then
    print_result 0 "DOCKER_PASSWORD défini (longueur: ${#DOCKER_PASSWORD})"
else
    print_warning "DOCKER_PASSWORD non défini"
fi

# Test 5: Fichier .env
if [ -f ".env" ]; then
    print_result 0 "Fichier .env trouvé"
    if grep -q "DOCKER_USERNAME" .env; then
        print_result 0 "DOCKER_USERNAME dans .env"
    else
        print_warning "DOCKER_USERNAME manquant dans .env"
    fi
    if grep -q "DOCKER_PASSWORD" .env; then
        print_result 0 "DOCKER_PASSWORD dans .env"
    else
        print_warning "DOCKER_PASSWORD manquant dans .env"
    fi
else
    print_warning "Fichier .env non trouvé"
fi

# Tests de fonctionnalité
echo ""
echo "🚀 Tests de fonctionnalité..."

# Test 6: Construction d'image
echo "🔨 Test de construction d'image..."
if docker build -t arkalia-quest:test . &> /tmp/docker_build.log; then
    print_result 0 "Construction d'image réussie"
    # Nettoyer l'image de test
    docker rmi arkalia-quest:test &> /dev/null
else
    print_result 1 "Échec de la construction d'image"
    echo "🔍 Détails de l'erreur:"
    cat /tmp/docker_build.log
fi

# Test 7: Authentification Docker (si credentials disponibles)
if [ -n "$DOCKER_USERNAME" ] && [ -n "$DOCKER_PASSWORD" ]; then
    echo "🔐 Test d'authentification Docker..."
    if echo "$DOCKER_PASSWORD" | docker login -u "$DOCKER_USERNAME" --password-stdin &> /tmp/docker_login.log; then
        print_result 0 "Authentification Docker réussie"
        # Se déconnecter
        docker logout &> /dev/null
    else
        print_result 1 "Échec de l'authentification Docker"
        echo "🔍 Détails de l'erreur:"
        cat /tmp/docker_login.log
    fi
else
    print_warning "Test d'authentification Docker ignoré (credentials manquants)"
fi

# Tests de scripts
echo ""
echo "📜 Tests des scripts..."

# Test 8: Scripts exécutables
if [ -x "scripts/docker-auth.sh" ]; then
    print_result 0 "scripts/docker-auth.sh exécutable"
else
    print_result 1 "scripts/docker-auth.sh non exécutable"
fi

if [ -x "scripts/deploy.sh" ]; then
    print_result 0 "scripts/deploy.sh exécutable"
else
    print_result 1 "scripts/deploy.sh non exécutable"
fi

# Test 9: Validation des scripts
echo "🔍 Validation de la syntaxe des scripts..."
if bash -n scripts/docker-auth.sh; then
    print_result 0 "scripts/docker-auth.sh syntaxe OK"
else
    print_result 1 "scripts/docker-auth.sh erreur de syntaxe"
fi

if bash -n scripts/deploy.sh; then
    print_result 0 "scripts/deploy.sh syntaxe OK"
else
    print_result 1 "scripts/deploy.sh erreur de syntaxe"
fi

# Nettoyage
rm -f /tmp/docker_build.log /tmp/docker_login.log

# Résumé
echo ""
echo "📊 Résumé des tests"
echo "=================="

echo "🎯 Tests de base: Docker installé et fonctionnel"
echo "🔧 Configuration: Variables d'environnement et fichiers .env"
echo "🚀 Fonctionnalité: Construction d'image et authentification"
echo "📜 Scripts: Exécutables et syntaxe valide"

echo ""
echo "💡 Prochaines étapes:"
if [ -n "$DOCKER_USERNAME" ] && [ -n "$DOCKER_PASSWORD" ]; then
    echo "   ✅ Credentials Docker configurés"
    echo "   🚀 Prêt pour le déploiement: ./scripts/deploy.sh docker"
else
    echo "   🔐 Configurer les credentials Docker:"
    echo "      export DOCKER_USERNAME='votre_username'"
    echo "      export DOCKER_PASSWORD='votre_password'"
    echo "   📁 Ou créer un fichier .env"
fi

echo "   🧪 Tester l'authentification: ./scripts/docker-auth.sh"
echo "   📚 Consulter la documentation: docs/DOCKER_AUTH.md"

echo ""
echo "�� Tests terminés !"
