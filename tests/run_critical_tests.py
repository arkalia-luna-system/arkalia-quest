#!/usr/bin/env python3
"""
🚀 LANCEUR DES TESTS CRITIQUES - ARKALIA QUEST
Lance tous les tests critiques pour valider la qualité du jeu
PRIORITÉ ABSOLUE - Validation de la stabilité et des performances
"""

import json
import os
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path

# Configuration des tests
TEST_CONFIG = {
    "base_url": "http://localhost:5001",
    "timeout": 30,
    "parallel": False,
    "generate_reports": True,
    "coverage_target": 85,
}

# Structure des tests par priorités
TEST_PRIORITIES = {
    "🔥 CRITIQUE": {
        "description": "Tests des modules critiques et de la stabilité",
        "tests": [
            "tests/core/test_luna_emotions_complete.py",
            "tests/core/test_gamification_complete.py",
            "tests/performance/test_performance_complete.py",
        ],
        "required": True,
    },
    "⚡ HAUTE PRIORITÉ": {
        "description": "Tests d'interface et d'accessibilité",
        "tests": [
            "tests/test_accessibility_complete.py",
            "tests/test_ui_tutoriel_experience.py",
            "tests/test_ui_terminal_experience.py",
        ],
        "required": True,
    },
    "📱 PRIORITÉ MOYENNE": {
        "description": "Tests d'expérience utilisateur",
        "tests": [
            "tests/test_ui_improvements_teen.py",
            "tests/test_immersive_system_complete.py",
            "tests/test_ui_pwa_mobile_experience.py",
        ],
        "required": False,
    },
}

# Couleurs pour l'affichage
COLORS = {
    "reset": "\033[0m",
    "bold": "\033[1m",
    "red": "\033[91m",
    "green": "\033[92m",
    "yellow": "\033[93m",
    "blue": "\033[94m",
    "magenta": "\033[95m",
    "cyan": "\033[96m",
}


