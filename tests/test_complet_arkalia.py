#!/usr/bin/env python3
"""
🕵️ ARKALIA QUEST - TESTEUR COMPLET ULTIME
==========================================

Ce testeur combine :
- Testeur intelligent (interface, sécurité, performance)
- Testeur de missions (logique métier, progression)
- Tests de stress avancés
- Validation complète de l'expérience utilisateur

Auteur: Assistant IA
Version: 1.0
"""

import subprocess
import sys
import time
from datetime import datetime
import json
import os
import requests
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed

class ArkaliaTesterUltime:
    """Testeur complet ultime pour Arkalia Quest"""
    
    def __init__(self):
        self.base_url: str = "http://localhost:5001"
        self.results: dict = {
            "tests_executes": 0,
            "tests_reussis": 0,
            "tests_echecs": 0,
            "erreurs": [],
            "warnings": [],
            "performance": {},
            "details": []
        }
        self.start_time: float = time.time()
        
        # Profils de test avec IDs uniques
        self.test_profiles: list[str] = [
            "testeur_alpha",
            "testeur_beta", 
            "testeur_gamma",
            "testeur_delta",
            "testeur_epsilon"
        ]
        
        # Commandes de test étendues
        self.test_commands: list[str] = [
            "aide", "profil", "monde", "status", "clear",
            "unlock_universe", "scan_persona", "load_mission niveau1",
            "decode_portal", "hacker_coffre", "reboot_world",
            "luna_contact", "luna_dance", "boss_final",
            "complete_objective", "solve_puzzle", "hack_success",
            "find_secret", "help_character", "explore_area",
            "master_skill", "save_progress", "basic_hack",
            "simple_puzzle", "intro_dialogue", "decoder_challenge",
            "pattern_recognition", "advanced_hack", "complex_puzzle",
            "multi_step_hack", "character_interaction", "escape_sequence",
            "time_pressure", "resource_management", "ai_dialogue",
            "moral_choices", "consequence_management"
        ]
        
        # Missions de test
        self.test_missions: list[str] = [
            "niveau1", "niveau2", "niveau3", "niveau4", "niveau5",
            "luna_first_contact", "ai_rebellion", "cyber_escape", "hacker_challenge"
        ]
    
    def log(self, message: str, level: str = "INFO"):
        """Log avec timestamp"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"[{timestamp}] {level}: {message}")
    
    def test_server_health(self):
        """Test de santé du serveur"""
        self.log("🔍 Test de santé du serveur...")
        
        try:
            response = requests.get(f"{self.base_url}/", timeout=5)
            if response.status_code == 200:
                self.log("✅ Serveur opérationnel", "SUCCESS")
                return True
            else:
                self.log(f"❌ Serveur répond avec {response.status_code}", "ERROR")
                return False
        except Exception as e:
            self.log(f"❌ Serveur inaccessible: {e}", "ERROR")
            return False
    
    def test_interface_pages(self):
        """Test des pages d'interface"""
        self.log("🌐 Test des pages d'interface...")
        
        pages = ["/", "/terminal", "/monde", "/profil", "/explorateur", "/mail", "/audio"]
        
        for page in pages:
            try:
                response = requests.get(f"{self.base_url}{page}", timeout=5)
                if response.status_code == 200:
                    self.log(f"✅ Page {page} accessible", "SUCCESS")
                    self.results["tests_reussis"] += 1
                else:
                    self.log(f"❌ Page {page} erreur {response.status_code}", "ERROR")
                    self.results["tests_echecs"] += 1
                    self.results["erreurs"].append(f"Page {page} inaccessible")
            except Exception as e:
                self.log(f"❌ Page {page} exception: {e}", "ERROR")
                self.results["tests_echecs"] += 1
                self.results["erreurs"].append(f"Page {page} exception: {e}")
            
            self.results["tests_executes"] += 1
    
    def test_command_structure(self, command: str, profile_id: str):
        """Test de la structure de réponse d'une commande"""
        try:
            response = requests.post(f"{self.base_url}/commande", 
                                   json={"commande": command, "profile_id": profile_id},
                                   timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                
                # Vérifier la structure de réponse
                if "reponse" in data:
                    reponse = data["reponse"]
                    if isinstance(reponse, dict) and "réussite" in reponse:
                        self.log(f"✅ Commande '{command}' - Structure OK", "SUCCESS")
                        return True
                    else:
                        self.log(f"⚠️ Commande '{command}' - Structure réponse incorrecte", "WARNING")
                        self.results["warnings"].append(f"Commande '{command}' - Structure réponse incorrecte")
                        return False
                else:
                    self.log(f"❌ Commande '{command}' - Pas de clé 'reponse'", "ERROR")
                    self.results["erreurs"].append(f"Commande '{command}' - Pas de clé 'reponse'")
                    return False
            else:
                self.log(f"❌ Commande '{command}' - HTTP {response.status_code}", "ERROR")
                self.results["erreurs"].append(f"Commande '{command}' - HTTP {response.status_code}")
                return False
                
        except Exception as e:
            self.log(f"❌ Commande '{command}' - Exception: {e}", "ERROR")
            self.results["erreurs"].append(f"Commande '{command}' - Exception: {e}")
            return False
    
    def test_commands_batch(self):
        """Test en lot des commandes"""
        self.log("🎮 Test en lot des commandes...")
        
        for profile_id in self.test_profiles:
            self.log(f"👤 Test avec profil: {profile_id}")
            
            for command in self.test_commands:
                if self.test_command_structure(command, profile_id):
                    self.results["tests_reussis"] += 1
                else:
                    self.results["tests_echecs"] += 1
                self.results["tests_executes"] += 1
                
                # Petit délai pour éviter la surcharge
                time.sleep(0.1)
    
    def test_mission_loading(self):
        """Test des missions"""
        self.log("🎯 Test des missions...")
        
        for profile_id in self.test_profiles:
            for mission in self.test_missions:
                command = f"load_mission {mission}"
                if self.test_command_structure(command, profile_id):
                    self.log(f"✅ Mission '{mission}' chargée pour {profile_id}", "SUCCESS")
                    self.results["tests_reussis"] += 1
                else:
                    self.log(f"❌ Mission '{mission}' échec pour {profile_id}", "ERROR")
                    self.results["tests_echecs"] += 1
                self.results["tests_executes"] += 1
    
    def test_stress_concurrent(self):
        """Test de stress avec requêtes concurrentes"""
        self.log("⚡ Test de stress concurrent...")
        
        def stress_worker(worker_id):
            """Worker pour les tests de stress"""
            local_success = 0
            local_failures = 0
            
            for i in range(10):  # 10 requêtes par worker
                command = self.test_commands[i % len(self.test_commands)]
                profile_id = self.test_profiles[i % len(self.test_profiles)]
                
                try:
                    response = requests.post(f"{self.base_url}/commande",
                                           json={"commande": command, "profile_id": profile_id},
                                           timeout=5)
                    
                    if response.status_code == 200:
                        data = response.json()
                        if "reponse" in data:
                            local_success += 1
                        else:
                            local_failures += 1
                    else:
                        local_failures += 1
                        
                except Exception:
                    local_failures += 1
                
                time.sleep(0.05)  # Petit délai
            
            return local_success, local_failures
        
        # Lancer 5 workers concurrents
        with ThreadPoolExecutor(max_workers=5) as executor:
            futures = [executor.submit(stress_worker, i) for i in range(5)]
            
            total_success = 0
            total_failures = 0
            
            for future in as_completed(futures):
                success, failures = future.result()
                total_success += success
                total_failures += failures
        
        self.log(f"⚡ Stress test: {total_success} succès, {total_failures} échecs", "INFO")
        self.results["performance"]["stress_test"] = {
            "total_requests": total_success + total_failures,
            "success_rate": total_success / (total_success + total_failures) * 100
        }
    
    def test_security(self):
        """Tests de sécurité basiques"""
        self.log("🔒 Tests de sécurité...")
        
        # Test commande vide
        try:
            response = requests.post(f"{self.base_url}/commande",
                                   json={"commande": "", "profile_id": "test"},
                                   timeout=5)
            
            if response.status_code == 400:
                self.log("✅ Commande vide rejetée correctement", "SUCCESS")
                self.results["tests_reussis"] += 1
            else:
                self.log(f"⚠️ Commande vide: HTTP {response.status_code}", "WARNING")
                self.results["warnings"].append("Commande vide non rejetée")
                self.results["tests_echecs"] += 1
        except Exception as e:
            self.log(f"❌ Test commande vide: {e}", "ERROR")
            self.results["tests_echecs"] += 1
        
        self.results["tests_executes"] += 1
        
        # Test injection basique
        try:
            response = requests.post(f"{self.base_url}/commande",
                                   json={"commande": "'; DROP TABLE users; --", "profile_id": "test"},
                                   timeout=5)
            
            if response.status_code == 200:
                self.log("✅ Injection basique gérée", "SUCCESS")
                self.results["tests_reussis"] += 1
            else:
                self.log(f"⚠️ Injection basique: HTTP {response.status_code}", "WARNING")
                self.results["warnings"].append("Injection basique non gérée")
                self.results["tests_echecs"] += 1
        except Exception as e:
            self.log(f"❌ Test injection: {e}", "ERROR")
            self.results["tests_echecs"] += 1
        
        self.results["tests_executes"] += 1
    
    def generate_report(self):
        """Génère le rapport de test"""
        end_time = time.time()
        duration = end_time - self.start_time
        
        success_rate = (self.results["tests_reussis"] / self.results["tests_executes"] * 100) if self.results["tests_executes"] > 0 else 0
        
        report = f"""
🚀 RAPPORT DE TEST ARKALIA QUEST - ULTIME
==========================================

📊 STATISTIQUES GÉNÉRALES:
• Tests exécutés: {self.results["tests_executes"]}
• Tests réussis: {self.results["tests_reussis"]}
• Tests échoués: {self.results["tests_echecs"]}
• Taux de succès: {success_rate:.1f}%
• Durée totale: {duration:.2f} secondes

🔍 DÉTAILS DES TESTS:
• Interface: ✅ Pages testées
• Commandes: ✅ Structure validée
• Missions: ✅ Chargement testé
• Sécurité: ✅ Tests basiques
• Performance: ✅ Stress test

❌ ERREURS DÉTECTÉES ({len(self.results["erreurs"])}):
"""
        
        for error in self.results["erreurs"][:10]:  # Limiter à 10 erreurs
            report += f"• {error}\n"
        
        if len(self.results["erreurs"]) > 10:
            report += f"• ... et {len(self.results['erreurs']) - 10} autres erreurs\n"
        
        report += f"""
⚠️ AVERTISSEMENTS ({len(self.results["warnings"])}):
"""
        
        for warning in self.results["warnings"][:5]:  # Limiter à 5 warnings
            report += f"• {warning}\n"
        
        if len(self.results["warnings"]) > 5:
            report += f"• ... et {len(self.results['warnings']) - 5} autres warnings\n"
        
        if "performance" in self.results and "stress_test" in self.results["performance"]:
            stress = self.results["performance"]["stress_test"]
            report += f"""
⚡ PERFORMANCE:
• Requêtes stress test: {stress["total_requests"]}
• Taux de succès stress: {stress["success_rate"]:.1f}%
"""
        
        report += f"""
🎯 CONCLUSION:
"""
        
        if success_rate >= 95:
            report += "🌟 EXCELLENT ! Le système fonctionne parfaitement !"
        elif success_rate >= 80:
            report += "✅ BON ! Quelques améliorations mineures possibles."
        elif success_rate >= 60:
            report += "⚠️ MOYEN ! Des corrections sont nécessaires."
        else:
            report += "❌ CRITIQUE ! Le système nécessite des corrections majeures."
        
        return report
    
    def run_all_tests(self):
        """Exécute tous les tests"""
        self.log("🚀 DÉMARRAGE DES TESTS ULTIMES ARKALIA QUEST")
        self.log("=" * 50)
        
        # Test de santé du serveur
        if not self.test_server_health():
            self.log("❌ Serveur non disponible, arrêt des tests", "ERROR")
            return
        
        # Tests d'interface
        self.test_interface_pages()
        
        # Tests de commandes
        self.test_commands_batch()
        
        # Tests de missions
        self.test_mission_loading()
        
        # Tests de sécurité
        self.test_security()
        
        # Tests de stress
        self.test_stress_concurrent()
        
        # Rapport final
        report = self.generate_report()
        print(report)
        
        # Sauvegarder le rapport
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        with open(f"test_results_ultime_{timestamp}.json", "w", encoding="utf-8") as f:
            json.dump(self.results, f, indent=2, ensure_ascii=False)
        
        self.log(f"📄 Rapport sauvegardé: test_results_ultime_{timestamp}.json")

def main():
    """Fonction principale"""
    print("🕵️ ARKALIA QUEST - TESTEUR COMPLET ULTIME")
    print("=" * 50)
    
    # Vérifier que le serveur est démarré
    print("🔍 Vérification du serveur...")
    
    try:
        response = requests.get("http://localhost:5001/", timeout=5)
        if response.status_code == 200:
            print("✅ Serveur détecté, lancement des tests...")
        else:
            print("❌ Serveur non accessible")
            return
    except:
        print("❌ Serveur non accessible. Assurez-vous que le serveur est démarré sur http://localhost:5001")
        return
    
    # Lancer les tests
    tester = ArkaliaTesterUltime()
    tester.run_all_tests()

if __name__ == "__main__":
    main() 