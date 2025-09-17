#!/usr/bin/env python3
"""
Test de charge réel pour Arkalia Quest
Simule des utilisateurs réels naviguant sur l'application
"""

import asyncio
import json
import statistics
import time

import aiohttp

# Configuration
BASE_URL = "http://localhost:5001"
CONCURRENT_USERS = 50
REQUESTS_PER_USER = 20
TIMEOUT = 30


class TestChargeReel:
    """Test de charge réel avec simulation d'utilisateurs"""

    def setup_method(self):
        """Configuration avant chaque test"""
        self.results = []
        self.start_time = None
        self.end_time = None

    async def _test_endpoint(self, session: aiohttp.ClientSession, endpoint: str) -> dict:
        """Test un endpoint spécifique (méthode privée)"""
        start_time = time.time()

        try:
            async with session.get(
                f"{BASE_URL}{endpoint}",
                timeout=aiohttp.ClientTimeout(total=TIMEOUT),
            ) as response:
                response_time = time.time() - start_time
                status_code = response.status

                # Lire le contenu pour simuler un utilisateur réel
                content = await response.text()

                return {
                    "endpoint": endpoint,
                    "status_code": status_code,
                    "response_time": response_time,
                    "content_length": len(content),
                    "success": 200 <= status_code < 400,
                }

        except Exception as e:
            response_time = time.time() - start_time
            return {
                "endpoint": endpoint,
                "status_code": 0,
                "response_time": response_time,
                "content_length": 0,
                "success": False,
                "error": str(e),
            }

    async def simulate_user_session(
        self,
        session: aiohttp.ClientSession,
        user_id: int,
    ) -> list[dict]:
        """Simule une session utilisateur complète"""
        user_results = []

        # Endpoints à tester dans un ordre logique
        endpoints = [
            "/",  # Accueil
            "/tutorial",  # Tutoriel
            "/terminal",  # Terminal
            "/profil",  # Profil
            "/dashboard",  # Dashboard
            "/monde",  # Monde
            "/leaderboard",  # Leaderboard
            "/explorateur",  # Explorateur
            "/mail",  # Mail
            "/audio",  # Audio
            "/accessibility",  # Accessibilité
            "/api/profile/summary",  # API profil
            "/api/gamification/summary",  # API gamification
            "/api/tutorial/steps",  # API tutoriel
            "/api/leaderboard",  # API leaderboard
            "/api/educational-games/list",  # API jeux
            "/api/educational-games/stats",  # API stats jeux
        ]

        # Simuler une navigation utilisateur réaliste
        for i, endpoint in enumerate(endpoints):
            # Pause entre les requêtes pour simuler un utilisateur réel
            if i > 0:
                await asyncio.sleep(0.1 + (i * 0.05))

            result = await self._test_endpoint(session, endpoint)
            result["user_id"] = user_id
            result["request_order"] = i
            user_results.append(result)

            # Simuler des erreurs occasionnelles (comme dans la vraie vie)
            if i % 7 == 0:  # Tous les 7 endpoints
                await asyncio.sleep(0.5)  # Pause plus longue

        return user_results

    async def run_load_test(self):
        """Lance le test de charge complet"""
        print(f"🚀 Démarrage du test de charge avec {CONCURRENT_USERS} utilisateurs simultanés")
        print(f"📊 {REQUESTS_PER_USER} requêtes par utilisateur")
        print(f"⏱️  Timeout: {TIMEOUT}s")
        print("-" * 60)

        self.start_time = time.time()

        # Configuration de la session HTTP
        connector = aiohttp.TCPConnector(limit=100, limit_per_host=50)
        timeout = aiohttp.ClientTimeout(total=TIMEOUT)

        async with aiohttp.ClientSession(connector=connector, timeout=timeout) as session:
            # Créer les tâches pour tous les utilisateurs
            tasks = []
            for user_id in range(CONCURRENT_USERS):
                task = self.simulate_user_session(session, user_id)
                tasks.append(task)

            # Exécuter toutes les tâches en parallèle
            print("🔄 Exécution des sessions utilisateur...")
            user_sessions = await asyncio.gather(*tasks, return_exceptions=True)

            # Collecter tous les résultats
            for session_result in user_sessions:
                if isinstance(session_result, list):
                    self.results.extend(session_result)
                else:
                    print(f"❌ Erreur dans la session: {session_result}")

        self.end_time = time.time()

        # Analyser les résultats
        self.analyze_results()

    def analyze_results(self):
        """Analyse les résultats du test de charge"""
        if not self.results:
            print("❌ Aucun résultat à analyser")
            return

        total_requests = len(self.results)
        successful_requests = sum(1 for r in self.results if r["success"])
        failed_requests = total_requests - successful_requests

        # Statistiques de temps de réponse
        response_times = [r["response_time"] for r in self.results if r["success"]]

        if response_times:
            avg_response_time = statistics.mean(response_times)
            median_response_time = statistics.median(response_times)
            min_response_time = min(response_times)
            max_response_time = max(response_times)
            p95_response_time = (
                statistics.quantiles(response_times, n=20)[18]
                if len(response_times) >= 20
                else max_response_time
            )
        else:
            avg_response_time = median_response_time = min_response_time = max_response_time = (
                p95_response_time
            ) = 0

        # Statistiques par endpoint
        endpoint_stats = {}
        for result in self.results:
            endpoint = result["endpoint"]
            if endpoint not in endpoint_stats:
                endpoint_stats[endpoint] = {"total": 0, "success": 0, "times": []}

            endpoint_stats[endpoint]["total"] += 1
            if result["success"]:
                endpoint_stats[endpoint]["success"] += 1
                endpoint_stats[endpoint]["times"].append(result["response_time"])

        # Calcul du débit
        total_time = self.end_time - self.start_time
        throughput = total_requests / total_time if total_time > 0 else 0

        # Affichage des résultats
        print("\n" + "=" * 60)
        print("📊 RÉSULTATS DU TEST DE CHARGE")
        print("=" * 60)

        print(f"⏱️  Durée totale: {total_time:.2f}s")
        print(f"📈 Débit: {throughput:.2f} req/s")
        print(f"📊 Total des requêtes: {total_requests}")
        print(
            f"✅ Requêtes réussies: {successful_requests} ({successful_requests / total_requests * 100:.1f}%)",
        )
        print(
            f"❌ Requêtes échouées: {failed_requests} ({failed_requests / total_requests * 100:.1f}%)",
        )

        print("\n⏱️  TEMPS DE RÉPONSE:")
        print(f"   Moyenne: {avg_response_time * 1000:.1f}ms")
        print(f"   Médiane: {median_response_time * 1000:.1f}ms")
        print(f"   Min: {min_response_time * 1000:.1f}ms")
        print(f"   Max: {max_response_time * 1000:.1f}ms")
        print(f"   95e percentile: {p95_response_time * 1000:.1f}ms")

        print("\n🌐 STATISTIQUES PAR ENDPOINT:")
        for endpoint, stats in endpoint_stats.items():
            success_rate = stats["success"] / stats["total"] * 100 if stats["total"] > 0 else 0
            avg_time = statistics.mean(stats["times"]) * 1000 if stats["times"] else 0
            print(f"   {endpoint}: {success_rate:.1f}% succès, {avg_time:.1f}ms moy")

        # Évaluation de la performance
        print("\n🎯 ÉVALUATION DE LA PERFORMANCE:")

        if successful_requests / total_requests >= 0.95:
            print("   ✅ Taux de succès: EXCELLENT (>95%)")
        elif successful_requests / total_requests >= 0.90:
            print("   🟡 Taux de succès: BON (90-95%)")
        else:
            print("   ❌ Taux de succès: À AMÉLIORER (<90%)")

        if avg_response_time < 0.5:
            print("   ✅ Temps de réponse: EXCELLENT (<500ms)")
        elif avg_response_time < 1.0:
            print("   🟡 Temps de réponse: BON (500ms-1s)")
        else:
            print("   ❌ Temps de réponse: À AMÉLIORER (>1s)")

        if throughput >= 10:
            print("   ✅ Débit: EXCELLENT (>10 req/s)")
        elif throughput >= 5:
            print("   🟡 Débit: BON (5-10 req/s)")
        else:
            print("   ❌ Débit: À AMÉLIORER (<5 req/s)")

        # Recommandations
        print("\n💡 RECOMMANDATIONS:")
        if failed_requests > 0:
            print("   • Analyser les erreurs pour identifier les points faibles")

        if avg_response_time > 1.0:
            print("   • Optimiser les requêtes lentes")
            print("   • Vérifier la base de données et les requêtes")

        if throughput < 5:
            print("   • Augmenter la capacité du serveur")
            print("   • Optimiser le code et la base de données")

        # Sauvegarder les résultats
        self.save_results()

    def save_results(self):
        """Sauvegarde les résultats dans un fichier JSON"""
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        filename = f"load_test_results_{timestamp}.json"

        results_summary = {
            "timestamp": timestamp,
            "test_config": {
                "concurrent_users": CONCURRENT_USERS,
                "requests_per_user": REQUESTS_PER_USER,
                "timeout": TIMEOUT,
            },
            "summary": {
                "total_requests": len(self.results),
                "successful_requests": sum(1 for r in self.results if r["success"]),
                "failed_requests": sum(1 for r in self.results if not r["success"]),
                "total_time": self.end_time - self.start_time if self.end_time else 0,
            },
            "detailed_results": self.results,
        }

        try:
            with open(filename, "w", encoding="utf-8") as f:
                json.dump(results_summary, f, indent=2, ensure_ascii=False)
            print(f"\n💾 Résultats sauvegardés dans: {filename}")
        except Exception as e:
            print(f"❌ Erreur lors de la sauvegarde: {e}")

    def test_load_test_class_initialization(self):
        """Test que la classe TestChargeReel s'initialise correctement"""
        # Ce test vérifie que la classe peut être instanciée
        # et que les méthodes de base fonctionnent
        test_instance = TestChargeReel()
        test_instance.setup_method()

        # Vérifier que les attributs sont initialisés
        assert test_instance.results == []
        assert test_instance.start_time is None
        assert test_instance.end_time is None

        print("✅ Test d'initialisation de la classe TestChargeReel réussi")


async def main():
    """Fonction principale"""
    print("🌌 ARKALIA QUEST - TEST DE CHARGE RÉEL")
    print("=" * 50)

    # Vérifier que l'application est accessible
    try:
        async with (
            aiohttp.ClientSession() as session,
            session.get(f"{BASE_URL}/health", timeout=5) as response,
        ):
            if response.status != 200:
                print(f"❌ L'application n'est pas accessible (status: {response.status})")
                return
            print("✅ Application accessible, démarrage du test...")
    except Exception as e:
        print(f"❌ Impossible de se connecter à l'application: {e}")
        print("   Assurez-vous que l'application Flask est démarrée sur http://localhost:5001")
        return

    # Lancer le test
    load_tester = TestChargeReel()
    await load_tester.run_load_test()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n⏹️  Test interrompu par l'utilisateur")
    except Exception as e:
        print(f"\n❌ Erreur lors du test: {e}")
