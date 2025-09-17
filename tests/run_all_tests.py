#!/usr/bin/env python3
"""
Script de lancement unifié pour tous les tests - Arkalia Quest
Gère l'exécution, les résultats et les rapports de tous les tests
"""

import json
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path


def check_server():
    """Vérifie que le serveur est accessible"""
    try:
        import requests

        response = requests.get("http://localhost:5001/", timeout=5)
        return response.status_code == 200
    except Exception:
        return False


def run_test_script(script_path, test_name):
    """Exécute un script de test et capture le résultat"""
    print(f"\n🧪 EXÉCUTION: {test_name}")
    print("=" * 50)

    start_time = time.time()

    try:
        # Exécuter le script
        result = subprocess.run(
            [sys.executable, str(script_path)],
            check=False,
            capture_output=True,
            text=True,
            timeout=300,  # 5 minutes max
        )

        end_time = time.time()
        duration = round(end_time - start_time, 2)

        success = result.returncode == 0

        return {
            "test_name": test_name,
            "script_path": str(script_path),
            "success": success,
            "duration": duration,
            "stdout": result.stdout,
            "stderr": result.stderr,
            "return_code": result.returncode,
        }

    except subprocess.TimeoutExpired:
        return {
            "test_name": test_name,
            "script_path": str(script_path),
            "success": False,
            "duration": 300,
            "error": "Timeout - Test trop long",
        }
    except Exception as e:
        return {
            "test_name": test_name,
            "script_path": str(script_path),
            "success": False,
            "duration": 0,
            "error": str(e),
        }


def run_experience_tests():
    """Exécute les tests d'expérience utilisateur"""
    print("\n🎮 TESTS D'EXPÉRIENCE UTILISATEUR")
    print("=" * 40)

    experience_tests = [
        "test_ui_boutons_actions_experience.py",
        "test_ui_navigation_experience.py",
        "test_ui_terminal_experience.py",
        "test_ui_pwa_mobile_experience.py",
        "test_ui_tutoriel_experience.py",
    ]

    results = []

    for test_file in experience_tests:
        test_path = Path(test_file)
        if test_path.exists():
            result = run_test_script(test_path, test_file.replace(".py", ""))
            results.append(result)
        else:
            print(f"⚠️ Test non trouvé: {test_file}")

    return results


def run_stable_tests():
    """Exécute les tests de stabilité"""
    print("\n🔧 TESTS DE STABILITÉ")
    print("=" * 30)

    stable_tests = [
        "test_stable_version_complete.py",
        "test_security_complete.py",
        "test_performance_stress.py",
        "test_gamification_complete.py",
        "test_complet_arkalia.py",
    ]

    results = []

    for test_file in stable_tests:
        test_path = Path(test_file)
        if test_path.exists():
            result = run_test_script(test_path, test_file.replace(".py", ""))
            results.append(result)
        else:
            print(f"⚠️ Test non trouvé: {test_file}")

    return results


def run_script_tests():
    """Exécute les tests de scripts"""
    print("\n📜 TESTS DE SCRIPTS")
    print("=" * 25)

    script_tests = [
        "test_boutons_rapide.py",
        "test_tutoriel.py",
        "test_interface_complete.py",
        "test_os2142_complete.py",
        "test_phase1_complete.py",
    ]

    results = []

    for test_file in script_tests:
        test_path = Path("scripts") / test_file
        if test_path.exists():
            result = run_test_script(test_path, test_file.replace(".py", ""))
            results.append(result)
        else:
            print(f"⚠️ Test non trouvé: {test_file}")

    return results


