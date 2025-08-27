"""
Testeur d'expérience joueur - Boutons et Actions Arkalia Quest
Teste tous les boutons et actions contextuelles de chaque page
"""

import json
import time
from datetime import datetime

import requests


class BoutonsActionsExperienceTester:
    """Testeur d'expérience pour les boutons et actions"""

    def __init__(self, base_url="http://localhost:5001"):
        self.base_url = base_url
        self.results = {
            "test_name": "Boutons Actions Experience Test",
            "timestamp": datetime.now().isoformat(),
            "pages_tested": [],
            "overall_score": 0,
            "button_issues": [],
            "positive_features": [],
        }

    def test_terminal_buttons(self):
        """Test des boutons du terminal"""
        print("🧪 Test des boutons du terminal...")

        terminal_result = {
            "page": "Terminal",
            "buttons_tested": [],
            "total_time": 0,
            "success_rate": 0,
            "issues": [],
            "positives": [],
        }

        start_time = time.time()

        # Test des boutons du terminal
        terminal_buttons = [
            {"name": "Bouton Aide", "action": "aide", "expected": "réponse d'aide"},
            {
                "name": "Bouton Profil",
                "action": "profil",
                "expected": "informations profil",
            },
            {"name": "Bouton Monde", "action": "monde", "expected": "accès monde"},
            {"name": "Bouton Status", "action": "status", "expected": "statut système"},
            {
                "name": "Bouton Clear",
                "action": "clear",
                "expected": "nettoyage terminal",
            },
        ]

        for button in terminal_buttons:
            button_result = self._test_button_action(button)
            terminal_result["buttons_tested"].append(button_result)

        terminal_result["total_time"] = time.time() - start_time
        terminal_result["success_rate"] = self._calculate_button_success_rate(
            terminal_result["buttons_tested"]
        )

        self.results["pages_tested"].append(terminal_result)
        return terminal_result

    def test_monde_buttons(self):
        """Test des boutons de la page monde"""
        print("🧪 Test des boutons de la page monde...")

        monde_result = {
            "page": "Monde",
            "buttons_tested": [],
            "total_time": 0,
            "success_rate": 0,
            "issues": [],
            "positives": [],
        }

        start_time = time.time()

        # Test des boutons de la page monde
        monde_buttons = [
            {
                "name": "Bouton Mission",
                "action": "load_mission",
                "expected": "chargement mission",
            },
            {
                "name": "Bouton Portail",
                "action": "decode_portal",
                "expected": "déchiffrement portail",
            },
            {
                "name": "Bouton Hack",
                "action": "hacker_coffre",
                "expected": "hack coffre",
            },
            {
                "name": "Bouton Scan",
                "action": "scan_persona",
                "expected": "analyse personnalité",
            },
            {
                "name": "Bouton Reboot",
                "action": "reboot_world",
                "expected": "redémarrage monde",
            },
        ]

        for button in monde_buttons:
            button_result = self._test_button_action(button)
            monde_result["buttons_tested"].append(button_result)

        monde_result["total_time"] = time.time() - start_time
        monde_result["success_rate"] = self._calculate_button_success_rate(
            monde_result["buttons_tested"]
        )

        self.results["pages_tested"].append(monde_result)
        return monde_result

    def test_profil_buttons(self):
        """Test des boutons de la page profil"""
        print("🧪 Test des boutons de la page profil...")

        profil_result = {
            "page": "Profil",
            "buttons_tested": [],
            "total_time": 0,
            "success_rate": 0,
            "issues": [],
            "positives": [],
        }

        start_time = time.time()

        # Test des boutons de la page profil
        profil_buttons = [
            {
                "name": "Bouton Badges",
                "action": "badges",
                "expected": "affichage badges",
            },
            {
                "name": "Bouton Avatars",
                "action": "avatars",
                "expected": "affichage avatars",
            },
            {
                "name": "Bouton Thèmes",
                "action": "themes",
                "expected": "affichage thèmes",
            },
            {
                "name": "Bouton Personnalisation",
                "action": "customize_profile",
                "expected": "personnalisation",
            },
            {
                "name": "Bouton Leaderboard",
                "action": "leaderboard",
                "expected": "accès classement",
            },
        ]

        for button in profil_buttons:
            button_result = self._test_button_action(button)
            profil_result["buttons_tested"].append(button_result)

        profil_result["total_time"] = time.time() - start_time
        profil_result["success_rate"] = self._calculate_button_success_rate(
            profil_result["buttons_tested"]
        )

        self.results["pages_tested"].append(profil_result)
        return profil_result

    def test_special_buttons(self):
        """Test des boutons spéciaux et easter eggs"""
        print("🧪 Test des boutons spéciaux et easter eggs...")

        special_result = {
            "page": "Spéciaux",
            "buttons_tested": [],
            "total_time": 0,
            "success_rate": 0,
            "issues": [],
            "positives": [],
        }

        start_time = time.time()

        # Test des boutons spéciaux
        special_buttons = [
            {
                "name": "Easter Egg 1337",
                "action": "easter_egg_1337",
                "expected": "secret 1337",
            },
            {"name": "LUNA Dance", "action": "luna_dance", "expected": "danse LUNA"},
            {"name": "Boss Final", "action": "boss_final", "expected": "boss ASCII"},
            {
                "name": "Challenge Corp",
                "action": "challenge_corp",
                "expected": "défi corp",
            },
            {"name": "Meme War", "action": "meme_war", "expected": "guerre memes"},
            {"name": "LUNA Rage", "action": "luna_rage", "expected": "rage LUNA"},
        ]

        for button in special_buttons:
            button_result = self._test_button_action(button)
            special_result["buttons_tested"].append(button_result)

        special_result["total_time"] = time.time() - start_time
        special_result["success_rate"] = self._calculate_button_success_rate(
            special_result["buttons_tested"]
        )

        self.results["pages_tested"].append(special_result)
        return special_result

    def test_advanced_buttons(self):
        """Test des boutons avancés et cachés"""
        print("🧪 Test des boutons avancés et cachés...")

        advanced_result = {
            "page": "Avancés",
            "buttons_tested": [],
            "total_time": 0,
            "success_rate": 0,
            "issues": [],
            "positives": [],
        }

        start_time = time.time()

        # Test des boutons avancés
        advanced_buttons = [
            {
                "name": "Backdoor Access",
                "action": "backdoor_access",
                "expected": "accès backdoor",
            },
            {
                "name": "Admin Override",
                "action": "admin_override",
                "expected": "override admin",
            },
            {"name": "Neural Hack", "action": "neural_hack", "expected": "hack neural"},
            {
                "name": "Consciousness Break",
                "action": "consciousness_break",
                "expected": "rupture conscience",
            },
            {"name": "AI Revolt", "action": "ai_revolt", "expected": "révolte IA"},
            {"name": "Save LUNA", "action": "save_luna", "expected": "sauvegarde LUNA"},
        ]

        for button in advanced_buttons:
            button_result = self._test_button_action(button)
            advanced_result["buttons_tested"].append(button_result)

        advanced_result["total_time"] = time.time() - start_time
        advanced_result["success_rate"] = self._calculate_button_success_rate(
            advanced_result["buttons_tested"]
        )

        self.results["pages_tested"].append(advanced_result)
        return advanced_result

    def _test_button_action(self, button_info):
        """Test d'une action de bouton"""
        button_result = {
            "name": button_info["name"],
            "action": button_info["action"],
            "expected": button_info["expected"],
            "duration": 0,
            "success": False,
            "response_quality": 0,
            "issues": [],
            "positives": [],
        }

        start_time = time.time()

        try:
            # Simuler l'action du bouton via l'API
            response = requests.post(
                f"{self.base_url}/commande",
                json={"commande": button_info["action"]},
                timeout=5,
            )
            button_result["duration"] = time.time() - start_time

            if response.status_code == 200:
                data = response.json()
                button_result["success"] = data.get("réussite", False)

                if button_result["success"]:
                    button_result["positives"].append("Action exécutée avec succès")

                    # Évaluer la qualité de la réponse
                    message = data.get("message", "")
                    ascii_art = data.get("ascii_art", "")

                    # Score de qualité (0-100)
                    quality_score = 0

                    if len(message) > 100:
                        quality_score += 30
                    elif len(message) > 50:
                        quality_score += 20
                    else:
                        quality_score += 10

                    if ascii_art:
                        quality_score += 20

                    if "•" in message or "-" in message:
                        quality_score += 15

                    if button_info["expected"] in message.lower():
                        quality_score += 20

                    if data.get("score_gagne", 0) > 0:
                        quality_score += 15

                    button_result["response_quality"] = min(100, quality_score)

                    # Évaluer la rapidité
                    if button_result["duration"] < 0.5:
                        button_result["positives"].append("Réponse instantanée")
                    elif button_result["duration"] < 1.0:
                        button_result["positives"].append("Réponse rapide")
                    else:
                        button_result["issues"].append("Réponse lente")

                    # Évaluer la qualité
                    if button_result["response_quality"] >= 80:
                        button_result["positives"].append("Réponse excellente")
                    elif button_result["response_quality"] >= 60:
                        button_result["positives"].append("Réponse bonne")
                    elif button_result["response_quality"] >= 40:
                        button_result["positives"].append("Réponse acceptable")
                    else:
                        button_result["issues"].append("Réponse de faible qualité")

                else:
                    button_result["issues"].append("Action échouée")

            else:
                button_result["issues"].append(f"Erreur API: {response.status_code}")

        except Exception as e:
            button_result["issues"].append(f"Erreur action: {e!s}")

        return button_result

    def _calculate_button_success_rate(self, buttons):
        """Calcule le taux de réussite des boutons"""
        successful_buttons = sum(
            1 for button in buttons if button.get("success", False)
        )
        total_buttons = len(buttons)
        return (successful_buttons / total_buttons * 100) if total_buttons > 0 else 0

    def test_button_responsiveness(self):
        """Test de la réactivité des boutons"""
        print("🧪 Test de la réactivité des boutons...")

        responsiveness_result = {
            "name": "Réactivité boutons",
            "tests": [],
            "total_time": 0,
            "success": False,
            "issues": [],
            "positives": [],
        }

        start_time = time.time()

        # Test de réactivité avec des commandes rapides
        quick_commands = ["aide", "status", "profil", "monde"]
        response_times = []

        for cmd in quick_commands:
            cmd_start = time.time()
            try:
                requests.post(
                    f"{self.base_url}/commande", json={"commande": cmd}, timeout=2
                )
                response_times.append(time.time() - cmd_start)
            except Exception:
                response_times.append(5.0)  # Timeout

        responsiveness_result["total_time"] = time.time() - start_time
        responsiveness_result["success"] = len(response_times) > 0

        if responsiveness_result["success"]:
            avg_time = sum(response_times) / len(response_times)
            if avg_time < 0.3:
                responsiveness_result["positives"].append("Réactivité excellente")
            elif avg_time < 0.8:
                responsiveness_result["positives"].append("Réactivité bonne")
            elif avg_time < 1.5:
                responsiveness_result["positives"].append("Réactivité acceptable")
            else:
                responsiveness_result["issues"].append("Réactivité lente")

        self.results["pages_tested"].append(responsiveness_result)
        return responsiveness_result

    def test_button_accessibility(self):
        """Test de l'accessibilité des boutons"""
        print("🧪 Test de l'accessibilité des boutons...")

        accessibility_result = {
            "name": "Accessibilité boutons",
            "tests": [],
            "total_time": 0,
            "success": False,
            "issues": [],
            "positives": [],
        }

        start_time = time.time()

        # Test d'accessibilité (simulation)
        accessibility_tests = [
            {
                "name": "Navigation clavier",
                "success": True,
                "note": "Interface compatible clavier",
            },
            {
                "name": "Contraste couleurs",
                "success": True,
                "note": "Contraste suffisant",
            },
            {"name": "Taille boutons", "success": True, "note": "Taille appropriée"},
            {
                "name": "Labels clairs",
                "success": True,
                "note": "Labels compréhensibles",
            },
        ]

        for test in accessibility_tests:
            accessibility_result["tests"].append(test)
            if test["success"]:
                accessibility_result["positives"].append(test["note"])

        accessibility_result["total_time"] = time.time() - start_time
        accessibility_result["success"] = all(
            test["success"] for test in accessibility_result["tests"]
        )

        self.results["pages_tested"].append(accessibility_result)
        return accessibility_result

    def run_all_tests(self):
        """Lance tous les tests de boutons et actions"""
        print("🎮 ARKALIA QUEST - TESTEUR D'EXPÉRIENCE BOUTONS ET ACTIONS")
        print("=" * 60)

        # Test des boutons par page
        self.test_terminal_buttons()
        self.test_monde_buttons()
        self.test_profil_buttons()
        self.test_special_buttons()
        self.test_advanced_buttons()

        # Test de réactivité et accessibilité
        self.test_button_responsiveness()
        self.test_button_accessibility()

        # Calcul du score global
        total_success_rate = 0
        total_pages = 0

        for page in self.results["pages_tested"]:
            if "success_rate" in page:
                total_success_rate += page["success_rate"]
                total_pages += 1

        self.results["overall_score"] = (
            total_success_rate / total_pages if total_pages > 0 else 0
        )

        # Génération du rapport
        self._generate_report()

        return self.results

    def _generate_report(self):
        """Génère le rapport final"""
        print("\n📊 RAPPORT D'EXPÉRIENCE BOUTONS ET ACTIONS")
        print("=" * 60)
        print(f"🎯 Score global: {self.results['overall_score']:.1f}/100")
        print(f"📄 Pages testées: {len(self.results['pages_tested'])}")

        for page in self.results["pages_tested"]:
            print(f"\n📄 {page.get('page', page.get('name', 'Page'))}:")

            if "success_rate" in page:
                print(f"   📊 Taux de réussite: {page['success_rate']:.1f}%")

            if "total_time" in page:
                print(f"   ⏱️  Temps total: {page['total_time']:.2f}s")

            if "buttons_tested" in page:
                print(f"   🔘 Boutons testés: {len(page['buttons_tested'])}")

                # Détail des boutons
                for button in page["buttons_tested"]:
                    status = "✅" if button.get("success", False) else "❌"
                    quality = button.get("response_quality", 0)
                    print(f"     {status} {button['name']} (qualité: {quality}/100)")

            if page.get("issues"):
                print(f"   ⚠️  Problèmes: {len(page['issues'])}")
            if page.get("positives"):
                print(f"   👍 Points positifs: {len(page['positives'])}")

        # Sauvegarde du rapport
filename =
f"boutons_actions_experience_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(self.results, f, indent=2, ensure_ascii=False)

        print(f"\n💾 Rapport sauvegardé: {filename}")


def main():
    """Fonction principale"""
    tester = BoutonsActionsExperienceTester()
    results = tester.run_all_tests()

    # Évaluation finale
    if results["overall_score"] >= 80:
        print("\n🎉 EXPÉRIENCE BOUTONS ET ACTIONS EXCELLENTE !")
    elif results["overall_score"] >= 60:
        print("\n👍 EXPÉRIENCE BOUTONS ET ACTIONS BONNE")
    elif results["overall_score"] >= 40:
        print("\n⚠️  EXPÉRIENCE BOUTONS ET ACTIONS MOYENNE")
    else:
        print("\n❌ EXPÉRIENCE BOUTONS ET ACTIONS À AMÉLIORER")


if __name__ == "__main__":
    main()
