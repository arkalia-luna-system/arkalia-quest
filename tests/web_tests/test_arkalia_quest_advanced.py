#!/usr/bin/env python3
"""
Script de test avancé pour Arkalia Quest
Teste les fonctionnalités spécifiques du jeu selon le plan de test utilisateur
"""

import json
import os
import re
import sys
import time
from datetime import datetime

import requests

# Ajouter le répertoire racine au path
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, project_root)

from utils.logger import GameLogger

# Initialiser le logger
game_logger = GameLogger()


class ArkaliaQuestAdvancedTester:
    """Testeur avancé pour les fonctionnalités spécifiques d'Arkalia Quest"""

    def __init__(self, base_url: str = "https://arkalia-quest.onrender.com"):
        self.base_url = base_url
        self.session = requests.Session()
        self.test_results = []
        self.start_time = datetime.now()

        # Configuration des tests
        self.timeout = 10

    def log_test(
        self, test_name: str, status: str, details: str = "", duration: float = 0
    ):
        """Enregistre un résultat de test"""
        result = {
            "test": test_name,
            "status": status,
            "details": details,
            "duration": duration,
            "timestamp": datetime.now().isoformat(),
        }
        self.test_results.append(result)

        status_emoji = "✅" if status == "PASS" else "❌" if status == "FAIL" else "⏭️"
        game_logger.info(f"{status_emoji} {test_name}: {status}")
        if details:
            game_logger.info(f"   📝 {details}")
        if duration > 0:
            game_logger.info(f"   ⏱️ {duration:.2f}s")
        print()

    def test_design_matrix_colors(self) -> bool:
        """Test la présence des couleurs Matrix (#00ff00)"""
        start_time = time.time()
        try:
            response = self.session.get(f"{self.base_url}/", timeout=self.timeout)
            duration = time.time() - start_time

            if response.status_code == 200:
                content = response.text
                # Rechercher les couleurs Matrix
                matrix_colors = re.findall(
                    r"#00ff00|#0f0|rgb\(0,\s*255,\s*0\)",
                    content,
                    re.IGNORECASE,
                )

                if matrix_colors:
                    self.log_test(
                        "Design Matrix (#00ff00)",
                        "PASS",
                        f"Couleurs Matrix trouvées: {len(matrix_colors)}",
                        duration,
                    )
                    return True
                self.log_test(
                    "Design Matrix (#00ff00)",
                    "FAIL",
                    "Aucune couleur Matrix (#00ff00) trouvée",
                    duration,
                )
                return False
            self.log_test(
                "Design Matrix (#00ff00)",
                "FAIL",
                f"Page inaccessible: {response.status_code}",
                duration,
            )
            return False
        except requests.exceptions.RequestException as e:
            duration = time.time() - start_time
            self.log_test("Design Matrix (#00ff00)", "FAIL", f"Erreur: {e!s}", duration)
            return False

    def test_tutorial_functionality(self) -> bool:
        """Test les fonctionnalités du tutoriel"""
        start_time = time.time()
        try:
            response = self.session.get(
                f"{self.base_url}/tutorial", timeout=self.timeout
            )
            duration = time.time() - start_time

            if response.status_code == 200:
                content = response.text

                # Vérifier les éléments du tutoriel
                tutorial_elements = [
                    "tutoriel" in content.lower(),
                    "étape" in content.lower() or "step" in content.lower(),
                    "suivant" in content.lower() or "next" in content.lower(),
                    "progression" in content.lower(),
                ]

                elements_found = sum(tutorial_elements)

                if elements_found >= 2:
                    self.log_test(
                        "Fonctionnalités Tutoriel",
                        "PASS",
                        f"Éléments tutoriel trouvés: {elements_found}/4",
                        duration,
                    )
                    return True
                self.log_test(
                    "Fonctionnalités Tutoriel",
                    "FAIL",
                    f"Peu d'éléments tutoriel: {elements_found}/4",
                    duration,
                )
                return False
            self.log_test(
                "Fonctionnalités Tutoriel",
                "FAIL",
                f"Page tutoriel inaccessible: {response.status_code}",
                duration,
            )
            return False
        except requests.exceptions.RequestException as e:
            duration = time.time() - start_time
            self.log_test(
                "Fonctionnalités Tutoriel", "FAIL", f"Erreur: {e!s}", duration
            )
            return False

    def test_terminal_commands(self) -> bool:
        """Test les commandes du terminal"""
        start_time = time.time()
        try:
            response = self.session.get(
                f"{self.base_url}/terminal", timeout=self.timeout
            )
            duration = time.time() - start_time

            if response.status_code == 200:
                content = response.text

                # Vérifier les éléments du terminal
                terminal_elements = [
                    "terminal" in content.lower(),
                    "commande" in content.lower() or "command" in content.lower(),
                    "input" in content.lower() or "textarea" in content.lower(),
                    "help" in content.lower() or "aide" in content.lower(),
                ]

                elements_found = sum(terminal_elements)

                if elements_found >= 3:
                    self.log_test(
                        "Fonctionnalités Terminal",
                        "PASS",
                        f"Éléments terminal trouvés: {elements_found}/4",
                        duration,
                    )
                    return True
                self.log_test(
                    "Fonctionnalités Terminal",
                    "FAIL",
                    f"Éléments terminal manquants: {elements_found}/4",
                    duration,
                )
                return False
            self.log_test(
                "Fonctionnalités Terminal",
                "FAIL",
                f"Page terminal inaccessible: {response.status_code}",
                duration,
            )
            return False
        except requests.exceptions.RequestException as e:
            duration = time.time() - start_time
            self.log_test(
                "Fonctionnalités Terminal", "FAIL", f"Erreur: {e!s}", duration
            )
            return False

    def test_world_progression(self) -> bool:
        """Test la progression dans le monde"""
        start_time = time.time()
        try:
            response = self.session.get(f"{self.base_url}/monde", timeout=self.timeout)
            duration = time.time() - start_time

            if response.status_code == 200:
                content = response.text

                # Vérifier les éléments de progression
                progression_elements = [
                    "monde" in content.lower() or "world" in content.lower(),
                    "progression" in content.lower() or "progress" in content.lower(),
                    "barre" in content.lower() or "bar" in content.lower(),
                    "pourcentage" in content.lower() or "%" in content,
                ]

                elements_found = sum(progression_elements)

                if elements_found >= 2:
                    self.log_test(
                        "Progression Monde",
                        "PASS",
                        f"Éléments progression trouvés: {elements_found}/4",
                        duration,
                    )
                    return True
                self.log_test(
                    "Progression Monde",
                    "FAIL",
                    f"Éléments progression manquants: {elements_found}/4",
                    duration,
                )
                return False
            self.log_test(
                "Progression Monde",
                "FAIL",
                f"Page monde inaccessible: {response.status_code}",
                duration,
            )
            return False
        except requests.exceptions.RequestException as e:
            duration = time.time() - start_time
            self.log_test("Progression Monde", "FAIL", f"Erreur: {e!s}", duration)
            return False

    def test_dashboard_na_values(self) -> bool:
        """Test les valeurs N/A dans le dashboard"""
        start_time = time.time()
        try:
            response = self.session.get(
                f"{self.base_url}/dashboard", timeout=self.timeout
            )
            duration = time.time() - start_time

            if response.status_code == 200:
                content = response.text

                # Vérifier la présence de valeurs N/A
                na_values = [
                    "N/A" in content,
                    "n/a" in content.lower(),
                    "non disponible" in content.lower(),
                    "pas de données" in content.lower(),
                ]

                na_found = any(na_values)

                if na_found:
                    self.log_test(
                        "Valeurs N/A Dashboard",
                        "PASS",
                        "Valeurs N/A présentes dans le dashboard",
                        duration,
                    )
                    return True
                self.log_test(
                    "Valeurs N/A Dashboard",
                    "FAIL",
                    "Valeurs N/A manquantes dans le dashboard",
                    duration,
                )
                return False
            self.log_test(
                "Valeurs N/A Dashboard",
                "FAIL",
                f"Page dashboard inaccessible: {response.status_code}",
                duration,
            )
            return False
        except requests.exceptions.RequestException as e:
            duration = time.time() - start_time
            self.log_test("Valeurs N/A Dashboard", "FAIL", f"Erreur: {e!s}", duration)
            return False

    def test_audio_functionality(self) -> bool:
        """Test les fonctionnalités audio"""
        start_time = time.time()
        try:
            response = self.session.get(f"{self.base_url}/", timeout=self.timeout)
            duration = time.time() - start_time

            if response.status_code == 200:
                content = response.text

                # Vérifier les éléments audio
                audio_elements = [
                    "audio" in content.lower(),
                    "sound" in content.lower() or "son" in content.lower(),
                    "volume" in content.lower(),
                    "test audio" in content.lower() or "test_audio" in content.lower(),
                ]

                elements_found = sum(audio_elements)

                if elements_found >= 2:
                    self.log_test(
                        "Fonctionnalités Audio",
                        "PASS",
                        f"Éléments audio trouvés: {elements_found}/4",
                        duration,
                    )
                    return True
                self.log_test(
                    "Fonctionnalités Audio",
                    "FAIL",
                    f"Éléments audio manquants: {elements_found}/4",
                    duration,
                )
                return False
            self.log_test(
                "Fonctionnalités Audio",
                "FAIL",
                f"Page inaccessible: {response.status_code}",
                duration,
            )
            return False
        except requests.exceptions.RequestException as e:
            duration = time.time() - start_time
            self.log_test("Fonctionnalités Audio", "FAIL", f"Erreur: {e!s}", duration)
            return False

    def test_accessibility_features(self) -> bool:
        """Test les fonctionnalités d'accessibilité"""
        start_time = time.time()
        try:
            response = self.session.get(f"{self.base_url}/", timeout=self.timeout)
            duration = time.time() - start_time

            if response.status_code == 200:
                content = response.text

                # Vérifier les fonctionnalités d'accessibilité
                accessibility_features = [
                    "skip-link" in content,
                    "aria-" in content,
                    "role=" in content,
                    "alt=" in content,
                    "accessibility" in content.lower()
                    or "accessibilité" in content.lower(),
                ]

                features_found = sum(accessibility_features)

                if features_found >= 3:
                    self.log_test(
                        "Fonctionnalités Accessibilité",
                        "PASS",
                        f"Fonctionnalités accessibilité trouvées: {features_found}/5",
                        duration,
                    )
                    return True
                self.log_test(
                    "Fonctionnalités Accessibilité",
                    "FAIL",
                    f"Fonctionnalités accessibilité manquantes: {features_found}/5",
                    duration,
                )
                return False
            self.log_test(
                "Fonctionnalités Accessibilité",
                "FAIL",
                f"Page inaccessible: {response.status_code}",
                duration,
            )
            return False
        except requests.exceptions.RequestException as e:
            duration = time.time() - start_time
            self.log_test(
                "Fonctionnalités Accessibilité", "FAIL", f"Erreur: {e!s}", duration
            )
            return False

    def test_responsive_breakpoints(self) -> bool:
        """Test les breakpoints responsive"""
        start_time = time.time()
        try:
            response = self.session.get(f"{self.base_url}/", timeout=self.timeout)
            duration = time.time() - start_time

            if response.status_code == 200:
                content = response.text

                # Vérifier les breakpoints responsive
                breakpoints = [
                    "320px" in content,
                    "375px" in content,
                    "768px" in content,
                    "1024px" in content,
                    "1440px" in content,
                    "@media" in content,
                ]

                breakpoints_found = sum(breakpoints)

                if breakpoints_found >= 2:
                    self.log_test(
                        "Breakpoints Responsive",
                        "PASS",
                        f"Breakpoints trouvés: {breakpoints_found}/6",
                        duration,
                    )
                    return True
                self.log_test(
                    "Breakpoints Responsive",
                    "FAIL",
                    f"Breakpoints manquants: {breakpoints_found}/6",
                    duration,
                )
                return False
            self.log_test(
                "Breakpoints Responsive",
                "FAIL",
                f"Page inaccessible: {response.status_code}",
                duration,
            )
            return False
        except requests.exceptions.RequestException as e:
            duration = time.time() - start_time
            self.log_test("Breakpoints Responsive", "FAIL", f"Erreur: {e!s}", duration)
            return False

    def test_luna_ai_features(self) -> bool:
        """Test les fonctionnalités de l'IA LUNA"""
        start_time = time.time()
        try:
            response = self.session.get(f"{self.base_url}/", timeout=self.timeout)
            duration = time.time() - start_time

            if response.status_code == 200:
                content = response.text

                # Vérifier les fonctionnalités LUNA
                luna_features = [
                    "luna" in content.lower(),
                    "ia" in content.lower() or "ai" in content.lower(),
                    "émotion" in content.lower() or "emotion" in content.lower(),
                    "assistant" in content.lower(),
                ]

                features_found = sum(luna_features)

                if features_found >= 2:
                    self.log_test(
                        "Fonctionnalités LUNA IA",
                        "PASS",
                        f"Fonctionnalités LUNA trouvées: {features_found}/4",
                        duration,
                    )
                    return True
                self.log_test(
                    "Fonctionnalités LUNA IA",
                    "FAIL",
                    f"Fonctionnalités LUNA manquantes: {features_found}/4",
                    duration,
                )
                return False
            self.log_test(
                "Fonctionnalités LUNA IA",
                "FAIL",
                f"Page inaccessible: {response.status_code}",
                duration,
            )
            return False
        except requests.exceptions.RequestException as e:
            duration = time.time() - start_time
            self.log_test("Fonctionnalités LUNA IA", "FAIL", f"Erreur: {e!s}", duration)
            return False

    def run_advanced_test_suite(self):
        """Exécute la suite de tests avancés"""
        game_logger.info(r"🌌 ARKALIA QUEST - TESTS AVANCÉS FONCTIONNALITÉS")
        print("=" * 60)
        game_logger.info(f"🎯 URL de test: {self.base_url}")
        print(f"⏰ Début des tests: {self.start_time.strftime('%Y-%m-%d %H:%M:%S')}")
        print()

        # Tests des fonctionnalités spécifiques
        game_logger.info(r"🎨 1. TESTS DESIGN ET COULEURS")
        print("-" * 40)
        self.test_design_matrix_colors()

        game_logger.info(r"🎯 2. TESTS TUTORIEL")
        print("-" * 40)
        self.test_tutorial_functionality()

        game_logger.info(r"⌨️ 3. TESTS TERMINAL")
        print("-" * 40)
        self.test_terminal_commands()

        game_logger.info(r"🌍 4. TESTS MONDE ET PROGRESSION")
        print("-" * 40)
        self.test_world_progression()

        game_logger.info(r"📊 5. TESTS DASHBOARD")
        print("-" * 40)
        self.test_dashboard_na_values()

        game_logger.info(r"🔊 6. TESTS AUDIO")
        print("-" * 40)
        self.test_audio_functionality()

        game_logger.info(r"♿ 7. TESTS ACCESSIBILITÉ")
        print("-" * 40)
        self.test_accessibility_features()

        game_logger.info(r"📱 8. TESTS RESPONSIVE")
        print("-" * 40)
        self.test_responsive_breakpoints()

        game_logger.info(r"🤖 9. TESTS IA LUNA")
        print("-" * 40)
        self.test_luna_ai_features()

        # Génération du rapport final
        self.generate_final_report()

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
        game_logger.info(r"📊 RAPPORT FINAL DES TESTS AVANCÉS")
        print("=" * 60)
        game_logger.info(f"⏰ Durée totale: {total_duration:.2f}s")
        game_logger.info(f"🧪 Tests exécutés: {total_tests}")
        game_logger.info(f"✅ Tests réussis: {passed_tests}")
        game_logger.info(f"❌ Tests échoués: {failed_tests}")
        game_logger.info(f"⏭️ Tests ignorés: {skipped_tests}")
        game_logger.info(f"📈 Taux de réussite: {success_rate:.1f}%")
        print()

        # Tests échoués
        if failed_tests > 0:
            game_logger.info(r"❌ TESTS ÉCHOUÉS:")
            print("-" * 30)
            for result in self.test_results:
                if result["status"] == "FAIL":
                    print(f"• {result['test']}: {result['details']}")
            print()

        # Recommandations spécifiques
        game_logger.info(r"💡 RECOMMANDATIONS SPÉCIFIQUES:")
        print("-" * 30)

        # Analyser les résultats par catégorie
        categories = {
            "Design": [r for r in self.test_results if "Design" in r["test"]],
            "Tutoriel": [r for r in self.test_results if "Tutoriel" in r["test"]],
            "Terminal": [r for r in self.test_results if "Terminal" in r["test"]],
            "Monde": [r for r in self.test_results if "Monde" in r["test"]],
            "Dashboard": [r for r in self.test_results if "Dashboard" in r["test"]],
            "Audio": [r for r in self.test_results if "Audio" in r["test"]],
            "Accessibilité": [
                r for r in self.test_results if "Accessibilité" in r["test"]
            ],
            "Responsive": [r for r in self.test_results if "Responsive" in r["test"]],
            "LUNA": [r for r in self.test_results if "LUNA" in r["test"]],
        }

        for category, tests in categories.items():
            if tests:
                passed = len([t for t in tests if t["status"] == "PASS"])
                total = len(tests)
                rate = (passed / total * 100) if total > 0 else 0

                if rate >= 80:
                    game_logger.info(f"✅ {category}: Excellent ({rate:.0f}%)")
                elif rate >= 60:
                    game_logger.info(f"⚠️ {category}: À améliorer ({rate:.0f}%)")
                else:
                    game_logger.info(f"❌ {category}: Problèmes majeurs ({rate:.0f}%)")

        # Sauvegarde du rapport
        report_file = (
            f"advanced_test_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        )
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
                    "categories": {k: len(v) for k, v in categories.items()},
                },
                f,
                indent=2,
                ensure_ascii=False,
            )

        game_logger.info(f"📄 Rapport détaillé sauvegardé: {report_file}")


def main():
    """Fonction principale"""
    if len(sys.argv) > 1:
        base_url = sys.argv[1]
    else:
        base_url = "https://arkalia-quest.onrender.com"

    game_logger.info(f"🚀 Démarrage des tests avancés Arkalia Quest sur {base_url}")
    print()

    tester = ArkaliaQuestAdvancedTester(base_url)
    tester.run_advanced_test_suite()


if __name__ == "__main__":
    main()
