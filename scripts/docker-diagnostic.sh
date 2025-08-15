#!/bin/bash

# 🔍 Script de diagnostic Docker pour Arkalia Quest
# Usage: ./scripts/docker-diagnostic.sh

set -e

echo "🔍 Diagnostic Docker - Arkalia Quest"
echo "===================================="

# Couleurs
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

print_status() {
    local status=$1
    local message=$2
    
    if [ $status -eq 0 ]; then
        echo -e "${GREEN}✅ $message${NC}"
    else
        echo -e "${RED}❌ $message${NC}"
    fi
}

print_warning() {
    echo -e "${YELLOW}⚠️ $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ️ $1${NC}"
}

# Test 1: Vérification de l'environnement
echo ""
echo "🔍 Test 1: Environnement"
echo "------------------------"

# Variables d'environnement
if [ -n "$DOCKER_USERNAME" ]; then
    print_status 0 "DOCKER_USERNAME défini: $DOCKER_USERNAME"
else
    print_status 1 "DOCKER_USERNAME non défini"
fi

if [ -n "$DOCKER_PASSWORD" ]; then
    print_status 0 "DOCKER_PASSWORD défini (longueur: ${#DOCKER_PASSWORD})"
else
    print_status 1 "DOCKER_PASSWORD non défini"
fi

# Test 2: Vérification Docker
echo ""
echo "🔍 Test 2: Docker"
echo "-----------------"

if command -v docker &> /dev/null; then
    DOCKER_VERSION=$(docker --version)
    print_status 0 "Docker installé: $DOCKER_VERSION"
else
    print_status 1 "Docker non installé"
    exit 1
fi

if docker info &> /dev/null; then
    print_status 0 "Docker daemon accessible"
else
    print_status 1 "Docker daemon non accessible"
    echo "💡 Solution: sudo systemctl start docker"
    exit 1
fi

# Test 3: Test d'authentification
echo ""
echo "🔍 Test 3: Authentification Docker"
echo "----------------------------------"

if [ -n "$DOCKER_USERNAME" ] && [ -n "$DOCKER_PASSWORD" ]; then
    echo "🧪 Test d'authentification avec credentials disponibles..."
    
    # Test avec registry explicite
    echo "🔐 Test 1: docker.io (Docker Hub)"
    if echo "$DOCKER_PASSWORD" | docker login -u "$DOCKER_USERNAME" --password-stdin "docker.io" 2>/tmp/docker_test1.log; then
        print_status 0 "Authentification Docker Hub réussie"
        docker logout &> /dev/null
    else
        print_status 1 "Échec authentification Docker Hub"
        echo "🔍 Erreur:"
        cat /tmp/docker_test1.log
    fi
    
    # Test avec registry GitHub Container Registry
    echo "🔐 Test 2: ghcr.io (GitHub Container Registry)"
    if echo "$DOCKER_PASSWORD" | docker login -u "$DOCKER_USERNAME" --password-stdin "ghcr.io" 2>/tmp/docker_test2.log; then
        print_status 0 "Authentification GitHub Container Registry réussie"
        docker logout &> /dev/null
    else
        print_status 1 "Échec authentification GitHub Container Registry"
        echo "🔍 Erreur:"
        cat /tmp/docker_test2.log
    fi
    
    # Test sans registry (peut causer des problèmes)
    echo "🔐 Test 3: Sans registry spécifié (peut causer des erreurs TTY)"
    if echo "$DOCKER_PASSWORD" | docker login -u "$DOCKER_USERNAME" --password-stdin 2>/tmp/docker_test3.log; then
        print_status 0 "Authentification sans registry réussie"
        docker logout &> /dev/null
    else
        print_status 1 "Échec authentification sans registry (attendu)"
        echo "🔍 Erreur (normale sans registry):"
        cat /tmp/docker_test3.log
    fi
    
else
    print_warning "Pas de credentials disponibles pour le test d'authentification"
fi

# Test 4: Vérification des scripts
echo ""
echo "🔍 Test 4: Scripts"
echo "------------------"

# Vérifier que les scripts sont exécutables
if [ -x "scripts/docker-auth.sh" ]; then
    print_status 0 "scripts/docker-auth.sh exécutable"
else
    print_status 1 "scripts/docker-auth.sh non exécutable"
    chmod +x scripts/docker-auth.sh
    print_status 0 "Permissions corrigées pour scripts/docker-auth.sh"
fi

if [ -x "scripts/test-docker.sh" ]; then
    print_status 0 "scripts/test-docker.sh exécutable"
else
    print_status 1 "scripts/test-docker.sh non exécutable"
    chmod +x scripts/test-docker.sh
    print_status 0 "Permissions corrigées pour scripts/test-docker.sh"
fi

# Test 5: Validation de la syntaxe
echo ""
echo "🔍 Test 5: Validation syntaxe"
echo "-----------------------------"

if bash -n scripts/docker-auth.sh; then
    print_status 0 "scripts/docker-auth.sh syntaxe OK"
else
    print_status 1 "scripts/docker-auth.sh erreur de syntaxe"
fi

if bash -n scripts/test-docker.sh; then
    print_status 0 "scripts/test-docker.sh syntaxe OK"
else
    print_status 1 "scripts/test-docker.sh erreur de syntaxe"
fi

# Nettoyage
rm -f /tmp/docker_test*.log

# Résumé et recommandations
echo ""
echo "📊 Résumé du diagnostic"
echo "======================="

echo ""
echo "💡 Recommandations:"
echo "   1. Toujours spécifier un registry: docker.io, ghcr.io, etc."
echo "   2. Utiliser des variables d'environnement pour les credentials"
echo "   3. Tester l'authentification avant le déploiement"
echo "   4. Utiliser le script docker-auth.sh pour l'authentification"

echo ""
echo "🚀 Commandes recommandées:"
echo "   # Authentification Docker Hub"
echo "   echo \"\$DOCKER_PASSWORD\" | docker login -u \"\$DOCKER_USERNAME\" --password-stdin docker.io"
echo ""
echo "   # Authentification GitHub Container Registry"
echo "   echo \"\$DOCKER_PASSWORD\" | docker login -u \"\$DOCKER_USERNAME\" --password-stdin ghcr.io"
echo ""
echo "   # Utiliser le script d'authentification"
echo "   ./scripts/docker-auth.sh docker.io"

echo ""
echo "🎉 Diagnostic terminé !"