def print_header():
    """Affiche l'en-tête du lanceur de tests"""
    print(f"{COLORS['bold']}{COLORS['cyan']}")
    print("=" * 80)
    game_logger.info(r"🚀 LANCEUR DES TESTS CRITIQUES - ARKALIA QUEST")
    print("=" * 80)
    print(f"{COLORS['reset']}")
    print(f"📅 Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    game_logger.info(r"🎯 Objectif: Validation complète de la qualité du jeu")
    print(f"📊 Couverture cible: {TEST_CONFIG['coverage_target']}%")
    print(f"⚡ Mode parallèle: {'Activé' if TEST_CONFIG['parallel'] else 'Désactivé'}")
    print()


def check_environment():
    """Vérifie l'environnement de test"""
    print(f"{COLORS['blue']}🔍 VÉRIFICATION DE L'ENVIRONNEMENT{COLORS['reset']}")
    print("-" * 50)

    # Vérifier Python
    python_version = sys.version_info
    game_logger.info(
        f"🐍 Python: {python_version.major}.{python_version.minor}.{python_version.micro}"
    )

    if python_version < (3, 8):
        print(f"{COLORS['red']}❌ Python 3.8+ requis{COLORS['reset']}")
        return False
    print(f"{COLORS['green']}✅ Version Python compatible{COLORS['reset']}")

    # Vérifier les dépendances
    required_packages = ["pytest", "black", "ruff"]
    missing_packages = []

    for package in required_packages:
        try:
            __import__(package)
            print(f"{COLORS['green']}✅ {package} disponible{COLORS['reset']}")
        except ImportError:
            print(f"{COLORS['red']}❌ {package} manquant{COLORS['reset']}")
            missing_packages.append(package)

    if missing_packages:
        print(
            f"\n{COLORS['yellow']}⚠️ Installez les packages"
            + "manquants:{COLORS['reset']}"
        )
        print(f"pip install {' '.join(missing_packages)}")
        return False

    # Vérifier la structure des tests
    test_dir = Path("tests")
    if not test_dir.exists():
        print(f"{COLORS['red']}❌ Dossier tests/ manquant{COLORS['reset']}")
        return False

    print(f"{COLORS['green']}✅ Structure des tests valide{COLORS['reset']}")

    print()
    return True


def run_code_quality_checks():
    """Exécute les vérifications de qualité du code"""
    print(f"{COLORS['blue']}🔧 VÉRIFICATIONS DE QUALITÉ DU CODE{COLORS['reset']}")
    print("-" * 50)

    # Vérifier le formatage avec Black
    game_logger.info(r"🎨 Vérification du formatage avec Black...")
    try:
        result = subprocess.run(
            ["black", "--check", "."],
            check=False,
            capture_output=True,
            text=True,
            timeout=60,
        )

        if result.returncode == 0:
            print(f"{COLORS['green']}✅ Code correctement formaté{COLORS['reset']}")
        else:
            print(
                f"{COLORS['yellow']}⚠️ Code non formaté, application de"
                "Black...{COLORS['reset']}",
            )
            subprocess.run(["black", "."], check=True)
            print(f"{COLORS['green']}✅ Formatage appliqué{COLORS['reset']}")
    except subprocess.TimeoutExpired:
        print(
            f"{COLORS['red']}❌ Timeout lors de la vérification Black{COLORS['reset']}"
        )
    except Exception as e:
        print(f"{COLORS['red']}❌ Erreur Black: {e}{COLORS['reset']}")

    # Vérifier la qualité avec Ruff
    game_logger.info(r"🧹 Vérification de la qualité avec Ruff...")
    try:
        result = subprocess.run(
            ["ruff", "check", "."],
            check=False,
            capture_output=True,
            text=True,
            timeout=60,
        )

        if result.returncode == 0:
            print(f"{COLORS['green']}✅ Code conforme aux standards{COLORS['reset']}")
        else:
            print(
                f"{COLORS['yellow']}⚠️  Problèmes de qualité détectés{COLORS['reset']}"
            )
            print(result.stdout)
            print(f"{COLORS['yellow']}⚠️  Correction automatique...{COLORS['reset']}")
            subprocess.run(["ruff", "check", "--fix", "."], check=True)
            print(f"{COLORS['green']}✅ Corrections appliquées{COLORS['reset']}")
    except subprocess.TimeoutExpired:
        print(
            f"{COLORS['red']}❌ Timeout lors de la vérification Ruff{COLORS['reset']}"
        )
    except Exception as e:
        print(f"{COLORS['red']}❌ Erreur Ruff: {e}{COLORS['reset']}")

    print()


def run_test_category(category_name, category_info):
    """Exécute une catégorie de tests"""
    print(
        f"{COLORS['blue']}{category_name} -"
        + "{category_info['description']}{COLORS['reset']}"
    )
    print("-" * 60)

    results = {
        "total": 0,
        "passed": 0,
        "failed": 0,
        "errors": 0,
        "duration": 0,
    }

    start_time = time.time()

    for test_file in category_info["tests"]:
        if not os.path.exists(test_file):
            print(
                f"{COLORS['yellow']}⚠️ Fichier de test manquant:"
                + "{test_file}{COLORS['reset']}"
            )
            continue

        game_logger.info(f"🧪 Exécution: {test_file}")

        try:
            # Exécuter le test avec pytest
            cmd = [
                "python",
                "-m",
                "pytest",
                test_file,
                "-v",
                "--tb=short",
                "--strict-markers",
                "--disable-warnings",
            ]

            if TEST_CONFIG["parallel"]:
                cmd.extend(["-n", "auto"])

            result = subprocess.run(
                cmd,
                check=False,
                capture_output=True,
                text=True,
                timeout=TEST_CONFIG["timeout"] * 60,
            )

            # Analyser le résultat
            if result.returncode == 0:
                print(f"{COLORS['green']}✅ Test réussi{COLORS['reset']}")
                results["passed"] += 1
            else:
                print(f"{COLORS['red']}❌ Test échoué{COLORS['reset']}")
                print(result.stdout)
                print(result.stderr)
                results["failed"] += 1

            results["total"] += 1

        except subprocess.TimeoutExpired:
            print(f"{COLORS['red']}❌ Timeout du test{COLORS['reset']}")
            results["errors"] += 1
            results["total"] += 1
        except Exception as e:
            print(f"{COLORS['red']}❌ Erreur d'exécution: {e}{COLORS['reset']}")
            results["errors"] += 1
            results["total"] += 1

    end_time = time.time()
    results["duration"] = end_time - start_time

    # Afficher le résumé de la catégorie
    game_logger.info(f"\n📊 Résumé {category_name}:")
    print(f"   Total: {results['total']}")
    print(f"   Réussis: {results['passed']}")
    print(f"   Échoués: {results['failed']}")
    print(f"   Erreurs: {results['errors']}")
    print(f"   Durée: {results['duration']:.2f}s")

    # Vérifier si la catégorie est critique
    if category_info["required"]:
        success_rate = (
            results["passed"] / results["total"] if results["total"] > 0 else 0
        )
        if success_rate < 0.8:  # 80% de succès minimum
            print(f"{COLORS['red']}❌ Catégorie critique échouée{COLORS['reset']}")
            return False

    print()
    return True


def run_coverage_analysis():
    """Exécute l'analyse de couverture"""
    print(f"{COLORS['blue']}📊 ANALYSE DE COUVERTURE{COLORS['reset']}")
    print("-" * 50)

    try:
        # Exécuter les tests avec couverture
        cmd = [
            "python",
            "-m",
            "pytest",
            "--cov=core",
            "--cov=arkalia_engine",
            "--cov=app",
            "--cov-report=html",
            "--cov-report=term-missing",
            "--cov-fail-under",
            str(TEST_CONFIG["coverage_target"]),
            "tests/core/",
            "tests/performance/",
        ]

        result = subprocess.run(
            cmd,
            check=False,
            capture_output=True,
            text=True,
            timeout=300,  # 5 minutes pour la couverture
        )

        if result.returncode == 0:
            print(f"{COLORS['green']}✅ Couverture atteinte{COLORS['reset']}")
        else:
            print(f"{COLORS['yellow']}⚠️  Couverture insuffisante{COLORS['reset']}")
            print(result.stdout)

        # Afficher le rapport de couverture
        game_logger.info(r"\n📈 Rapport de couverture:")
        print(result.stdout)

    except subprocess.TimeoutExpired:
        print(f"{COLORS['red']}❌ Timeout de l'analyse de couverture{COLORS['reset']}")
    except Exception as e:
        print(f"{COLORS['red']}❌ Erreur d'analyse de couverture: {e}{COLORS['reset']}")

    print()


def generate_test_report():
    """Génère un rapport de test complet"""
    print(f"{COLORS['blue']}📋 GÉNÉRATION DU RAPPORT{COLORS['reset']}")
    print("-" * 50)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_file = f"tests/reports/test_report_{timestamp}.json"

    # Créer le dossier reports s'il n'existe pas
    os.makedirs("tests/reports", exist_ok=True)

    # Données du rapport
    report_data = {
        "timestamp": datetime.now().isoformat(),
        "test_config": TEST_CONFIG,
        "python_version": f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}",
        "test_priorities": TEST_PRIORITIES,
        "summary": {
            "total_categories": len(TEST_PRIORITIES),
            "critical_tests": sum(
                len(cat["tests"]) for cat in TEST_PRIORITIES.values() if cat["required"]
            ),
            "optional_tests": sum(
                len(cat["tests"])
                for cat in TEST_PRIORITIES.values()
                if not cat["required"]
            ),
        },
    }

    # Sauvegarder le rapport
    try:
        with open(report_file, "w", encoding="utf-8") as f:
            json.dump(report_data, f, indent=2, ensure_ascii=False)

        print(f"{COLORS['green']}✅ Rapport généré: {report_file}{COLORS['reset']}")
    except Exception as e:
        print(
            f"{COLORS['red']}❌ Erreur de génération du rapport: {e}{COLORS['reset']}"
        )

    print()


