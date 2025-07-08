#!/usr/bin/env python3
"""
🎮 ARKALIA QUEST - TESTEUR GAMIFICATION COMPLET
===============================================

Ce testeur valide :
- Système de leaderboard
- Badges secrets et achievements
- Calcul XP et niveaux
- Progression de gamification
- API de gamification

Auteur: Assistant IA
Version: 1.0
"""

import requests
import json
import time
from datetime import datetime
import random

class GamificationTester:
    """Testeur complet de la gamification"""
    
    def __init__(self):
        self.base_url = "http://localhost:5001"
        self.results = {
            "tests_executes": 0,
            "tests_reussis": 0,
            "tests_echecs": 0,
            "erreurs": [],
            "warnings": [],
            "details": []
        }
        self.start_time = time.time()
        
        # Profils de test
        self.test_profiles = [
            "testeur_gamification_1",
            "testeur_gamification_2", 
            "testeur_gamification_3",
            "testeur_gamification_4",
            "testeur_gamification_5"
        ]
        
        # Commandes pour tester la gamification
        self.gamification_commands = [
            "aide", "profil", "monde", "status",
            "unlock_universe", "scan_persona", "load_mission niveau1",
            "decode_portal", "hacker_coffre", "reboot_world",
            "assistant_pirate", "generer_meme", "decoder_message",
            "invoquer_dragon", "choisir_avatar", "badges", "avatars"
        ]
    
    def log(self, message: str, level: str = "INFO"):
        """Log avec timestamp"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"[{timestamp}] {level}: {message}")
    
    def test_leaderboard_api(self):
        """Test de l'API leaderboard"""
        self.log("🏆 Test de l'API leaderboard...")
        
        try:
            response = requests.get(f"{self.base_url}/api/leaderboard")
            if response.status_code == 200:
                data = response.json()
                
                # Vérifier la structure
                required_keys = ["top_players", "statistics", "last_updated"]
                if all(key in data for key in required_keys):
                    self.log("✅ API leaderboard fonctionne", "SUCCESS")
                    self.results["tests_reussis"] += 1
                    
                    # Vérifier les statistiques
                    stats = data["statistics"]
                    if isinstance(stats.get("total_players"), int) and \
                       isinstance(stats.get("total_score"), (int, float)) and \
                       isinstance(stats.get("average_score"), (int, float)):
                        self.log("✅ Statistiques leaderboard valides", "SUCCESS")
                    else:
                        self.log("⚠️ Statistiques leaderboard incomplètes", "WARNING")
                        self.results["warnings"].append("Statistiques leaderboard incomplètes")
                else:
                    self.log("❌ Structure API leaderboard incorrecte", "ERROR")
                    self.results["tests_echecs"] += 1
                    self.results["erreurs"].append("Structure API leaderboard incorrecte")
            else:
                self.log(f"❌ Erreur HTTP {response.status_code} sur API leaderboard", "ERROR")
                self.results["tests_echecs"] += 1
                self.results["erreurs"].append(f"Erreur HTTP {response.status_code} sur API leaderboard")
        except Exception as e:
            self.log(f"❌ Erreur API leaderboard: {e}", "ERROR")
            self.results["tests_echecs"] += 1
            self.results["erreurs"].append(f"Erreur API leaderboard: {e}")
        
        self.results["tests_executes"] += 1
    
    def test_leaderboard_page(self):
        """Test de la page leaderboard"""
        self.log("📄 Test de la page leaderboard...")
        
        try:
            response = requests.get(f"{self.base_url}/leaderboard")
            if response.status_code == 200:
                content = response.text
                
                # Vérifier le contenu de la page
                required_elements = [
                    "LEADERBOARD ARKALIA QUEST",
                    "stats-grid",
                    "leaderboard-table",
                    "refresh-button"
                ]
                
                if all(element in content for element in required_elements):
                    self.log("✅ Page leaderboard fonctionne", "SUCCESS")
                    self.results["tests_reussis"] += 1
                else:
                    self.log("❌ Éléments manquants dans la page leaderboard", "ERROR")
                    self.results["tests_echecs"] += 1
                    self.results["erreurs"].append("Éléments manquants dans la page leaderboard")
            else:
                self.log(f"❌ Erreur HTTP {response.status_code} sur page leaderboard", "ERROR")
                self.results["tests_echecs"] += 1
                self.results["erreurs"].append(f"Erreur HTTP {response.status_code} sur page leaderboard")
        except Exception as e:
            self.log(f"❌ Erreur page leaderboard: {e}", "ERROR")
            self.results["tests_echecs"] += 1
            self.results["erreurs"].append(f"Erreur page leaderboard: {e}")
        
        self.results["tests_executes"] += 1
    
    def test_gamification_summary_api(self):
        """Test de l'API gamification summary"""
        self.log("📊 Test de l'API gamification summary...")
        
        try:
            response = requests.get(f"{self.base_url}/api/gamification/summary")
            if response.status_code == 200:
                data = response.json()
                
                # Vérifier la structure
                required_keys = [
                    "player_rank", "total_players", "level_progress", 
                    "badges_count", "missions_completed", "achievements_count",
                    "total_score", "leaderboard_stats"
                ]
                
                if all(key in data for key in required_keys):
                    self.log("✅ API gamification summary fonctionne", "SUCCESS")
                    self.results["tests_reussis"] += 1
                    
                    # Vérifier la progression de niveau
                    level_progress = data["level_progress"]
                    if isinstance(level_progress.get("current_level"), int) and \
                       isinstance(level_progress.get("progress_percentage"), (int, float)):
                        self.log("✅ Progression de niveau valide", "SUCCESS")
                    else:
                        self.log("⚠️ Progression de niveau incomplète", "WARNING")
                        self.results["warnings"].append("Progression de niveau incomplète")
                else:
                    self.log("❌ Structure API gamification summary incorrecte", "ERROR")
                    self.results["tests_echecs"] += 1
                    self.results["erreurs"].append("Structure API gamification summary incorrecte")
            else:
                self.log(f"❌ Erreur HTTP {response.status_code} sur API gamification summary", "ERROR")
                self.results["tests_echecs"] += 1
                self.results["erreurs"].append(f"Erreur HTTP {response.status_code} sur API gamification summary")
        except Exception as e:
            self.log(f"❌ Erreur API gamification summary: {e}", "ERROR")
            self.results["tests_echecs"] += 1
            self.results["erreurs"].append(f"Erreur API gamification summary: {e}")
        
        self.results["tests_executes"] += 1
    
    def test_badges_secrets_system(self):
        """Test du système de badges secrets"""
        self.log("🔓 Test du système de badges secrets...")
        
        for profile_id in self.test_profiles:
            try:
                # Simuler des actions pour débloquer des badges
                commands_to_test = [
                    "aide", "profil", "monde", "status",
                    "unlock_universe", "scan_persona"
                ]
                
                for cmd in commands_to_test:
                    response = requests.post(f"{self.base_url}/commande", 
                                           json={"commande": cmd})
                    
                    if response.status_code == 200:
                        data = response.json()
                        if "reponse" in data:
                            reponse = data["reponse"]
                            
                            # Vérifier si un badge a été débloqué
                            if "badge_unlocked" in reponse:
                                badge_id = reponse["badge_unlocked"]
                                self.log(f"✅ Badge débloqué: {badge_id} pour {profile_id}", "SUCCESS")
                                self.results["tests_reussis"] += 1
                            elif "achievement_unlocked" in reponse:
                                achievement_id = reponse["achievement_unlocked"]
                                self.log(f"✅ Achievement débloqué: {achievement_id} pour {profile_id}", "SUCCESS")
                                self.results["tests_reussis"] += 1
                    else:
                        self.log(f"⚠️ Erreur commande {cmd}: {response.status_code}", "WARNING")
                        self.results["warnings"].append(f"Erreur commande {cmd}: {response.status_code}")
                
                self.results["tests_executes"] += 1
                
            except Exception as e:
                self.log(f"❌ Erreur test badges secrets pour {profile_id}: {e}", "ERROR")
                self.results["tests_echecs"] += 1
                self.results["erreurs"].append(f"Erreur test badges secrets pour {profile_id}: {e}")
    
    def test_xp_and_leveling(self):
        """Test du système XP et de niveau"""
        self.log("📈 Test du système XP et de niveau...")
        
        try:
            # Tester différentes commandes pour gagner de l'XP
            xp_commands = [
                "aide", "profil", "monde", "unlock_universe", 
                "scan_persona", "hacker_coffre", "decode_portal"
            ]
            
            for cmd in xp_commands:
                response = requests.post(f"{self.base_url}/commande", 
                                       json={"commande": cmd})
                
                if response.status_code == 200:
                    data = response.json()
                    if "reponse" in data:
                        reponse = data["reponse"]
                        
                        # Vérifier si le profil a été mis à jour
                        if reponse.get("profile_updated", False):
                            self.log(f"✅ Profil mis à jour pour commande: {cmd}", "SUCCESS")
                            self.results["tests_reussis"] += 1
                        else:
                            self.log(f"⚠️ Profil non mis à jour pour: {cmd}", "WARNING")
                            self.results["warnings"].append(f"Profil non mis à jour pour: {cmd}")
                else:
                    self.log(f"⚠️ Erreur commande XP {cmd}: {response.status_code}", "WARNING")
                    self.results["warnings"].append(f"Erreur commande XP {cmd}: {response.status_code}")
            
            self.results["tests_executes"] += 1
            
        except Exception as e:
            self.log(f"❌ Erreur test XP: {e}", "ERROR")
            self.results["tests_echecs"] += 1
            self.results["erreurs"].append(f"Erreur test XP: {e}")
    
    def test_service_worker(self):
        """Test du service worker PWA"""
        self.log("🔧 Test du service worker PWA...")
        
        try:
            response = requests.get(f"{self.base_url}/static/js/service-worker.js")
            if response.status_code == 200:
                content = response.text
                
                # Vérifier le contenu du service worker
                required_elements = [
                    "CACHE_NAME",
                    "urlsToCache",
                    "install",
                    "activate", 
                    "fetch",
                    "push",
                    "notificationclick"
                ]
                
                if all(element in content for element in required_elements):
                    self.log("✅ Service worker PWA fonctionne", "SUCCESS")
                    self.results["tests_reussis"] += 1
                else:
                    self.log("❌ Éléments manquants dans le service worker", "ERROR")
                    self.results["tests_echecs"] += 1
                    self.results["erreurs"].append("Éléments manquants dans le service worker")
            else:
                self.log(f"❌ Erreur HTTP {response.status_code} sur service worker", "ERROR")
                self.results["tests_echecs"] += 1
                self.results["erreurs"].append(f"Erreur HTTP {response.status_code} sur service worker")
        except Exception as e:
            self.log(f"❌ Erreur service worker: {e}", "ERROR")
            self.results["tests_echecs"] += 1
            self.results["erreurs"].append(f"Erreur service worker: {e}")
        
        self.results["tests_executes"] += 1
    
    def test_pwa_manifest(self):
        """Test du manifest PWA"""
        self.log("📱 Test du manifest PWA...")
        
        try:
            response = requests.get(f"{self.base_url}/static/manifest.json")
            if response.status_code == 200:
                data = response.json()
                
                # Vérifier la structure du manifest
                required_keys = ["name", "short_name", "description", "start_url", "display", "theme_color"]
                if all(key in data for key in required_keys):
                    self.log("✅ Manifest PWA valide", "SUCCESS")
                    self.results["tests_reussis"] += 1
                else:
                    self.log("❌ Structure manifest PWA incorrecte", "ERROR")
                    self.results["tests_echecs"] += 1
                    self.results["erreurs"].append("Structure manifest PWA incorrecte")
            else:
                self.log(f"❌ Erreur HTTP {response.status_code} sur manifest PWA", "ERROR")
                self.results["tests_echecs"] += 1
                self.results["erreurs"].append(f"Erreur HTTP {response.status_code} sur manifest PWA")
        except Exception as e:
            self.log(f"❌ Erreur manifest PWA: {e}", "ERROR")
            self.results["tests_echecs"] += 1
            self.results["erreurs"].append(f"Erreur manifest PWA: {e}")
        
        self.results["tests_executes"] += 1
    
    def run_all_tests(self):
        """Exécute tous les tests de gamification"""
        self.log("🚀 DÉMARRAGE DES TESTS DE GAMIFICATION COMPLETS")
        self.log("=" * 60)
        
        # Tests API et pages
        self.test_leaderboard_api()
        self.test_leaderboard_page()
        self.test_gamification_summary_api()
        
        # Tests système de gamification
        self.test_badges_secrets_system()
        self.test_xp_and_leveling()
        
        # Tests PWA
        self.test_service_worker()
        self.test_pwa_manifest()
        
        # Rapport final
        self.generate_report()
    
    def generate_report(self):
        """Génère le rapport final"""
        end_time = time.time()
        duration = end_time - self.start_time
        
        self.log("=" * 60)
        self.log("📊 RAPPORT FINAL - TESTS GAMIFICATION")
        self.log("=" * 60)
        
        self.log(f"⏱️ Durée totale: {duration:.2f} secondes")
        self.log(f"🧪 Tests exécutés: {self.results['tests_executes']}")
        self.log(f"✅ Tests réussis: {self.results['tests_reussis']}")
        self.log(f"❌ Tests échoués: {self.results['tests_echecs']}")
        self.log(f"⚠️ Warnings: {len(self.results['warnings'])}")
        self.log(f"🚨 Erreurs: {len(self.results['erreurs'])}")
        
        # Calcul du taux de réussite
        if self.results["tests_executes"] > 0:
            success_rate = (self.results["tests_reussis"] / self.results["tests_executes"]) * 100
            self.log(f"📈 Taux de réussite: {success_rate:.1f}%")
        
        # Détails des erreurs
        if self.results["erreurs"]:
            self.log("\n🚨 ERREURS DÉTECTÉES:")
            for error in self.results["erreurs"][:5]:  # Afficher les 5 premières
                self.log(f"• {error}")
            if len(self.results["erreurs"]) > 5:
                self.log(f"• ... et {len(self.results['erreurs']) - 5} autres erreurs")
        
        # Détails des warnings
        if self.results["warnings"]:
            self.log("\n⚠️ WARNINGS:")
            for warning in self.results["warnings"][:3]:  # Afficher les 3 premiers
                self.log(f"• {warning}")
            if len(self.results["warnings"]) > 3:
                self.log(f"• ... et {len(self.results['warnings']) - 3} autres warnings")
        
        # Conclusion
        if self.results["tests_echecs"] == 0 and len(self.results["erreurs"]) == 0:
            self.log("\n🎉 TOUS LES TESTS DE GAMIFICATION SONT PASSÉS !")
            self.log("✅ Le système de gamification est 100% fonctionnel")
        else:
            self.log(f"\n⚠️ {self.results['tests_echecs']} tests ont échoué")
            self.log("🔧 Des corrections sont nécessaires")
        
        self.log("=" * 60)


if __name__ == "__main__":
    tester = GamificationTester()
    tester.run_all_tests() 