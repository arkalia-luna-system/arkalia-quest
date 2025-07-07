#!/usr/bin/env python3
"""
Test Interface Complète Arkalia Quest
Vérifie tous les éléments visuels, animations, effets sonores et accessibilité
"""

import json
import time
import requests
from datetime import datetime
from typing import Dict, List, Any

class ArkaliaInterfaceTester:
    def __init__(self, base_url="http://localhost:5001"):
        self.base_url = base_url
        self.results = {
            "total_tests": 0,
            "passed": 0,
            "failed": 0,
            "errors": []
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
    
    def test_terminal_page(self) -> Dict[str, Any]:
        """Teste la page terminal complète"""
        print("\n🎮 Test de la page Terminal")
        print("=" * 50)
        
        results = {"tests": 0, "successful": 0}
        
        try:
            response = requests.get(f"{self.base_url}/terminal", timeout=10)
            results["tests"] += 1
            
            if response.status_code == 200:
                results["successful"] += 1
                print("✅ Chargement de la page terminal - Succès")
                
                content = response.text
                
                # Vérifier les éléments essentiels
                essential_elements = [
                    "terminal-header",
                    "terminal-output", 
                    "terminal-input",
                    "audio-toggle",
                    "progressBarContainer",
                    "playerLevel",
                    "playerScore",
                    "playerBadges"
                ]
                
                for element in essential_elements:
                    results["tests"] += 1
                    if element in content:
                        results["successful"] += 1
                        print(f"  ✅ Élément {element} présent")
                    else:
                        print(f"  ❌ Élément {element} manquant")
                
                # Vérifier les scripts JS
                js_files = [
                    "terminal.js",
                    "effects.js", 
                    "hacking-effects.js"
                ]
                
                for js_file in js_files:
                    results["tests"] += 1
                    if js_file in content:
                        results["successful"] += 1
                        print(f"  ✅ Script {js_file} chargé")
                    else:
                        print(f"  ❌ Script {js_file} manquant")
                
                # Vérifier les styles CSS
                if "style.css" in content:
                    results["successful"] += 1
                    print("  ✅ Styles CSS chargés")
                else:
                    print("  ❌ Styles CSS manquants")
                
            else:
                print(f"❌ Chargement de la page terminal - Échec: HTTP {response.status_code}")
                
        except Exception as e:
            print(f"❌ Erreur de chargement: {e}")
        
        return results
    
    def test_responsive_design(self) -> Dict[str, Any]:
        """Teste le design responsive"""
        print("\n📱 Test du design responsive")
        print("=" * 50)
        
        results = {"tests": 0, "successful": 0}
        
        try:
            response = requests.get(f"{self.base_url}/terminal", timeout=10)
            results["tests"] += 1
            
            if response.status_code == 200:
                results["successful"] += 1
                content = response.text
                
                # Vérifier les éléments responsive
                responsive_elements = [
                    "@media",
                    "max-width",
                    "min-width",
                    "vw",
                    "vh",
                    "flex",
                    "grid"
                ]
                
                for element in responsive_elements:
                    results["tests"] += 1
                    if element in content:
                        results["successful"] += 1
                        print(f"  ✅ Élément responsive {element} présent")
                    else:
                        print(f"  ❌ Élément responsive {element} manquant")
                        
        except Exception as e:
            print(f"❌ Erreur responsive: {e}")
        
        return results
    
    def test_audio_system(self) -> Dict[str, Any]:
        """Teste le système audio"""
        print("\n🔊 Test du système audio")
        print("=" * 50)
        
        results = {"tests": 0, "successful": 0}
        
        # Test des commandes avec effets sonores
        audio_commands = [
            "kill_virus",
            "hack_system", 
            "find_shadow",
            "challenge_corp",
            "save_luna"
        ]
        
        for command in audio_commands:
            try:
                response = requests.post(
                    f"{self.base_url}/commande",
                    json={"cmd": command},
                    timeout=5
                )
                results["tests"] += 1
                
                if response.status_code == 200:
                    data = response.json()
                    if "animation" in data or "réussite" in data:
                        results["successful"] += 1
                        print(f"  ✅ {command} - Effet audio/visuel présent")
                    else:
                        print(f"  ❌ {command} - Pas d'effet audio/visuel")
                else:
                    print(f"  ❌ {command} - Erreur HTTP {response.status_code}")
                    
            except Exception as e:
                print(f"  ❌ {command} - Erreur: {e}")
            
            time.sleep(0.3)
        
        return results
    
    def test_animations(self) -> Dict[str, Any]:
        """Teste les animations et effets visuels"""
        print("\n🎨 Test des animations")
        print("=" * 50)
        
        results = {"tests": 0, "successful": 0}
        
        # Test des commandes avec animations
        animation_commands = [
            "kill_virus",
            "hack_system",
            "find_shadow", 
            "easter_egg_1337",
            "luna_rage",
            "meme_war"
        ]
        
        for command in animation_commands:
            try:
                response = requests.post(
                    f"{self.base_url}/commande",
                    json={"cmd": command},
                    timeout=5
                )
                results["tests"] += 1
                
                if response.status_code == 200:
                    data = response.json()
                    if "animation" in data or "badge" in data:
                        results["successful"] += 1
                        print(f"  ✅ {command} - Animation/badge présent")
                    else:
                        print(f"  ❌ {command} - Pas d'animation/badge")
                else:
                    print(f"  ❌ {command} - Erreur HTTP {response.status_code}")
                    
            except Exception as e:
                print(f"  ❌ {command} - Erreur: {e}")
            
            time.sleep(0.3)
        
        return results
    
    def test_accessibility(self) -> Dict[str, Any]:
        """Teste l'accessibilité"""
        print("\n♿ Test de l'accessibilité")
        print("=" * 50)
        
        results = {"tests": 0, "successful": 0}
        
        try:
            response = requests.get(f"{self.base_url}/terminal", timeout=10)
            results["tests"] += 1
            
            if response.status_code == 200:
                results["successful"] += 1
                content = response.text
                
                # Vérifier les éléments d'accessibilité
                accessibility_elements = [
                    "aria-label",
                    "tabindex",
                    "role=",
                    "alt=",
                    "title=",
                    "focus",
                    "outline"
                ]
                
                for element in accessibility_elements:
                    results["tests"] += 1
                    if element in content:
                        results["successful"] += 1
                        print(f"  ✅ Élément d'accessibilité {element} présent")
                    else:
                        print(f"  ❌ Élément d'accessibilité {element} manquant")
                        
        except Exception as e:
            print(f"❌ Erreur accessibilité: {e}")
        
        return results
    
    def test_progress_system(self) -> Dict[str, Any]:
        """Teste le système de progression visuel"""
        print("\n📊 Test du système de progression")
        print("=" * 50)
        
        results = {"tests": 0, "successful": 0}
        
        # Test de progression du score
        try:
            # Score initial
            response = requests.post(
                f"{self.base_url}/commande",
                json={"cmd": "profil"},
                timeout=5
            )
            results["tests"] += 1
            
            if response.status_code == 200:
                data = response.json()
                if "profil" in data and "score" in data["profil"]:
                    initial_score = data["profil"]["score"]
                    results["successful"] += 1
                    print(f"  ✅ Score initial récupéré: {initial_score}")
                    
                    # Effectuer une action pour gagner des points
                    response2 = requests.post(
                        f"{self.base_url}/commande",
                        json={"cmd": "kill_virus"},
                        timeout=5
                    )
                    results["tests"] += 1
                    
                    if response2.status_code == 200:
                        data2 = response2.json()
                        if "profil" in data2 and "score" in data2["profil"]:
                            new_score = data2["profil"]["score"]
                            if new_score > initial_score:
                                results["successful"] += 1
                                print(f"  ✅ Progression du score: {initial_score} → {new_score}")
                            else:
                                print(f"  ❌ Pas de progression du score")
                        else:
                            print(f"  ❌ Pas de données de profil dans la réponse")
                    else:
                        print(f"  ❌ Erreur lors du test de progression")
                else:
                    print(f"  ❌ Pas de données de score dans la réponse")
            else:
                print(f"  ❌ Erreur HTTP {response.status_code}")
                
        except Exception as e:
            print(f"  ❌ Erreur: {e}")
        
        return results
    
    def test_badge_system_visual(self) -> Dict[str, Any]:
        """Teste le système de badges visuel"""
        print("\n🏆 Test du système de badges visuel")
        print("=" * 50)
        
        results = {"tests": 0, "successful": 0}
        
        # Test d'affichage des badges
        try:
            response = requests.post(
                f"{self.base_url}/commande",
                json={"cmd": "badges"},
                timeout=5
            )
            results["tests"] += 1
            
            if response.status_code == 200:
                data = response.json()
                if "réussite" in data and data["réussite"]:
                    results["successful"] += 1
                    print("  ✅ Affichage des badges - Succès")
                    
                    # Vérifier la présence de badges dans le profil
                    if "profil" in data and "badges" in data["profil"]:
                        badges = data["profil"]["badges"]
                        results["successful"] += 1
                        print(f"  ✅ {len(badges)} badges présents dans le profil")
                    else:
                        print("  ❌ Pas de badges dans le profil")
                else:
                    print("  ❌ Échec de l'affichage des badges")
            else:
                print(f"  ❌ Erreur HTTP {response.status_code}")
                
        except Exception as e:
            print(f"  ❌ Erreur: {e}")
        
        return results
    
    def test_error_handling_visual(self) -> Dict[str, Any]:
        """Teste la gestion visuelle des erreurs"""
        print("\n🚨 Test de la gestion visuelle des erreurs")
        print("=" * 50)
        
        results = {"tests": 0, "successful": 0}
        
        # Test de commande inexistante
        try:
            response = requests.post(
                f"{self.base_url}/commande",
                json={"cmd": "commande_inexistante_test_12345"},
                timeout=5
            )
            results["tests"] += 1
            
            if response.status_code == 200:
                data = response.json()
                if "error" in data or not data.get("réussite", True):
                    results["successful"] += 1
                    print("  ✅ Gestion d'erreur - Commande inexistante")
                else:
                    print("  ❌ Gestion d'erreur - Commande inexistante non détectée")
            else:
                print(f"  ❌ Erreur HTTP {response.status_code}")
                
        except Exception as e:
            print(f"  ❌ Erreur: {e}")
        
        # Test de commande vide
        try:
            response = requests.post(
                f"{self.base_url}/commande",
                json={"cmd": ""},
                timeout=5
            )
            results["tests"] += 1
            
            if response.status_code == 200:
                data = response.json()
                if "error" in data or not data.get("réussite", True):
                    results["successful"] += 1
                    print("  ✅ Gestion d'erreur - Commande vide")
                else:
                    print("  ❌ Gestion d'erreur - Commande vide non détectée")
            else:
                print(f"  ❌ Erreur HTTP {response.status_code}")
                
        except Exception as e:
            print(f"  ❌ Erreur: {e}")
        
        return results
    
    def run_complete_interface_test(self) -> Dict[str, Any]:
        """Lance le test complet de l'interface"""
        print("🎨 DÉMARRAGE DU TEST D'INTERFACE COMPLÈTE ARKALIA QUEST")
        print("=" * 60)
        
        start_time = time.time()
        
        # Tests de l'interface
        terminal_results = self.test_terminal_page()
        responsive_results = self.test_responsive_design()
        audio_results = self.test_audio_system()
        animation_results = self.test_animations()
        accessibility_results = self.test_accessibility()
        progress_results = self.test_progress_system()
        badge_results = self.test_badge_system_visual()
        error_results = self.test_error_handling_visual()
        
        # Calcul des résultats
        total_tests = (
            terminal_results["tests"] +
            responsive_results["tests"] +
            audio_results["tests"] +
            animation_results["tests"] +
            accessibility_results["tests"] +
            progress_results["tests"] +
            badge_results["tests"] +
            error_results["tests"]
        )
        
        total_successful = (
            terminal_results["successful"] +
            responsive_results["successful"] +
            audio_results["successful"] +
            animation_results["successful"] +
            accessibility_results["successful"] +
            progress_results["successful"] +
            badge_results["successful"] +
            error_results["successful"]
        )
        
        end_time = time.time()
        duration = end_time - start_time
        
        # Rapport final
        print("\n" + "=" * 60)
        print("📊 RAPPORT FINAL DU TEST D'INTERFACE")
        print("=" * 60)
        print(f"⏱️  Durée totale: {duration:.2f} secondes")
        print(f"🧪 Tests effectués: {total_tests}")
        print(f"✅ Tests réussis: {total_successful}")
        print(f"❌ Tests échoués: {total_tests - total_successful}")
        print(f"📈 Taux de réussite: {(total_successful/total_tests)*100:.1f}%")
        
        # Détails par catégorie
        print("\n🎯 RÉSULTATS PAR CATÉGORIE:")
        categories = [
            ("Terminal", terminal_results),
            ("Responsive", responsive_results),
            ("Audio", audio_results),
            ("Animations", animation_results),
            ("Accessibilité", accessibility_results),
            ("Progression", progress_results),
            ("Badges", badge_results),
            ("Gestion d'erreurs", error_results)
        ]
        
        for name, results in categories:
            success_rate = (results["successful"] / results["tests"]) * 100 if results["tests"] > 0 else 0
            print(f"  {name}: {results['successful']}/{results['tests']} ({success_rate:.1f}%)")
        
        return {
            "total_tests": total_tests,
            "successful": total_successful,
            "failed": total_tests - total_successful,
            "success_rate": (total_successful/total_tests)*100 if total_tests > 0 else 0,
            "duration": duration,
            "terminal_results": terminal_results,
            "responsive_results": responsive_results,
            "audio_results": audio_results,
            "animation_results": animation_results,
            "accessibility_results": accessibility_results,
            "progress_results": progress_results,
            "badge_results": badge_results,
            "error_results": error_results
        }

def main():
    """Fonction principale pour lancer le test d'interface"""
    tester = ArkaliaInterfaceTester()
    results = tester.run_complete_interface_test()
    
    # Sauvegarder les résultats
    with open("interface_test_results.json", "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False, default=str)
    
    print(f"\n💾 Résultats sauvegardés dans interface_test_results.json")
    
    if results.get("success_rate", 0) >= 85:
        print("🎉 TEST D'INTERFACE RÉUSSI ! L'interface est parfaite pour les ados !")
        return 0
    else:
        print("⚠️  TEST D'INTERFACE PARTIEL - Certains éléments peuvent être améliorés")
        return 1

if __name__ == "__main__":
    exit(main()) 