def main():
    """Fonction principale du lanceur de tests"""
    print_header()

    # Vérifier l'environnement
    if not check_environment():
        print(
            f"{COLORS['red']}❌ Environnement invalide, arrêt des tests{COLORS['reset']}"
        )
        sys.exit(1)

    # Exécuter les vérifications de qualité
    run_code_quality_checks()

    # Exécuter les tests par catégorie
    all_tests_passed = True

    for category_name, category_info in TEST_PRIORITIES.items():
        category_success = run_test_category(category_name, category_info)
        if not category_success and category_info["required"]:
            all_tests_passed = False

    # Exécuter l'analyse de couverture
    run_coverage_analysis()

    # Générer le rapport
    if TEST_CONFIG["generate_reports"]:
        generate_test_report()

    # Affichage du résumé final
    print(f"{COLORS['bold']}{COLORS['cyan']}🎯 RÉSUMÉ FINAL{COLORS['reset']}")
    print("=" * 80)

    if all_tests_passed:
        print(
            f"{COLORS['green']}🎉 TOUS LES TESTS CRITIQUES ONT RÉUSSI !{COLORS['reset']}"
        )
        print(
            f"{COLORS['green']}✅ Arkalia Quest est prêt pour la"
            + "production{COLORS['reset']}"
        )
        sys.exit(0)
    else:
        print(f"{COLORS['red']}❌ CERTAINS TESTS CRITIQUES ONT ÉCHOUÉ{COLORS['reset']}")
        print(
            f"{COLORS['yellow']}⚠️ Vérifiez les erreurs avant le"
            + "déploiement{COLORS['reset']}"
        )
        sys.exit(1)


if __name__ == "__main__":
    main()
