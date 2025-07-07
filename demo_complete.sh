#!/bin/bash

# Script de démonstration complète Arkalia Quest
# Lance le serveur, teste tout, et propose l'enregistrement vidéo

echo "🎬 DÉMONSTRATION COMPLÈTE ARKALIA QUEST"
echo "======================================="
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

# Activer l'environnement virtuel
show_step "Activation de l'environnement virtuel..."
source .venv-quest/bin/activate 2>/dev/null || {
    show_warning "Environnement virtuel non trouvé, utilisation de Python système"
}

# Vérifier les dépendances
show_step "Vérification des dépendances..."
if ! python3 -c "import flask, requests" 2>/dev/null; then
    show_warning "Dépendances manquantes. Installation..."
    pip install -r requirements.txt
fi
show_success "Dépendances installées"

# Créer le dossier de sortie
mkdir -p demo_videos

# Arrêter le serveur s'il tourne déjà
show_step "Arrêt du serveur existant..."
pkill -f "python.*app.py" 2>/dev/null
sleep 2

# Lancer le serveur en arrière-plan
show_step "Démarrage du serveur Arkalia Quest..."
python3 app.py > server.log 2>&1 &
SERVER_PID=$!

# Attendre que le serveur démarre
sleep 5

# Vérifier que le serveur fonctionne
show_step "Vérification du serveur..."
if curl -s http://localhost:5001 > /dev/null; then
    show_success "Serveur démarré sur http://localhost:5001"
else
    show_error "Le serveur n'a pas démarré correctement"
    echo "Logs du serveur:"
    cat server.log
    kill $SERVER_PID 2>/dev/null
    exit 1
fi

# Ouvrir le navigateur
show_step "Ouverture du navigateur..."
open http://localhost:5001
sleep 3

# Lancer la démonstration automatique
show_step "Lancement de la démonstration automatique..."
python3 demo_video_amelioree.py
DEMO_RESULT=$?

echo ""
echo -e "${PURPLE}🎬 RÉSULTATS DE LA DÉMONSTRATION${NC}"
echo "======================================"

if [ $DEMO_RESULT -eq 0 ]; then
    show_success "Démonstration parfaite ! Tous les tests réussis"
    echo ""
    echo -e "${CYAN}Que souhaitez-vous faire maintenant ?${NC}"
    echo "1) Enregistrer une vidéo de démonstration"
    echo "2) Continuer à tester manuellement"
    echo "3) Arrêter le serveur et quitter"
    echo ""
    
    read -p "Votre choix (1-3): " choice
    
    case $choice in
        1)
            show_info "Lancement de l'enregistrement vidéo..."
            echo ""
            echo "💡 Instructions pour l'enregistrement:"
            echo "• Le navigateur est déjà ouvert sur Arkalia Quest"
            echo "• Naviguez dans l'interface pendant l'enregistrement"
            echo "• Testez quelques commandes dans le terminal"
            echo "• Appuyez sur Ctrl+C pour arrêter l'enregistrement"
            echo ""
            read -p "Appuyez sur Entrée pour commencer l'enregistrement..."
            ./record_video_final.sh
            ;;
        2)
            show_info "Serveur en cours d'exécution sur http://localhost:5001"
            show_info "Appuyez sur Ctrl+C pour arrêter le serveur"
            wait $SERVER_PID
            ;;
        3)
            show_info "Arrêt du serveur..."
            kill $SERVER_PID 2>/dev/null
            show_success "Au revoir !"
            exit 0
            ;;
        *)
            show_error "Choix invalide"
            ;;
    esac
else
    show_error "La démonstration a échoué"
    echo "Logs du serveur:"
    cat server.log
    kill $SERVER_PID 2>/dev/null
    exit 1
fi

# Nettoyage
echo ""
show_step "Nettoyage..."
kill $SERVER_PID 2>/dev/null
show_success "Serveur arrêté"
show_success "Démonstration terminée !" 