def generate_report(all_results):
    """Génère un rapport global de tous les tests"""
    session_id = datetime.now().strftime("%Y%m%d_%H%M%S")

    # Organiser les résultats par catégorie
    experience_results = [r for r in all_results if "ui_" in r["test_name"]]
    stable_results = [
        r
        for r in all_results
        if any(
            x in r["test_name"]
            for x in [
                "stable",
                "security",
                "performance",
                "gamification",
                "complet_arkalia",
            ]
        )
    ]
    script_results = [
        r
        for r in all_results
        if r["test_name"]
        in [
            "test_boutons_rapide",
            "test_tutoriel",
            "test_interface_complete",
            "test_os2142_complete",
            "test_phase1_complete",
        ]
    ]

    report = {
        "session_id": session_id,
        "timestamp": datetime.now().isoformat(),
        "summary": {
            "total_tests": len(all_results),
            "successful_tests": sum(1 for r in all_results if r.get("success")),
            "failed_tests": sum(1 for r in all_results if not r.get("success")),
            "total_duration": sum(r.get("duration", 0) for r in all_results),
        },
        "categories": {
            "experience_tests": {
                "count": len(experience_results),
                "successful": sum(1 for r in experience_results if r.get("success")),
                "results": experience_results,
            },
            "stable_tests": {
                "count": len(stable_results),
                "successful": sum(1 for r in stable_results if r.get("success")),
                "results": stable_results,
            },
            "script_tests": {
                "count": len(script_results),
                "successful": sum(1 for r in script_results if r.get("success")),
                "results": script_results,
            },
        },
        "all_results": all_results,
    }

    # Sauvegarder le rapport
    reports_dir = Path("reports")
    reports_dir.mkdir(exist_ok=True)

    filename = f"complete_test_report_{session_id}.json"
    filepath = reports_dir / filename

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2, ensure_ascii=False)

    return report, filepath


def main():
    """Fonction principale"""
    print("🚀 LANCEMENT DE TOUS LES TESTS - ARKALIA QUEST")
    print("=" * 60)

    # Vérifier que le serveur est accessible
    if not check_server():
        print("❌ Serveur non accessible. Démarrez le serveur avec: python app.py")
        return

    print("✅ Serveur accessible")

    # Créer les dossiers nécessaires
    Path("results").mkdir(exist_ok=True)
    Path("reports").mkdir(exist_ok=True)

    all_results = []

    # Exécuter tous les types de tests
    print("\n" + "=" * 60)
    print("🎯 DÉBUT DE L'EXÉCUTION DES TESTS")
    print("=" * 60)

    # Tests d'expérience utilisateur
    experience_results = run_experience_tests()
    all_results.extend(experience_results)

    # Tests de stabilité
    stable_results = run_stable_tests()
    all_results.extend(stable_results)

    # Tests de scripts
    script_results = run_script_tests()
    all_results.extend(script_results)

    # Générer le rapport global
    print("\n" + "=" * 60)
    print("📋 GÉNÉRATION DU RAPPORT GLOBAL")
    print("=" * 60)

    report, filepath = generate_report(all_results)

    # Afficher le résumé
    print("\n🎯 RÉSUMÉ FINAL")
    print("=" * 30)
    print(f"📊 Total des tests: {report['summary']['total_tests']}")
    print(f"✅ Tests réussis: {report['summary']['successful_tests']}")
    print(f"❌ Tests échoués: {report['summary']['failed_tests']}")
    print(f"⏱️ Durée totale: {report['summary']['total_duration']}s")

    print(f"\n📋 RAPPORT SAUVEGARDÉ: {filepath}")

    # Afficher les détails par catégorie
    print("\n📈 DÉTAILS PAR CATÉGORIE:")
    print(
        f"🎮 Tests d'expérience: {report['categories']['experience_tests']['successful']}/{report['categories']['experience_tests']['count']}",
    )
    print(
        f"🔧 Tests de stabilité: {report['categories']['stable_tests']['successful']}/{report['categories']['stable_tests']['count']}",
    )
    print(
        f"📜 Tests de scripts: {report['categories']['script_tests']['successful']}/{report['categories']['script_tests']['count']}",
    )

    # Afficher les tests échoués
    failed_tests = [r for r in all_results if not r.get("success")]
    if failed_tests:
        print("\n❌ TESTS ÉCHOUÉS:")
        for test in failed_tests:
            print(f"  - {test['test_name']}: {test.get('error', 'Erreur inconnue')}")

    print("\n🎉 EXÉCUTION TERMINÉE !")


if __name__ == "__main__":
    main()
