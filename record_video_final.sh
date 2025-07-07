#!/bin/bash

# Script d'enregistrement vidéo final pour Arkalia Quest
# Utilise les paramètres corrects pour macOS

echo "🎬 ENREGISTREMENT VIDÉO FINAL ARKALIA QUEST"
echo "==========================================="

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

echo "🎥 Démarrage de l'enregistrement dans 5 secondes..."
echo "   Assurez-vous que le navigateur est ouvert sur Arkalia Quest"
sleep 5

# Enregistrement avec les paramètres corrects pour macOS
echo "🎬 Enregistrement en cours... (Ctrl+C pour arrêter)"

ffmpeg -f avfoundation \
       -i "0:none" \
       -r 30 \
       -crf 18 \
       -preset fast \
       -pix_fmt yuv420p \
       -movflags +faststart \
       -y \
       "$OUTPUT_FILE"

# Vérifier si l'enregistrement a réussi
if [ -f "$OUTPUT_FILE" ] && [ -s "$OUTPUT_FILE" ]; then
    echo ""
    echo "✅ Enregistrement terminé avec succès!"
    echo "📁 Fichier sauvegardé: $OUTPUT_FILE"
    
    # Afficher les informations du fichier
    file_size=$(du -h "$OUTPUT_FILE" | cut -f1)
    echo "📊 Taille du fichier: $file_size"
    
    echo ""
    echo "🎬 Vous pouvez maintenant visionner votre démonstration!"
    echo "💡 Ouvrez le fichier avec: open $OUTPUT_FILE"
else
    echo ""
    echo "❌ L'enregistrement a échoué"
    echo "💡 Essayez de redémarrer le script ou vérifiez les permissions"
fi

echo ""
echo "🎉 Merci d'avoir testé Arkalia Quest !" 