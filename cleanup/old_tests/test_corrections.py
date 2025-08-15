#!/usr/bin/env python3
"""
Script de test des corrections Arkalia Quest
Vérifie que toutes les erreurs ont été corrigées
"""

import json
from datetime import datetime

import requests


class CorrectionsTester:
    """Testeur des corrections d'Arkalia Quest"""

    def __init__(self, base_url="http://localhost:5001"):
        self.base_url = base_url
        self.results = []

    def test_page_profil(self):
        """Test de la page profil (erreur 500 corrigée)"""
        print("🔍 Test de la page profil...")
        try:
            response = requests.get(f"{self.base_url}/profil", timeout=5)
            success = response.status_code == 200
            self.results.append(
                {
                    "test": "Page Profil",
                    "success": success,
                    "status_code": response.status_code,
                    "error": None if success else f"Status {response.status_code}",
                }
            )
            print(f"✅ Page profil: {'SUCCÈS' if success else 'ÉCHEC'}")
            return success
        except Exception as e:
            self.results.append(
                {
                    "test": "Page Profil",
                    "success": False,
                    "status_code": None,
                    "error": str(e),
                }
            )
            print(f"❌ Page profil: ERREUR - {e}")
            return False

    def test_css_file(self):
        """Test du fichier CSS (erreur 404 corrigée)"""
        print("🔍 Test du fichier CSS...")
        try:
            response = requests.get(f"{self.base_url}/static/css/style.css", timeout=5)
            success = response.status_code == 200
            self.results.append(
                {
                    "test": "Fichier CSS",
                    "success": success,
                    "status_code": response.status_code,
                    "error": None if success else f"Status {response.status_code}",
                }
            )
            print(f"✅ Fichier CSS: {'SUCCÈS' if success else 'ÉCHEC'}")
            return success
        except Exception as e:
            self.results.append(
                {
                    "test": "Fichier CSS",
                    "success": False,
                    "status_code": None,
                    "error": str(e),
                }
            )
            print(f"❌ Fichier CSS: ERREUR - {e}")
            return False

    def test_api_leaderboard(self):
        """Test de l'API leaderboard (erreur 500 corrigée)"""
        print("🔍 Test de l'API leaderboard...")
        try:
            response = requests.get(f"{self.base_url}/api/leaderboard", timeout=5)
            success = response.status_code == 200
            if success:
                data = response.json()
                has_data = "top_players" in data and "statistics" in data
                success = has_data
            self.results.append(
                {
                    "test": "API Leaderboard",
                    "success": success,
                    "status_code": response.status_code,
                    "error": None if success else "Données manquantes",
                }
            )
            print(f"✅ API Leaderboard: {'SUCCÈS' if success else 'ÉCHEC'}")
            return success
        except Exception as e:
            self.results.append(
                {
                    "test": "API Leaderboard",
                    "success": False,
                    "status_code": None,
                    "error": str(e),
                }
            )
            print(f"❌ API Leaderboard: ERREUR - {e}")
            return False

    def test_command_hack_system(self):
        """Test de la commande hack_system (commande non reconnue corrigée)"""
        print("🔍 Test de la commande hack_system...")
        try:
            response = requests.post(
                f"{self.base_url}/commande", json={"commande": "hack_system"}, timeout=5
            )
            success = response.status_code == 200
            if success:
                data = response.json()
                command_success = data.get("reponse", {}).get("réussite", False)
                success = command_success
            self.results.append(
                {
                    "test": "Commande hack_system",
                    "success": success,
                    "status_code": response.status_code,
                    "error": None if success else "Commande non reconnue",
                }
            )
            print(f"✅ Commande hack_system: {'SUCCÈS' if success else 'ÉCHEC'}")
            return success
        except Exception as e:
            self.results.append(
                {
                    "test": "Commande hack_system",
                    "success": False,
                    "status_code": None,
                    "error": str(e),
                }
            )
            print(f"❌ Commande hack_system: ERREUR - {e}")
            return False

    def test_other_commands(self):
        """Test d'autres commandes de hacking"""
        commands = ["kill_virus", "find_shadow", "challenge_corp", "decode_portal"]
        print("🔍 Test des autres commandes de hacking...")

        for cmd in commands:
            try:
                response = requests.post(
                    f"{self.base_url}/commande", json={"commande": cmd}, timeout=5
                )
                success = response.status_code == 200
                if success:
                    data = response.json()
                    command_success = data.get("reponse", {}).get("réussite", False)
                    success = command_success

                self.results.append(
                    {
                        "test": f"Commande {cmd}",
                        "success": success,
                        "status_code": response.status_code,
                        "error": None if success else "Commande non reconnue",
                    }
                )
                print(f"✅ Commande {cmd}: {'SUCCÈS' if success else 'ÉCHEC'}")

            except Exception as e:
                self.results.append(
                    {
                        "test": f"Commande {cmd}",
                        "success": False,
                        "status_code": None,
                        "error": str(e),
                    }
                )
                print(f"❌ Commande {cmd}: ERREUR - {e}")

    def test_pages_accessibility(self):
        """Test de l'accessibilité des pages principales"""
        pages = ["/", "/terminal", "/monde", "/leaderboard"]
        print("🔍 Test de l'accessibilité des pages...")

        for page in pages:
            try:
                response = requests.get(f"{self.base_url}{page}", timeout=5)
                success = response.status_code == 200
                self.results.append(
                    {
                        "test": f"Page {page}",
                        "success": success,
                        "status_code": response.status_code,
                        "error": None if success else f"Status {response.status_code}",
                    }
                )
                print(f"✅ Page {page}: {'SUCCÈS' if success else 'ÉCHEC'}")

            except Exception as e:
                self.results.append(
                    {
                        "test": f"Page {page}",
                        "success": False,
                        "status_code": None,
                        "error": str(e),
                    }
                )
                print(f"❌ Page {page}: ERREUR - {e}")

    def run_all_tests(self):
        """Lance tous les tests"""
        print("🎮" + "=" * 60 + "🎮")
        print("🔧 TEST DES CORRECTIONS - ARKALIA QUEST")
        print("📅 " + datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        print("=" * 64)

        # Tests des erreurs critiques corrigées
        self.test_page_profil()
        self.test_css_file()
        self.test_api_leaderboard()
        self.test_command_hack_system()

        # Tests supplémentaires
        self.test_other_commands()
        self.test_pages_accessibility()

        # Résumé final
        self.generate_report()

    def generate_report(self):
        """Génère un rapport des tests"""
        print("\n" + "=" * 64)
        print("📊 RAPPORT DES TESTS")
        print("=" * 64)

        total_tests = len(self.results)
        successful_tests = sum(1 for r in self.results if r["success"])
        failed_tests = total_tests - successful_tests

        print(f"📈 Total des tests: {total_tests}")
        print(f"✅ Tests réussis: {successful_tests}")
        print(f"❌ Tests échoués: {failed_tests}")
        print(f"📊 Taux de succès: {(successful_tests/total_tests)*100:.1f}%")

        if failed_tests > 0:
            print("\n❌ TESTS ÉCHOUÉS:")
            for result in self.results:
                if not result["success"]:
                    print(f"  • {result['test']}: {result['error']}")

        print("\n✅ TESTS RÉUSSIS:")
        for result in self.results:
            if result["success"]:
                print(f"  • {result['test']}")

        # Sauvegarder le rapport
        report = {
            "timestamp": datetime.now().isoformat(),
            "summary": {
                "total_tests": total_tests,
                "successful_tests": successful_tests,
                "failed_tests": failed_tests,
                "success_rate": (successful_tests / total_tests) * 100,
            },
            "results": self.results,
        }

        with open("test_corrections_report.json", "w", encoding="utf-8") as f:
            json.dump(report, f, indent=2, ensure_ascii=False)

        print("\n📄 Rapport sauvegardé: test_corrections_report.json")

        if failed_tests == 0:
            print("\n🎉 TOUTES LES CORRECTIONS FONCTIONNENT PARFAITEMENT !")
        else:
            print(f"\n⚠️  {failed_tests} erreur(s) restante(s) à corriger.")


if __name__ == "__main__":
    tester = CorrectionsTester()
    tester.run_all_tests()
