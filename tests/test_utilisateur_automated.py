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


class TestUtilisateurAutomated:
    """Classe pour les tests automatisés de validation utilisateur"""

    def __init__(self):
        self.results = {
            "timestamp": datetime.now().isoformat(),
            "tests": {},
            "summary": {},
        }

    def test_interface_responsive(self):
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

        self.results["tests"]["responsive"] = {
            "status": "pass" if responsive_ok else "fail",
            "details": (
                "Fichiers CSS responsive présents"
                if responsive_ok
                else "Fichiers CSS manquants"
            ),
        }
        return responsive_ok

    def test_accessibility(self):
        """Test des fonctionnalités d'accessibilité"""
        print("♿ Test d'accessibilité...")

        # Vérifier les fichiers d'accessibilité
        accessibility_files = [
            "static/css/accessibility.css",
            "static/js/accessibility.js",
        ]

        accessibility_ok = True
        for file in accessibility_files:
            if not os.path.exists(file):
                print(f"❌ {file} manquant")
                accessibility_ok = False
            else:
                print(f"✅ {file} présent")

        # Vérifier le contenu du fichier CSS d'accessibilité
        if os.path.exists("static/css/accessibility.css"):
            with open("static/css/accessibility.css", "r") as f:
                content = f.read()
                if "contrast" in content.lower() and "focus" in content.lower():
                    print("✅ Styles d'accessibilité détectés")
                else:
                    print("⚠️ Styles d'accessibilité limités")
                    accessibility_ok = False

        self.results["tests"]["accessibility"] = {
            "status": "pass" if accessibility_ok else "fail",
            "details": (
                "Fonctionnalités d'accessibilité présentes"
                if accessibility_ok
                else "Fonctionnalités d'accessibilité manquantes"
            ),
        }
        return accessibility_ok

    def test_performance_files(self):
        """Test de la performance des fichiers"""
        print("⚡ Test de performance...")

        # Vérifier la taille des fichiers principaux
        files_to_check = [
            "static/js/mini-games-interface.js",
            "static/css/arkalia-luna-vision.css",
            "static/js/terminal.js",
        ]

        performance_ok = True
        for file_path in files_to_check:
            if os.path.exists(file_path):
                size = os.path.getsize(file_path)
                size_kb = size / 1024
                print(f"📊 {file_path}: {size_kb:.1f} KB")

                # Vérifier que les fichiers ne sont pas trop lourds
                if size_kb > 100:  # Plus de 100KB
                    print(f"⚠️ {file_path} est assez lourd ({size_kb:.1f} KB)")
                else:
                    print(f"✅ {file_path} taille acceptable")
            else:
                print(f"❌ {file_path} manquant")
                performance_ok = False

        self.results["tests"]["performance"] = {
            "status": "pass" if performance_ok else "fail",
            "details": (
                "Fichiers de taille acceptable"
                if performance_ok
                else "Problèmes de taille de fichiers"
            ),
        }
        return performance_ok

    def test_content_quality(self):
        """Test de la qualité du contenu"""
        print("📚 Test de qualité du contenu...")

        # Vérifier les missions
        missions_dir = "data/missions"
        missions_ok = True

        if os.path.exists(missions_dir):
            mission_files = [f for f in os.listdir(missions_dir) if f.endswith(".json")]
            print(f"📋 {len(mission_files)} missions trouvées")

            for mission_file in mission_files:
                try:
                    with open(
                        os.path.join(missions_dir, mission_file), "r", encoding="utf-8"
                    ) as f:
                        mission = json.load(f)

                    # Vérifier la structure de la mission
                    required_fields = [
                        "id",
                        "title",
                        "description",
                        "difficulty",
                        "steps",
                    ]
                    for field in required_fields:
                        if field not in mission:
                            print(f"❌ {mission_file}: champ '{field}' manquant")
                            missions_ok = False

                    if missions_ok:
                        print(f"✅ {mission_file}: structure correcte")

                except Exception as e:
                    print(f"❌ Erreur lecture {mission_file}: {e}")
                    missions_ok = False
        else:
            print("❌ Dossier missions manquant")
            missions_ok = False

        # Vérifier les badges
        badges_ok = True
        if os.path.exists("data/badges_secrets.json"):
            try:
                with open("data/badges_secrets.json", "r", encoding="utf-8") as f:
                    badges = json.load(f)

                if "badges_secrets" in badges:
                    badge_count = len(badges["badges_secrets"])
                    print(f"🏆 {badge_count} badges trouvés")

                    if badge_count >= 10:
                        print("✅ Nombre de badges suffisant")
                    else:
                        print("⚠️ Peu de badges disponibles")
                        badges_ok = False
                else:
                    print("❌ Structure badges incorrecte")
                    badges_ok = False

            except Exception as e:
                print(f"❌ Erreur lecture badges: {e}")
                badges_ok = False
        else:
            print("❌ Fichier badges manquant")
            badges_ok = False

        content_ok = missions_ok and badges_ok
        self.results["tests"]["content_quality"] = {
            "status": "pass" if content_ok else "fail",
            "details": "Contenu de qualité" if content_ok else "Problèmes de contenu",
        }
        return content_ok

    def test_educational_value(self):
        """Test de la valeur éducative"""
        print("🎓 Test de valeur éducative...")

        try:
            from core.educational_games_engine import EducationalGamesEngine

            ege = EducationalGamesEngine()
            games = ege.get_available_games(1)

            print(f"🎮 {len(games)} mini-jeux disponibles")

            # Analyser les types de jeux
            game_types = {}
            for game in games:
                game_type = game.get("type", "unknown")
                game_types[game_type] = game_types.get(game_type, 0) + 1

            print("📊 Types de jeux:")
            for game_type, count in game_types.items():
                print(f"  - {game_type}: {count} jeux")

            # Vérifier la diversité
            if len(game_types) >= 3:
                print("✅ Diversité des types de jeux")
                educational_ok = True
            else:
                print("⚠️ Peu de diversité dans les types de jeux")
                educational_ok = False

            # Vérifier les points
            total_points = sum(game.get("points", 0) for game in games)
            print(f"🎯 Total points disponibles: {total_points}")

            if total_points >= 500:
                print("✅ Système de points équilibré")
            else:
                print("⚠️ Peu de points disponibles")
                educational_ok = False

        except Exception as e:
            print(f"❌ Erreur test éducatif: {e}")
            educational_ok = False

        self.results["tests"]["educational_value"] = {
            "status": "pass" if educational_ok else "fail",
            "details": (
                "Valeur éducative élevée"
                if educational_ok
                else "Valeur éducative limitée"
            ),
        }
        return educational_ok

    def run_all_tests(self):
        """Exécute tous les tests automatisés"""
        print("🚀 TESTS AUTOMATISÉS DE VALIDATION UTILISATEUR")
        print("=" * 60)

        tests = [
            ("Interface Responsive", self.test_interface_responsive),
            ("Accessibilité", self.test_accessibility),
            ("Performance", self.test_performance_files),
            ("Qualité du Contenu", self.test_content_quality),
            ("Valeur Éducative", self.test_educational_value),
        ]

        results = []
        for test_name, test_func in tests:
            print(f"\n🔍 {test_name}...")
            try:
                result = test_func()
                results.append(result)
                print(
                    f"{'✅' if result else '❌'} {test_name}: {'PASS' if result else 'FAIL'}"
                )
            except Exception as e:
                print(f"💥 Erreur dans {test_name}: {e}")
                results.append(False)

        # Résumé
        passed = sum(results)
        total = len(results)

        print("\n" + "=" * 60)
        print("📊 RÉSULTATS DES TESTS AUTOMATISÉS:")
        print(f"✅ Tests réussis: {passed}/{total}")
        print(f"❌ Tests échoués: {total - passed}/{total}")

        self.results["summary"] = {
            "total_tests": total,
            "passed_tests": passed,
            "failed_tests": total - passed,
            "success_rate": (passed / total) * 100 if total > 0 else 0,
        }

        if passed == total:
            print("\n🎉 TOUS LES TESTS AUTOMATISÉS SONT PASSÉS !")
            print("✅ Le jeu est prêt pour les tests utilisateur manuels")
        else:
            print(f"\n⚠️ {total - passed} test(s) ont échoué")
            print("🔧 Des corrections sont nécessaires avant les tests utilisateur")

        return passed == total

    def save_report(self, filename="test_utilisateur_automated_report.json"):
        """Sauvegarde le rapport de test"""
        report_path = os.path.join("tests", "reports", filename)
        os.makedirs(os.path.dirname(report_path), exist_ok=True)

        with open(report_path, "w", encoding="utf-8") as f:
            json.dump(self.results, f, indent=2, ensure_ascii=False)

        print(f"\n📄 Rapport sauvegardé: {report_path}")


def main():
    """Fonction principale"""
    tester = TestUtilisateurAutomated()
    success = tester.run_all_tests()
    tester.save_report()

    return 0 if success else 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
