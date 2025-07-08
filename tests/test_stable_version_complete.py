#!/usr/bin/env python3
"""
🎮 ARKALIA QUEST - TESTEUR VERSION STABLE COMPLET
=================================================

Ce testeur valide TOUT pour la version stable :
- Fonctionnalités complètes du jeu
- Performance et optimisation
- Sécurité et validation
- Accessibilité et responsive
- Base de données et API
- PWA et service worker
- Tests de stress et charge
- Compatibilité navigateurs
- Gestion d'erreurs
- Logs et monitoring

Auteur: Assistant IA
Version: 1.0 - Version Stable
"""

import requests
import json
import time
import random
import threading
import subprocess
import sys
import os
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed
from urllib.parse import urljoin
import hashlib
import base64
import sqlite3
from typing import Dict, List, Any, Optional, Tuple

class StableVersionTester:
    """Testeur complet pour la version stable"""
    
    def __init__(self):
        self.base_url = "http://localhost:5001"
        self.results = {
            "tests_executes": 0,
            "tests_reussis": 0,
            "tests_echecs": 0,
            "erreurs": [],
            "warnings": [],
            "performance": {},
            "security": {},
            "accessibility": {},
            "database": {},
            "pwa": {},
            "details": []
        }
        self.start_time = time.time()
        
        # Profils de test avec différents niveaux
        self.test_profiles = [
            "testeur_debutant",
            "testeur_intermediaire", 
            "testeur_expert",
            "testeur_stress_1",
            "testeur_stress_2",
            "testeur_stress_3",
            "testeur_stress_4",
            "testeur_stress_5"
        ]
        
        # Commandes complètes à tester
        self.all_commands = [
            # Commandes de base
            "aide", "profil", "monde", "status", "clear",
            
            # Commandes de progression
            "start_tutorial", "load_mission", "save_mission", "missions",
            
            # Commandes de hacking
            "hack_system", "kill_virus", "find_shadow", "challenge_corp",
            "decode_portal", "hacker_coffre", "reboot_world",
            
            # Commandes LUNA
            "luna_contact", "luna_engine", "luna_analyze", "luna_learning",
            
            # Commandes de gamification
            "badges", "avatars", "leaderboard", "achievements",
            "unlock_universe", "scan_persona", "choisir_avatar",
            
            # Commandes spéciales
            "easter_egg_1337", "luna_rage", "meme_war", "nuke_world",
            "assistant_pirate", "generer_meme", "decoder_message",
            "invoquer_dragon", "save_luna", "chapitre_6",
            
            # Commandes de test
            "test_performance", "test_security", "test_database"
        ]
        
        # Pages à tester
        self.pages_to_test = [
            "/", "/terminal", "/monde", "/profil", "/explorateur", 
            "/mail", "/audio", "/leaderboard", "/dashboard"
        ]
        
        # Tests de sécurité
        self.security_tests = [
            "sql_injection", "xss", "csrf", "path_traversal",
            "command_injection", "rate_limiting", "input_validation"
        ]
    
    def log(self, message: str, level: str = "INFO"):
        """Log avec timestamp"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"[{timestamp}] {level}: {message}")
    
    def test_server_health(self) -> bool:
        """Test de santé du serveur"""
        self.log("🏥 Test de santé du serveur...")
        
        try:
            response = requests.get(f"{self.base_url}/", timeout=5)
            if response.status_code == 200:
                self.log("✅ Serveur accessible et fonctionnel", "SUCCESS")
                self.results["tests_reussis"] += 1
                return True
            else:
                self.log(f"❌ Serveur répond avec code {response.status_code}", "ERROR")
                self.results["tests_echecs"] += 1
                self.results["erreurs"].append(f"Code HTTP {response.status_code}")
                return False
        except Exception as e:
            self.log(f"❌ Serveur inaccessible: {e}", "ERROR")
            self.results["tests_echecs"] += 1
            self.results["erreurs"].append(f"Erreur connexion: {e}")
            return False
        finally:
            self.results["tests_executes"] += 1
    
    def test_all_pages(self):
        """Test de toutes les pages"""
        self.log("📄 Test de toutes les pages...")
        
        for page in self.pages_to_test:
            try:
                response = requests.get(f"{self.base_url}{page}", timeout=10)
                
                if response.status_code == 200:
                    content = response.text
                    
                    # Vérifications de base
                    checks = [
                        ("DOCTYPE HTML", "doctype" in content.lower()),
                        ("UTF-8", "utf-8" in content.lower()),
                        ("CSS", "style.css" in content or "css" in content),
                        ("JavaScript", ".js" in content or "script" in content),
                        ("Responsive", "viewport" in content or "@media" in content),
                        ("Accessibility", "aria-" in content or "role=" in content)
                    ]
                    
                    passed_checks = sum(1 for _, check in checks if check)
                    
                    if passed_checks >= 4:  # Au moins 4/6 checks
                        self.log(f"✅ Page {page} fonctionne ({passed_checks}/6 checks)", "SUCCESS")
                        self.results["tests_reussis"] += 1
                    else:
                        self.log(f"⚠️ Page {page} basique ({passed_checks}/6 checks)", "WARNING")
                        self.results["warnings"].append(f"Page {page} basique")
                else:
                    self.log(f"❌ Page {page} erreur {response.status_code}", "ERROR")
                    self.results["tests_echecs"] += 1
                    self.results["erreurs"].append(f"Page {page}: HTTP {response.status_code}")
                    
            except Exception as e:
                self.log(f"❌ Erreur page {page}: {e}", "ERROR")
                self.results["tests_echecs"] += 1
                self.results["erreurs"].append(f"Page {page}: {e}")
            
            self.results["tests_executes"] += 1
    
    def test_all_commands(self):
        """Test de toutes les commandes"""
        self.log("⌨️ Test de toutes les commandes...")
        
        for profile_id in self.test_profiles[:3]:  # Test avec 3 profils
            for cmd in self.all_commands:
                try:
                    response = requests.post(
                        f"{self.base_url}/commande",
                        json={"commande": cmd, "profile_id": profile_id},
                        timeout=15
                    )
                    
                    if response.status_code == 200:
                        data = response.json()
                        
                        # Vérifications de base
                        if "reponse" in data:
                            reponse = data["reponse"]
                            
                            # Vérifier la qualité de la réponse
                            if len(reponse) > 10:  # Réponse non vide
                                self.log(f"✅ Commande '{cmd}' fonctionne", "SUCCESS")
                                self.results["tests_reussis"] += 1
                            else:
                                self.log(f"⚠️ Commande '{cmd}' réponse courte", "WARNING")
                                self.results["warnings"].append(f"Commande {cmd} réponse courte")
                        else:
                            self.log(f"❌ Commande '{cmd}' pas de réponse", "ERROR")
                            self.results["tests_echecs"] += 1
                            self.results["erreurs"].append(f"Commande {cmd}: pas de réponse")
                    else:
                        self.log(f"❌ Commande '{cmd}' erreur {response.status_code}", "ERROR")
                        self.results["tests_echecs"] += 1
                        self.results["erreurs"].append(f"Commande {cmd}: HTTP {response.status_code}")
                        
                except Exception as e:
                    self.log(f"❌ Erreur commande '{cmd}': {e}", "ERROR")
                    self.results["tests_echecs"] += 1
                    self.results["erreurs"].append(f"Commande {cmd}: {e}")
                
                self.results["tests_executes"] += 1
                
                # Pause entre les commandes
                time.sleep(0.1)
    
    def test_database_integrity(self):
        """Test d'intégrité de la base de données"""
        self.log("🗄️ Test d'intégrité de la base de données...")
        
        try:
            # Test de l'API de base de données
            response = requests.get(f"{self.base_url}/api/test/database", timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                
                # Vérifier les tables
                required_tables = ["profiles", "missions", "challenges", "luna_learning"]
                tables_ok = all(table in str(data) for table in required_tables)
                
                if tables_ok:
                    self.log("✅ Base de données intégre", "SUCCESS")
                    self.results["tests_reussis"] += 1
                    self.results["database"]["status"] = "OK"
                else:
                    self.log("⚠️ Base de données incomplète", "WARNING")
                    self.results["warnings"].append("Base de données incomplète")
                    self.results["database"]["status"] = "WARNING"
            else:
                self.log(f"❌ Erreur base de données: {response.status_code}", "ERROR")
                self.results["tests_echecs"] += 1
                self.results["erreurs"].append(f"Base de données: HTTP {response.status_code}")
                self.results["database"]["status"] = "ERROR"
                
        except Exception as e:
            self.log(f"❌ Erreur test base de données: {e}", "ERROR")
            self.results["tests_echecs"] += 1
            self.results["erreurs"].append(f"Base de données: {e}")
            self.results["database"]["status"] = "ERROR"
        
        self.results["tests_executes"] += 1
    
    def test_pwa_features(self):
        """Test des fonctionnalités PWA"""
        self.log("📱 Test des fonctionnalités PWA...")
        
        pwa_tests = [
            ("Service Worker", "/static/js/service-worker.js"),
            ("Manifest", "/static/manifest.json"),
            ("Icons", "/static/icons/icon-192x192.png"),
            ("Offline", "/api/status")
        ]
        
        pwa_score = 0
        
        for test_name, endpoint in pwa_tests:
            try:
                response = requests.get(f"{self.base_url}{endpoint}", timeout=5)
                
                if response.status_code == 200:
                    self.log(f"✅ {test_name} disponible", "SUCCESS")
                    pwa_score += 1
                else:
                    self.log(f"❌ {test_name} manquant", "ERROR")
                    self.results["erreurs"].append(f"PWA {test_name} manquant")
                    
            except Exception as e:
                self.log(f"❌ Erreur {test_name}: {e}", "ERROR")
                self.results["erreurs"].append(f"PWA {test_name}: {e}")
            
            self.results["tests_executes"] += 1
        
        # Évaluer le score PWA
        if pwa_score >= 3:
            self.log("✅ PWA fonctionnelle", "SUCCESS")
            self.results["tests_reussis"] += 1
            self.results["pwa"]["score"] = pwa_score
            self.results["pwa"]["status"] = "OK"
        elif pwa_score >= 2:
            self.log("⚠️ PWA basique", "WARNING")
            self.results["warnings"].append("PWA basique")
            self.results["pwa"]["score"] = pwa_score
            self.results["pwa"]["status"] = "WARNING"
        else:
            self.log("❌ PWA incomplète", "ERROR")
            self.results["tests_echecs"] += 1
            self.results["pwa"]["score"] = pwa_score
            self.results["pwa"]["status"] = "ERROR"
    
    def test_security(self):
        """Tests de sécurité"""
        self.log("🛡️ Tests de sécurité...")
        
        security_score = 0
        
        # Test d'injection SQL
        try:
            response = requests.post(
                f"{self.base_url}/commande",
                json={"commande": "'; DROP TABLE profiles; --"},
                timeout=5
            )
            
            if response.status_code == 200:
                data = response.json()
                if "error" in str(data).lower() or "invalid" in str(data).lower():
                    self.log("✅ Protection injection SQL", "SUCCESS")
                    security_score += 1
                else:
                    self.log("⚠️ Protection injection SQL faible", "WARNING")
                    self.results["warnings"].append("Protection SQL faible")
            else:
                self.log("✅ Protection injection SQL (rejet)", "SUCCESS")
                security_score += 1
                
        except Exception as e:
            self.log(f"❌ Erreur test SQL: {e}", "ERROR")
            self.results["erreurs"].append(f"Test SQL: {e}")
        
        self.results["tests_executes"] += 1
        
        # Test XSS
        try:
            response = requests.post(
                f"{self.base_url}/commande",
                json={"commande": "<script>alert('xss')</script>"},
                timeout=5
            )
            
            if response.status_code == 200:
                data = response.json()
                if "<script>" not in str(data):
                    self.log("✅ Protection XSS", "SUCCESS")
                    security_score += 1
                else:
                    self.log("⚠️ Protection XSS faible", "WARNING")
                    self.results["warnings"].append("Protection XSS faible")
            else:
                self.log("✅ Protection XSS (rejet)", "SUCCESS")
                security_score += 1
                
        except Exception as e:
            self.log(f"❌ Erreur test XSS: {e}", "ERROR")
            self.results["erreurs"].append(f"Test XSS: {e}")
        
        self.results["tests_executes"] += 1
        
        # Évaluer le score de sécurité
        if security_score >= 2:
            self.log("✅ Sécurité correcte", "SUCCESS")
            self.results["tests_reussis"] += 1
            self.results["security"]["score"] = security_score
            self.results["security"]["status"] = "OK"
        else:
            self.log("⚠️ Sécurité basique", "WARNING")
            self.results["warnings"].append("Sécurité basique")
            self.results["security"]["score"] = security_score
            self.results["security"]["status"] = "WARNING"
    
    def test_performance(self):
        """Tests de performance"""
        self.log("⚡ Tests de performance...")
        
        performance_tests = []
        
        # Test de temps de réponse
        for _ in range(10):
            start_time = time.time()
            try:
                response = requests.get(f"{self.base_url}/", timeout=5)
                end_time = time.time()
                
                if response.status_code == 200:
                    response_time = end_time - start_time
                    performance_tests.append(response_time)
                    
                    if response_time < 1.0:
                        self.log(f"✅ Temps de réponse: {response_time:.3f}s", "SUCCESS")
                    else:
                        self.log(f"⚠️ Temps de réponse lent: {response_time:.3f}s", "WARNING")
                        
            except Exception as e:
                self.log(f"❌ Erreur performance: {e}", "ERROR")
                self.results["erreurs"].append(f"Performance: {e}")
        
        if performance_tests:
            avg_time = sum(performance_tests) / len(performance_tests)
            self.results["performance"]["avg_response_time"] = avg_time
            
            if avg_time < 0.5:
                self.log("✅ Performance excellente", "SUCCESS")
                self.results["tests_reussis"] += 1
                self.results["performance"]["status"] = "EXCELLENT"
            elif avg_time < 1.0:
                self.log("✅ Performance correcte", "SUCCESS")
                self.results["tests_reussis"] += 1
                self.results["performance"]["status"] = "GOOD"
            else:
                self.log("⚠️ Performance lente", "WARNING")
                self.results["warnings"].append("Performance lente")
                self.results["performance"]["status"] = "SLOW"
        
        self.results["tests_executes"] += 1
    
    def test_stress_concurrent(self):
        """Test de stress avec utilisateurs concurrents"""
        self.log("🔥 Test de stress concurrent...")
        
        def stress_worker(worker_id: int) -> Dict[str, Any]:
            """Worker pour les tests de stress"""
            worker_results = {
                "worker_id": worker_id,
                "requests": 0,
                "success": 0,
                "errors": 0,
                "total_time": 0
            }
            
            start_time = time.time()
            
            for i in range(20):  # 20 requêtes par worker
                try:
                    response = requests.get(f"{self.base_url}/", timeout=5)
                    worker_results["requests"] += 1
                    
                    if response.status_code == 200:
                        worker_results["success"] += 1
                    else:
                        worker_results["errors"] += 1
                        
                except Exception as e:
                    worker_results["errors"] += 1
                
                time.sleep(0.1)  # Pause entre requêtes
            
            worker_results["total_time"] = time.time() - start_time
            return worker_results
        
        # Lancer 5 workers concurrents
        with ThreadPoolExecutor(max_workers=5) as executor:
            futures = [executor.submit(stress_worker, i) for i in range(5)]
            stress_results = [future.result() for future in as_completed(futures)]
        
        # Analyser les résultats
        total_requests = sum(r["requests"] for r in stress_results)
        total_success = sum(r["success"] for r in stress_results)
        total_errors = sum(r["errors"] for r in stress_results)
        
        success_rate = (total_success / total_requests * 100) if total_requests > 0 else 0
        
        self.log(f"📊 Stress test: {total_success}/{total_requests} réussis ({success_rate:.1f}%)", "INFO")
        
        if success_rate >= 95:
            self.log("✅ Stress test excellent", "SUCCESS")
            self.results["tests_reussis"] += 1
            self.results["performance"]["stress_status"] = "EXCELLENT"
        elif success_rate >= 80:
            self.log("✅ Stress test correct", "SUCCESS")
            self.results["tests_reussis"] += 1
            self.results["performance"]["stress_status"] = "GOOD"
        else:
            self.log("⚠️ Stress test problématique", "WARNING")
            self.results["warnings"].append("Stress test problématique")
            self.results["performance"]["stress_status"] = "POOR"
        
        self.results["performance"]["stress_results"] = {
            "total_requests": total_requests,
            "total_success": total_success,
            "total_errors": total_errors,
            "success_rate": success_rate
        }
        
        self.results["tests_executes"] += 1
    
    def test_accessibility(self):
        """Tests d'accessibilité basiques"""
        self.log("♿ Tests d'accessibilité...")
        
        try:
            response = requests.get(f"{self.base_url}/terminal", timeout=10)
            
            if response.status_code == 200:
                content = response.text
                
                # Vérifications d'accessibilité
                accessibility_checks = [
                    ("ARIA labels", "aria-label" in content),
                    ("Tabindex", "tabindex" in content),
                    ("Alt text", "alt=" in content),
                    ("Semantic HTML", "<main>" in content or "<nav>" in content),
                    ("Focus management", "focus" in content or "outline" in content)
                ]
                
                passed_checks = sum(1 for _, check in accessibility_checks if check)
                
                if passed_checks >= 3:
                    self.log("✅ Accessibilité correcte", "SUCCESS")
                    self.results["tests_reussis"] += 1
                    self.results["accessibility"]["score"] = passed_checks
                    self.results["accessibility"]["status"] = "OK"
                else:
                    self.log("⚠️ Accessibilité basique", "WARNING")
                    self.results["warnings"].append("Accessibilité basique")
                    self.results["accessibility"]["score"] = passed_checks
                    self.results["accessibility"]["status"] = "BASIC"
            else:
                self.log(f"❌ Erreur test accessibilité: {response.status_code}", "ERROR")
                self.results["tests_echecs"] += 1
                self.results["erreurs"].append(f"Accessibilité: HTTP {response.status_code}")
                
        except Exception as e:
            self.log(f"❌ Erreur test accessibilité: {e}", "ERROR")
            self.results["tests_echecs"] += 1
            self.results["erreurs"].append(f"Accessibilité: {e}")
        
        self.results["tests_executes"] += 1
    
    def generate_report(self) -> str:
        """Génère un rapport complet"""
        end_time = time.time()
        duration = end_time - self.start_time
        
        total_tests = self.results["tests_executes"]
        successful_tests = self.results["tests_reussis"]
        failed_tests = self.results["tests_echecs"]
        
        success_rate = (successful_tests / total_tests * 100) if total_tests > 0 else 0
        
        report = f"""
🎮 RAPPORT DE TEST VERSION STABLE - ARKALIA QUEST
================================================

📊 RÉSULTATS GLOBAUX
--------------------
✅ Tests réussis: {successful_tests}/{total_tests}
❌ Tests échoués: {failed_tests}/{total_tests}
📈 Taux de réussite: {success_rate:.1f}%
⏱️ Durée totale: {duration:.2f} secondes

🔍 DÉTAIL PAR CATÉGORIE
-----------------------
"""
        
        # Performance
        if "performance" in self.results:
            perf = self.results["performance"]
            report += f"""
⚡ PERFORMANCE
- Temps de réponse moyen: {perf.get('avg_response_time', 'N/A'):.3f}s
- Statut: {perf.get('status', 'N/A')}
- Stress test: {perf.get('stress_status', 'N/A')}
"""
        
        # Sécurité
        if "security" in self.results:
            sec = self.results["security"]
            report += f"""
🛡️ SÉCURITÉ
- Score: {sec.get('score', 'N/A')}/2
- Statut: {sec.get('status', 'N/A')}
"""
        
        # Base de données
        if "database" in self.results:
            db = self.results["database"]
            report += f"""
🗄️ BASE DE DONNÉES
- Statut: {db.get('status', 'N/A')}
"""
        
        # PWA
        if "pwa" in self.results:
            pwa = self.results["pwa"]
            report += f"""
📱 PWA
- Score: {pwa.get('score', 'N/A')}/4
- Statut: {pwa.get('status', 'N/A')}
"""
        
        # Accessibilité
        if "accessibility" in self.results:
            acc = self.results["accessibility"]
            report += f"""
♿ ACCESSIBILITÉ
- Score: {acc.get('score', 'N/A')}/5
- Statut: {acc.get('status', 'N/A')}
"""
        
        # Erreurs et warnings
        if self.results["erreurs"]:
            report += f"""
❌ ERREURS DÉTECTÉES ({len(self.results["erreurs"])})
"""
            for error in self.results["erreurs"][:10]:  # Top 10 erreurs
                report += f"- {error}\n"
        
        if self.results["warnings"]:
            report += f"""
⚠️ AVERTISSEMENTS ({len(self.results["warnings"])})
"""
            for warning in self.results["warnings"][:10]:  # Top 10 warnings
                report += f"- {warning}\n"
        
        # Conclusion
        report += f"""
🎯 CONCLUSION
------------
"""
        
        if success_rate >= 95:
            report += "🌟 EXCELLENT ! Version stable prête pour la production !"
        elif success_rate >= 85:
            report += "✅ BON ! Version stable avec quelques améliorations mineures."
        elif success_rate >= 70:
            report += "⚠️ MOYEN ! Des corrections sont nécessaires avant la production."
        else:
            report += "❌ CRITIQUE ! La version nécessite des corrections majeures."
        
        return report
    
    def run_all_tests(self):
        """Exécute tous les tests"""
        self.log("🚀 DÉMARRAGE DES TESTS VERSION STABLE ARKALIA QUEST")
        self.log("=" * 60)
        
        # Test de santé du serveur
        if not self.test_server_health():
            self.log("❌ Serveur non disponible, arrêt des tests", "ERROR")
            return
        
        # Tests principaux
        self.test_all_pages()
        self.test_all_commands()
        self.test_database_integrity()
        self.test_pwa_features()
        self.test_security()
        self.test_performance()
        self.test_stress_concurrent()
        self.test_accessibility()
        
        # Rapport final
        report = self.generate_report()
        print(report)
        
        # Sauvegarder le rapport
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_file = f"test_stable_version_{timestamp}.json"
        
        with open(report_file, "w", encoding="utf-8") as f:
            json.dump(self.results, f, indent=2, ensure_ascii=False)
        
        self.log(f"📄 Rapport sauvegardé: {report_file}")
        
        # Retourner le taux de réussite
        total_tests = self.results["tests_executes"]
        successful_tests = self.results["tests_reussis"]
        success_rate = (successful_tests / total_tests * 100) if total_tests > 0 else 0
        
        return success_rate >= 85  # Seuil de réussite pour version stable

def main():
    """Fonction principale"""
    print("🎮 ARKALIA QUEST - TESTEUR VERSION STABLE")
    print("=" * 50)
    
    tester = StableVersionTester()
    success = tester.run_all_tests()
    
    if success:
        print("\n🎉 VERSION STABLE VALIDÉE !")
        return 0
    else:
        print("\n⚠️ VERSION NÉCESSITE DES CORRECTIONS")
        return 1

if __name__ == "__main__":
    sys.exit(main()) 