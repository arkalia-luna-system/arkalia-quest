#!/usr/bin/env python3
"""
⚡ ARKALIA QUEST - TESTEUR PERFORMANCE & STRESS
===============================================

Ce testeur valide :
- Performance sous charge
- Tests de stress avancés
- Métriques de performance
- Limites du système
- Stabilité en production

Auteur: Assistant IA
Version: 1.0
"""

import requests
import time
import threading
import json
import statistics
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
from typing import Dict, List, Any, Tuple

class PerformanceStressTester:
    """Testeur de performance et stress"""
    
    def __init__(self):
        self.base_url = "http://localhost:5001"
        self.results = {
            "performance": {},
            "stress": {},
            "limits": {},
            "metrics": {}
        }
        
        # Endpoints à tester
        self.endpoints = [
            "/", "/terminal", "/monde", "/profil", "/api/status",
            "/api/leaderboard", "/api/gamification/summary"
        ]
        
        # Commandes à tester
        self.commands = [
            "aide", "profil", "status", "badges", "missions"
        ]
    
    def log(self, message: str):
        """Log avec timestamp"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"[{timestamp}] {message}")
    
    def measure_response_time(self, url: str, method: str = "GET", data: Dict = None) -> Tuple[float, int, bool]:
        """Mesure le temps de réponse d'un endpoint"""
        start_time = time.time()
        success = False
        status_code = 0
        
        try:
            if method == "GET":
                response = requests.get(url, timeout=10)
            else:
                response = requests.post(url, json=data, timeout=10)
            
            status_code = response.status_code
            success = response.status_code == 200
            
        except Exception as e:
            self.log(f"Erreur {url}: {e}")
        
        end_time = time.time()
        response_time = end_time - start_time
        
        return response_time, status_code, success
    
    def test_single_performance(self):
        """Test de performance simple"""
        self.log("⚡ Test de performance simple...")
        
        results = []
        
        for endpoint in self.endpoints:
            response_time, status_code, success = self.measure_response_time(f"{self.base_url}{endpoint}")
            
            if success:
                results.append(response_time)
                self.log(f"✅ {endpoint}: {response_time:.3f}s")
            else:
                self.log(f"❌ {endpoint}: {response_time:.3f}s (HTTP {status_code})")
        
        if results:
            avg_time = statistics.mean(results)
            min_time = min(results)
            max_time = max(results)
            
            self.results["performance"]["simple"] = {
                "avg_response_time": avg_time,
                "min_response_time": min_time,
                "max_response_time": max_time,
                "total_requests": len(results),
                "successful_requests": len(results)
            }
            
            self.log(f"📊 Performance: {avg_time:.3f}s (min: {min_time:.3f}s, max: {max_time:.3f}s)")
    
    def test_concurrent_performance(self, num_workers: int = 10, requests_per_worker: int = 20):
        """Test de performance concurrente"""
        self.log(f"🔥 Test de performance concurrente ({num_workers} workers, {requests_per_worker} req/worker)...")
        
        def worker(worker_id: int) -> List[float]:
            """Worker pour les tests concurrents"""
            worker_results = []
            
            for i in range(requests_per_worker):
                endpoint = self.endpoints[i % len(self.endpoints)]
                response_time, status_code, success = self.measure_response_time(f"{self.base_url}{endpoint}")
                
                if success:
                    worker_results.append(response_time)
                
                time.sleep(0.1)  # Pause entre requêtes
            
            return worker_results
        
        # Lancer les workers
        all_results = []
        with ThreadPoolExecutor(max_workers=num_workers) as executor:
            futures = [executor.submit(worker, i) for i in range(num_workers)]
            
            for future in as_completed(futures):
                worker_results = future.result()
                all_results.extend(worker_results)
        
        if all_results:
            avg_time = statistics.mean(all_results)
            min_time = min(all_results)
            max_time = max(all_results)
            p95_time = statistics.quantiles(all_results, n=20)[18]  # 95th percentile
            
            self.results["performance"]["concurrent"] = {
                "avg_response_time": avg_time,
                "min_response_time": min_time,
                "max_response_time": max_time,
                "p95_response_time": p95_time,
                "total_requests": len(all_results),
                "successful_requests": len(all_results),
                "workers": num_workers,
                "requests_per_worker": requests_per_worker
            }
            
            self.log(f"📊 Concurrent: {avg_time:.3f}s (p95: {p95_time:.3f}s, {len(all_results)} req)")
    
    def test_stress_gradual(self):
        """Test de stress graduel"""
        self.log("💥 Test de stress graduel...")
        
        stress_levels = [1, 2, 5, 10, 15, 20]  # Nombre de workers
        stress_results = []
        
        for num_workers in stress_levels:
            self.log(f"🔥 Test avec {num_workers} workers...")
            
            start_time = time.time()
            success_count = 0
            total_requests = 0
            
            def stress_worker():
                nonlocal success_count, total_requests
                
                for _ in range(10):  # 10 requêtes par worker
                    endpoint = self.endpoints[0]  # Page principale
                    response_time, status_code, success = self.measure_response_time(f"{self.base_url}{endpoint}")
                    
                    total_requests += 1
                    if success:
                        success_count += 1
                    
                    time.sleep(0.05)  # Pause courte
            
            # Lancer les workers
            threads = []
            for i in range(num_workers):
                thread = threading.Thread(target=stress_worker)
                threads.append(thread)
                thread.start()
            
            # Attendre la fin
            for thread in threads:
                thread.join()
            
            end_time = time.time()
            duration = end_time - start_time
            
            success_rate = (success_count / total_requests * 100) if total_requests > 0 else 0
            requests_per_second = total_requests / duration if duration > 0 else 0
            
            stress_results.append({
                "workers": num_workers,
                "success_rate": success_rate,
                "requests_per_second": requests_per_second,
                "total_requests": total_requests,
                "successful_requests": success_count,
                "duration": duration
            })
            
            self.log(f"📊 {num_workers} workers: {success_rate:.1f}% succès, {requests_per_second:.1f} req/s")
            
            # Arrêter si le taux de succès chute trop
            if success_rate < 80:
                self.log(f"⚠️ Taux de succès trop bas ({success_rate:.1f}%), arrêt du test")
                break
        
        self.results["stress"]["gradual"] = stress_results
        
        # Trouver la limite
        max_workers = 0
        for result in stress_results:
            if result["success_rate"] >= 90:
                max_workers = result["workers"]
        
        self.results["limits"]["max_concurrent_users"] = max_workers
        self.log(f"🎯 Limite détectée: {max_workers} utilisateurs concurrents")
    
    def test_command_performance(self):
        """Test de performance des commandes"""
        self.log("⌨️ Test de performance des commandes...")
        
        command_results = {}
        
        for cmd in self.commands:
            response_times = []
            
            # Tester chaque commande 10 fois
            for _ in range(10):
                response_time, status_code, success = self.measure_response_time(
                    f"{self.base_url}/commande",
                    method="POST",
                    data={"commande": cmd}
                )
                
                if success:
                    response_times.append(response_time)
                
                time.sleep(0.1)
            
            if response_times:
                avg_time = statistics.mean(response_times)
                min_time = min(response_times)
                max_time = max(response_times)
                
                command_results[cmd] = {
                    "avg_response_time": avg_time,
                    "min_response_time": min_time,
                    "max_response_time": max_time,
                    "total_requests": len(response_times)
                }
                
                self.log(f"✅ {cmd}: {avg_time:.3f}s (min: {min_time:.3f}s, max: {max_time:.3f}s)")
        
        self.results["performance"]["commands"] = command_results
    
    def test_memory_usage(self):
        """Test d'utilisation mémoire (simulation)"""
        self.log("🧠 Test d'utilisation mémoire...")
        
        # Simuler l'utilisation mémoire en faisant beaucoup de requêtes
        memory_test_results = []
        
        for batch_size in [10, 50, 100, 200]:
            self.log(f"🧠 Test mémoire avec {batch_size} requêtes...")
            
            start_time = time.time()
            success_count = 0
            
            # Faire des requêtes en batch
            for i in range(batch_size):
                response_time, status_code, success = self.measure_response_time(f"{self.base_url}/")
                
                if success:
                    success_count += 1
                
                if i % 10 == 0:  # Pause tous les 10
                    time.sleep(0.1)
            
            end_time = time.time()
            duration = end_time - start_time
            
            success_rate = (success_count / batch_size * 100) if batch_size > 0 else 0
            requests_per_second = batch_size / duration if duration > 0 else 0
            
            memory_test_results.append({
                "batch_size": batch_size,
                "success_rate": success_rate,
                "requests_per_second": requests_per_second,
                "duration": duration
            })
            
            self.log(f"📊 Batch {batch_size}: {success_rate:.1f}% succès, {requests_per_second:.1f} req/s")
        
        self.results["performance"]["memory"] = memory_test_results
    
    def generate_performance_report(self) -> str:
        """Génère un rapport de performance"""
        report = f"""
⚡ RAPPORT DE PERFORMANCE & STRESS - ARKALIA QUEST
=================================================

📊 PERFORMANCE SIMPLE
---------------------
"""
        
        if "simple" in self.results["performance"]:
            simple = self.results["performance"]["simple"]
            report += f"""
- Temps de réponse moyen: {simple['avg_response_time']:.3f}s
- Temps minimum: {simple['min_response_time']:.3f}s
- Temps maximum: {simple['max_response_time']:.3f}s
- Requêtes réussies: {simple['successful_requests']}/{simple['total_requests']}
"""
        
        if "concurrent" in self.results["performance"]:
            concurrent = self.results["performance"]["concurrent"]
            report += f"""
📊 PERFORMANCE CONCURRENTE
--------------------------
- Temps de réponse moyen: {concurrent['avg_response_time']:.3f}s
- P95: {concurrent['p95_response_time']:.3f}s
- Workers: {concurrent['workers']}
- Requêtes par worker: {concurrent['requests_per_worker']}
- Total requêtes: {concurrent['total_requests']}
"""
        
        if "commands" in self.results["performance"]:
            report += f"""
⌨️ PERFORMANCE DES COMMANDES
----------------------------
"""
            for cmd, data in self.results["performance"]["commands"].items():
                report += f"- {cmd}: {data['avg_response_time']:.3f}s\n"
        
        if "limits" in self.results:
            limits = self.results["limits"]
            report += f"""
🎯 LIMITES DÉTECTÉES
--------------------
- Utilisateurs concurrents max: {limits.get('max_concurrent_users', 'N/A')}
"""
        
        if "stress" in self.results and "gradual" in self.results["stress"]:
            report += f"""
💥 TESTS DE STRESS
------------------
"""
            for result in self.results["stress"]["gradual"]:
                report += f"- {result['workers']} workers: {result['success_rate']:.1f}% succès, {result['requests_per_second']:.1f} req/s\n"
        
        # Recommandations
        report += f"""
🎯 RECOMMANDATIONS
------------------
"""
        
        if "simple" in self.results["performance"]:
            avg_time = self.results["performance"]["simple"]["avg_response_time"]
            if avg_time < 0.5:
                report += "✅ Performance excellente - Prêt pour la production\n"
            elif avg_time < 1.0:
                report += "✅ Performance correcte - Quelques optimisations possibles\n"
            else:
                report += "⚠️ Performance lente - Optimisations nécessaires\n"
        
        if "limits" in self.results:
            max_users = self.results["limits"]["max_concurrent_users"]
            if max_users >= 10:
                report += "✅ Capacité concurrente excellente\n"
            elif max_users >= 5:
                report += "✅ Capacité concurrente correcte\n"
            else:
                report += "⚠️ Capacité concurrente limitée\n"
        
        return report
    
    def run_all_tests(self):
        """Exécute tous les tests de performance"""
        self.log("🚀 DÉMARRAGE DES TESTS DE PERFORMANCE & STRESS")
        self.log("=" * 50)
        
        # Tests de performance
        self.test_single_performance()
        self.test_concurrent_performance()
        self.test_command_performance()
        self.test_memory_usage()
        
        # Tests de stress
        self.test_stress_gradual()
        
        # Rapport final
        report = self.generate_performance_report()
        print(report)
        
        # Sauvegarder les résultats
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        with open(f"performance_stress_results_{timestamp}.json", "w", encoding="utf-8") as f:
            json.dump(self.results, f, indent=2, ensure_ascii=False)
        
        self.log(f"📄 Résultats sauvegardés: performance_stress_results_{timestamp}.json")
        
        return self.results

def main():
    """Fonction principale"""
    print("⚡ ARKALIA QUEST - TESTEUR PERFORMANCE & STRESS")
    print("=" * 50)
    
    tester = PerformanceStressTester()
    results = tester.run_all_tests()
    
    # Évaluer les résultats
    if "simple" in results["performance"]:
        avg_time = results["performance"]["simple"]["avg_response_time"]
        if avg_time < 1.0:
            print("\n🎉 PERFORMANCE EXCELLENTE !")
            return 0
        else:
            print("\n⚠️ PERFORMANCE À AMÉLIORER")
            return 1
    
    return 0

if __name__ == "__main__":
    exit(main()) 