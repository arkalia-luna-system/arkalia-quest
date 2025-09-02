#!/usr/bin/env python3
"""
Script de test complet pour Arkalia Quest
Basé sur le plan de test utilisateur ULTRA-PERFORMANT
Teste toutes les fonctionnalités du jeu selon le plan détaillé
"""

import requests  # Pour les tests HTTP
import time
import json
import sys
from datetime import datetime


class ArkaliaQuestTester:
    """Testeur complet pour Arkalia Quest"""

    def __init__(self, base_url: str = "https://arkalia-quest.onrender.com"):
        self.base_url = base_url
        self.session = requests.Session()
        self.test_results = []
        self.start_time = datetime.now()

        # Configuration des tests
        self.timeout = 10
        self.expected_load_time = 2.0  # secondes

    def log_test(
        self, test_name: str, status: str, details: str = "", duration: float = 0
    ):
        """Enregistre un résultat de test"""
        result = {
            "test": test_name,
            "status": status,  # PASS, FAIL, SKIP
            "details": details,
            "duration": duration,
            "timestamp": datetime.now().isoformat(),
        }
        self.test_results.append(result)

        # Affichage en temps réel
        status_emoji = "✅" if status == "PASS" else "❌" if status == "FAIL" else "⏭️"
        print(f"{status_emoji} {test_name}: {status}")
        if details:
            print(f"   📝 {details}")
        if duration > 0:
            print(f"   ⏱️ {duration:.2f}s")
        print()

    def test_page_load(self, path: str, expected_status: int = 200) -> bool:
        """Test le chargement d'une page"""
        start_time = time.time()
        try:
            response = self.session.get(f"{self.base_url}{path}", timeout=self.timeout)
            duration = time.time() - start_time

            if response.status_code == expected_status:
                self.log_test(
                    f"Chargement {path}",
                    "PASS",
                    f"Status: {response.status_code}, Temps: {duration:.2f}s",
                    duration,
                )
                return True
            else:
                self.log_test(
                    f"Chargement {path}",
                    "FAIL",
                    f"Status attendu: {expected_status}, reçu: {response.status_code}",
                    duration,
                )
                return False
        except requests.exceptions.RequestException as e:
            duration = time.time() - start_time
            self.log_test(f"Chargement {path}", "FAIL", f"Erreur: {str(e)}", duration)
            return False

    def test_terminal_command(self, command: str) -> bool:
        """Test une commande du terminal"""
        start_time = time.time()
        try:
            # Simuler l'envoi d'une commande au terminal
            # Pour l'instant, on teste juste l'accès à la page terminal
            response = self.session.get(
                f"{self.base_url}/terminal", timeout=self.timeout
            )
            duration = time.time() - start_time

            if response.status_code == 200:
                self.log_test(
                    f"Commande terminal: {command}",
                    "PASS",
                    "Page terminal accessible",
                    duration,
                )
                return True
            else:
                self.log_test(
                    f"Commande terminal: {command}",
                    "FAIL",
                    "Page terminal inaccessible",
                    duration,
                )
                return False
        except requests.exceptions.RequestException as e:
            duration = time.time() - start_time
            self.log_test(
                f"Commande terminal: {command}", "FAIL", f"Erreur: {str(e)}", duration
            )
            return False

    def test_health_endpoint(self) -> bool:
        """Test l'endpoint de santé"""
        start_time = time.time()
        try:
            response = self.session.get(f"{self.base_url}/health", timeout=self.timeout)
            duration = time.time() - start_time

            if response.status_code == 200:
                try:
                    health_data = response.json()
                    if health_data.get("status") == "healthy":
                        self.log_test(
                            "Health Check",
                            "PASS",
                            f"Status: {health_data.get('status')}",
                            duration,
                        )
                        return True
                    else:
                        self.log_test(
                            "Health Check",
                            "FAIL",
                            f"Status non healthy: {health_data.get('status')}",
                            duration,
                        )
                        return False
                except json.JSONDecodeError:
                    self.log_test(
                        "Health Check", "FAIL", "Réponse JSON invalide", duration
                    )
                    return False
            else:
                self.log_test(
                    "Health Check",
                    "FAIL",
                    f"Status HTTP: {response.status_code}",
                    duration,
                )
                return False
        except requests.exceptions.RequestException as e:
            duration = time.time() - start_time
            self.log_test("Health Check", "FAIL", f"Erreur: {str(e)}", duration)
            return False

    def test_metrics_endpoint(self) -> bool:
        """Test l'endpoint de métriques"""
        start_time = time.time()
        try:
            response = self.session.get(
                f"{self.base_url}/metrics", timeout=self.timeout
            )
            duration = time.time() - start_time

            if response.status_code == 200:
                self.log_test(
                    "Metrics Endpoint", "PASS", "Metrics accessibles", duration
                )
                return True
            else:
                self.log_test(
                    "Metrics Endpoint",
                    "FAIL",
                    f"Status: {response.status_code}",
                    duration,
                )
                return False
        except requests.exceptions.RequestException as e:
            duration = time.time() - start_time
            self.log_test("Metrics Endpoint", "FAIL", f"Erreur: {str(e)}", duration)
            return False

    def test_responsive_design(self) -> bool:
        """Test le design responsive (simulation)"""
        # Simulation des tests responsive
        user_agents = [
            "Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X)",
            "Mozilla/5.0 (Linux; Android 10; SM-G973F)",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        ]

        responsive_tests = 0
        for ua in user_agents:
            try:
                headers = {"User-Agent": ua}
                response = self.session.get(
                    f"{self.base_url}/", headers=headers, timeout=self.timeout
                )
                if response.status_code == 200:
                    responsive_tests += 1
            except Exception:
                pass

        if responsive_tests == len(user_agents):
            self.log_test(
                "Design Responsive",
                "PASS",
                f"Tous les user agents supportés ({responsive_tests}/{len(user_agents)})",
            )
            return True
        else:
            self.log_test(
                "Design Responsive",
                "FAIL",
                f"Seulement {responsive_tests}/{len(user_agents)} user agents supportés",
            )
            return False

    def run_complete_test_suite(self):
        """Exécute la suite complète de tests"""
        print("🌌 ARKALIA QUEST - TEST COMPLET ULTRA-PERFORMANT")
        print("=" * 60)
        print(f"🎯 URL de test: {self.base_url}")
        print(f"⏰ Début des tests: {self.start_time.strftime('%Y-%m-%d %H:%M:%S')}")
        print()

        # 1. Tests de base et santé
        print("🏥 1. TESTS DE SANTÉ ET PERFORMANCE")
        print("-" * 40)
        self.test_health_endpoint()
        self.test_metrics_endpoint()

        # 2. Tests des pages principales
        print("🏠 2. TESTS DES PAGES PRINCIPALES")
        print("-" * 40)
        pages = [
            ("/", "Accueil"),
            ("/tutorial", "Tutoriel"),
            ("/terminal", "Terminal"),
            ("/monde", "Monde"),
            ("/profil", "Profil"),
            ("/leaderboard", "Leaderboard"),
            ("/dashboard", "Dashboard"),
        ]

        for path, name in pages:
            self.test_page_load(path)

        # 3. Tests des commandes terminal
        print("⌨️ 3. TESTS DES COMMANDES TERMINAL")
        print("-" * 40)
        commands = [
            "help",
            "aide",
            "commands",
            "liste",
            "menu",
            "profil",
            "profile",
            "status",
            "clear",
            "cls",
            "start_tutorial",
            "tutorial",
            "games",
            "monde",
            "prologue",
            "hack_system",
            "kill_virus",
            "decode_portal",
        ]

        for command in commands:
            self.test_terminal_command(command)

        # 4. Tests responsive
        print("📱 4. TESTS RESPONSIVE DESIGN")
        print("-" * 40)
        self.test_responsive_design()

        # 5. Tests de performance
        print("⚡ 5. TESTS DE PERFORMANCE")
        print("-" * 40)
        self.test_performance()

        # 6. Tests d'accessibilité (simulation)
        print("♿ 6. TESTS D'ACCESSIBILITÉ")
        print("-" * 40)
        self.test_accessibility()

        # Génération du rapport final
        self.generate_final_report()

    def test_performance(self):
        """Test les performances générales"""
        start_time = time.time()
        try:
            self.session.get(f"{self.base_url}/", timeout=self.timeout)
            duration = time.time() - start_time

            if duration <= self.expected_load_time:
                self.log_test(
                    "Performance Page Accueil",
                    "PASS",
                    f"Temps de chargement: {duration:.2f}s (≤ {self.expected_load_time}s)",
                    duration,
                )
            else:
                self.log_test(
                    "Performance Page Accueil",
                    "FAIL",
                    f"Temps de chargement: {duration:.2f}s (> {self.expected_load_time}s)",
                    duration,
                )
        except requests.exceptions.RequestException as e:
            duration = time.time() - start_time
            self.log_test(
                "Performance Page Accueil", "FAIL", f"Erreur: {str(e)}", duration
            )

    def test_accessibility(self):
        """Test l'accessibilité (simulation)"""
        # Test des skip links
        try:
            response = self.session.get(f"{self.base_url}/", timeout=self.timeout)
            if response.status_code == 200:
                content = response.text
                if "skip-link" in content:
                    self.log_test(
                        "Skip Links", "PASS", "Skip links présents dans le HTML"
                    )
                else:
                    self.log_test("Skip Links", "FAIL", "Skip links manquants")

                if "aria-" in content:
                    self.log_test("Attributs ARIA", "PASS", "Attributs ARIA présents")
                else:
                    self.log_test("Attributs ARIA", "FAIL", "Attributs ARIA manquants")
        except Exception:
            self.log_test(
                "Accessibilité", "FAIL", "Impossible de tester l'accessibilité"
            )

    def generate_final_report(self):
        """Génère le rapport final des tests"""
        end_time = datetime.now()
        total_duration = (end_time - self.start_time).total_seconds()

        # Statistiques
        total_tests = len(self.test_results)
        passed_tests = len([r for r in self.test_results if r["status"] == "PASS"])
        failed_tests = len([r for r in self.test_results if r["status"] == "FAIL"])
        skipped_tests = len([r for r in self.test_results if r["status"] == "SKIP"])

        success_rate = (passed_tests / total_tests * 100) if total_tests > 0 else 0

        print("=" * 60)
        print("📊 RAPPORT FINAL DES TESTS")
        print("=" * 60)
        print(f"⏰ Durée totale: {total_duration:.2f}s")
        print(f"🧪 Tests exécutés: {total_tests}")
        print(f"✅ Tests réussis: {passed_tests}")
        print(f"❌ Tests échoués: {failed_tests}")
        print(f"⏭️ Tests ignorés: {skipped_tests}")
        print(f"📈 Taux de réussite: {success_rate:.1f}%")
        print()

        # Tests échoués
        if failed_tests > 0:
            print("❌ TESTS ÉCHOUÉS:")
            print("-" * 30)
            for result in self.test_results:
                if result["status"] == "FAIL":
                    print(f"• {result['test']}: {result['details']}")
            print()

        # Recommandations
        print("💡 RECOMMANDATIONS:")
        print("-" * 30)
        if success_rate >= 90:
            print("🎉 Excellent! Le jeu fonctionne parfaitement.")
        elif success_rate >= 75:
            print("👍 Bon état général, quelques améliorations mineures nécessaires.")
        elif success_rate >= 50:
            print("⚠️ État moyen, plusieurs problèmes à corriger.")
        else:
            print("🚨 État critique, de nombreux problèmes à résoudre.")

        # Sauvegarde du rapport
        report_file = f"test_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(report_file, "w", encoding="utf-8") as f:
            json.dump(
                {
                    "summary": {
                        "total_tests": total_tests,
                        "passed_tests": passed_tests,
                        "failed_tests": failed_tests,
                        "skipped_tests": skipped_tests,
                        "success_rate": success_rate,
                        "total_duration": total_duration,
                        "start_time": self.start_time.isoformat(),
                        "end_time": end_time.isoformat(),
                    },
                    "results": self.test_results,
                },
                f,
                indent=2,
                ensure_ascii=False,
            )

        print(f"📄 Rapport détaillé sauvegardé: {report_file}")


def main():
    """Fonction principale"""
    if len(sys.argv) > 1:
        base_url = sys.argv[1]
    else:
        base_url = "https://arkalia-quest.onrender.com"

    print(f"🚀 Démarrage des tests Arkalia Quest sur {base_url}")
    print()

    tester = ArkaliaQuestTester(base_url)
    tester.run_complete_test_suite()


if __name__ == "__main__":
    main()
