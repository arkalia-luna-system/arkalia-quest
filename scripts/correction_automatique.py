#!/usr/bin/env python3
"""
🔧 CORRECTION AUTOMATIQUE ARKALIA QUEST
======================================

Script pour corriger automatiquement les problèmes détectés par l'audit
"""

import os
import re
import subprocess
from pathlib import Path

# Import du logger
try:
    from utils.logger import game_logger
except ImportError:
    import logging

    game_logger = logging.getLogger("correction_automatique")


def fix_print_debug():
    """Remplace les prints de debug par des logs"""
    game_logger.info(r"🔧 Correction des prints de debug...")

    python_files = []
    for root, dirs, files in os.walk("."):
        dirs[:] = [
            d for d in dirs if d not in ["venv", "__pycache__", ".git", "node_modules"]
        ]
        for file in files:
            if file.endswith(".py"):
                python_files.append(Path(root) / file)

    for file_path in python_files:
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()

            original_content = content

            # Remplacer les prints de debug par des logs
            content = re.sub(
                r'print\s*\(\s*["\']([^"\']*)["\']\s*\)',
                r'game_logger.info(r"\1")',
                content,
            )

            content = re.sub(
                r'print\s*\(\s*f["\']([^"\']*)["\']\s*\)',
                r'game_logger.info(f"\1")',
                content,
            )

            if content != original_content:
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(content)
                game_logger.info(f"✅ Corrigé: {file_path}")

        except Exception as e:
            game_logger.info(f"❌ Erreur {file_path}: {e}")


def fix_imports():
    """Corrige les imports problématiques"""
    game_logger.info(r"🔧 Correction des imports...")

    # Ajouter les imports manquants dans app.py
    app_py = Path("app.py")
    if app_py.exists():
        with open(app_py, "r", encoding="utf-8") as f:
            content = f.read()

        # Vérifier si game_logger est importé
        if (
            "game_logger" in content
            and "from utils.logger import game_logger" not in content
        ):
            # Ajouter l'import
            content = content.replace(
                "from flask import Flask, render_template, request, jsonify, session",
                "from flask import Flask, render_template, request, jsonify, session\nfrom utils.logger import game_logger",
            )

            with open(app_py, "w", encoding="utf-8") as f:
                f.write(content)
            game_logger.info(r"✅ Imports corrigés dans app.py")


def fix_encoding_issues():
    """Corrige les problèmes d'encodage"""
    print("🔧 Correction des problèmes d'encodage...")

    # Supprimer les fichiers cachés macOS
    subprocess.run(["find", ".", "-name", "._*", "-delete"], check=False)
    game_logger.info(r"✅ Fichiers cachés supprimés")


def fix_long_functions():
    """Divise les fonctions trop longues"""
    game_logger.info(r"🔧 Correction des fonctions trop longues...")

    # Pour l'instant, on se contente de logger les fonctions longues
    # Une refactorisation manuelle sera nécessaire
    game_logger.info(
        r"⚠️  Refactorisation manuelle nécessaire pour les fonctions longues"
    )


def run_linting_fixes():
    """Exécute les corrections de linting automatiques"""
    game_logger.info(r"🔧 Exécution des corrections de linting...")

    try:
        # Black
        subprocess.run(["python", "-m", "black", "."], check=True)
        game_logger.info(r"✅ Black appliqué")

        # Ruff
        subprocess.run(["python", "-m", "ruff", "check", ".", "--fix"], check=True)
        game_logger.info(r"✅ Ruff appliqué")

    except subprocess.CalledProcessError as e:
        game_logger.info(f"❌ Erreur linting: {e}")


def main():
    """Fonction principale"""
    game_logger.info(r"🚀 DÉMARRAGE DES CORRECTIONS AUTOMATIQUES")
    print("=" * 50)

    fix_encoding_issues()
    fix_print_debug()
    fix_imports()
    fix_long_functions()
    run_linting_fixes()

    print("\n" + "=" * 50)
    game_logger.info(r"✅ CORRECTIONS AUTOMATIQUES TERMINÉES")
    game_logger.info(r"📋 Prochaines étapes recommandées :")
    game_logger.info(r"   1. Refactoriser les fonctions trop longues manuellement")
    game_logger.info(r"   2. Vérifier les TODO/FIXME restants")
    print("   3. Tester l'application après corrections")


if __name__ == "__main__":
    main()
