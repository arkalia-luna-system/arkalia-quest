#!/bin/bash

# Script d'enregistrement vidéo pour Arkalia Quest
# Enregistre l'écran pendant la démonstration

echo "🎬 PRÉPARATION DE L'ENREGISTREMENT VIDÉO ARKALIA QUEST"
echo "=================================================="

# Vérifier que ffmpeg est installé
if ! command -v ffmpeg &> /dev/null; then
    echo "❌ ffmpeg n'est pas installé. Installez-le avec: brew install ffmpeg"
    exit 1
fi

# Créer le dossier de sortie
mkdir -p demo_videos

# Nom du fichier de sortie avec timestamp
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
OUTPUT_FILE="demo_videos/arkalia_quest_demo_${TIMESTAMP}.mp4"

echo "📹 Démarrage de l'enregistrement..."
echo "🎯 Fichier de sortie: $OUTPUT_FILE"
echo "⏱️  Durée estimée: 2-3 minutes"
echo ""
echo "💡 Instructions:"
echo "1. Ouvrez http://localhost:5001 dans votre navigateur"
echo "2. Naviguez dans l'interface pendant l'enregistrement"
echo "3. Testez les commandes dans le terminal"
echo "4. Appuyez sur Ctrl+C pour arrêter l'enregistrement"
echo ""

# Démarrer l'enregistrement avec ffmpeg
# -f avfoundation: capture d'écran macOS
# -i "1": écran principal (0 = webcam, 1 = écran)
# -r 30: 30 FPS
# -crf 18: qualité élevée
# -preset fast: encodage rapide
# -pix_fmt yuv420p: compatibilité maximale

echo "🎥 Démarrage de l'enregistrement dans 3 secondes..."
sleep 3

ffmpeg -f avfoundation \
       -i "1" \
       -r 30 \
       -crf 18 \
       -preset fast \
       -pix_fmt yuv420p \
       -movflags +faststart \
       "$OUTPUT_FILE"

echo ""
echo "✅ Enregistrement terminé!"
echo "📁 Fichier sauvegardé: $OUTPUT_FILE"
echo "🎬 Vous pouvez maintenant visionner votre démonstration!" 