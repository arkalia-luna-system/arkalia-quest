#!/bin/bash
# 🚀 Script de build personnalisé pour Render
# Force l'utilisation de pip et de Python 3.10.14

echo "🐍 Vérification de la version Python..."
python --version

echo "📦 Mise à jour de pip..."
pip install --upgrade pip

echo "🔧 Installation des dépendances..."
pip install -r requirements.txt

echo "✅ Build terminé avec succès !"
