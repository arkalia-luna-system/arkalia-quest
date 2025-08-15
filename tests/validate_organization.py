#!/usr/bin/env python3
"""
Script de validation de l'organisation des tests - Arkalia Quest
Vérifie que tous les éléments de la nouvelle structure fonctionnent
"""

import os
import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path

def check_structure():
    """Vérifie la structure des dossiers"""
    print("📁 VÉRIFICATION DE LA STRUCTURE")
    print("=" * 35)
    
    required_dirs = [
        "results",
        "reports", 
        "scripts"
    ]
    
    required_files = [
        "README_TESTS.md",
        "run_all_tests.py",
        "test_manager.py",
        "cleanup_old_reports.py"
    ]
    
    all_good = True
    
    # Vérifier les dossiers
    for dir_name in required_dirs:
        if os.path.exists(dir_name):
            print(f"✅ Dossier {dir_name}/ : Présent")
        else:
            print(f"❌ Dossier {dir_name}/ : Manquant")
            all_good = False
    
    # Vérifier les fichiers
    for file_name in required_files:
        if os.path.exists(file_name):
            print(f"✅ Fichier {file_name} : Présent")
        else:
            print(f"❌ Fichier {file_name} : Manquant")
            all_good = False
    
    return all_good

def check_test_files():
    """Vérifie la présence des fichiers de test"""
    print("\n🧪 VÉRIFICATION DES FICHIERS DE TEST")
    print("=" * 40)
    
    # Tests d'expérience utilisateur
    ui_tests = [
        "test_ui_boutons_actions_experience.py",
        "test_ui_navigation_experience.py",
        "test_ui_terminal_experience.py",
        "test_ui_pwa_mobile_experience.py",
        "test_ui_tutoriel_experience.py"
    ]
    
    # Tests de stabilité
    stable_tests = [
        "test_stable_version_complete.py",
        "test_security_complete.py",
        "test_performance_stress.py",
        "test_gamification_complete.py",
        "test_complet_arkalia.py"
    ]
    
    # Tests de scripts
    script_tests = [
        "scripts/test_boutons_rapide.py",
        "scripts/test_tutoriel.py",
        "scripts/test_interface_complete.py",
        "scripts/test_os2142_complete.py",
        "scripts/test_phase1_complete.py"
    ]
    
    all_tests = ui_tests + stable_tests + script_tests
    missing_tests = []
    present_tests = []
    
    for test_file in all_tests:
        if os.path.exists(test_file):
            present_tests.append(test_file)
            print(f"✅ {test_file}")
        else:
            missing_tests.append(test_file)
            print(f"❌ {test_file}")
    
    print(f"\n📊 Résumé:")
    print(f"  ✅ Tests présents: {len(present_tests)}")
    print(f"  ❌ Tests manquants: {len(missing_tests)}")
    
    return len(missing_tests) == 0

def test_quick_script():
    """Teste un script rapide pour vérifier le fonctionnement"""
    print("\n🚀 TEST D'UN SCRIPT RAPIDE")
    print("=" * 30)
    
    if not os.path.exists("scripts/test_boutons_rapide.py"):
        print("❌ Script test_boutons_rapide.py non trouvé")
        return False
    
    try:
        # Lancer le test
        result = subprocess.run(
            [sys.executable, "scripts/test_boutons_rapide.py"],
            capture_output=True,
            text=True,
            timeout=60
        )
        
        if result.returncode == 0:
            print("✅ Script exécuté avec succès")
            
            # Vérifier qu'un fichier de résultat a été créé
            results_files = list(Path("results").glob("test_boutons_rapide_*.json"))
            if results_files:
                print(f"✅ Fichier de résultat créé: {results_files[-1].name}")
                
                # Vérifier le contenu du fichier
                try:
                    with open(results_files[-1], 'r', encoding='utf-8') as f:
                        data = json.load(f)
                    
                    required_fields = ["test_name", "session_id", "timestamp", "success"]
                    missing_fields = [field for field in required_fields if field not in data]
                    
                    if not missing_fields:
                        print("✅ Structure JSON correcte")
                        return True
                    else:
                        print(f"❌ Champs manquants: {missing_fields}")
                        return False
                        
                except Exception as e:
                    print(f"❌ Erreur lecture JSON: {e}")
                    return False
            else:
                print("❌ Aucun fichier de résultat créé")
                return False
        else:
            print(f"❌ Erreur d'exécution: {result.stderr}")
            return False
            
    except subprocess.TimeoutExpired:
        print("❌ Timeout lors de l'exécution")
        return False
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False

