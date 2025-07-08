#!/bin/bash

# 🕵️ ARKALIA QUEST - LANCEUR DE TESTS INTELLIGENTS
# ================================================

echo "🕵️ ARKALIA QUEST - TESTEUR INTELLIGENT COMPLET"
echo "================================================"
echo ""

# Vérification de l'environnement
echo "🔍 Vérification de l'environnement..."

# Vérifier si Python est installé
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 n'est pas installé"
    exit 1
fi

# Vérifier si le serveur est en cours d'exécution
echo "🌐 Vérification du serveur Arkalia Quest..."
if ! curl -s http://localhost:5001 > /dev/null; then
    echo "❌ Le serveur Arkalia Quest n'est pas accessible sur http://localhost:5001"
    echo "💡 Assurez-vous que le serveur est démarré avec: python app.py"
    exit 1
fi

echo "✅ Serveur accessible"
echo ""

# Vérifier les dépendances Python
echo "📦 Vérification des dépendances..."
python3 -c "import requests, json, time, random, threading, concurrent.futures, urllib.parse, sys, os, datetime, hashlib, base64" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "❌ Dépendances Python manquantes"
    echo "💡 Installez les dépendances avec: pip install requests"
    exit 1
fi

echo "✅ Dépendances OK"
echo ""

# Configuration des tests
echo "⚙️ Configuration des tests..."
echo "   - URL: http://localhost:5001"
echo "   - Utilisateurs concurrents: 5"
echo "   - Tests de stress: 100 requêtes"
echo "   - Timeout: 10 secondes"
echo ""

# Confirmation de l'utilisateur
read -p "🚀 Lancer les tests intelligents ? (y/N): " -n 1 -r
echo ""
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "⏹️ Tests annulés"
    exit 0
fi

echo ""
echo "🚀 Démarrage des tests intelligents..."
echo "⏰ Début: $(date)"
echo ""

# Lancement des tests
python3 test_intelligent_complet.py

# Vérification du fichier de résultats
echo ""
echo "📊 Vérification des résultats..."
if ls test_results_*.json 1> /dev/null 2>&1; then
    latest_result=$(ls -t test_results_*.json | head -1)
    echo "✅ Résultats sauvegardés dans: $latest_result"
    
    # Affichage d'un résumé rapide
    echo ""
    echo "📈 RÉSUMÉ RAPIDE:"
    python3 -c "
import json
import sys
try:
    with open('$latest_result', 'r') as f:
        data = json.load(f)
    results = data['results']
    total = results['tests_total']
    passed = results['tests_passed']
    failed = results['tests_failed']
    success_rate = (passed / total * 100) if total > 0 else 0
    
    print(f'   🎯 Tests totaux: {total}')
    print(f'   ✅ Tests réussis: {passed}')
    print(f'   ❌ Tests échoués: {failed}')
    print(f'   📈 Taux de succès: {success_rate:.1f}%')
    print(f'   🚨 Erreurs: {len(results[\"errors\"])}')
    print(f'   🔒 Problèmes sécurité: {len(results[\"security_issues\"])}')
    print(f'   🎨 Problèmes UX: {len(results[\"ux_issues\"])}')
    
    if success_rate >= 95:
        print('   🎉 ÉTAT: EXCELLENT')
    elif success_rate >= 80:
        print('   👍 ÉTAT: BON')
    elif success_rate >= 60:
        print('   ⚠️ ÉTAT: MOYEN')
    else:
        print('   🚨 ÉTAT: CRITIQUE')
        
except Exception as e:
    print(f'   ❌ Erreur lecture résultats: {e}')
"
else
    echo "❌ Aucun fichier de résultats trouvé"
fi

echo ""
echo "🏁 Tests terminés !"
echo "⏰ Fin: $(date)"
echo ""
echo "💡 Pour voir les détails complets, consultez le fichier test_results_*.json" 