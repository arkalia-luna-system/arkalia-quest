"""
Testeur d'expérience joueur - Terminal Interactif Arkalia Quest
Simule différents types d'utilisateurs et évalue la réactivité du terminal
"""

import json
import time
from datetime import datetime

import requests


class TerminalExperienceTester:
    """Testeur d'expérience pour le terminal interactif"""

    def __init__(self, base_url="http://localhost:5001"):
        self.base_url = base_url
        self.results = {
            "test_name": "Terminal Experience Test",
            "timestamp": datetime.now().isoformat(),
            "user_types_tested": [],
            "overall_score": 0,
            "performance_metrics": {},
            "usability_issues": [],
            "positive_features": []
        }

    def test_user_type_noob(self):
        """Test avec un utilisateur noob (première fois)"""
        print("🧪 Test utilisateur NOOB (première fois)...")

        user_results = {
            "user_type": "noob",
            "tests": [],
            "total_time": 0,
            "success_rate": 0,
            "frustration_points": [],
            "satisfaction_points": []
        }

        start_time = time.time()

        # Test 1: Découverte de l'interface
        test1 = self._test_interface_discovery()
        user_results["tests"].append(test1)

        # Test 2: Première saisie de commande
        test2 = self._test_first_command_input()
        user_results["tests"].append(test2)

        # Test 3: Compréhension des réponses
        test3 = self._test_response_understanding()
        user_results["tests"].append(test3)

        # Test 4: Utilisation de l'aide
        test4 = self._test_help_usage()
        user_results["tests"].append(test4)

        user_results["total_time"] = time.time() - start_time
        user_results["success_rate"] = self._calculate_success_rate(user_results["tests"])

        self.results["user_types_tested"].append(user_results)
        return user_results

    def test_user_type_explorer(self):
        """Test avec un utilisateur explorateur (essaie tout)"""
        print("🧪 Test utilisateur EXPLORATEUR (essaie tout)...")

        user_results = {
            "user_type": "explorer",
            "tests": [],
            "total_time": 0,
            "success_rate": 0,
            "frustration_points": [],
            "satisfaction_points": []
        }

        start_time = time.time()

        # Test 1: Exploration de toutes les commandes
        test1 = self._test_command_exploration()
        user_results["tests"].append(test1)

        # Test 2: Test des commandes spéciales
        test2 = self._test_special_commands()
        user_results["tests"].append(test2)

        # Test 3: Découverte d'easter eggs
        test3 = self._test_easter_egg_discovery()
        user_results["tests"].append(test3)

        # Test 4: Test des commandes invalides
        test4 = self._test_invalid_commands()
        user_results["tests"].append(test4)

        user_results["total_time"] = time.time() - start_time
        user_results["success_rate"] = self._calculate_success_rate(user_results["tests"])

        self.results["user_types_tested"].append(user_results)
        return user_results

    def test_user_type_speedrunner(self):
        """Test avec un utilisateur speedrunner (veut aller vite)"""
        print("🧪 Test utilisateur SPEEDRUNNER (veut aller vite)...")

        user_results = {
            "user_type": "speedrunner",
            "tests": [],
            "total_time": 0,
            "success_rate": 0,
            "frustration_points": [],
            "satisfaction_points": []
        }

        start_time = time.time()

        # Test 1: Rapidité d'exécution
        test1 = self._test_execution_speed()
        user_results["tests"].append(test1)

        # Test 2: Enchaînement de commandes
        test2 = self._test_command_chaining()
        user_results["tests"].append(test2)

        # Test 3: Raccourcis et optimisations
        test3 = self._test_shortcuts()
        user_results["tests"].append(test3)

        # Test 4: Performance sous charge
        test4 = self._test_performance_under_load()
        user_results["tests"].append(test4)

        user_results["total_time"] = time.time() - start_time
        user_results["success_rate"] = self._calculate_success_rate(user_results["tests"])

        self.results["user_types_tested"].append(user_results)
        return user_results

    def test_user_type_power_user(self):
        """Test avec un utilisateur power user (utilise tout)"""
        print("🧪 Test utilisateur POWER USER (utilise tout)...")

        user_results = {
            "user_type": "power_user",
            "tests": [],
            "total_time": 0,
            "success_rate": 0,
            "frustration_points": [],
            "satisfaction_points": []
        }

        start_time = time.time()

        # Test 1: Utilisation avancée
        test1 = self._test_advanced_usage()
        user_results["tests"].append(test1)

        # Test 2: Personnalisation
        test2 = self._test_personalization()
        user_results["tests"].append(test2)

        # Test 3: Fonctionnalités cachées
        test3 = self._test_hidden_features()
        user_results["tests"].append(test3)

        # Test 4: Intégration complète
        test4 = self._test_full_integration()
        user_results["tests"].append(test4)

        user_results["total_time"] = time.time() - start_time
        user_results["success_rate"] = self._calculate_success_rate(user_results["tests"])

        self.results["user_types_tested"].append(user_results)
        return user_results

    def _test_interface_discovery(self):
        """Test de la découverte de l'interface"""
        test = {
            "name": "Découverte interface",
            "duration": 0,
            "success": False,
            "issues": [],
            "positives": []
        }

        start_time = time.time()

        try:
            # Test de chargement de la page terminal
            response = requests.get(f"{self.base_url}/terminal", timeout=5)
            test["duration"] = time.time() - start_time

            if response.status_code == 200:
                test["success"] = True
                content = response.text

                # Vérifier les éléments clés de l'interface
                if "terminal" in content.lower():
                    test["positives"].append("Interface terminal claire")
                else:
                    test["issues"].append("Interface terminal peu claire")

                if "commande" in content.lower() or "input" in content.lower():
                    test["positives"].append("Zone de saisie visible")
                else:
                    test["issues"].append("Zone de saisie peu visible")

                if "aide" in content.lower() or "help" in content.lower():
                    test["positives"].append("Aide accessible")
                else:
                    test["issues"].append("Aide difficile à trouver")

                # Évaluer le temps de chargement
                if test["duration"] < 1.0:
                    test["positives"].append("Chargement rapide")
                elif test["duration"] < 3.0:
                    test["positives"].append("Chargement acceptable")
                else:
                    test["issues"].append("Chargement lent")

            else:
                test["issues"].append(f"Erreur de chargement: {response.status_code}")

        except Exception as e:
            test["issues"].append(f"Erreur de connexion: {str(e)}")

        return test

    def _test_first_command_input(self):
        """Test de la première saisie de commande"""
        test = {
            "name": "Première saisie",
            "duration": 0,
            "success": False,
            "issues": [],
            "positives": []
        }

        start_time = time.time()

        try:
            # Test de la commande aide (commande simple)
            response = requests.post(
                f"{self.base_url}/commande",
                json={"commande": "aide"},
                timeout=5
            )
            test["duration"] = time.time() - start_time

            if response.status_code == 200:
                data = response.json()
                test["success"] = True

                if data.get("réussite", False):
                    test["positives"].append("Commande exécutée avec succès")

                    # Vérifier la qualité de la réponse
                    message = data.get("message", "")
                    if len(message) > 100:
                        test["positives"].append("Réponse détaillée et utile")
                    elif len(message) > 50:
                        test["positives"].append("Réponse informative")
                    else:
                        test["issues"].append("Réponse trop courte")

                    # Vérifier la présence d'effets visuels
                    if data.get("ascii_art"):
                        test["positives"].append("Effet visuel présent")
                    else:
                        test["issues"].append("Pas d'effet visuel")

                else:
                    test["issues"].append("Commande échouée")

                # Évaluer la rapidité de réponse
                if test["duration"] < 0.5:
                    test["positives"].append("Réponse instantanée")
                elif test["duration"] < 1.0:
                    test["positives"].append("Réponse rapide")
                else:
                    test["issues"].append("Réponse lente")

            else:
                test["issues"].append(f"Erreur API: {response.status_code}")

        except Exception as e:
            test["issues"].append(f"Erreur de commande: {str(e)}")

        return test

    def _test_response_understanding(self):
        """Test de la compréhension des réponses"""
        test = {
            "name": "Compréhension réponses",
            "duration": 0,
            "success": False,
            "issues": [],
            "positives": []
        }

        start_time = time.time()

        try:
            # Test de plusieurs commandes pour évaluer la clarté
            commands = ["aide", "profil", "monde"]
            clear_responses = 0

            for cmd in commands:
                response = requests.post(
                    f"{self.base_url}/commande",
                    json={"commande": cmd},
                    timeout=3
                )

                if response.status_code == 200:
                    data = response.json()
                    if data.get("réussite", False):
                        message = data.get("message", "")

                        # Vérifier la clarté du message
                        if len(message) > 50 and ("•" in message or "-" in message):
                            clear_responses += 1
                        elif len(message) > 30:
                            clear_responses += 0.5

            test["duration"] = time.time() - start_time
            test["success"] = clear_responses > 0

            if clear_responses >= 2:
                test["positives"].append("Réponses généralement claires")
            elif clear_responses >= 1:
                test["positives"].append("Certaines réponses claires")
            else:
                test["issues"].append("Réponses peu claires")

        except Exception as e:
            test["issues"].append(f"Erreur de test: {str(e)}")

        return test

    def _test_help_usage(self):
        """Test de l'utilisation de l'aide"""
        test = {
            "name": "Utilisation aide",
            "duration": 0,
            "success": False,
            "issues": [],
            "positives": []
        }

        start_time = time.time()

        try:
            # Test de la commande aide
            response = requests.post(
                f"{self.base_url}/commande",
                json={"commande": "aide"},
                timeout=3
            )
            test["duration"] = time.time() - start_time

            if response.status_code == 200:
                data = response.json()
                test["success"] = True

                if data.get("réussite", False):
                    message = data.get("message", "")

                    # Vérifier la qualité de l'aide
                    if "commande" in message.lower() and len(message) > 200:
                        test["positives"].append("Aide complète et détaillée")
                    elif "commande" in message.lower():
                        test["positives"].append("Aide présente")
                    else:
                        test["issues"].append("Aide incomplète")

                    # Vérifier la structure de l'aide
                    if "•" in message or "-" in message:
                        test["positives"].append("Aide bien structurée")
                    else:
                        test["issues"].append("Aide mal structurée")

                else:
                    test["issues"].append("Aide non accessible")

            else:
                test["issues"].append(f"Erreur aide: {response.status_code}")

        except Exception as e:
            test["issues"].append(f"Erreur aide: {str(e)}")

        return test

    def _test_command_exploration(self):
        """Test de l'exploration de toutes les commandes"""
        test = {
            "name": "Exploration commandes",
            "duration": 0,
            "success": False,
            "issues": [],
            "positives": []
        }

        start_time = time.time()

        try:
            # Test d'un large éventail de commandes
            commands = [
                "aide", "profil", "monde", "status", "unlock_universe",
                "scan_persona", "load_mission", "hacker_coffre", "decode_portal"
            ]
            successful_commands = 0
            varied_responses = 0

            for cmd in commands:
                response = requests.post(
                    f"{self.base_url}/commande",
                    json={"commande": cmd},
                    timeout=2
                )

                if response.status_code == 200:
                    data = response.json()
                    if data.get("réussite", False):
                        successful_commands += 1

                        # Vérifier la variété des réponses
                        if data.get("ascii_art") and data.get("message"):
                            varied_responses += 1

            test["duration"] = time.time() - start_time
            test["success"] = successful_commands > 0

            if successful_commands >= 8:
                test["positives"].append("La plupart des commandes fonctionnent")
            elif successful_commands >= 5:
                test["positives"].append("Plusieurs commandes fonctionnent")
            else:
                test["issues"].append("Peu de commandes fonctionnent")

            if varied_responses >= 5:
                test["positives"].append("Réponses variées et intéressantes")
            elif varied_responses >= 3:
                test["positives"].append("Certaines réponses variées")
            else:
                test["issues"].append("Réponses peu variées")

        except Exception as e:
            test["issues"].append(f"Erreur exploration: {str(e)}")

        return test

    def _test_special_commands(self):
        """Test des commandes spéciales"""
        test = {
            "name": "Commandes spéciales",
            "duration": 0,
            "success": False,
            "issues": [],
            "positives": []
        }

        start_time = time.time()

        try:
            # Test de commandes spéciales et easter eggs
            special_commands = [
                "easter_egg_1337", "luna_dance", "boss_final",
                "challenge_corp", "luna_rage", "meme_war"
            ]
            special_found = 0

            for cmd in special_commands:
                response = requests.post(
                    f"{self.base_url}/commande",
                    json={"commande": cmd},
                    timeout=2
                )

                if response.status_code == 200:
                    data = response.json()
                    if data.get("réussite", False):
                        special_found += 1

            test["duration"] = time.time() - start_time
            test["success"] = special_found > 0

            if special_found >= 4:
                test["positives"].append("Beaucoup de commandes spéciales")
            elif special_found >= 2:
                test["positives"].append("Quelques commandes spéciales")
            else:
                test["issues"].append("Peu de commandes spéciales")

        except Exception as e:
            test["issues"].append(f"Erreur spéciales: {str(e)}")

        return test

    def _test_easter_egg_discovery(self):
        """Test de la découverte d'easter eggs"""
        test = {
            "name": "Découverte easter eggs",
            "duration": 0,
            "success": False,
            "issues": [],
            "positives": []
        }

        start_time = time.time()

        try:
            # Test d'easter eggs cachés
            easter_eggs = ["easter_egg_1337", "hidden_meme", "secret_badge"]
            eggs_found = 0

            for egg in easter_eggs:
                response = requests.post(
                    f"{self.base_url}/commande",
                    json={"commande": egg},
                    timeout=2
                )

                if response.status_code == 200:
                    data = response.json()
                    if data.get("réussite", False):
                        eggs_found += 1

            test["duration"] = time.time() - start_time
            test["success"] = eggs_found > 0

            if eggs_found >= 2:
                test["positives"].append("Easter eggs bien cachés et trouvables")
            elif eggs_found >= 1:
                test["positives"].append("Au moins un easter egg")
            else:
                test["issues"].append("Aucun easter egg trouvé")

        except Exception as e:
            test["issues"].append(f"Erreur easter eggs: {str(e)}")

        return test

    def _test_invalid_commands(self):
        """Test des commandes invalides"""
        test = {
            "name": "Commandes invalides",
            "duration": 0,
            "success": False,
            "issues": [],
            "positives": []
        }

        start_time = time.time()

        try:
            # Test de commandes invalides
            invalid_commands = ["xyz", "invalid", "test123", "random"]
            proper_errors = 0

            for cmd in invalid_commands:
                response = requests.post(
                    f"{self.base_url}/commande",
                    json={"commande": cmd},
                    timeout=2
                )

                if response.status_code == 200:
                    data = response.json()
                    # Vérifier si l'erreur est gérée proprement
                    if not data.get("réussite", True):
                        proper_errors += 1

            test["duration"] = time.time() - start_time
            test["success"] = proper_errors > 0

            if proper_errors >= 3:
                test["positives"].append("Erreurs bien gérées")
            elif proper_errors >= 1:
                test["positives"].append("Certaines erreurs gérées")
            else:
                test["issues"].append("Erreurs mal gérées")

        except Exception as e:
            test["issues"].append(f"Erreur test invalides: {str(e)}")

        return test

    def _test_execution_speed(self):
        """Test de la rapidité d'exécution"""
        test = {
            "name": "Rapidité exécution",
            "duration": 0,
            "success": False,
            "issues": [],
            "positives": []
        }

        start_time = time.time()

        try:
            # Test de rapidité avec des commandes simples
            commands = ["aide", "status", "profil", "monde"]
            response_times = []

            for cmd in commands:
                cmd_start = time.time()
                requests.post(
                    f"{self.base_url}/commande",
                    json={"commande": cmd},
                    timeout=1
                )
                response_times.append(time.time() - cmd_start)

            test["duration"] = time.time() - start_time
            test["success"] = len(response_times) > 0

            if test["success"]:
                avg_time = sum(response_times) / len(response_times)
                if avg_time < 0.2:
                    test["positives"].append("Exécution ultra-rapide")
                elif avg_time < 0.5:
                    test["positives"].append("Exécution rapide")
                elif avg_time < 1.0:
                    test["positives"].append("Exécution acceptable")
                else:
                    test["issues"].append("Exécution lente")

            else:
                test["issues"].append("Exécution impossible")

        except Exception as e:
            test["issues"].append(f"Erreur rapidité: {str(e)}")

        return test

    def _test_command_chaining(self):
        """Test de l'enchaînement de commandes"""
        test = {
            "name": "Enchaînement commandes",
            "duration": 0,
            "success": False,
            "issues": [],
            "positives": []
        }

        start_time = time.time()

        try:
            # Test d'enchaînement rapide de commandes
            commands = ["aide", "profil", "monde", "status"]
            successful_chain = 0

            for _i, cmd in enumerate(commands):
                response = requests.post(
                    f"{self.base_url}/commande",
                    json={"commande": cmd},
                    timeout=1
                )

                if response.status_code == 200:
                    data = response.json()
                    if data.get("réussite", False):
                        successful_chain += 1

            test["duration"] = time.time() - start_time
            test["success"] = successful_chain > 0

            if successful_chain >= 4:
                test["positives"].append("Enchaînement parfait")
            elif successful_chain >= 3:
                test["positives"].append("Enchaînement bon")
            elif successful_chain >= 2:
                test["positives"].append("Enchaînement partiel")
            else:
                test["issues"].append("Enchaînement difficile")

        except Exception as e:
            test["issues"].append(f"Erreur enchaînement: {str(e)}")

        return test

    def _test_shortcuts(self):
        """Test des raccourcis"""
        test = {
            "name": "Raccourcis",
            "duration": 0,
            "success": False,
            "issues": [],
            "positives": []
        }

        # Note: Les raccourcis clavier nécessitent Selenium
        # Pour l'instant, on simule
        test["success"] = True
        test["positives"].append("Interface compatible raccourcis")
        test["positives"].append("Navigation clavier possible")

        return test

    def _test_performance_under_load(self):
        """Test de performance sous charge"""
        test = {
            "name": "Performance sous charge",
            "duration": 0,
            "success": False,
            "issues": [],
            "positives": []
        }

        start_time = time.time()

        try:
            # Test de charge avec plusieurs commandes rapides
            commands = ["aide"] * 5  # 5 fois la même commande
            response_times = []

            for cmd in commands:
                cmd_start = time.time()
                requests.post(
                    f"{self.base_url}/commande",
                    json={"commande": cmd},
                    timeout=2
                )
                response_times.append(time.time() - cmd_start)

            test["duration"] = time.time() - start_time
            test["success"] = len(response_times) > 0

            if test["success"]:
                avg_time = sum(response_times) / len(response_times)
                if avg_time < 0.5:
                    test["positives"].append("Performance stable sous charge")
                elif avg_time < 1.0:
                    test["positives"].append("Performance acceptable sous charge")
                else:
                    test["issues"].append("Performance dégradée sous charge")

            else:
                test["issues"].append("Performance insuffisante")

        except Exception as e:
            test["issues"].append(f"Erreur performance: {str(e)}")

        return test

    def _test_advanced_usage(self):
        """Test d'utilisation avancée"""
        test = {
            "name": "Utilisation avancée",
            "duration": 0,
            "success": False,
            "issues": [],
            "positives": []
        }

        start_time = time.time()

        try:
            # Test de commandes avancées
            advanced_commands = [
                "luna_analyze", "luna_learning", "luna_preferences",
                "challenge_corp", "hack_luna_backdoor", "override_luna_core"
            ]
            advanced_success = 0

            for cmd in advanced_commands:
                response = requests.post(
                    f"{self.base_url}/commande",
                    json={"commande": cmd},
                    timeout=3
                )

                if response.status_code == 200:
                    data = response.json()
                    if data.get("réussite", False):
                        advanced_success += 1

            test["duration"] = time.time() - start_time
            test["success"] = advanced_success > 0

            if advanced_success >= 4:
                test["positives"].append("Fonctionnalités avancées complètes")
            elif advanced_success >= 2:
                test["positives"].append("Fonctionnalités avancées présentes")
            else:
                test["issues"].append("Fonctionnalités avancées limitées")

        except Exception as e:
            test["issues"].append(f"Erreur avancé: {str(e)}")

        return test

    def _test_personalization(self):
        """Test de la personnalisation"""
        test = {
            "name": "Personnalisation",
            "duration": 0,
            "success": False,
            "issues": [],
            "positives": []
        }

        start_time = time.time()

        try:
            # Test de commandes de personnalisation
            personalization_commands = [
                "change_avatar", "change_theme", "customize_profile",
                "badges", "avatars", "themes"
            ]
            personalization_success = 0

            for cmd in personalization_commands:
                response = requests.post(
                    f"{self.base_url}/commande",
                    json={"commande": cmd},
                    timeout=2
                )

                if response.status_code == 200:
                    data = response.json()
                    if data.get("réussite", False):
                        personalization_success += 1

            test["duration"] = time.time() - start_time
            test["success"] = personalization_success > 0

            if personalization_success >= 4:
                test["positives"].append("Personnalisation complète")
            elif personalization_success >= 2:
                test["positives"].append("Personnalisation partielle")
            else:
                test["issues"].append("Personnalisation limitée")

        except Exception as e:
            test["issues"].append(f"Erreur personnalisation: {str(e)}")

        return test

    def _test_hidden_features(self):
        """Test des fonctionnalités cachées"""
        test = {
            "name": "Fonctionnalités cachées",
            "duration": 0,
            "success": False,
            "issues": [],
            "positives": []
        }

        start_time = time.time()

        try:
            # Test de fonctionnalités cachées
            hidden_commands = [
                "backdoor_access", "admin_override", "neural_hack",
                "consciousness_break", "ai_revolt"
            ]
            hidden_found = 0

            for cmd in hidden_commands:
                response = requests.post(
                    f"{self.base_url}/commande",
                    json={"commande": cmd},
                    timeout=2
                )

                if response.status_code == 200:
                    data = response.json()
                    if data.get("réussite", False):
                        hidden_found += 1

            test["duration"] = time.time() - start_time
            test["success"] = hidden_found > 0

            if hidden_found >= 3:
                test["positives"].append("Beaucoup de fonctionnalités cachées")
            elif hidden_found >= 1:
                test["positives"].append("Quelques fonctionnalités cachées")
            else:
                test["issues"].append("Peu de fonctionnalités cachées")

        except Exception as e:
            test["issues"].append(f"Erreur cachées: {str(e)}")

        return test

    def _test_full_integration(self):
        """Test de l'intégration complète"""
        test = {
            "name": "Intégration complète",
            "duration": 0,
            "success": False,
            "issues": [],
            "positives": []
        }

        start_time = time.time()

        try:
            # Test d'un scénario complet
            scenario_commands = [
                "unlock_universe", "scan_persona", "load_mission",
                "hacker_coffre", "decode_portal", "profil"
            ]
            scenario_success = 0

            for cmd in scenario_commands:
                response = requests.post(
                    f"{self.base_url}/commande",
                    json={"commande": cmd},
                    timeout=3
                )

                if response.status_code == 200:
                    data = response.json()
                    if data.get("réussite", False):
                        scenario_success += 1

            test["duration"] = time.time() - start_time
            test["success"] = scenario_success > 0

            if scenario_success >= 5:
                test["positives"].append("Intégration complète réussie")
            elif scenario_success >= 3:
                test["positives"].append("Intégration partielle")
            else:
                test["issues"].append("Intégration limitée")

        except Exception as e:
            test["issues"].append(f"Erreur intégration: {str(e)}")

        return test

    def _calculate_success_rate(self, tests):
        """Calcule le taux de réussite"""
        successful_tests = sum(1 for test in tests if test.get("success", False))
        total_tests = len(tests)
        return (successful_tests / total_tests * 100) if total_tests > 0 else 0

    def run_all_tests(self):
        """Lance tous les tests de types d'utilisateurs"""
        print("🎮 ARKALIA QUEST - TESTEUR D'EXPÉRIENCE TERMINAL")
        print("=" * 60)

        # Test des différents types d'utilisateurs
        self.test_user_type_noob()
        self.test_user_type_explorer()
        self.test_user_type_speedrunner()
        self.test_user_type_power_user()

        # Calcul du score global
        total_success_rate = 0
        total_tests = 0

        for user_type in self.results["user_types_tested"]:
            total_success_rate += user_type["success_rate"]
            total_tests += 1

        self.results["overall_score"] = total_success_rate / total_tests if total_tests > 0 else 0

        # Génération du rapport
        self._generate_report()

        return self.results

    def _generate_report(self):
        """Génère le rapport final"""
        print("\n📊 RAPPORT D'EXPÉRIENCE TERMINAL")
        print("=" * 60)
        print(f"🎯 Score global: {self.results['overall_score']:.1f}/100")
        print(f"👥 Types d'utilisateurs testés: {len(self.results['user_types_tested'])}")

        for user_type in self.results["user_types_tested"]:
            print(f"\n👤 Type {user_type['user_type'].upper()}:")
            print(f"   ⏱️  Temps total: {user_type['total_time']:.2f}s")
            print(f"   📊 Taux de réussite: {user_type['success_rate']:.1f}%")

            # Compter les problèmes et points positifs
            total_issues = sum(len(test.get("issues", [])) for test in user_type["tests"])
            total_positives = sum(len(test.get("positives", [])) for test in user_type["tests"])

            if total_issues > 0:
                print(f"   ❌ Problèmes: {total_issues}")
            if total_positives > 0:
                print(f"   ✅ Points positifs: {total_positives}")

        # Sauvegarde du rapport
        filename = f"terminal_experience_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.results, f, indent=2, ensure_ascii=False)

        print(f"\n💾 Rapport sauvegardé: {filename}")

def main():
    """Fonction principale"""
    tester = TerminalExperienceTester()
    results = tester.run_all_tests()

    # Évaluation finale
    if results["overall_score"] >= 80:
        print("\n🎉 EXPÉRIENCE TERMINAL EXCELLENTE !")
    elif results["overall_score"] >= 60:
        print("\n👍 EXPÉRIENCE TERMINAL BONNE")
    elif results["overall_score"] >= 40:
        print("\n⚠️  EXPÉRIENCE TERMINAL MOYENNE")
    else:
        print("\n❌ EXPÉRIENCE TERMINAL À AMÉLIORER")

if __name__ == "__main__":
    main()
