#!/usr/bin/env python3
"""
Test automatisé pour validation utilisateur d'Arkalia Quest
Complète les tests manuels avec des vérifications automatiques
"""

import json
import os
import sys
from datetime import datetime

# Ajouter le répertoire parent au path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def test_interface_responsive():
    """Test de la responsivité de l'interface"""
    print("📱 Test de responsivité...")

    # Vérifier que les fichiers CSS responsive existent
    css_files = ["static/css/responsive.css", "static/css/arkalia-luna-vision.css"]

    responsive_ok = True
    for css_file in css_files:
        if not os.path.exists(css_file):
            print(f"❌ {css_file} manquant")
            responsive_ok = False
        else:
            print(f"✅ {css_file} présent")

    assert responsive_ok, "Fichiers CSS responsive manquants"


def test_accessibility():
    """Test des fonctionnalités d'accessibilité"""
    print("♿ Test d'accessibilité...")

    # Vérifier que les fichiers d'accessibilité existent
    accessibility_files = [
        "static/js/accessibility.js",
        "templates/accessibility_panel.html",
    ]

    accessibility_ok = True
    for file_path in accessibility_files:
        if not os.path.exists(file_path):
            print(f"❌ {file_path} manquant")
            accessibility_ok = False
        else:
            print(f"✅ {file_path} présent")

    assert accessibility_ok, "Fichiers d'accessibilité manquants"


def test_performance():
    """Test des optimisations de performance"""
    print("⚡ Test de performance...")

    # Vérifier que les fichiers de performance existent
    performance_files = [
        "static/css/performance-optimized.css",
        "static/js/performance-optimizer.js",
    ]

    performance_ok = True
    for file_path in performance_files:
        if not os.path.exists(file_path):
            print(f"❌ {file_path} manquant")
            performance_ok = False
        else:
            print(f"✅ {file_path} présent")

    assert performance_ok, "Fichiers de performance manquants"


def test_content_quality():
    """Test de la qualité du contenu"""
    print("📚 Test de qualité du contenu...")

    # Vérifier que les fichiers de contenu existent
    content_files = [
        "data/missions/intro.json",
        "data/missions/prologue.json",
        "data/badges_secrets.json",
    ]

    content_ok = True
    for file_path in content_files:
        if not os.path.exists(file_path):
            print(f"❌ {file_path} manquant")
            content_ok = False
        else:
            print(f"✅ {file_path} présent")

    assert content_ok, "Fichiers de contenu manquants"


def test_educational_value():
    """Test de la valeur éducative"""
    print("🎓 Test de valeur éducative...")

    # Vérifier que les fichiers éducatifs existent
    educational_files = [
        "core/educational_games_engine.py",
        "static/js/educational_games.js",
    ]

    educational_ok = True
    for file_path in educational_files:
        if not os.path.exists(file_path):
            print(f"❌ {file_path} manquant")
            educational_ok = False
        else:
            print(f"✅ {file_path} présent")

    assert educational_ok, "Fichiers éducatifs manquants"


def main():
    """Fonction principale de test"""
    print("🚀 TEST AUTOMATISÉ DE VALIDATION UTILISATEUR")
    print("=" * 50)

    tests = [
        test_interface_responsive,
        test_accessibility,
        test_performance,
        test_content_quality,
        test_educational_value,
    ]

    results = {
        "timestamp": datetime.now().isoformat(),
        "tests": {},
        "summary": {"total": len(tests), "passed": 0, "failed": 0},
    }

    for test_func in tests:
        try:
            test_func()
            results["tests"][test_func.__name__] = {"status": "pass"}
            results["summary"]["passed"] += 1
            print(f"✅ {test_func.__name__} réussi")
        except Exception as e:
            results["tests"][test_func.__name__] = {
                "status": "fail",
                "error": str(e),
            }
            results["summary"]["failed"] += 1
            print(f"❌ {test_func.__name__} échoué: {e}")

    # Sauvegarder les résultats
    output_file = f"reports/test_reports/test_utilisateur_automated_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    print(f"\n📊 Résultats sauvegardés dans {output_file}")
    print(f"✅ {results['summary']['passed']} tests réussis")
    print(f"❌ {results['summary']['failed']} tests échoués")

    return results["summary"]["failed"] == 0


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
