#!/usr/bin/env python3
"""
Script de test des commandes et missions d'Arkalia Quest
Teste spécifiquement les commandes du terminal et les missions du jeu
"""

import json
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import requests

# Constantes
EXCELLENT_RATE = 80
GOOD_RATE = 60
MEDIUM_RATE = 50
EXCELLENT_SUMMARY_RATE = 90
GOOD_SUMMARY_RATE = 75


class ArkaliaQuestCommandsTester:
    """Testeur des commandes et missions d'Arkalia Quest"""

    def __init__(self, base_url: str = "https://arkalia-quest.onrender.com"):
        self.base_url = base_url
        self.session = requests.Session()
        self.test_results = []
        self.start_time = datetime.now()

        # Configuration des tests
        self.timeout = 10

        # Commandes à tester
        self.basic_commands = [
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
        ]

        self.tutorial_commands = ["start_tutorial", "tutorial", "tuto"]

        self.game_commands = ["games", "play_game", "game_stats", "daily_challenges"]

        self.story_commands = [
            "prologue",
            "acte_1",
            "acte_2",
            "acte_3",
            "acte_4",
            "acte_5",
            "acte_6",
            "epilogue",
        ]

        self.action_commands = [
            "hack_system",
            "kill_virus",
            "find_shadow",
            "challenge_corp",
            "decode_portal",
            "hacker_coffre",
            "boss_final",
        ]

        self.luna_commands = [
            "luna_contact",
            "luna_emotion",
            "luna_help",
            "luna_status",
        ]

        self.navigation_commands = ["monde", "world", "explorer", "naviguer"]

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

        # status_emoji = "✅" if status == "PASS" else "❌" if status == "FAIL" else "⏭️"
        # game_logger.info(f"{status_emoji} {test_name}: {status}")
        if details:
            game_logger.info(f"   📝 {details}")
        if duration > 0:
            game_logger.info(f"   ⏱️ {duration:.2f}s")
        # print()

    def test_command_availability(self, command: str) -> bool:
        """Test la disponibilité d'une commande"""
        start_time = time.time()
        try:
            # Tester l'accès à la page terminal
            response = self.session.get(
                f"{self.base_url}/terminal", timeout=self.timeout
            )
            duration = time.time() - start_time

            if response.status_code == 200:
                content = response.text

                # Vérifier si la commande est mentionnée dans le contenu
                command_found = (
                    command.lower() in content.lower()
                    or f'"{command}"' in content
                    or f"'{command}'" in content
                )

                if command_found:
                    self.log_test(
                        f"Commande: {command}",
                        "PASS",
                        "Commande trouvée dans le terminal",
                        duration,
                    )
                    return True
                self.log_test(
                    f"Commande: {command}",
                    "FAIL",
                    "Commande non trouvée dans le terminal",
                    duration,
                )
                return False
            self.log_test(
                f"Commande: {command}",
                "FAIL",
                f"Page terminal inaccessible: {response.status_code}",
                duration,
            )
            return False
        except requests.exceptions.RequestException as e:
            duration = time.time() - start_time
            self.log_test(f"Commande: {command}", "FAIL", f"Erreur: {e!s}", duration)
            return False

    def test_mission_progression(self) -> bool:
        """Test la progression des missions"""
        start_time = time.time()
        try:
            response = self.session.get(f"{self.base_url}/profil", timeout=self.timeout)
            duration = time.time() - start_time

            if response.status_code == 200:
                content = response.text

                # Vérifier les éléments de progression
                progression_elements = [
                    "mission" in content.lower(),
                    "progression" in content.lower() or "progress" in content.lower(),
                    "niveau" in content.lower() or "level" in content.lower(),
                    "badge" in content.lower(),
                    "score" in content.lower() or "point" in content.lower(),
                ]

                elements_found = sum(progression_elements)

                if elements_found >= 3:
                    self.log_test(
                        "Progression Missions",
                        "PASS",
                        f"Éléments progression trouvés: {elements_found}/5",
                        duration,
                    )
                    return True
                self.log_test(
                    "Progression Missions",
                    "FAIL",
                    f"Éléments progression manquants: {elements_found}/5",
                    duration,
                )
                return False
            self.log_test(
                "Progression Missions",
                "FAIL",
                f"Page profil inaccessible: {response.status_code}",
                duration,
            )
            return False
        except requests.exceptions.RequestException as e:
            duration = time.time() - start_time
            self.log_test("Progression Missions", "FAIL", f"Erreur: {e!s}", duration)
            return False

    def test_leaderboard_functionality(self) -> bool:
        """Test la fonctionnalité du leaderboard"""
        start_time = time.time()
        try:
            response = self.session.get(
                f"{self.base_url}/leaderboard", timeout=self.timeout
            )
            duration = time.time() - start_time

            if response.status_code == 200:
                content = response.text

                # Vérifier les éléments du leaderboard
                leaderboard_elements = [
                    "leaderboard" in content.lower() or "classement" in content.lower(),
                    "score" in content.lower() or "point" in content.lower(),
                    "rang" in content.lower() or "rank" in content.lower(),
                    "utilisateur" in content.lower() or "user" in content.lower(),
                ]

                elements_found = sum(leaderboard_elements)

                if elements_found >= 2:
                    self.log_test(
                        "Fonctionnalité Leaderboard",
                        "PASS",
                        f"Éléments leaderboard trouvés: {elements_found}/4",
                        duration,
                    )
                    return True
                self.log_test(
                    "Fonctionnalité Leaderboard",
                    "FAIL",
                    f"Éléments leaderboard manquants: {elements_found}/4",
                    duration,
                )
                return False
            self.log_test(
                "Fonctionnalité Leaderboard",
                "FAIL",
                f"Page leaderboard inaccessible: {response.status_code}",
                duration,
            )
            return False
        except requests.exceptions.RequestException as e:
            duration = time.time() - start_time
            self.log_test(
                "Fonctionnalité Leaderboard", "FAIL", f"Erreur: {e!s}", duration
            )
            return False

    def test_educational_games(self) -> bool:
        """Test les jeux éducatifs"""
        start_time = time.time()
        try:
            response = self.session.get(f"{self.base_url}/", timeout=self.timeout)
            duration = time.time() - start_time

            if response.status_code == 200:
                content = response.text

                # Vérifier les éléments des jeux éducatifs
                game_elements = [
                    "jeu" in content.lower() or "game" in content.lower(),
                    "éducatif" in content.lower() or "educational" in content.lower(),
                    "mini-jeu" in content.lower() or "minigame" in content.lower(),
                    "logique" in content.lower() or "logic" in content.lower(),
                    "cybersécurité" in content.lower()
                    or "cybersecurity" in content.lower(),
                ]

                elements_found = sum(game_elements)

                if elements_found >= 3:
                    self.log_test(
                        "Jeux Éducatifs",
                        "PASS",
                        f"Éléments jeux trouvés: {elements_found}/5",
                        duration,
                    )
                    return True
                self.log_test(
                    "Jeux Éducatifs",
                    "FAIL",
                    f"Éléments jeux manquants: {elements_found}/5",
                    duration,
                )
                return False
            self.log_test(
                "Jeux Éducatifs",
                "FAIL",
                f"Page inaccessible: {response.status_code}",
                duration,
            )
            return False
        except requests.exceptions.RequestException as e:
            duration = time.time() - start_time
            self.log_test("Jeux Éducatifs", "FAIL", f"Erreur: {e!s}", duration)
            return False

    def test_luna_ai_interaction(self) -> bool:
        """Test l'interaction avec l'IA LUNA"""
        start_time = time.time()
        try:
            response = self.session.get(f"{self.base_url}/", timeout=self.timeout)
            duration = time.time() - start_time

            if response.status_code == 200:
                content = response.text

                # Vérifier les éléments de LUNA
                luna_elements = [
                    "luna" in content.lower(),
                    "ia" in content.lower() or "ai" in content.lower(),
                    "émotion" in content.lower() or "emotion" in content.lower(),
                    "assistant" in content.lower(),
                    "guide" in content.lower(),
                ]

                elements_found = sum(luna_elements)

                if elements_found >= 3:
                    self.log_test(
                        "Interaction LUNA IA",
                        "PASS",
                        f"Éléments LUNA trouvés: {elements_found}/5",
                        duration,
                    )
                    return True
                self.log_test(
                    "Interaction LUNA IA",
                    "FAIL",
                    f"Éléments LUNA manquants: {elements_found}/5",
                    duration,
                )
                return False
            self.log_test(
                "Interaction LUNA IA",
                "FAIL",
                f"Page inaccessible: {response.status_code}",
                duration,
            )
            return False
        except requests.exceptions.RequestException as e:
            duration = time.time() - start_time
            self.log_test("Interaction LUNA IA", "FAIL", f"Erreur: {e!s}", duration)
            return False

    def test_game_objectives(self) -> bool:
        """Test les objectifs du jeu"""
        start_time = time.time()
        try:
            response = self.session.get(f"{self.base_url}/", timeout=self.timeout)
            duration = time.time() - start_time

            if response.status_code == 200:
                content = response.text

                # Vérifier les objectifs du jeu
                objective_elements = [
                    "hacker" in content.lower(),
                    "aventure" in content.lower() or "adventure" in content.lower(),
                    "mission" in content.lower(),
                    "objectif" in content.lower() or "goal" in content.lower(),
                    "découvrir" in content.lower() or "discover" in content.lower(),
                ]

                elements_found = sum(objective_elements)

                if elements_found >= 3:
                    self.log_test(
                        "Objectifs du Jeu",
                        "PASS",
                        f"Objectifs trouvés: {elements_found}/5",
                        duration,
                    )
                    return True
                self.log_test(
                    "Objectifs du Jeu",
                    "FAIL",
                    f"Objectifs manquants: {elements_found}/5",
                    duration,
                )
                return False
            self.log_test(
                "Objectifs du Jeu",
                "FAIL",
                f"Page inaccessible: {response.status_code}",
                duration,
            )
            return False
        except requests.exceptions.RequestException as e:
            duration = time.time() - start_time
            self.log_test("Objectifs du Jeu", "FAIL", f"Erreur: {e!s}", duration)
            return False

    def run_commands_test_suite(self):
        """Exécute la suite de tests des commandes"""
        # game_logger.info(r"🌌 ARKALIA QUEST - TESTS COMMANDES ET MISSIONS")
        # print("=" * 60)
        # game_logger.info(f"🎯 URL de test: {self.base_url}")
        # print(f"⏰ Début des tests: {self.start_time.strftime('%Y-%m-%d %H:%M:%S')}")
        # print()

        # Tests des commandes de base
        # game_logger.info(r"⌨️ 1. TESTS COMMANDES DE BASE")
        # print("-" * 40)
        for command in self.basic_commands:
            self.test_command_availability(command)

        # Tests des commandes tutoriel
        # game_logger.info(r"🎯 2. TESTS COMMANDES TUTORIEL")
        # print("-" * 40)
        for command in self.tutorial_commands:
            self.test_command_availability(command)

        # Tests des commandes de jeux
        # game_logger.info(r"🎮 3. TESTS COMMANDES JEUX")
        # print("-" * 40)
        for command in self.game_commands:
            self.test_command_availability(command)

        # Tests des commandes d'histoire
        # game_logger.info(r"📖 4. TESTS COMMANDES HISTOIRE")
        # print("-" * 40)
        for command in self.story_commands:
            self.test_command_availability(command)

        # Tests des commandes d'action
        # game_logger.info(r"⚡ 5. TESTS COMMANDES ACTION")
        # print("-" * 40)
        for command in self.action_commands:
            self.test_command_availability(command)

        # Tests des commandes LUNA
        # game_logger.info(r"🤖 6. TESTS COMMANDES LUNA")
        # print("-" * 40)
        for command in self.luna_commands:
            self.test_command_availability(command)

        # Tests des commandes de navigation
        # game_logger.info(r"🌍 7. TESTS COMMANDES NAVIGATION")
        # print("-" * 40)
        for command in self.navigation_commands:
            self.test_command_availability(command)

        # Tests des fonctionnalités du jeu
        # game_logger.info(r"🎯 8. TESTS FONCTIONNALITÉS JEU")
        # print("-" * 40)
        self.test_mission_progression()
        self.test_leaderboard_functionality()
        self.test_educational_games()
        self.test_luna_ai_interaction()
        self.test_game_objectives()

        # Génération du rapport final
        self.generate_final_report()

    def generate_final_report(self):
        """Génère le rapport final des tests"""
        end_time = datetime.now(timezone.utc)
        total_duration = (end_time - self.start_time).total_seconds()

        # Statistiques
        total_tests = len(self.test_results)
        passed_tests = len([r for r in self.test_results if r["status"] == "PASS"])
        failed_tests = len([r for r in self.test_results if r["status"] == "FAIL"])
        skipped_tests = len([r for r in self.test_results if r["status"] == "SKIP"])

        success_rate = (passed_tests / total_tests * 100) if total_tests > 0 else 0

        # print("=" * 60)
        # game_logger.info(r"📊 RAPPORT FINAL DES TESTS COMMANDES")
        # print("=" * 60)
        # game_logger.info(f"⏰ Durée totale: {total_duration:.2f}s")
        # game_logger.info(f"🧪 Tests exécutés: {total_tests}")
        # game_logger.info(f"✅ Tests réussis: {passed_tests}")
        # game_logger.info(f"❌ Tests échoués: {failed_tests}")
        # game_logger.info(f"⏭️ Tests ignorés: {skipped_tests}")
        # game_logger.info(f"📈 Taux de réussite: {success_rate:.1f}%")
        # print()

        # Analyse par catégorie de commandes
        command_categories = {
            "Commandes de Base": [
                r
                for r in self.test_results
                if any(cmd in r["test"] for cmd in self.basic_commands)
            ],
            "Commandes Tutoriel": [
                r
                for r in self.test_results
                if any(cmd in r["test"] for cmd in self.tutorial_commands)
            ],
            "Commandes Jeux": [
                r
                for r in self.test_results
                if any(cmd in r["test"] for cmd in self.game_commands)
            ],
            "Commandes Histoire": [
                r
                for r in self.test_results
                if any(cmd in r["test"] for cmd in self.story_commands)
            ],
            "Commandes Action": [
                r
                for r in self.test_results
                if any(cmd in r["test"] for cmd in self.action_commands)
            ],
            "Commandes LUNA": [
                r
                for r in self.test_results
                if any(cmd in r["test"] for cmd in self.luna_commands)
            ],
            "Commandes Navigation": [
                r
                for r in self.test_results
                if any(cmd in r["test"] for cmd in self.navigation_commands)
            ],
            "Fonctionnalités": [
                r
                for r in self.test_results
                if not any(
                    cmd in r["test"]
                    for cmd in self.basic_commands
                    + self.tutorial_commands
                    + self.game_commands
                    + self.story_commands
                    + self.action_commands
                    + self.luna_commands
                    + self.navigation_commands
                )
            ],
        }

        # game_logger.info(r"📋 ANALYSE PAR CATÉGORIE:")
        # print("-" * 30)
        for category, tests in command_categories.items():
            if tests:
                passed = len([t for t in tests if t["status"] == "PASS"])
                total = len(tests)
                rate = (passed / total * 100) if total > 0 else 0

                if rate >= EXCELLENT_RATE:
                    game_logger.info(
                        f"✅ {category}: Excellent ({rate:.0f}% - {passed}/{total})"
                    )
                elif rate >= GOOD_RATE:
                    game_logger.info(
                        f"⚠️ {category}: À améliorer ({rate:.0f}% - {passed}/{total})"
                    )
                else:
                    game_logger.info(
                        f"❌ {category}: Problèmes majeurs ({rate:.0f}% - {passed}/{total})"
                    )

        # Tests échoués
        if failed_tests > 0:
            print()
            game_logger.info(r"❌ TESTS ÉCHOUÉS:")
            print("-" * 30)
            for result in self.test_results:
                if result["status"] == "FAIL":
                    print(f"• {result['test']}: {result['details']}")

        # Recommandations
        # print()
        # game_logger.info(r"💡 RECOMMANDATIONS:")
        # print("-" * 30)
        if success_rate >= EXCELLENT_SUMMARY_RATE:
            print(
                "🎉 Excellent! Toutes les commandes et fonctionnalités fonctionnent parfaitement.",
            )
        elif success_rate >= GOOD_SUMMARY_RATE:
            game_logger.info(r"👍 Bon état général, quelques commandes à vérifier.")
        elif success_rate >= MEDIUM_RATE:
            game_logger.info(
                r"⚠️ État moyen, plusieurs commandes nécessitent des corrections."
            )
        else:
            game_logger.info(
                r"🚨 État critique, de nombreuses commandes ne fonctionnent pas."
            )

        # Sauvegarde du rapport
        report_file = f"commands_test_report_{datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S')}.json"
        with Path(report_file).open("w", encoding="utf-8") as f:
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
                    "categories": {k: len(v) for k, v in command_categories.items()},
                },
                f,
                indent=2,
                ensure_ascii=False,
            )

        # game_logger.info(f"📄 Rapport détaillé sauvegardé: {report_file}")


def main():
    """Fonction principale"""
    base_url = (
        sys.argv[1] if len(sys.argv) > 1 else "https://arkalia-quest.onrender.com"
    )

    # game_logger.info(f"🚀 Démarrage des tests commandes Arkalia Quest sur {base_url}")
    # print()

    tester = ArkaliaQuestCommandsTester(base_url)
    tester.run_commands_test_suite()


if __name__ == "__main__":
    main()
