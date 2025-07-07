#!/bin/bash

# Script de lancement complet pour la démonstration vidéo Arkalia Quest
# Lance le serveur, ouvre le navigateur, et prépare l'enregistrement

echo "🎬 DÉMONSTRATION VIDÉO ARKALIA QUEST"
echo "===================================="
echo ""

# Couleurs pour l'affichage
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Fonction pour afficher les étapes
show_step() {
    echo -e "${BLUE}📋 $1${NC}"
}

show_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

show_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

show_error() {
    echo -e "${RED}❌ $1${NC}"
}

show_info() {
    echo -e "${CYAN}ℹ️  $1${NC}"
}

# Vérifier que Python est installé
show_step "Vérification de Python..."
if ! command -v python3 &> /dev/null; then
    show_error "Python3 n'est pas installé"
    exit 1
fi
show_success "Python3 disponible"

# Vérifier que ffmpeg est installé
show_step "Vérification de ffmpeg..."
if ! command -v ffmpeg &> /dev/null; then
    show_warning "ffmpeg n'est pas installé. Installation..."
    brew install ffmpeg
    if [ $? -ne 0 ]; then
        show_error "Impossible d'installer ffmpeg"
        exit 1
    fi
fi
show_success "ffmpeg disponible"

# Vérifier que l'environnement virtuel existe
show_step "Vérification de l'environnement virtuel..."
if [ ! -d ".venv-quest" ]; then
    show_warning "Environnement virtuel non trouvé. Création..."
    python3 -m venv .venv-quest
    source .venv-quest/bin/activate
    pip install -r requirements.txt
else
    show_success "Environnement virtuel trouvé"
fi

# Activer l'environnement virtuel
source .venv-quest/bin/activate

# Vérifier les dépendances
show_step "Vérification des dépendances..."
if ! python3 -c "import flask, requests" 2>/dev/null; then
    show_warning "Dépendances manquantes. Installation..."
    pip install -r requirements.txt
fi
show_success "Dépendances installées"

# Créer le dossier de sortie
mkdir -p demo_videos

# Lancer le serveur en arrière-plan
show_step "Démarrage du serveur Arkalia Quest..."
python3 app.py &
SERVER_PID=$!

# Attendre que le serveur démarre
sleep 3

# Vérifier que le serveur fonctionne
show_step "Vérification du serveur..."
if curl -s http://localhost:5001 > /dev/null; then
    show_success "Serveur démarré sur http://localhost:5001"
else
    show_error "Le serveur n'a pas démarré correctement"
    kill $SERVER_PID 2>/dev/null
    exit 1
fi

# Ouvrir le navigateur
show_step "Ouverture du navigateur..."
open http://localhost:5001
sleep 2

# Afficher les instructions
echo ""
echo -e "${PURPLE}🎬 INSTRUCTIONS POUR L'ENREGISTREMENT:${NC}"
echo "=============================================="
echo ""
echo -e "${CYAN}1.${NC} Le navigateur s'est ouvert sur Arkalia Quest"
echo -e "${CYAN}2.${NC} Naviguez dans l'interface pour montrer les fonctionnalités:"
echo "   • Page d'accueil avec le design sombre"
echo "   • Terminal avec les commandes"
echo "   • Pages monde et profil"
echo "   • Effets visuels et animations"
echo "   • Responsive design (redimensionnez la fenêtre)"
echo ""
echo -e "${CYAN}3.${NC} Testez quelques commandes dans le terminal:"
echo "   • aide"
echo "   • luna_contact"
echo "   • badges"
echo "   • profil"
echo "   • hack_system"
echo ""
echo -e "${CYAN}4.${NC} Quand vous êtes prêt, lancez l'enregistrement:"
echo ""

# Menu pour choisir le type d'enregistrement
echo -e "${YELLOW}Choisissez le type d'enregistrement:${NC}"
echo "1) Enregistrement manuel (vous naviguez)"
echo "2) Démonstration automatique (script)"
echo "3) Démonstration guidée (Selenium)"
echo "4) Quitter"
echo ""

read -p "Votre choix (1-4): " choice

case $choice in
    1)
        show_info "Lancement de l'enregistrement manuel..."
        ./record_demo.sh
        ;;
    2)
        show_info "Lancement de la démonstration automatique..."
        python3 demo_script.py &
        sleep 2
        ./record_demo.sh
        ;;
    3)
        show_info "Lancement de la démonstration guidée..."
        python3 demo_guided.py &
        sleep 5
        ./record_demo.sh
        ;;
    4)
        show_info "Arrêt du serveur..."
        kill $SERVER_PID 2>/dev/null
        show_success "Au revoir !"
        exit 0
        ;;
    *)
        show_error "Choix invalide"
        ;;
esac

# Nettoyage
echo ""
show_step "Nettoyage..."
kill $SERVER_PID 2>/dev/null
show_success "Serveur arrêté"
show_success "Démonstration terminée !" 