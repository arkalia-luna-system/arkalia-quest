#!/bin/bash
# Script de lancement pour l'évaluation d'Arkalia Quest

echo "🎮 ARKALIA QUEST - LANCEMENT POUR ÉVALUATION"
echo "=============================================="

# Vérifier que le venv est activé
if [[ "$VIRTUAL_ENV" == "" ]]; then
    echo "⚠️  Activation de l'environnement virtuel..."
    source venv/bin/activate
fi

# Vérifier que l'application n'est pas déjà en cours
if pgrep -f "flask run" > /dev/null; then
    echo "✅ L'application est déjà en cours d'exécution"
else
    echo "🚀 Lancement de l'application..."
    python -m flask run --host=0.0.0.0 --port=5001 &
    sleep 3
fi

# Vérifier que l'application répond
echo "🔍 Vérification de l'application..."
if curl -s http://localhost:5001/ > /dev/null; then
    echo "✅ Application accessible sur http://localhost:5001/"
else
    echo "❌ L'application ne répond pas. Vérifiez les logs."
    exit 1
fi

echo ""
echo "📋 GUIDES D'ÉVALUATION DISPONIBLES :"
echo "   📖 PLAN_EVALUATION_JOUEURS.md - Guide complet"
echo "   📝 RAPPORT_EVALUATION_SIMPLE.md - Rapport simple"
echo "   🎮 GUIDE_TESTEUR_RAPIDE.md - Guide rapide"
echo ""
echo "🔧 OUTILS DE COLLECTE :"
echo "   python collect_evaluations.py - Collecteur d'évaluations"
echo ""
echo "🌐 ACCÈS AU JEU :"
echo "   http://localhost:5001/"
echo "   http://127.0.0.1:5001/"
echo "   http://192.168.129.35:5001/"
echo ""
echo "🎯 PRÊT POUR L'ÉVALUATION !"
echo "=============================="
