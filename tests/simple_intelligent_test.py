#!/usr/bin/env python3
"""
🎮 Testeur Intelligent Simplifié - Arkalia Quest
Version adaptée pour macOS et tests rapides
"""

import json
import os
import sys
import time
from datetime import datetime

import requests

# Ajouter le répertoire racine au path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from utils.logger import GameLogger  # noqa: E402

# Initialiser le logger
game_logger = GameLogger()


class SimpleIntelligentTester:
    """Testeur intelligent simplifié qui utilise l'API directement"""

    def __init__(self, base_url: str = "http://localhost:5001"):
        self.base_url = base_url
        self.session = requests.Session()
        self.test_results = []

        # Personnalités d'ados
        self.personalities = {
            "alex_explorer": {
                "name": "Alex",
                "style": "explorer",
                "patience": 8,
                "curiosity": 9,
                "commands": [
                    "aide",
                    "profil",
                    "monde",
                    "badges",
                    "luna_contact",
                    "scan_persona",
                ],
                "behavior": "Curieux et patient, aime découvrir",
            },
            "sam_speedrunner": {
                "name": "Sam",
                "style": "speedrunner",
                "patience": 3,
                "curiosity": 4,
                "commands": [
                    "hack_system",
                    "hacker_coffre",
                    "decode_portal",
                    "challenge_corp",
                    "boss_final",
                ],
                "behavior": "Impatient et rapide, veut tout faire vite",
            },
            "maya_completionist": {
                "name": "Maya",
                "style": "completionist",
                "patience": 9,
                "curiosity": 7,
                "commands": [
                    "unlock_universe",
                    "load_mission",
                    "reboot_world",
                    "luna_dance",
                    "easter_egg_1337",
                ],
                "behavior": "Patient et perfectionniste, veut tout finir",
            },
            "leo_chaos": {
                "name": "Leo",
                "style": "chaos",
                "patience": 2,
                "curiosity": 10,
                "commands": [
                    "hack_the_planet",
                    "give_me_all_points",
                    "delete_everything",
                    "lol_what_happens",
                    "test123",
                    "",
                ],
                "behavior": "Impatient et chaotique, aime casser",
            },
        }

    def test_command(self, personality: str, command: str) -> dict:
        """Teste une commande et retourne le résultat"""
        try:
            print(f"🎮 {self.personalities[personality]['name']} essaie: '{command}'")

            response = self.session.post(
                f"{self.base_url}/commande",
                json={"commande": command},
                timeout=10,
            )

            if response.status_code == 200:
                result = response.json()
                # L'API retourne la réponse dans un objet 'reponse'
                if "reponse" in result:
                    reponse = result["reponse"]
                    success = reponse.get("réussite", False)
                    message = reponse.get("message", "")
                    score_gained = reponse.get("score_gagne", 0)
                    badge = reponse.get("badge", "")
                else:
                    # Fallback pour l'ancien format
                    success = result.get("réussite", False)
                    message = result.get("message", "")
                    score_gained = result.get("score_gagne", 0)
                    badge = result.get("badge", "")

                # Afficher le résultat avec plus de détails
                if success:
                    game_logger.info(
                        f"✅ SUCCÈS! Score: +{score_gained}, Badge: {badge}"
                    )
                    game_logger.info(f"   💬 {message[:80]}...")
                else:
                    game_logger.info(f"❌ ÉCHEC: {message[:80]}...")

                return {
                    "personality": personality,
                    "command": command,
                    "success": success,
                    "message": message,
                    "score_gained": score_gained,
                    "badge": badge,
                    "timestamp": datetime.now().isoformat(),
                }
            game_logger.info(f"❌ Erreur HTTP: {response.status_code}")
            return {
                "personality": personality,
                "command": command,
                "success": False,
                "error": f"HTTP {response.status_code}",
                "timestamp": datetime.now().isoformat(),
            }

        except Exception as e:
            game_logger.info(f"❌ Exception: {e}")
            return {
                "personality": personality,
                "command": command,
                "success": False,
                "error": str(e),
                "timestamp": datetime.now().isoformat(),
            }

    def test_tutorial(self, personality: str) -> list[dict]:
        """Teste le tutoriel avec une personnalité"""
        print(f"\n🎓 {self.personalities[personality]['name']} teste le tutoriel...")

        results = []

        # Test du démarrage du tutoriel
        result = self.test_command(personality, "start_tutorial")
        results.append(result)

        # Test de quelques commandes selon la personnalité
        self.personalities[personality]

        # Choisir des commandes selon la personnalité
        if personality == "alex_explorer":
            commands = [
                "aide",
                "profil",
                "monde",
                "badges",
                "luna_contact",
                "scan_persona",
            ]
        elif personality == "sam_speedrunner":
            commands = [
                "hack_system",
                "hacker_coffre",
                "challenge_corp",
                "boss_final",
                "decode_portal",
            ]
        elif personality == "maya_completionist":
            commands = [
                "unlock_universe",
                "load_mission",
                "luna_dance",
                "easter_egg_1337",
                "reboot_world",
            ]
        elif personality == "leo_chaos":
            commands = [
                "hack_the_planet",
                "give_me_all_points",
                "delete_everything",
                "make_me_admin",
                "lol_what_happens",
            ]
        else:
            commands = ["aide", "profil"]

        # Tester les commandes
        for cmd in commands:
            result = self.test_command(personality, cmd)
            results.append(result)
            time.sleep(0.5)  # Pause entre les commandes

        return results

    def test_edge_cases(self, personality: str) -> list[dict]:
        """Teste des cas limites selon la personnalité"""
        print(
            f"\n🔧 {self.personalities[personality]['name']} teste les cas limites..."
        )

        results = []
        self.personalities[personality]

        # Commandes bizarres selon la personnalité
        if personality == "leo_chaos":
            weird_commands = [
                "hack_the_planet",
                "give_me_all_points",
                "make_me_admin",
                "delete_everything",
                "lol_what_happens",
                "test123",
                "",
                "   ",
                "émojis🚀🎮",
                "very_long_command_that_should_not_work_at_all_because_it_is_too_long_and_weird",
            ]
        else:
            weird_commands = ["invalid_command", "test123", "", "émojis🚀🎮"]

        for cmd in weird_commands:
            result = self.test_command(personality, cmd)
            results.append(result)
            time.sleep(0.3)

        return results

    def test_personality(self, personality: str) -> dict:
        """Teste complètement une personnalité"""
        print(f"\n🎮 TEST DE {self.personalities[personality]['name'].upper()}")
        print("=" * 50)

        personality_data = self.personalities[personality]
        print(f"🧠 Style: {personality_data['style']}")
        print(f"⏱️  Patience: {personality_data['patience']}/10")
        print(f"🔍 Curiosité: {personality_data['curiosity']}/10")
        print(f"🎯 Comportement: {personality_data['behavior']}")

        all_results = []

        # Test du tutoriel
        tutorial_results = self.test_tutorial(personality)
        all_results.extend(tutorial_results)

        # Test des cas limites
        edge_results = self.test_edge_cases(personality)
        all_results.extend(edge_results)

        # Statistiques
        total_commands = len(all_results)
        successful_commands = len([r for r in all_results if r.get("success", False)])
        total_score = sum([r.get("score_gained", 0) for r in all_results])
        badges_earned = len([r for r in all_results if r.get("badge")])

        print(f"\n📊 RÉSULTATS DE {personality_data['name']}:")
        game_logger.info(f"   • Commandes testées: {total_commands}")
        game_logger.info(f"   • Commandes réussies: {successful_commands}")
        game_logger.info(f"   • Score total gagné: {total_score}")
        game_logger.info(f"   • Badges gagnés: {badges_earned}")

        return {
            "personality": personality,
            "personality_data": personality_data,
            "results": all_results,
            "stats": {
                "total_commands": total_commands,
                "successful_commands": successful_commands,
                "success_rate": (
                    successful_commands / total_commands if total_commands > 0 else 0
                ),
                "total_score": total_score,
                "badges_earned": badges_earned,
            },
            "timestamp": datetime.now().isoformat(),
        }

    def run_all_tests(self) -> dict:
        """Lance tous les tests avec toutes les personnalités"""
        print("🎮" + "=" * 60 + "🎮")
        game_logger.info(r"🧠 TESTEUR INTELLIGENT SIMPLIFIÉ - ARKALIA QUEST")
        print("🎯 Test avec 4 personnalités d'ados de 13 ans")
        print("=" * 64)

        all_results = {}

        personalities = [
            "alex_explorer",
            "sam_speedrunner",
            "maya_completionist",
            "leo_chaos",
        ]

        for personality in personalities:
            try:
                result = self.test_personality(personality)
                all_results[personality] = result
                print(f"\n✅ Test terminé pour {result['personality_data']['name']}")
                time.sleep(1)  # Pause entre les personnalités

            except Exception as e:
                game_logger.info(f"❌ Erreur avec {personality}: {e}")
                all_results[personality] = {
                    "personality": personality,
                    "error": str(e),
                    "timestamp": datetime.now().isoformat(),
                }

        # Rapport final
        self.generate_final_report(all_results)

        return all_results

    def generate_final_report(self, all_results: dict):
        """Génère un rapport final"""
        game_logger.info(r"\n🎉 RAPPORT FINAL")
        print("=" * 50)

        total_commands = 0
        total_successful = 0
        total_score = 0
        total_badges = 0

        for _personality, result in all_results.items():
            if "stats" in result:
                stats = result["stats"]
                total_commands += stats["total_commands"]
                total_successful += stats["successful_commands"]
                total_score += stats["total_score"]
                total_badges += stats["badges_earned"]

                print(
                    f"\n🧭 {result['personality_data']['name']} ({result['personality_data']['style']}):",
                )
                print(
                    f"• Succès: {stats['successful_commands']}/{stats['total_commands']} ({stats['success_rate'] * 100:.1f}%)",
                )
                print(f"   • Score: {stats['total_score']} points")
                print(f"   • Badges: {stats['badges_earned']}")

        game_logger.info(r"\n📊 TOTAL GLOBAL:")
        game_logger.info(f"   • Commandes testées: {total_commands}")
        game_logger.info(f"   • Commandes réussies: {total_successful}")
        print(
            (
                f"   • Taux de succès: {total_successful / total_commands * 100:.1f}%"
                if total_commands > 0
                else "   • Taux de succès: 0%"
            ),
        )
        game_logger.info(f"   • Score total: {total_score}")
        game_logger.info(f"   • Badges total: {total_badges}")

        # Sauvegarder le rapport
        filename = f"tests/reports/simple_test_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(all_results, f, indent=2, ensure_ascii=False)

        game_logger.info(f"\n💾 Rapport sauvegardé: {filename}")

        # Messages des "faux joueurs"
        print("\n🎭 CE QUE DISENT TES 'FAUX JOUEURS':")
        print("=" * 50)

        for _personality, result in all_results.items():
            if "personality_data" in result:
                name = result["personality_data"]["name"]
                style = result["personality_data"]["style"]
                stats = result.get("stats", {})
                success_rate = stats.get("success_rate", 0) * 100
                total_score = stats.get("total_score", 0)
                badges_earned = stats.get("badges_earned", 0)

                if style == "explorer":
                    if success_rate > 50:
                        print(
                            f"🧭 {name}: 'Wow, ce jeu est trop cool ! J'ai trouvé plein de trucs cachés ! ({success_rate:.1f}% de succès)'",
                        )
                    else:
                        print(
                            f"🧭 {name}: 'Hmm, c'est pas facile de tout découvrir... ({success_rate:.1f}% de succès)'",
                        )
                elif style == "speedrunner":
                    if success_rate > 50:
                        print(
                            f"⚡ {name}: 'C'est rapide et efficace ! J'aime ça ! ({success_rate:.1f}% de succès)'",
                        )
                    else:
                        print(
                            f"⚡ {name}: 'C'est trop lent ! Je veux aller plus vite ! ({success_rate:.1f}% de succès)'",
                        )
                elif style == "completionist":
                    if badges_earned > 0:
                        print(
                            f"🏆 {name}: 'J'ai gagné {badges_earned} badges et {total_score} points ! Je veux tous les avoir !'",
                        )
                    else:
                        print(
                            f"🏆 {name}: 'Je n'ai pas encore de badges... Je dois continuer ! ({success_rate:.1f}% de succès)'",
                        )
                elif style == "chaos":
                    if success_rate < 20:
                        print(
                            f"🤪 {name}: 'Haha, j'ai essayé de casser le jeu ! C'était marrant ! ({success_rate:.1f}% de succès)'",
                        )
                    else:
                        print(
                            f"🤪 {name}: 'Même mes commandes bizarres marchent ! ({success_rate:.1f}% de succès)'",
                        )


def main():
    """Fonction principale"""
    tester = SimpleIntelligentTester()
    tester.run_all_tests()


if __name__ == "__main__":
    main()
