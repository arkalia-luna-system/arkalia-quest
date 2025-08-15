#!/usr/bin/env python3
"""
🧪 Test Complet du Système Immersif - Arkalia Quest
Test intégré du système d'émotions LUNA et des effets visuels
"""

import json
import random
import time
from datetime import datetime
from typing import Any, Dict

import requests


class ImmersiveSystemTester:
    """Testeur complet du système immersif"""

    def __init__(self, base_url: str = "http://localhost:5001"):
        self.base_url = base_url
        self.session = requests.Session()
        self.test_results = []
        self.luna_emotions_seen = set()
        self.effects_triggered = set()

        # Données de test
        self.test_commands = [
            "aide",
            "profil",
            "hack_system",
            "kill_virus",
            "find_shadow",
            "luna_contact",
            "luna_engine",
            "luna_analyze",
            "badges",
            "monde",
            "commande_inexistante_test"
        ]

    def run_complete_test(self) -> Dict[str, Any]:
        """Lance le test complet du système immersif"""
        print("🌟 TEST COMPLET DU SYSTÈME IMMERSIF ARKALIA QUEST")
        print("=" * 60)

        start_time = time.time()

        # Tests du système d'émotions LUNA
        print("\n🌙 TEST 1: SYSTÈME D'ÉMOTIONS LUNA")
        luna_results = self.test_luna_emotions()

        # Tests des effets visuels
        print("\n🎨 TEST 2: EFFETS VISUELS IMMERSIFS")
        visual_results = self.test_visual_effects()

        # Tests d'intégration
        print("\n🔗 TEST 3: INTÉGRATION COMPLÈTE")
        integration_results = self.test_integration()

        # Tests de performance
        print("\n⚡ TEST 4: PERFORMANCE ET STABILITÉ")
        performance_results = self.test_performance()

        end_time = time.time()
        total_duration = end_time - start_time

        # Compilation des résultats
        results = {
            "timestamp": datetime.now().isoformat(),
            "duration": total_duration,
            "luna_emotions": luna_results,
            "visual_effects": visual_results,
            "integration": integration_results,
            "performance": performance_results,
            "summary": self.generate_summary(luna_results, visual_results, integration_results, performance_results)
        }

        # Sauvegarder les résultats
        self.save_results(results)

        # Afficher le résumé
        self.display_summary(results)

        return results

    def test_luna_emotions(self) -> Dict[str, Any]:
        """Test du système d'émotions LUNA"""
        print("  🧪 Test des émotions LUNA...")

        emotions_test = {
            "total_commands": 0,
            "emotions_detected": 0,
            "emotion_types": set(),
            "intensity_range": {"min": 1.0, "max": 0.0},
            "response_times": [],
            "errors": []
        }

        for command in self.test_commands:
            try:
                start_time = time.time()

                response = self.session.post(
                    f"{self.base_url}/commande",
                    json={"commande": command},
                    timeout=10
                )

                response_time = time.time() - start_time
                emotions_test["response_times"].append(response_time)

                if response.status_code == 200:
                    data = response.json()
                    # Adapter pour parser la clé 'reponse'
                    if "reponse" in data:
                        data = data["reponse"]
                    emotions_test["total_commands"] += 1

                    # Vérifier la présence d'émotions LUNA
                    if "luna_emotion" in data:
                        emotions_test["emotions_detected"] += 1
                        emotions_test["emotion_types"].add(data["luna_emotion"])
                        self.luna_emotions_seen.add(data["luna_emotion"])

                        # Vérifier l'intensité
                        intensity = data.get("luna_intensity", 0.5)
                        emotions_test["intensity_range"]["min"] = min(emotions_test["intensity_range"]["min"], intensity)
                        emotions_test["intensity_range"]["max"] = max(emotions_test["intensity_range"]["max"], intensity)

                        # Vérifier la cohérence
                        self.validate_emotion_data(data)

                        print(f"    ✅ {command}: {data['luna_emotion']} (intensité: {intensity:.2f})")
                    else:
                        print(f"    ⚠️ {command}: Pas d'émotion LUNA détectée")
                        emotions_test["errors"].append(f"Pas d'émotion pour {command}")
                else:
                    print(f"    ❌ {command}: Erreur HTTP {response.status_code}")
                    emotions_test["errors"].append(f"HTTP {response.status_code} pour {command}")

            except Exception as e:
                print(f"    💥 {command}: Erreur - {str(e)}")
                emotions_test["errors"].append(f"Exception pour {command}: {str(e)}")

        # Calculer les statistiques
        emotions_test["emotion_types"] = list(emotions_test["emotion_types"])
        emotions_test["avg_response_time"] = sum(emotions_test["response_times"]) / len(emotions_test["response_times"]) if emotions_test["response_times"] else 0
        emotions_test["success_rate"] = (emotions_test["emotions_detected"] / emotions_test["total_commands"]) * 100 if emotions_test["total_commands"] > 0 else 0

        return emotions_test

    def test_visual_effects(self) -> Dict[str, Any]:
        """Test des effets visuels"""
        print("  🎨 Test des effets visuels...")

        effects_test = {
            "effects_detected": 0,
            "effect_types": set(),
            "colors_detected": set(),
            "sounds_detected": set(),
            "errors": []
        }

        # Tester avec des commandes qui déclenchent des effets
        effect_commands = ["hack_system", "kill_virus", "luna_contact", "luna_engine"]

        for command in effect_commands:
            try:
                response = self.session.post(
                    f"{self.base_url}/commande",
                    json={"commande": command},
                    timeout=10
                )

                if response.status_code == 200:
                    data = response.json()
                    # Adapter pour parser la clé 'reponse'
                    if "reponse" in data:
                        data = data["reponse"]

                    # Vérifier les effets
                    if "luna_effect" in data:
                        effects_test["effects_detected"] += 1
                        effects_test["effect_types"].add(data["luna_effect"])
                        self.effects_triggered.add(data["luna_effect"])

                    if "luna_color" in data:
                        effects_test["colors_detected"].add(data["luna_color"])

                    if "luna_sound" in data:
                        effects_test["sounds_detected"].add(data["luna_sound"])

                    print(f"    ✅ {command}: Effet {data.get('luna_effect', 'N/A')} - Couleur {data.get('luna_color', 'N/A')}")
                else:
                    print(f"    ❌ {command}: Erreur HTTP {response.status_code}")
                    effects_test["errors"].append(f"HTTP {response.status_code} pour {command}")

            except Exception as e:
                print(f"    💥 {command}: Erreur - {str(e)}")
                effects_test["errors"].append(f"Exception pour {command}: {str(e)}")

        # Convertir les sets en listes
        effects_test["effect_types"] = list(effects_test["effect_types"])
        effects_test["colors_detected"] = list(effects_test["colors_detected"])
        effects_test["sounds_detected"] = list(effects_test["sounds_detected"])

        return effects_test

    def test_integration(self) -> Dict[str, Any]:
        """Test d'intégration complète"""
        print("  🔗 Test d'intégration...")

        integration_test = {
            "integration_checks": 0,
            "integration_success": 0,
            "coherence_checks": 0,
            "coherence_success": 0,
            "errors": []
        }

        # Test de cohérence émotion-effet
        for command in self.test_commands[:5]:  # Test avec 5 commandes
            try:
                response = self.session.post(
                    f"{self.base_url}/commande",
                    json={"commande": command},
                    timeout=10
                )

                if response.status_code == 200:
                    data = response.json()
                    # Adapter pour parser la clé 'reponse'
                    if "reponse" in data:
                        data = data["reponse"]
                    integration_test["integration_checks"] += 1

                    # Vérifier la cohérence
                    if self.check_emotion_effect_coherence(data):
                        integration_test["integration_success"] += 1
                        print(f"    ✅ {command}: Cohérence émotion-effet OK")
                    else:
                        print(f"    ⚠️ {command}: Incohérence émotion-effet détectée")
                        integration_test["errors"].append(f"Incohérence pour {command}")

                    # Vérifier la structure des données
                    if self.validate_response_structure(data):
                        integration_test["coherence_success"] += 1
                    else:
                        integration_test["errors"].append(f"Structure invalide pour {command}")

                    integration_test["coherence_checks"] += 1

            except Exception as e:
                print(f"    💥 {command}: Erreur - {str(e)}")
                integration_test["errors"].append(f"Exception pour {command}: {str(e)}")

        # Calculer les taux de réussite
        integration_test["integration_rate"] = (integration_test["integration_success"] / integration_test["integration_checks"]) * 100 if integration_test["integration_checks"] > 0 else 0
        integration_test["coherence_rate"] = (integration_test["coherence_success"] / integration_test["coherence_checks"]) * 100 if integration_test["coherence_checks"] > 0 else 0

        return integration_test

    def test_performance(self) -> Dict[str, Any]:
        """Test de performance"""
        print("  ⚡ Test de performance...")

        performance_test = {
            "total_requests": 0,
            "successful_requests": 0,
            "response_times": [],
            "errors": [],
            "stress_test_results": {}
        }

        # Test de charge simple
        print("    🚀 Test de charge (10 requêtes simultanées)...")

        import queue
        import threading

        results_queue = queue.Queue()

        def make_request(command, request_id):
            try:
                start_time = time.time()
                response = self.session.post(
                    f"{self.base_url}/commande",
                    json={"commande": command},
                    timeout=5
                )
                response_time = time.time() - start_time

                # Adapter pour parser la clé 'reponse'
                data = None
                if response.status_code == 200:
                    try:
                        data = response.json()
                        if "reponse" in data:
                            data = data["reponse"]
                    except Exception:
                        pass

                results_queue.put({
                    "request_id": request_id,
                    "success": response.status_code == 200,
                    "response_time": response_time,
                    "status_code": response.status_code,
                    "data": data
                })
            except Exception as e:
                results_queue.put({
                    "request_id": request_id,
                    "success": False,
                    "response_time": 0,
                    "error": str(e)
                })

        # Lancer 10 requêtes simultanées
        threads = []
        for i in range(10):
            command = random.choice(self.test_commands)
            thread = threading.Thread(target=make_request, args=(command, i))
            threads.append(thread)
            thread.start()

        # Attendre la fin de tous les threads
        for thread in threads:
            thread.join()

        # Collecter les résultats
        while not results_queue.empty():
            result = results_queue.get()
            performance_test["total_requests"] += 1

            if result["success"]:
                performance_test["successful_requests"] += 1
                performance_test["response_times"].append(result["response_time"])
            else:
                performance_test["errors"].append(f"Requête {result['request_id']}: Échec")

        # Calculer les statistiques
        if performance_test["response_times"]:
            performance_test["avg_response_time"] = sum(performance_test["response_times"]) / len(performance_test["response_times"])
            performance_test["min_response_time"] = min(performance_test["response_times"])
            performance_test["max_response_time"] = max(performance_test["response_times"])
        else:
            performance_test["avg_response_time"] = 0
            performance_test["min_response_time"] = 0
            performance_test["max_response_time"] = 0

        performance_test["success_rate"] = (performance_test["successful_requests"] / performance_test["total_requests"]) * 100 if performance_test["total_requests"] > 0 else 0

        print(f"    📊 Performance: {performance_test['success_rate']:.1f}% succès, {performance_test['avg_response_time']:.3f}s moyenne")

        return performance_test

    def validate_emotion_data(self, data: Dict[str, Any]) -> bool:
        """Valide les données d'émotion"""
        required_fields = ["luna_emotion", "luna_intensity", "luna_color", "luna_effect", "luna_sound"]

        for field in required_fields:
            if field not in data:
                return False

        # Vérifier les types
        if not isinstance(data["luna_emotion"], str):
            return False
        if not isinstance(data["luna_intensity"], (int, float)):
            return False
        if not isinstance(data["luna_color"], str):
            return False
        if not isinstance(data["luna_effect"], str):
            return False
        if not isinstance(data["luna_sound"], str):
            return False

        # Vérifier les bornes
        if not (0.0 <= data["luna_intensity"] <= 1.0):
            return False

        return True

    def check_emotion_effect_coherence(self, data: Dict[str, Any]) -> bool:
        """Vérifie la cohérence émotion-effet"""
        if "luna_emotion" not in data or "luna_effect" not in data:
            return False

        # Mapping émotion-effet attendu
        expected_mapping = {
            "excited": "pulse_green",
            "worried": "shake_orange",
            "proud": "sparkle_magenta",
            "mysterious": "fade_cyan",
            "determined": "glow_red",
            "playful": "bounce_yellow",
            "focused": "zoom_blue",
            "surprised": "flash_pink",
            "calm": "float_lightblue",
            "energetic": "vibrate_green"
        }

        emotion = data["luna_emotion"]
        effect = data["luna_effect"]

        return expected_mapping.get(emotion) == effect

    def validate_response_structure(self, data: Dict[str, Any]) -> bool:
        """Valide la structure de la réponse"""
        required_fields = ["réussite", "message"]

        for field in required_fields:
            if field not in data:
                return False

        return True

    def generate_summary(self, luna_results: Dict, visual_results: Dict, integration_results: Dict, performance_results: Dict) -> Dict[str, Any]:
        """Génère un résumé des tests"""
        total_tests = (
            luna_results.get("total_commands", 0) +
            len(visual_results.get("effect_types", [])) +
            integration_results.get("integration_checks", 0) +
            performance_results.get("total_requests", 0)
        )

        total_success = (
            luna_results.get("emotions_detected", 0) +
            visual_results.get("effects_detected", 0) +
            integration_results.get("integration_success", 0) +
            performance_results.get("successful_requests", 0)
        )

        overall_success_rate = (total_success / total_tests) * 100 if total_tests > 0 else 0

        return {
            "total_tests": total_tests,
            "total_success": total_success,
            "overall_success_rate": overall_success_rate,
            "emotions_detected": len(self.luna_emotions_seen),
            "effects_triggered": len(self.effects_triggered),
            "avg_response_time": performance_results.get("avg_response_time", 0),
            "status": "EXCELLENT" if overall_success_rate >= 90 else "BON" if overall_success_rate >= 75 else "MOYEN" if overall_success_rate >= 50 else "MAUVAIS"
        }

    def save_results(self, results: Dict[str, Any]):
        """Sauvegarde les résultats"""
        filename = f"tests/results/immersive_system_test_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"

        # Créer le dossier si nécessaire
        import os
        os.makedirs("tests/results", exist_ok=True)

        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)

        print(f"\n💾 Résultats sauvegardés dans: {filename}")

    def display_summary(self, results: Dict[str, Any]):
        """Affiche le résumé des tests"""
        summary = results["summary"]

        print("\n" + "=" * 60)
        print("📊 RÉSUMÉ DU TEST IMMERSIF COMPLET")
        print("=" * 60)

        print(f"🎯 TAUX DE RÉUSSITE GLOBAL: {summary['overall_success_rate']:.1f}%")
        print(f"📈 STATUT: {summary['status']}")
        print(f"⏱️ TEMPS TOTAL: {results['duration']:.2f} secondes")
        print(f"🌙 ÉMOTIONS DÉTECTÉES: {summary['emotions_detected']}")
        print(f"🎨 EFFETS DÉCLENCHÉS: {summary['effects_triggered']}")
        print(f"⚡ TEMPS DE RÉPONSE MOYEN: {summary['avg_response_time']:.3f}s")

        print("\n📋 DÉTAILS:")
        print(f"  • Tests LUNA: {results['luna_emotions']['emotions_detected']}/{results['luna_emotions']['total_commands']} émotions détectées")
        print(f"  • Tests visuels: {results['visual_effects']['effects_detected']} effets détectés")
        print(f"  • Tests intégration: {results['integration']['integration_success']}/{results['integration']['integration_checks']} cohérences OK")
        print(f"  • Tests performance: {results['performance']['successful_requests']}/{results['performance']['total_requests']} requêtes réussies")

        if summary['status'] == "EXCELLENT":
            print("\n🎉 SYSTÈME IMMERSIF PARFAIT ! LUNA est prête à bluffer les ados !")
        elif summary['status'] == "BON":
            print("\n👍 SYSTÈME IMMERSIF FONCTIONNEL ! Quelques ajustements mineurs recommandés.")
        else:
            print("\n⚠️ SYSTÈME IMMERSIF À AMÉLIORER ! Des corrections sont nécessaires.")


def main():
    """Fonction principale"""
    print("🌟 TEST COMPLET DU SYSTÈME IMMERSIF ARKALIA QUEST")
    print("=" * 60)

    # Vérifier que le serveur est accessible
    try:
        response = requests.get("http://localhost:5001/api/status", timeout=5)
        if response.status_code != 200:
            print("❌ Serveur non accessible. Assurez-vous qu'Arkalia Quest est démarré sur le port 5001.")
            return False
    except:
        print("❌ Impossible de se connecter au serveur. Assurez-vous qu'Arkalia Quest est démarré.")
        return False

    # Lancer les tests
    tester = ImmersiveSystemTester()
    results = tester.run_complete_test()

    return results["summary"]["status"] in ["EXCELLENT", "BON"]


if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
