#!/usr/bin/env python3
"""
🧪 TESTS DES AMÉLIORATIONS UX ADOLESCENT - ARKALIA QUEST
Teste toutes les nouvelles fonctionnalités pour captiver les ados de 14 ans
"""

import json
from datetime import datetime

import requests


class TeenUXImprovementsTester:
    """Testeur des améliorations UX pour adolescents"""

    def __init__(self, base_url="http://localhost:5001"):
        self.base_url = base_url
        self.results = {
            "test_name": "Teen UX Improvements Test",
            "timestamp": datetime.now().isoformat(),
            "tests": [],
            "overall_score": 0,
            "improvements_tested": [],
            "issues_found": [],
            "recommendations": [],
        }

    def test_daily_challenges_system(self):
        """Test du système de défis quotidiens"""
        print("🎯 Test du système de défis quotidiens...")

        test = {
            "name": "Défis quotidiens",
            "success": False,
            "features_tested": [],
            "issues": [],
            "score": 0,
        }

        try:
            # Test de la commande daily_challenges
            response = requests.post(
                f"{self.base_url}/commande",
                json={"commande": "daily_challenges"},
                timeout=5,
            )

            if response.status_code == 200:
                data = response.json()
                response_data = data.get("reponse", data)
                if response_data.get("réussite", False):
                    test["success"] = True
                    test["score"] += 25
                    test["features_tested"].append(
                        "Commande daily_challenges fonctionne"
                    )

                    # Vérifier le contenu des défis
                    message = response_data.get("message", "")
                    if "Speed Hacker" in message:
                        test["score"] += 25
                        test["features_tested"].append("Défi Speed Hacker présent")
                    if "Code Master" in message:
                        test["score"] += 25
                        test["features_tested"].append("Défi Code Master présent")
                    if "Social Butterfly" in message:
                        test["score"] += 25
                        test["features_tested"].append("Défi Social Butterfly présent")

                    # Vérifier les barres de progression
                    if "█" in message and "░" in message:
                        test["score"] += 25
                        test["features_tested"].append(
                            "Barres de progression visuelles"
                        )
                    else:
                        test["issues"].append("Barres de progression manquantes")

                else:
                    test["issues"].append("Commande daily_challenges échouée")
            else:
                test["issues"].append(f"Erreur HTTP: {response.status_code}")

        except Exception as e:
            test["issues"].append(f"Erreur de test: {e!s}")

        self.results["tests"].append(test)
        return test

    def test_random_events_system(self):
        """Test du système d'événements aléatoires"""
        print("🎲 Test du système d'événements aléatoires...")

        test = {
            "name": "Événements aléatoires",
            "success": False,
            "features_tested": [],
            "issues": [],
            "score": 0,
        }

        try:
            # Test de la commande random_events
            response = requests.post(
                f"{self.base_url}/commande",
                json={"commande": "random_events"},
                timeout=5,
            )

            if response.status_code == 200:
                data = response.json()
                response_data = data.get("reponse", data)
                if response_data.get("réussite", False):
                    test["success"] = True
                    test["score"] += 25
                    test["features_tested"].append("Commande random_events fonctionne")

                    # Vérifier le contenu des événements
                    message = response_data.get("message", "")
                    if "Surprise LUNA" in message:
                        test["score"] += 25
                        test["features_tested"].append(
                            "Événement Surprise LUNA présent"
                        )
                    if "Badge Secret" in message:
                        test["score"] += 25
                        test["features_tested"].append("Événement Badge Secret présent")
                    if "Glitch Matrix" in message:
                        test["score"] += 25
                        test["features_tested"].append(
                            "Événement Glitch Matrix présent"
                        )

                    # Vérifier les informations de déclenchement
                    if "Déclencheur" in message and "Chance" in message:
                        test["score"] += 25
                        test["features_tested"].append(
                            "Informations de déclenchement présentes"
                        )
                    else:
                        test["issues"].append(
                            "Informations de déclenchement manquantes"
                        )

                else:
                    test["issues"].append("Commande random_events échouée")
            else:
                test["issues"].append(f"Erreur HTTP: {response.status_code}")

        except Exception as e:
            test["issues"].append(f"Erreur de test: {e!s}")

        self.results["tests"].append(test)
        return test

    def test_interactive_missions(self):
        """Test des missions interactives progressives"""
        print("🎮 Test des missions interactives...")

        test = {
            "name": "Missions interactives",
            "success": False,
            "features_tested": [],
            "issues": [],
            "score": 0,
        }

        try:
            # Test de la commande acte_1
            response = requests.post(
                f"{self.base_url}/commande", json={"commande": "acte_1"}, timeout=5
            )

            if response.status_code == 200:
                data = response.json()
                response_data = data.get("reponse", data)
                if response_data.get("réussite", False):
                    test["success"] = True
                    test["score"] += 25
                    test["features_tested"].append("Commande acte_1 fonctionne")

                    # Vérifier la progression de mission
                    if "mission_progress" in response_data:
                        test["score"] += 25
                        test["features_tested"].append(
                            "Progression de mission présente"
                        )
                    else:
                        test["issues"].append("Progression de mission manquante")

                    # Vérifier l'objectif suivant
                    if "next_action" in data:
                        test["score"] += 25
                        test["features_tested"].append("Objectif suivant défini")
                    else:
                        test["issues"].append("Objectif suivant manquant")

                    # Vérifier la progression visuelle
                    message = data.get("message", "")
                    if "1/4 étapes" in message:
                        test["score"] += 25
                        test["features_tested"].append("Progression visuelle présente")
                    else:
                        test["issues"].append("Progression visuelle manquante")

                else:
                    test["issues"].append("Commande acte_1 échouée")
            else:
                test["issues"].append(f"Erreur HTTP: {response.status_code}")

        except Exception as e:
            test["issues"].append(f"Erreur de test: {e!s}")

        self.results["tests"].append(test)
        return test

    def test_progressive_hack_system(self):
        """Test du système de hack progressif"""
        print("💻 Test du système de hack progressif...")

        test = {
            "name": "Hack progressif",
            "success": False,
            "features_tested": [],
            "issues": [],
            "score": 0,
        }

        try:
            # Test de la commande hack_system (étape 1)
            response = requests.post(
                f"{self.base_url}/commande", json={"commande": "hack_system"}, timeout=5
            )

            if response.status_code == 200:
                data = response.json()
                response_data = data.get("reponse", data)
                if response_data.get("réussite", False):
                    test["success"] = True
                    test["score"] += 25
                    test["features_tested"].append("Commande hack_system fonctionne")

                    # Vérifier la progression étape par étape
                    if "hack_progress" in response_data:
                        test["score"] += 25
                        test["features_tested"].append("Progression hack présente")
                    else:
                        test["issues"].append("Progression hack manquante")

                    # Vérifier l'étape actuelle
                    if "next_step" in data:
                        test["score"] += 25
                        test["features_tested"].append("Étape suivante définie")
                    else:
                        test["issues"].append("Étape suivante manquante")

                    # Vérifier la progression visuelle
                    message = data.get("message", "")
                    if "1/3 étapes" in message:
                        test["score"] += 25
                        test["features_tested"].append(
                            "Progression visuelle hack présente"
                        )
                    else:
                        test["issues"].append("Progression visuelle hack manquante")

                else:
                    test["issues"].append("Commande hack_system échouée")
            else:
                test["issues"].append(f"Erreur HTTP: {response.status_code}")

        except Exception as e:
            test["issues"].append(f"Erreur de test: {e!s}")

        self.results["tests"].append(test)
        return test

    def test_matrix_theme_consistency(self):
        """Test de la cohérence du thème Matrix"""
        print("🌐 Test de la cohérence du thème Matrix...")

        test = {
            "name": "Thème Matrix",
            "success": False,
            "features_tested": [],
            "issues": [],
            "score": 0,
        }

        try:
            # Test de la page d'accueil
            response = requests.get(f"{self.base_url}/", timeout=5)

            if response.status_code == 200:
                content = response.text
                test["success"] = True
                test["score"] += 25
                test["features_tested"].append("Page d'accueil accessible")

                # Vérifier les couleurs Matrix
                if "#00ff00" in content or "matrix" in content.lower():
                    test["score"] += 25
                    test["features_tested"].append("Couleurs Matrix présentes")
                else:
                    test["issues"].append("Couleurs Matrix manquantes")

                # Vérifier les animations Matrix
                if "matrix" in content.lower():
                    test["score"] += 25
                    test["features_tested"].append("Animations Matrix présentes")
                else:
                    test["issues"].append("Animations Matrix manquantes")

                # Vérifier la cohérence visuelle
                if "arkalia-luna-vision.css" in content:
                    test["score"] += 25
                    test["features_tested"].append("CSS Matrix chargé")
                else:
                    test["issues"].append("CSS Matrix manquant")

            else:
                test["issues"].append(f"Erreur HTTP: {response.status_code}")

        except Exception as e:
            test["issues"].append(f"Erreur de test: {e!s}")

        self.results["tests"].append(test)
        return test

    def run_all_tests(self):
        """Lance tous les tests d'améliorations UX"""
        print("🧪 ARKALIA QUEST - TESTS DES AMÉLIORATIONS UX ADOLESCENT")
        print("=" * 70)

        # Tests des nouvelles fonctionnalités
        self.test_daily_challenges_system()
        self.test_random_events_system()
        self.test_interactive_missions()
        self.test_progressive_hack_system()
        self.test_matrix_theme_consistency()

        # Calcul du score global
        total_score = 0
        total_tests = len(self.results["tests"])

        for test in self.results["tests"]:
            total_score += test["score"]

        self.results["overall_score"] = (
            (total_score / (total_tests * 100)) * 100 if total_tests > 0 else 0
        )

        # Génération du rapport
        self._generate_report()

        return self.results

    def _generate_report(self):
        """Génère le rapport final des tests"""
        print("\n📊 RAPPORT DES AMÉLIORATIONS UX ADOLESCENT")
        print("=" * 70)
        print(f"🎯 Score global: {self.results['overall_score']:.1f}/100")
        print(f"🧪 Tests effectués: {len(self.results['tests'])}")

        for test in self.results["tests"]:
            print(f"\n🎮 {test['name'].upper()}:")
            print(f"   📊 Score: {test['score']}/100")
            print(f"   ✅ Succès: {'Oui' if test['success'] else 'Non'}")

            if test["features_tested"]:
                print(f"   🌟 Fonctionnalités testées: {len(test['features_tested'])}")
                for feature in test["features_tested"]:
                    print(f"      • {feature}")

            if test["issues"]:
                print(f"   ❌ Problèmes: {len(test['issues'])}")
                for issue in test["issues"]:
                    print(f"      • {issue}")

        # Sauvegarde du rapport
filename =
f"teen_ux_improvements_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(self.results, f, indent=2, ensure_ascii=False)

        print(f"\n💾 Rapport sauvegardé: {filename}")


def main():
    """Fonction principale"""
    tester = TeenUXImprovementsTester()
    results = tester.run_all_tests()

    # Évaluation finale
    if results["overall_score"] >= 80:
        print("\n🎉 AMÉLIORATIONS UX EXCELLENTES POUR ADOS !")
    elif results["overall_score"] >= 60:
        print("\n👍 AMÉLIORATIONS UX BONNES POUR ADOS")
    elif results["overall_score"] >= 40:
        print("\n⚠️  AMÉLIORATIONS UX MOYENNES POUR ADOS")
    else:
        print("\n❌ AMÉLIORATIONS UX INSUFFISANTES POUR ADOS")


if __name__ == "__main__":
    main()
