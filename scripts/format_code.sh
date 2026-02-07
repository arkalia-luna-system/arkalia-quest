#!/bin/bash

# Script de formatage du code Arkalia Quest
# Évite les problèmes avec les fichiers cachés macOS

echo "🧹 Nettoyage des fichiers cachés macOS..."
find . -name "._*" -delete

echo "⚫ Formatage avec Black..."
black app.py core/ tests/ scripts/ engines/ utils/ config/

echo "🔍 Vérification avec Ruff..."
ruff check --fix app.py core/ tests/ scripts/ engines/ utils/ config/

echo "✅ Formatage terminé !"
