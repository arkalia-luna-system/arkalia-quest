#!/usr/bin/env python3
"""
Script de nettoyage et organisation des tests - Arkalia Quest
Nettoie les anciens rapports et organise les fichiers de tests
"""

import os
import shutil
from datetime import datetime, timedelta
from pathlib import Path


def cleanup_old_reports():
    """Nettoie les anciens rapports de plus de 30 jours"""
    print("🧹 NETTOYAGE DES ANCIENS RAPPORTS")
    print("=" * 40)

    # Dossiers à nettoyer
    cleanup_dirs = ["tests/results", "tests/reports"]

    cutoff_date = datetime.now() - timedelta(days=30)
    total_removed = 0

    for dir_path in cleanup_dirs:
        if not os.path.exists(dir_path):
            continue

        print(f"\n📁 Nettoyage de {dir_path}...")
        removed_count = 0

        for file_path in Path(dir_path).glob("*.json"):
            try:
                file_time = datetime.fromtimestamp(file_path.stat().st_mtime)
                if file_time < cutoff_date:
                    file_path.unlink()
                    removed_count += 1
                    print(f"  🗑️ Supprimé: {file_path.name}")
            except Exception as e:
                print(f"  ⚠️ Erreur avec {file_path.name}: {e}")

        total_removed += removed_count
        print(f"  ✅ {removed_count} fichiers supprimés")

    print(f"\n🎯 Total: {total_removed} fichiers supprimés")


def organize_root_files():
    """Organise les fichiers de tests dispersés à la racine"""
    print("\n📦 ORGANISATION DES FICHIERS À LA RACINE")
    print("=" * 45)

    # Fichiers à déplacer vers tests/reports
    report_patterns = [
        "*test*report*.json",
        "*experience*report*.json",
        "*performance*results*.json",
        "*security*results*.json",
        "*stable*test*.json",
    ]

    # Fichiers à déplacer vers tests/scripts
    script_patterns = ["test_*.py"]

    root_dir = Path("..")
    reports_dir = Path("reports")
    scripts_dir = Path("scripts")

    moved_count = 0

    # Déplacer les rapports
    for pattern in report_patterns:
        for file_path in root_dir.glob(pattern):
            if (
                file_path.is_file()
                and file_path.name != "diagnostic_boutons_report.json"
            ):
                try:
                    dest_path = reports_dir / file_path.name
                    shutil.move(str(file_path), str(dest_path))
                    print(f"  📄 Déplacé: {file_path.name} → reports/")
                    moved_count += 1
                except Exception as e:
                    print(f"  ⚠️ Erreur avec {file_path.name}: {e}")

    # Déplacer les scripts
    for pattern in script_patterns:
        for file_path in root_dir.glob(pattern):
            if file_path.is_file():
                try:
                    dest_path = scripts_dir / file_path.name
                    shutil.move(str(file_path), str(dest_path))
                    print(f"  📜 Déplacé: {file_path.name} → scripts/")
                    moved_count += 1
                except Exception as e:
                    print(f"  ⚠️ Erreur avec {file_path.name}: {e}")

    print(f"\n✅ {moved_count} fichiers organisés")


def create_summary():
    """Crée un résumé de l'état des tests"""
    print("\n📊 RÉSUMÉ DE L'ÉTAT DES TESTS")
    print("=" * 35)

    # Compter les fichiers dans chaque dossier
    dirs_to_check = {
        "tests/results": "Résultats individuels",
        "tests/reports": "Rapports globaux",
        "tests/scripts": "Scripts de test",
    }

    total_files = 0

    for dir_path, description in dirs_to_check.items():
        if os.path.exists(dir_path):
            file_count = len(list(Path(dir_path).glob("*")))
            total_files += file_count
            print(f"📁 {description}: {file_count} fichiers")
        else:
            print(f"📁 {description}: Dossier inexistant")

    print(f"\n🎯 Total: {total_files} fichiers de test")

    # Vérifier les tests manquants
    print("\n🔍 TESTS MANQUANTS:")
    missing_tests = []

    expected_tests = [
        "tests/test_ui_boutons_actions_experience.py",
        "tests/test_ui_navigation_experience.py",
        "tests/test_ui_terminal_experience.py",
        "tests/test_ui_pwa_mobile_experience.py",
        "tests/test_ui_tutoriel_experience.py",
        "tests/test_stable_version_complete.py",
        "tests/test_security_complete.py",
        "tests/test_performance_stress.py",
        "tests/test_gamification_complete.py",
        "tests/test_complet_arkalia.py",
    ]

    for test_path in expected_tests:
        if not os.path.exists(test_path):
            missing_tests.append(test_path)

    if missing_tests:
        for test in missing_tests:
            print(f"  ❌ {test}")
    else:
        print("  ✅ Tous les tests principaux sont présents")


def main():
    """Fonction principale"""
    print("🧹 ORGANISATION ET NETTOYAGE DES TESTS - ARKALIA QUEST")
    print("=" * 60)

    # Créer les dossiers nécessaires
    Path("results").mkdir(exist_ok=True)
    Path("reports").mkdir(exist_ok=True)
    Path("scripts").mkdir(exist_ok=True)

    # Nettoyer les anciens rapports
    cleanup_old_reports()

    # Organiser les fichiers à la racine
    organize_root_files()

    # Créer un résumé
    create_summary()

    print("\n🎉 ORGANISATION TERMINÉE !")
    print("📋 Consultez tests/README_TESTS.md pour plus d'informations")


if __name__ == "__main__":
    main()
