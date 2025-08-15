#!/bin/bash
# Script pour activer l'environnement Arkalia Quest

# Désactiver tout environnement virtuel existant
unset VIRTUAL_ENV
unset VENV_NAME

# Activer Arkalia Quest
export VENV_NAME="arkalia-quest"
export VIRTUAL_ENV="$(pwd)/.venv-quest"
export PATH="$(pwd)/.venv-quest/bin:$PATH"
export FLASK_APP=app.py
export FLASK_ENV=development

# Prompt Arkalia Quest
PS1='🎮 Arkalia-Quest 🕰️ %t — 📂 %1~ — 💾 $(df -h . | tail -1 | awk "{print \$4}") libres / $(df -h . | tail -1 | awk "{print \$2}")\n🌟 Kernel IA ultra-protection active ✅\n%n@%m %1~ %# '

echo "🎮 Environnement Arkalia Quest activé !"
echo "Python: $(which python)"
echo "VIRTUAL_ENV: $VIRTUAL_ENV" 