def check_reports_organization():
    """Vérifie l'organisation des rapports"""
    print("\n📋 VÉRIFICATION DE L'ORGANISATION DES RAPPORTS")
    print("=" * 50)
    
    # Compter les fichiers dans chaque dossier
    reports_count = len(list(Path("reports").glob("*.json")))
    results_count = len(list(Path("results").glob("*.json")))
    
    print(f"📄 Rapports dans reports/: {reports_count}")
    print(f"📊 Résultats dans results/: {results_count}")
    
    # Vérifier qu'il n'y a plus de fichiers à la racine
    root_files = list(Path("..").glob("*test*.py")) + list(Path("..").glob("*report*.json"))
    root_files = [f for f in root_files if f.is_file()]
    
    if root_files:
        print(f"⚠️ Fichiers encore à la racine: {len(root_files)}")
        for file in root_files[:5]:  # Afficher les 5 premiers
            print(f"  - {file.name}")
        if len(root_files) > 5:
            print(f"  ... et {len(root_files) - 5} autres")
    else:
        print("✅ Aucun fichier de test à la racine")
    
    return len(root_files) == 0

def generate_validation_report():
    """Génère un rapport de validation"""
    print("\n📊 GÉNÉRATION DU RAPPORT DE VALIDATION")
    print("=" * 45)
    
    report = {
        "timestamp": datetime.now().isoformat(),
        "validation_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "checks": {
            "structure": check_structure(),
            "test_files": check_test_files(),
            "quick_script": test_quick_script(),
            "reports_organization": check_reports_organization()
        }
    }
    
    # Calculer le score global
    passed_checks = sum(report["checks"].values())
    total_checks = len(report["checks"])
    score = (passed_checks / total_checks) * 100
    
    report["score"] = score
    report["passed_checks"] = passed_checks
    report["total_checks"] = total_checks
    
    # Sauvegarder le rapport
    filename = f"validation_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    filepath = Path("reports") / filename
    
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    
    print(f"📄 Rapport sauvegardé: {filepath}")
    
    return report, filepath

def main():
    """Fonction principale"""
    print("🔍 VALIDATION DE L'ORGANISATION DES TESTS - ARKALIA QUEST")
    print("=" * 65)
    
    # Effectuer toutes les vérifications
    report, filepath = generate_validation_report()
    
    # Afficher le résumé
    print(f"\n🎯 RÉSUMÉ DE LA VALIDATION")
    print("=" * 30)
    print(f"📊 Score global: {report['score']:.1f}%")
    print(f"✅ Vérifications réussies: {report['passed_checks']}/{report['total_checks']}")
    
    # Détails des vérifications
    for check_name, result in report["checks"].items():
        status = "✅" if result else "❌"
        print(f"{status} {check_name.replace('_', ' ').title()}")
    
    # Conclusion
    if report['score'] >= 90:
        print(f"\n🎉 EXCELLENT ! L'organisation est parfaitement fonctionnelle")
    elif report['score'] >= 75:
        print(f"\n✅ BON ! L'organisation fonctionne bien avec quelques améliorations mineures")
    elif report['score'] >= 50:
        print(f"\n⚠️ MOYEN ! L'organisation nécessite des corrections")
    else:
        print(f"\n❌ PROBLÉMATIQUE ! L'organisation nécessite une refonte")
    
    print(f"\n📋 Consultez le rapport détaillé: {filepath}")

if __name__ == "__main__":
    main() 