#!/usr/bin/env python3
"""
Test Multi-Profils Arkalia Quest
Simule plusieurs joueurs avec différents niveaux d'expérience
et teste toutes les fonctionnalités du jeu
"""

import json
import time
import requests
import random
from datetime import datetime
from typing import Dict, List, Any

class ArkaliaMultiProfileTester:
    def __init__(self, base_url="http://localhost:5001"):
        self.base_url = base_url
        self.test_results = {
            "total_tests": 0,
            "passed": 0,
            "failed": 0,
            "errors": []
        }
        
        # Profils de test
        self.profiles = {
            "debutant": {
                "name": "Hacker_Debutant",
                "style": "explorateur",
                "commands": ["aide", "start_tutorial", "luna_contact", "hack_system", "load_mission"]
            },
            "intermediaire": {
                "name": "Hacker_Intermediaire", 
                "style": "analytique",
                "commands": ["kill_virus", "find_shadow", "hack_system", "challenge_corp", "badges", "avatars"]
            },
            "expert": {
                "name": "Hacker_Expert",
                "style": "créatif",
                "commands": ["chapitre_6", "save_luna", "easter_egg_1337", "luna_rage", "meme_war", "nuke_world"]
            }
        }
    
    def log_test(self, test_name: str, success: bool, details: str = ""):
        """Enregistre un résultat de test"""
        self.test_results["total_tests"] += 1
        if success:
            self.test_results["passed"] += 1
            print(f"✅ {test_name}: PASSÉ")
        else:
            self.test_results["failed"] += 1
            self.test_results["errors"].append(f"{test_name}: {details}")
            print(f"❌ {test_name}: ÉCHOUÉ - {details}")
    
    def send_command(self, command: str) -> Dict[str, Any]:
        """Envoie une commande au serveur"""
        try:
            response = requests.post(
                f"{self.base_url}/commande",
                json={"cmd": command},
                timeout=10
            )
            return response.json() if response.status_code == 200 else {"error": f"HTTP {response.status_code}"}
        except Exception as e:
            return {"error": str(e)}
    
    def test_server_health(self) -> bool:
        """Teste si le serveur répond"""
        try:
            response = requests.get(f"{self.base_url}/", timeout=5)
            return response.status_code == 200
        except:
            return False
    
    def test_basic_commands(self, profile_type: str) -> Dict[str, Any]:
        """Teste les commandes de base pour un profil"""
        profile = self.profiles[profile_type]
        results = {"profile": profile_type, "commands_tested": 0, "successful": 0}
        
        print(f"\n🎮 Test du profil {profile_type.upper()}")
        print("=" * 50)
        
        for command in profile["commands"]:
            print(f"🔧 Test de la commande: {command}")
            response = self.send_command(command)
            
            results["commands_tested"] += 1
            
            if "error" not in response and response.get("réussite", False):
                results["successful"] += 1
                print(f"  ✅ {command} - Succès")
                
                # Vérifier la structure de réponse
                if "profil" in response:
                    profil = response["profil"]
                    if "score" in profil and "badges" in profil:
                        print(f"  📊 Score: {profil['score']}, Badges: {len(profil['badges'])}")
            else:
                print(f"  ❌ {command} - Échec: {response.get('error', response.get('message', 'Erreur inconnue'))}")
            
            time.sleep(0.5)  # Pause entre les commandes
        
        return results
    
    def test_mission_system(self) -> Dict[str, Any]:
        """Teste le système de missions"""
        print("\n🎯 Test du système de missions")
        print("=" * 50)
        
        results = {"missions_tested": 0, "successful": 0}
        
        # Test de chargement de mission
        response = self.send_command("load_mission")
        results["missions_tested"] += 1
        
        if "error" not in response and response.get("réussite", False):
            results["successful"] += 1
            print("✅ Chargement de mission - Succès")
            
            # Vérifier la structure de la mission
            if "mission" in response:
                mission = response["mission"]
                print(f"  📋 Mission: {mission.get('titre', 'Sans titre')}")
                print(f"  🎯 Difficulté: {mission.get('difficulte', 'Inconnue')}")
        else:
            print(f"❌ Chargement de mission - Échec: {response.get('error', 'Erreur inconnue')}")
        
        return results
    
    def test_badge_system(self) -> Dict[str, Any]:
        """Teste le système de badges"""
        print("\n🏆 Test du système de badges")
        print("=" * 50)
        
        results = {"badge_tests": 0, "successful": 0}
        
        # Test d'affichage des badges
        response = self.send_command("badges")
        results["badge_tests"] += 1
        
        if "error" not in response and response.get("réussite", False):
            results["successful"] += 1
            print("✅ Affichage des badges - Succès")
        else:
            print(f"❌ Affichage des badges - Échec: {response.get('error', 'Erreur inconnue')}")
        
        # Test de déblocage de badge
        response = self.send_command("unlock_badge")
        results["badge_tests"] += 1
        
        if "error" not in response:
            results["successful"] += 1
            print("✅ Déblocage de badge - Succès")
        else:
            print(f"❌ Déblocage de badge - Échec: {response.get('error', 'Erreur inconnue')}")
        
        return results
    
    def test_audio_controls(self) -> Dict[str, Any]:
        """Teste les contrôles audio"""
        print("\n🔊 Test des contrôles audio")
        print("=" * 50)
        
        results = {"audio_tests": 0, "successful": 0}
        
        # Test de commandes avec effets sonores
        commands_with_audio = ["kill_virus", "hack_system", "find_shadow"]
        
        for command in commands_with_audio:
            response = self.send_command(command)
            results["audio_tests"] += 1
            
            if "error" not in response and response.get("réussite", False):
                results["successful"] += 1
                print(f"✅ {command} avec audio - Succès")
            else:
                print(f"❌ {command} avec audio - Échec")
            
            time.sleep(0.3)
        
        return results
    
    def test_progression_system(self) -> Dict[str, Any]:
        """Teste le système de progression"""
        print("\n📈 Test du système de progression")
        print("=" * 50)
        
        results = {"progression_tests": 0, "successful": 0}
        
        # Test de progression du score
        initial_response = self.send_command("profil")
        if "error" not in initial_response and "profil" in initial_response:
            initial_score = initial_response["profil"].get("score", 0)
            print(f"📊 Score initial: {initial_score}")
            
            # Effectuer une action qui donne des points
            response = self.send_command("kill_virus")
            results["progression_tests"] += 1
            
            if "error" not in response and "profil" in response:
                new_score = response["profil"].get("score", 0)
                if new_score > initial_score:
                    results["successful"] += 1
                    print(f"✅ Progression du score: {initial_score} → {new_score}")
                else:
                    print(f"❌ Pas de progression du score")
            else:
                print(f"❌ Erreur lors du test de progression")
        
        return results
    
    def test_error_handling(self) -> Dict[str, Any]:
        """Teste la gestion des erreurs"""
        print("\n🚨 Test de la gestion des erreurs")
        print("=" * 50)
        
        results = {"error_tests": 0, "successful": 0}
        
        # Test de commande inexistante
        response = self.send_command("commande_inexistante_12345")
        results["error_tests"] += 1
        
        if "error" in response or not response.get("réussite", True):
            results["successful"] += 1
            print("✅ Gestion d'erreur - Commande inexistante")
        else:
            print("❌ Gestion d'erreur - Commande inexistante non détectée")
        
        # Test de commande vide
        response = self.send_command("")
        results["error_tests"] += 1
        
        if "error" in response or not response.get("réussite", True):
            results["successful"] += 1
            print("✅ Gestion d'erreur - Commande vide")
        else:
            print("❌ Gestion d'erreur - Commande vide non détectée")
        
        return results
    
    def test_responsive_interface(self) -> Dict[str, Any]:
        """Teste l'interface responsive"""
        print("\n📱 Test de l'interface responsive")
        print("=" * 50)
        
        results = {"responsive_tests": 0, "successful": 0}
        
        # Test de chargement du terminal
        try:
            response = requests.get(f"{self.base_url}/terminal", timeout=5)
            results["responsive_tests"] += 1
            
            if response.status_code == 200:
                results["successful"] += 1
                print("✅ Chargement du terminal - Succès")
                
                # Vérifier la présence d'éléments responsive
                content = response.text
                if "audio-toggle" in content and "progressBarContainer" in content:
                    results["successful"] += 1
                    print("✅ Éléments responsive présents")
                else:
                    print("❌ Éléments responsive manquants")
            else:
                print(f"❌ Chargement du terminal - Échec: HTTP {response.status_code}")
        except Exception as e:
            print(f"❌ Erreur de chargement: {e}")
        
        return results
    
    def run_complete_test_suite(self) -> Dict[str, Any]:
        """Lance la suite complète de tests"""
        print("🚀 DÉMARRAGE DES TESTS MULTI-PROFILS ARKALIA QUEST")
        print("=" * 60)
        
        start_time = time.time()
        
        # Test de santé du serveur
        if not self.test_server_health():
            print("❌ Serveur non accessible. Arrêt des tests.")
            return {"error": "Serveur non accessible"}
        
        print("✅ Serveur accessible")
        
        # Tests par profil
        profile_results = {}
        for profile_type in self.profiles.keys():
            profile_results[profile_type] = self.test_basic_commands(profile_type)
        
        # Tests spécifiques
        mission_results = self.test_mission_system()
        badge_results = self.test_badge_system()
        audio_results = self.test_audio_controls()
        progression_results = self.test_progression_system()
        error_results = self.test_error_handling()
        responsive_results = self.test_responsive_interface()
        
        # Calcul des résultats
        total_tests = (
            sum(r["commands_tested"] for r in profile_results.values()) +
            mission_results["missions_tested"] +
            badge_results["badge_tests"] +
            audio_results["audio_tests"] +
            progression_results["progression_tests"] +
            error_results["error_tests"] +
            responsive_results["responsive_tests"]
        )
        
        total_successful = (
            sum(r["successful"] for r in profile_results.values()) +
            mission_results["successful"] +
            badge_results["successful"] +
            audio_results["successful"] +
            progression_results["successful"] +
            error_results["successful"] +
            responsive_results["successful"]
        )
        
        end_time = time.time()
        duration = end_time - start_time
        
        # Rapport final
        print("\n" + "=" * 60)
        print("📊 RAPPORT FINAL DES TESTS")
        print("=" * 60)
        print(f"⏱️  Durée totale: {duration:.2f} secondes")
        print(f"🧪 Tests effectués: {total_tests}")
        print(f"✅ Tests réussis: {total_successful}")
        print(f"❌ Tests échoués: {total_tests - total_successful}")
        print(f"📈 Taux de réussite: {(total_successful/total_tests)*100:.1f}%")
        
        # Détails par profil
        print("\n👥 RÉSULTATS PAR PROFIL:")
        for profile_type, results in profile_results.items():
            success_rate = (results["successful"] / results["commands_tested"]) * 100 if results["commands_tested"] > 0 else 0
            print(f"  {profile_type.upper()}: {results['successful']}/{results['commands_tested']} ({success_rate:.1f}%)")
        
        return {
            "total_tests": total_tests,
            "successful": total_successful,
            "failed": total_tests - total_successful,
            "success_rate": (total_successful/total_tests)*100 if total_tests > 0 else 0,
            "duration": duration,
            "profile_results": profile_results,
            "mission_results": mission_results,
            "badge_results": badge_results,
            "audio_results": audio_results,
            "progression_results": progression_results,
            "error_results": error_results,
            "responsive_results": responsive_results
        }

def main():
    """Fonction principale pour lancer les tests"""
    tester = ArkaliaMultiProfileTester()
    results = tester.run_complete_test_suite()
    
    # Sauvegarder les résultats
    with open("test_results_multi_profiles.json", "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False, default=str)
    
    print(f"\n💾 Résultats sauvegardés dans test_results_multi_profiles.json")
    
    if results.get("success_rate", 0) >= 80:
        print("🎉 TESTS RÉUSSIS ! Arkalia Quest est prêt pour les ados rebelles !")
        return 0
    else:
        print("⚠️  TESTS PARTIELS - Certains problèmes détectés")
        return 1

if __name__ == "__main__":
    exit(main()) 