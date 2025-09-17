#!/usr/bin/env python3
"""
🧪 TESTS DE CHARGE - ARKALIA QUEST
Tests de performance sous charge pour valider la scalabilité
"""

import statistics
import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Any, Optional

import requests


class LoadTester:
    """Testeur de charge professionnel pour Arkalia Quest"""

    def __init__(self, base_url: str = "http://localhost:5000"):
        self.base_url = base_url
        self.results = {
            "total_requests": 0,
            "successful_requests": 0,
            "failed_requests": 0,
            "response_times": [],
            "errors": [],
            "start_time": None,
            "end_time": None,
        }
        self.lock = threading.Lock()

    def make_request(
        self,
        endpoint: str,
        method: str = "GET",
        data: Optional[dict[str, Any]] = None,
    ) -> dict[str, Any]:
        """Effectue une requête et mesure le temps de réponse"""
        start_time = time.time()

        try:
            if method == "GET":
                response = requests.get(f"{self.base_url}{endpoint}", timeout=10)
            elif method == "POST":
                response = requests.post(
                    f"{self.base_url}{endpoint}", json=data, timeout=10
                )
            else:
                raise ValueError(f"Méthode non supportée: {method}")

            response_time = time.time() - start_time

            with self.lock:
                self.results["total_requests"] += 1
                self.results["response_times"].append(response_time)

                if response.status_code == 200:
                    self.results["successful_requests"] += 1
                else:
                    self.results["failed_requests"] += 1
                    self.results["errors"].append(
                        {
                            "endpoint": endpoint,
                            "status_code": response.status_code,
                            "response": response.text[:200],
                        },
                    )

            return {
                "success": response.status_code == 200,
                "status_code": response.status_code,
                "response_time": response_time,
                "response_size": len(response.content),
            }

        except Exception as e:
            response_time = time.time() - start_time

            with self.lock:
                self.results["total_requests"] += 1
                self.results["failed_requests"] += 1
                self.results["errors"].append({"endpoint": endpoint, "error": str(e)})

            return {"success": False, "error": str(e), "response_time": response_time}

    def run_load_test(
        self,
        endpoints: list[dict[str, Any]],
        concurrent_users: int = 10,
        duration: int = 60,
    ) -> dict[str, Any]:
        """Lance un test de charge"""
        print(
            f"🚀 Démarrage du test de charge: {concurrent_users} utilisateurs, {duration}s"
        )

        self.results["start_time"] = time.time()
        end_time = self.results["start_time"] + duration

        # Fonction pour un utilisateur
        def user_workload():
            while time.time() < end_time:
                for endpoint_config in endpoints:
                    endpoint = endpoint_config["endpoint"]
                    method = endpoint_config.get("method", "GET")
                    data = endpoint_config.get("data")

                    self.make_request(endpoint, method, data)

                    # Pause entre requêtes
                    time.sleep(endpoint_config.get("delay", 0.1))

        # Lancer les utilisateurs concurrents
        with ThreadPoolExecutor(max_workers=concurrent_users) as executor:
            futures = [executor.submit(user_workload) for _ in range(concurrent_users)]

            # Attendre la fin du test
            for future in as_completed(futures):
                try:
                    future.result()
                except Exception as e:
                    print(f"❌ Erreur utilisateur: {e}")

        self.results["end_time"] = time.time()
        return self.generate_report()

    def generate_report(self) -> dict[str, Any]:
        """Génère un rapport de test de charge"""
        if not self.results["response_times"]:
            return {"error": "Aucune requête effectuée"}

        total_time = self.results["end_time"] - self.results["start_time"]
        response_times = self.results["response_times"]

        report = {
            "test_summary": {
                "total_duration": total_time,
                "total_requests": self.results["total_requests"],
                "successful_requests": self.results["successful_requests"],
                "failed_requests": self.results["failed_requests"],
                "success_rate": (
                    self.results["successful_requests"] / self.results["total_requests"]
                )
                * 100,
            },
            "performance_metrics": {
                "requests_per_second": self.results["total_requests"] / total_time,
                "average_response_time": statistics.mean(response_times),
                "median_response_time": statistics.median(response_times),
                "min_response_time": min(response_times),
                "max_response_time": max(response_times),
                "p95_response_time": sorted(response_times)[
                    int(len(response_times) * 0.95)
                ],
                "p99_response_time": sorted(response_times)[
                    int(len(response_times) * 0.99)
                ],
            },
            "errors": self.results["errors"][:10],  # Top 10 erreurs
            "recommendations": self._generate_recommendations(),
        }

        return report

    def _generate_recommendations(self) -> list[str]:
        """Génère des recommandations basées sur les résultats"""
        recommendations = []

        success_rate = (
            self.results["successful_requests"] / self.results["total_requests"]
        ) * 100
        if success_rate < 95:
            recommendations.append(
                "🔴 Taux de succès trop faible - Vérifier la stabilité du système",
            )

        avg_response_time = statistics.mean(self.results["response_times"])
        if avg_response_time > 1.0:
            recommendations.append(
                "⚠️ Temps de réponse moyen élevé - Optimiser les performances"
            )

        if self.results["failed_requests"] > 0:
            recommendations.append(
                "🔧 Erreurs détectées - Analyser les logs et corriger"
            )

        if not recommendations:
            recommendations.append(
                "✅ Performance excellente - Système stable et rapide"
            )

        return recommendations


def run_comprehensive_load_test():
    """Lance un test de charge complet"""
    print("🧪 TESTS DE CHARGE COMPLETS - ARKALIA QUEST")
    print("=" * 60)

    # Configuration des tests
    endpoints = [
        {"endpoint": "/", "delay": 0.5},  # Page d'accueil
        {"endpoint": "/terminal", "delay": 0.3},  # Terminal
        {
            "endpoint": "/commande",
            "method": "POST",
            "data": {"commande": "aide"},
            "delay": 0.2,
        },  # API commande
        {"endpoint": "/api/status", "delay": 0.1},  # API status
        {"endpoint": "/static/css/style.css", "delay": 0.1},  # Asset statique
    ]

    # Tests avec différents niveaux de charge
    test_scenarios = [
        {"users": 5, "duration": 30, "name": "Charge légère"},
        {"users": 10, "duration": 30, "name": "Charge moyenne"},
        {"users": 20, "duration": 30, "name": "Charge élevée"},
    ]

    tester = LoadTester()

    for scenario in test_scenarios:
        print(
            f"\n🎯 {scenario['name']}: {scenario['users']} utilisateurs, {scenario['duration']}s"
        )
        print("-" * 40)

        report = tester.run_load_test(
            endpoints=endpoints,
            concurrent_users=scenario["users"],
            duration=scenario["duration"],
        )

        if "error" not in report:
            summary = report["test_summary"]
            performance = report["performance_metrics"]

            print("📊 Résultats:")
            print(f"   Requêtes totales: {summary['total_requests']}")
            print(f"   Taux de succès: {summary['success_rate']:.1f}%")
            print(f"   Requêtes/seconde: {performance['requests_per_second']:.1f}")
            print(
                f"   Temps réponse moyen: {performance['average_response_time']:.3f}s"
            )
            print(f"   Temps réponse P95: {performance['p95_response_time']:.3f}s")

            if report["recommendations"]:
                print("\n💡 Recommandations:")
                for rec in report["recommendations"]:
                    print(f"   {rec}")
        else:
            print(f"❌ Erreur: {report['error']}")

    # Rapport final
    print("\n🎉 Test de charge terminé!")
    print("=" * 60)


if __name__ == "__main__":
    run_comprehensive_load_test()
