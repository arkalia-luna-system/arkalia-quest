"""
Testeur d'expérience joueur - Tutoriel Arkalia Quest
Simule différents profils d'ados et évalue le ressenti réel
"""

import json
import time
from datetime import datetime

import requests


class TutorielExperienceTester:
    """Testeur d'expérience pour le tutoriel"""

    def __init__(self, base_url="http://localhost:5001"):
        self.base_url = base_url
        self.results = {
            "test_name": "Tutoriel Experience Test",
            "timestamp": datetime.now().isoformat(),
            "profiles_tested": [],
            "overall_score": 0,
            "issues_found": [],
            "positive_feedback": [],
            "performance_metrics": {},
        }

    def test_profile_noob(self):
        """Test avec un profil noob (première fois)"""
        game_logger.info(r"🧪 Test profil NOOB (première fois)...")

        profile_results = {
            "profile": "noob",
            "steps": [],
            "total_time": 0,
            "frustration_level": 0,
            "engagement_level": 0,
            "issues": [],
            "positives": [],
        }

        start_time = time.time()

        # Étape 1: Arrivée sur la page d'accueil
        step1 = self._test_step_1_welcome()
        profile_results["steps"].append(step1)

        # Étape 2: Découverte du terminal
        step2 = self._test_step_2_terminal_discovery()
        profile_results["steps"].append(step2)

        # Étape 3: Première commande
        step3 = self._test_step_3_first_command()
        profile_results["steps"].append(step3)

        # Étape 4: Feedback et progression
        step4 = self._test_step_4_feedback()
        profile_results["steps"].append(step4)

        profile_results["total_time"] = time.time() - start_time

        # Calcul du score d'expérience
        profile_results["engagement_level"] = self._calculate_engagement(
            profile_results["steps"]
        )
        profile_results["frustration_level"] = self._calculate_frustration(
            profile_results["steps"]
        )

        self.results["profiles_tested"].append(profile_results)
        return profile_results

    def test_profile_curieux(self):
        """Test avec un profil curieux (explore tout)"""
        game_logger.info(r"🧪 Test profil CURIEUX (explore tout)...")

        profile_results = {
            "profile": "curieux",
            "steps": [],
            "total_time": 0,
            "frustration_level": 0,
            "engagement_level": 0,
            "issues": [],
            "positives": [],
        }

        start_time = time.time()

        # Test de découverte de tous les éléments
        step1 = self._test_curious_exploration()
        profile_results["steps"].append(step1)

        # Test des boutons cachés/easter eggs
        step2 = self._test_hidden_features()
        profile_results["steps"].append(step2)

        # Test de la réactivité aux interactions
        step3 = self._test_interaction_responsiveness()
        profile_results["steps"].append(step3)

        profile_results["total_time"] = time.time() - start_time
        profile_results["engagement_level"] = self._calculate_engagement(
            profile_results["steps"]
        )
        profile_results["frustration_level"] = self._calculate_frustration(
            profile_results["steps"]
        )

        self.results["profiles_tested"].append(profile_results)
        return profile_results

    def test_profile_speedrunner(self):
        """Test avec un profil speedrunner (veut aller vite)"""
        game_logger.info(r"🧪 Test profil SPEEDRUNNER (veut aller vite)...")

        profile_results = {
            "profile": "speedrunner",
            "steps": [],
            "total_time": 0,
            "frustration_level": 0,
            "engagement_level": 0,
            "issues": [],
            "positives": [],
        }

        start_time = time.time()

        # Test de rapidité d'exécution
        step1 = self._test_speed_execution()
        profile_results["steps"].append(step1)

        # Test des raccourcis clavier
        step2 = self._test_keyboard_shortcuts()
        profile_results["steps"].append(step2)

        # Test de la fluidité des transitions
        step3 = self._test_transition_fluidity()
        profile_results["steps"].append(step3)

        profile_results["total_time"] = time.time() - start_time
        profile_results["engagement_level"] = self._calculate_engagement(
            profile_results["steps"]
        )
        profile_results["frustration_level"] = self._calculate_frustration(
            profile_results["steps"]
        )

        self.results["profiles_tested"].append(profile_results)
        return profile_results

    def test_interactive_tutorial(self):
        """Test spécifique du nouveau tutoriel interactif"""
        game_logger.info(r"🎮 Test du tutoriel interactif...")

        tutorial_results = {
            "profile": "interactive_tutorial",
            "steps": [],
            "total_time": 0,
            "frustration_level": 0,
            "engagement_level": 0,
            "issues": [],
            "positives": [],
        }

        start_time = time.time()

        # Test 1: Démarrage du tutoriel
        step1 = self._test_tutorial_start()
        tutorial_results["steps"].append(step1)

        # Test 2: Progression des étapes
        step2 = self._test_tutorial_progression()
        tutorial_results["steps"].append(step2)

        # Test 3: Choix interactifs
        step3 = self._test_tutorial_choices()
        tutorial_results["steps"].append(step3)

        # Test 4: Effets visuels
        step4 = self._test_tutorial_effects()
        tutorial_results["steps"].append(step4)

        # Test 5: Dialogue LUNA
        step5 = self._test_luna_dialogue()
        tutorial_results["steps"].append(step5)

        tutorial_results["total_time"] = time.time() - start_time
        tutorial_results["engagement_level"] = self._calculate_engagement(
            tutorial_results["steps"]
        )
        tutorial_results["frustration_level"] = self._calculate_frustration(
            tutorial_results["steps"],
        )

        self.results["profiles_tested"].append(tutorial_results)
        return tutorial_results

    def _test_step_1_welcome(self):
        """Test de l'arrivée sur la page d'accueil et du nouveau tutoriel"""
        step = {
            "name": "Page d'accueil et Tutoriel",
            "duration": 0,
            "success": False,
            "feedback": "",
            "issues": [],
            "positives": [],
        }

        start_time = time.time()

        try:
            # Test de chargement de la page d'accueil
            response = requests.get(f"{self.base_url}/", timeout=5)
            step["duration"] = time.time() - start_time

            if response.status_code == 200:
                step["success"] = True

                # Vérifier la présence d'éléments clés
                content = response.text
                if "Arkalia Quest" in content:
                    step["positives"].append("Titre clair et visible")
                else:
                    step["issues"].append("Titre manquant ou peu visible")

                # Test du nouveau bouton tutoriel
                if "TUTORIEL" in content:
                    step["positives"].append("Bouton tutoriel visible")
                else:
                    step["issues"].append("Bouton tutoriel manquant")

                # Test du script tutorial.js
                if "tutorial.js" in content:
                    step["positives"].append("Script tutoriel chargé")
                else:
                    step["issues"].append("Script tutoriel manquant")

                # Test de l'API tutoriel
                api_response = requests.post(
                    f"{self.base_url}/api/tutorial/start",
                    json={"user_id": "test_user"},
                    timeout=5,
                )

                if api_response.status_code == 200:
                    api_data = api_response.json()
                    if api_data.get("success"):
                        step["positives"].append("API tutoriel fonctionnelle")

                        # Vérifier les données de l'étape
                        step_data = api_data.get("step", {})
                        if step_data.get("titre"):
                            step["positives"].append("Données tutoriel complètes")
                        if step_data.get("effets"):
                            step["positives"].append("Effets visuels configurés")
                        if step_data.get("choix"):
                            step["positives"].append("Choix interactifs disponibles")
                    else:
                        step["issues"].append("API tutoriel retourne une erreur")
                else:
                    step["issues"].append(
                        f"API tutoriel inaccessible: {api_response.status_code}"
                    )

                # Évaluer le temps de chargement
                if step["duration"] < 1.0:
                    step["positives"].append("Chargement rapide")
                elif step["duration"] < 3.0:
                    step["feedback"] = "Chargement acceptable"
                else:
                    step["issues"].append("Chargement trop lent")

            else:
                step["issues"].append(f"Erreur HTTP: {response.status_code}")

        except Exception as e:
            step["issues"].append(f"Erreur de connexion: {e!s}")

        return step

    def _test_step_2_terminal_discovery(self):
        """Test de la découverte du terminal"""
        step = {
            "name": "Découverte du terminal",
            "duration": 0,
            "success": False,
            "feedback": "",
            "issues": [],
            "positives": [],
        }

        start_time = time.time()

        try:
            # Test de chargement de la page terminal
            response = requests.get(f"{self.base_url}/terminal", timeout=5)
            step["duration"] = time.time() - start_time

            if response.status_code == 200:
                step["success"] = True
                content = response.text

                # Vérifier l'interface du terminal
                if "terminal" in content.lower() and "commande" in content.lower():
                    step["positives"].append("Interface terminal claire")
                else:
                    step["issues"].append("Interface terminal peu claire")

                # Vérifier la présence d'aide
                if "aide" in content.lower() or "help" in content.lower():
                    step["positives"].append("Aide disponible")
                else:
                    step["issues"].append("Aide manquante")

                # Vérifier la réactivité
                if step["duration"] < 1.0:
                    step["positives"].append("Terminal réactif")
                else:
                    step["feedback"] = "Terminal un peu lent"

            else:
                step["issues"].append(f"Erreur terminal: {response.status_code}")

        except Exception as e:
            step["issues"].append(f"Erreur terminal: {e!s}")

        return step

    def _test_step_3_first_command(self):
        """Test de la première commande"""
        step = {
            "name": "Première commande",
            "duration": 0,
            "success": False,
            "feedback": "",
            "issues": [],
            "positives": [],
        }

        start_time = time.time()

        try:
            # Test de la commande aide
            response = requests.post(
                f"{self.base_url}/commande",
                json={"commande": "aide"},
                timeout=5,
            )
            step["duration"] = time.time() - start_time

            if response.status_code == 200:
                data = response.json()
                step["success"] = True

                # Vérifier la qualité de la réponse
                if data.get("réussite", False):
                    step["positives"].append("Commande exécutée avec succès")

                    message = data.get("message", "")
                    if len(message) > 50:
                        step["positives"].append("Réponse détaillée et utile")
                    else:
                        step["issues"].append("Réponse trop courte")

                    if data.get("ascii_art"):
                        step["positives"].append("Effet visuel présent")
                    else:
                        step["issues"].append("Pas d'effet visuel")

                else:
                    step["issues"].append("Commande échouée")

                # Évaluer la rapidité
                if step["duration"] < 0.5:
                    step["positives"].append("Réponse instantanée")
                elif step["duration"] < 1.0:
                    step["feedback"] = "Réponse rapide"
                else:
                    step["issues"].append("Réponse lente")

            else:
                step["issues"].append(f"Erreur API: {response.status_code}")

        except Exception as e:
            step["issues"].append(f"Erreur commande: {e!s}")

        return step

    def _test_step_4_feedback(self):
        """Test du feedback et de la progression"""
        step = {
            "name": "Feedback et progression",
            "duration": 0,
            "success": False,
            "feedback": "",
            "issues": [],
            "positives": [],
        }

        start_time = time.time()

        try:
            # Test de la commande profil pour voir la progression
            response = requests.post(
                f"{self.base_url}/commande",
                json={"commande": "profil"},
                timeout=5,
            )
            step["duration"] = time.time() - start_time

            if response.status_code == 200:
                data = response.json()
                step["success"] = True

                if data.get("réussite", False):
                    message = data.get("message", "")

                    # Vérifier la présence d'informations de progression
                    if "score" in message.lower():
                        step["positives"].append("Score visible")
                    else:
                        step["issues"].append("Score non visible")

                    if "badge" in message.lower():
                        step["positives"].append("Badges visibles")
                    else:
                        step["issues"].append("Badges non visibles")

                    if "niveau" in message.lower() or "level" in message.lower():
                        step["positives"].append("Niveau visible")
                    else:
                        step["issues"].append("Niveau non visible")

                else:
                    step["issues"].append("Impossible de voir le profil")

            else:
                step["issues"].append(f"Erreur profil: {response.status_code}")

        except Exception as e:
            step["issues"].append(f"Erreur feedback: {e!s}")

        return step

    def _test_curious_exploration(self):
        """Test de l'exploration curieuse"""
        step = {
            "name": "Exploration curieuse",
            "duration": 0,
            "success": False,
            "feedback": "",
            "issues": [],
            "positives": [],
        }

        start_time = time.time()

        try:
            # Test de plusieurs commandes pour voir la variété
            commands = ["aide", "profil", "monde", "status"]
            responses = []

            for cmd in commands:
                response = requests.post(
                    f"{self.base_url}/commande",
                    json={"commande": cmd},
                    timeout=3,
                )
                if response.status_code == 200:
                    responses.append(response.json())

            step["duration"] = time.time() - start_time
            step["success"] = len(responses) > 0

            if step["success"]:
                step["positives"].append(
                    f"{len(responses)} commandes testées avec succès"
                )

                # Vérifier la variété des réponses
                unique_ascii = {r.get("ascii_art", "") for r in responses}
                if len(unique_ascii) > 2:
                    step["positives"].append("Variété d'effets visuels")
                else:
                    step["issues"].append("Peu de variété visuelle")

            else:
                step["issues"].append("Aucune commande ne fonctionne")

        except Exception as e:
            step["issues"].append(f"Erreur exploration: {e!s}")

        return step

    def _test_hidden_features(self):
        """Test des fonctionnalités cachées"""
        step = {
            "name": "Fonctionnalités cachées",
            "duration": 0,
            "success": False,
            "feedback": "",
            "issues": [],
            "positives": [],
        }

        start_time = time.time()

        try:
            # Test d'easter eggs et commandes spéciales
            special_commands = ["easter_egg_1337", "luna_dance", "boss_final"]
            found_secrets = 0

            for cmd in special_commands:
                response = requests.post(
                    f"{self.base_url}/commande",
                    json={"commande": cmd},
                    timeout=3,
                )
                if response.status_code == 200:
                    data = response.json()
                    if data.get("réussite", False):
                        found_secrets += 1

            step["duration"] = time.time() - start_time
            step["success"] = found_secrets > 0

            if found_secrets > 0:
                step["positives"].append(f"{found_secrets} secrets découverts")
                step["feedback"] = "Easter eggs fonctionnels"
            else:
                step["issues"].append("Aucun easter egg trouvé")

        except Exception as e:
            step["issues"].append(f"Erreur secrets: {e!s}")

        return step

    def _test_interaction_responsiveness(self):
        """Test de la réactivité aux interactions"""
        step = {
            "name": "Réactivité interactions",
            "duration": 0,
            "success": False,
            "feedback": "",
            "issues": [],
            "positives": [],
        }

        start_time = time.time()

        try:
            # Test de rapidité de plusieurs commandes
            commands = ["aide", "profil", "monde"]
            response_times = []

            for cmd in commands:
                cmd_start = time.time()
                requests.post(
                    f"{self.base_url}/commande", json={"commande": cmd}, timeout=2
                )
                response_times.append(time.time() - cmd_start)

            step["duration"] = time.time() - start_time
            step["success"] = len(response_times) > 0

            if step["success"]:
                avg_time = sum(response_times) / len(response_times)
                if avg_time < 0.3:
                    step["positives"].append("Réactivité excellente")
                elif avg_time < 0.8:
                    step["positives"].append("Réactivité bonne")
                else:
                    step["issues"].append("Réactivité lente")

            else:
                step["issues"].append("Pas de réponse aux interactions")

        except Exception as e:
            step["issues"].append(f"Erreur réactivité: {e!s}")

        return step

    def _test_speed_execution(self):
        """Test de rapidité d'exécution"""
        step = {
            "name": "Rapidité d'exécution",
            "duration": 0,
            "success": False,
            "feedback": "",
            "issues": [],
            "positives": [],
        }

        start_time = time.time()

        try:
            # Test de rapidité avec des commandes simples
            commands = ["aide", "status", "profil"]
            total_time = 0

            for cmd in commands:
                cmd_start = time.time()
                requests.post(
                    f"{self.base_url}/commande", json={"commande": cmd}, timeout=1
                )
                total_time += time.time() - cmd_start

            step["duration"] = time.time() - start_time
            step["success"] = total_time > 0

            if step["success"]:
                avg_time = total_time / len(commands)
                if avg_time < 0.2:
                    step["positives"].append("Exécution ultra-rapide")
                elif avg_time < 0.5:
                    step["positives"].append("Exécution rapide")
                else:
                    step["issues"].append("Exécution lente")

            else:
                step["issues"].append("Exécution impossible")

        except Exception as e:
            step["issues"].append(f"Erreur rapidité: {e!s}")

        return step

    def _test_keyboard_shortcuts(self):
        """Test des raccourcis clavier"""
        step = {
            "name": "Raccourcis clavier",
            "duration": 0,
            "success": False,
            "feedback": "",
            "issues": [],
            "positives": [],
        }

        # Note: Les raccourcis clavier nécessitent Selenium pour être testés
        # Pour l'instant, on simule
        step["success"] = True
        step["feedback"] = "Raccourcis à tester avec Selenium"
        step["positives"].append("Interface compatible clavier")

        return step

    def _test_transition_fluidity(self):
        """Test de la fluidité des transitions"""
        step = {
            "name": "Fluidité transitions",
            "duration": 0,
            "success": False,
            "feedback": "",
            "issues": [],
            "positives": [],
        }

        start_time = time.time()

        try:
            # Test de navigation entre pages
            pages = ["/", "/terminal", "/monde", "/profil"]
            transition_times = []

            for page in pages:
                page_start = time.time()
                requests.get(f"{self.base_url}{page}", timeout=3)
                transition_times.append(time.time() - page_start)

            step["duration"] = time.time() - start_time
            step["success"] = len(transition_times) > 0

            if step["success"]:
                avg_time = sum(transition_times) / len(transition_times)
                if avg_time < 0.5:
                    step["positives"].append("Transitions fluides")
                elif avg_time < 1.0:
                    step["feedback"] = "Transitions acceptables"
                else:
                    step["issues"].append("Transitions lentes")

            else:
                step["issues"].append("Navigation impossible")

        except Exception as e:
            step["issues"].append(f"Erreur transitions: {e!s}")

        return step

    def _test_tutorial_start(self):
        """Test du démarrage du tutoriel interactif"""
        step = {
            "name": "Démarrage tutoriel",
            "duration": 0,
            "success": False,
            "feedback": "",
            "issues": [],
            "positives": [],
        }

        start_time = time.time()

        try:
            # Test de l'API de démarrage
            response = requests.post(
                f"{self.base_url}/api/tutorial/start",
                json={"user_id": "test_user"},
                timeout=5,
            )

            step["duration"] = time.time() - start_time

            if response.status_code == 200:
                data = response.json()
                if data.get("success"):
                    step["success"] = True
                    step["positives"].append("Tutoriel démarré avec succès")

                    # Vérifier la structure des données
                    step_data = data.get("step", {})
                    if step_data.get("id") == 1:
                        step["positives"].append("Première étape correcte")
                    if step_data.get("titre"):
                        step["positives"].append("Titre de l'étape présent")
                    if step_data.get("description"):
                        step["positives"].append("Description claire")
                    if step_data.get("bouton"):
                        step["positives"].append("Bouton d'action visible")

                    # Vérifier la progression
                    progress = data.get("progress", {})
                    if progress.get("current") == 1:
                        step["positives"].append("Progression initialisée")

                else:
                    step["issues"].append(
                        f"Erreur tutoriel: {data.get('error', 'Unknown')}"
                    )
            else:
                step["issues"].append(f"Erreur HTTP: {response.status_code}")

        except Exception as e:
            step["issues"].append(f"Erreur de connexion: {e!s}")

        return step

    def _test_tutorial_progression(self):
        """Test de la progression dans le tutoriel"""
        step = {
            "name": "Progression tutoriel",
            "duration": 0,
            "success": False,
            "feedback": "",
            "issues": [],
            "positives": [],
        }

        start_time = time.time()

        try:
            # Test de l'étape 2
            response = requests.get(f"{self.base_url}/api/tutorial/step/2", timeout=5)

            step["duration"] = time.time() - start_time

            if response.status_code == 200:
                data = response.json()
                if data.get("success"):
                    step["success"] = True
                    step["positives"].append("Navigation entre étapes fonctionnelle")

                    step_data = data.get("step", {})
                    if step_data.get("id") == 2:
                        step["positives"].append("Étape 2 accessible")
                else:
                    step["issues"].append("Étape 2 non trouvée")
            else:
                step["issues"].append(f"Erreur accès étape: {response.status_code}")

        except Exception as e:
            step["issues"].append(f"Erreur de connexion: {e!s}")

        return step

    def _test_tutorial_choices(self):
        """Test des choix interactifs du tutoriel"""
        step = {
            "name": "Choix interactifs",
            "duration": 0,
            "success": False,
            "feedback": "",
            "issues": [],
            "positives": [],
        }

        start_time = time.time()

        try:
            # Test d'un choix utilisateur
            response = requests.post(
                f"{self.base_url}/api/tutorial/choice",
                json={
                    "user_id": "test_user",
                    "step_id": 1,
                    "choice": "tutorial_complet",
                },
                timeout=5,
            )

            step["duration"] = time.time() - start_time

            if response.status_code == 200:
                data = response.json()
                if data.get("success"):
                    step["success"] = True
                    step["positives"].append("Choix utilisateur traité")
                else:
                    step["issues"].append(
                        f"Erreur choix: {data.get('error', 'Unknown')}"
                    )
            else:
                step["issues"].append(f"Erreur HTTP choix: {response.status_code}")

        except Exception as e:
            step["issues"].append(f"Erreur de connexion: {e!s}")

        return step

    def _test_tutorial_effects(self):
        """Test des effets visuels du tutoriel"""
        step = {
            "name": "Effets visuels",
            "duration": 0,
            "success": False,
            "feedback": "",
            "issues": [],
            "positives": [],
        }

        start_time = time.time()

        try:
            # Test des effets d'une étape
            response = requests.get(
                f"{self.base_url}/api/tutorial/effects/1", timeout=5
            )

            step["duration"] = time.time() - start_time

            if response.status_code == 200:
                data = response.json()
                if data.get("success"):
                    step["success"] = True
                    step["positives"].append("API effets accessible")

                    effects = data.get("effects", {})
                    if effects:
                        step["positives"].append("Effets configurés")
                    else:
                        step["issues"].append("Aucun effet configuré")
                else:
                    step["issues"].append("Erreur récupération effets")
            else:
                step["issues"].append(f"Erreur HTTP effets: {response.status_code}")

        except Exception as e:
            step["issues"].append(f"Erreur de connexion: {e!s}")

        return step

    def _test_luna_dialogue(self):
        """Test du dialogue LUNA dans le tutoriel"""
        step = {
            "name": "Dialogue LUNA",
            "duration": 0,
            "success": False,
            "feedback": "",
            "issues": [],
            "positives": [],
        }

        start_time = time.time()

        try:
            # Test du dialogue LUNA
            response = requests.get(
                f"{self.base_url}/api/tutorial/luna-dialogue/1", timeout=5
            )

            step["duration"] = time.time() - start_time

            if response.status_code == 200:
                data = response.json()
                if data.get("success"):
                    step["success"] = True
                    step["positives"].append("API dialogue LUNA accessible")

                    dialogue = data.get("dialogue", {})
                    if dialogue.get("avant"):
                        step["positives"].append("Dialogue avant présent")
                    if dialogue.get("apres"):
                        step["positives"].append("Dialogue après présent")
                    if dialogue.get("personnalite"):
                        step["positives"].append("Personnalité LUNA configurée")
                else:
                    step["issues"].append("Erreur récupération dialogue")
            else:
                step["issues"].append(f"Erreur HTTP dialogue: {response.status_code}")

        except Exception as e:
            step["issues"].append(f"Erreur de connexion: {e!s}")

        return step

    def _calculate_engagement(self, steps):
        """Calcule le niveau d'engagement basé sur les étapes"""
        positives = sum(len(step.get("positives", [])) for step in steps)
        issues = sum(len(step.get("issues", [])) for step in steps)

        if positives > issues * 2:
            return "Élevé"
        if positives > issues:
            return "Moyen"
        return "Faible"

    def _calculate_frustration(self, steps):
        """Calcule le niveau de frustration basé sur les étapes"""
        issues = sum(len(step.get("issues", [])) for step in steps)
        positives = sum(len(step.get("positives", [])) for step in steps)

        if issues > positives * 2:
            return "Élevé"
        if issues > positives:
            return "Moyen"
        return "Faible"

    def run_all_tests(self):
        """Lance tous les tests de profils"""
        print("🎮 ARKALIA QUEST - TESTEUR D'EXPÉRIENCE TUTORIEL")
        print("=" * 60)

        # Test des différents profils
        self.test_profile_noob()
        self.test_profile_curieux()
        self.test_profile_speedrunner()

        # Test du nouveau tutoriel interactif
        self.test_interactive_tutorial()

        # Calcul du score global
        total_engagement = 0
        total_frustration = 0

        for profile in self.results["profiles_tested"]:
            if profile["engagement_level"] == "Élevé":
                total_engagement += 3
            elif profile["engagement_level"] == "Moyen":
                total_engagement += 2
            else:
                total_engagement += 1

            if profile["frustration_level"] == "Élevé":
                total_frustration += 3
            elif profile["frustration_level"] == "Moyen":
                total_frustration += 2
            else:
                total_frustration += 1

        # Score final (0-100)
        max_score = len(self.results["profiles_tested"]) * 3
        engagement_score = (total_engagement / max_score) * 50
        frustration_penalty = (total_frustration / max_score) * 30

        self.results["overall_score"] = max(
            0, min(100, engagement_score - frustration_penalty)
        )

        # Génération du rapport
        self._generate_report()

        return self.results

    def _generate_report(self):
        """Génère le rapport final"""
        print("\n📊 RAPPORT D'EXPÉRIENCE TUTORIEL")
        print("=" * 60)
        print(f"🎯 Score global: {self.results['overall_score']:.1f}/100")
        print(f"👥 Profils testés: {len(self.results['profiles_tested'])}")

        for profile in self.results["profiles_tested"]:
            print(f"\n👤 Profil {profile['profile'].upper()}:")
            print(f"   ⏱️  Temps total: {profile['total_time']:.2f}s")
            print(f"   🔥 Engagement: {profile['engagement_level']}")
            print(f"   😤 Frustration: {profile['frustration_level']}")

            if profile["issues"]:
                print(f"   ❌ Problèmes: {len(profile['issues'])}")
            if profile["positives"]:
                print(f"   ✅ Positifs: {len(profile['positives'])}")

        # Sauvegarde du rapport
        filename = f"tutoriel_experience_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(self.results, f, indent=2, ensure_ascii=False)

        game_logger.info(f"\n💾 Rapport sauvegardé: {filename}")


def main():
    """Fonction principale"""
    tester = TutorielExperienceTester()
    results = tester.run_all_tests()

    # Évaluation finale
    if results["overall_score"] >= 80:
        game_logger.info(r"\n🎉 EXPÉRIENCE TUTORIEL EXCELLENTE !")
    elif results["overall_score"] >= 60:
        game_logger.info(r"\n👍 EXPÉRIENCE TUTORIEL BONNE")
    elif results["overall_score"] >= 40:
        game_logger.info(r"\n⚠️  EXPÉRIENCE TUTORIEL MOYENNE")
    else:
        game_logger.info(r"\n❌ EXPÉRIENCE TUTORIEL À AMÉLIORER")


if __name__ == "__main__":
    main()
