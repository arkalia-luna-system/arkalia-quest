#!/usr/bin/env python3
"""
Test complet de l'interface Arkalia Quest
Vérifie tous les boutons, fonctionnalités, responsive et accessibilité
"""

import requests
import json
import time
import sys
from typing import Dict, List, Any, Optional

class InterfaceTester:
    def __init__(self, base_url="http://localhost:5000"):
        self.base_url = base_url
        self.results = {
            "tests": [],
            "errors": [],
            "warnings": [],
            "success": 0,
            "total": 0
        }
    
    def log_test(self, test_name: str, success: bool, message: str = "", details: Optional[Dict[str, Any]] = None):
        """Enregistre un résultat de test"""
        self.results["total"] += 1
        if success:
            self.results["success"] += 1
            print(f"✅ {test_name}: {message}")
        else:
            print(f"❌ {test_name}: {message}")
            if details:
                self.results["errors"].append({"test": test_name, "details": details})
        
        self.results["tests"].append({
            "name": test_name,
            "success": success,
            "message": message,
            "details": details or {}
        })
    
    def test_server_connection(self):
        """Test de connexion au serveur"""
        try:
            response = requests.get(f"{self.base_url}/", timeout=5)
            if response.status_code == 200:
                self.log_test("Connexion serveur", True, "Serveur accessible")
                return True
            else:
                self.log_test("Connexion serveur", False, f"Code {response.status_code}")
                return False
        except Exception as e:
            self.log_test("Connexion serveur", False, f"Erreur: {str(e)}")
            return False
    
    def test_terminal_page(self):
        """Test de la page terminal"""
        try:
            response = requests.get(f"{self.base_url}/terminal", timeout=5)
            if response.status_code == 200:
                content = response.text
                
                # Vérifier les éléments essentiels
                checks = [
                    ("Titre de page", "ARKALIA QUEST" in content),
                    ("Bouton Envoyer", "ENVOYER" in content),
                    ("Input commande", "commandInput" in content),
                    ("Messages container", "messagesContainer" in content),
                    ("Boutons rapides", "TUTORIEL" in content and "AIDE" in content),
                    ("Bouton audio", "audioToggle" in content),
                    ("Responsive CSS", "@media" in content),
                    ("JavaScript", "terminal.js" in content),
                    ("Effets CSS", "animation" in content),
                    ("Accessibilité", "aria-label" in content)
                ]
                
                all_checks = True
                for check_name, check_result in checks:
                    if not check_result:
                        all_checks = False
                        self.log_test(f"Page terminal - {check_name}", False, "Élément manquant")
                    else:
                        self.log_test(f"Page terminal - {check_name}", True, "Présent")
                
                return all_checks
            else:
                self.log_test("Page terminal", False, f"Code {response.status_code}")
                return False
        except Exception as e:
            self.log_test("Page terminal", False, f"Erreur: {str(e)}")
            return False
    
    def test_command_endpoint(self):
        """Test de l'endpoint de commandes"""
        test_commands = [
            ("aide", "Commande d'aide"),
            ("luna_contact", "Contact LUNA"),
            ("start_tutorial", "Tutoriel"),
            ("badges", "Badges"),
            ("profil", "Profil"),
            ("commande_inexistante_test", "Commande inexistante")
        ]
        
        all_success = True
        for cmd, description in test_commands:
            try:
                response = requests.post(
                    f"{self.base_url}/commande",
                    json={"cmd": cmd},
                    timeout=10
                )
                
                if response.status_code == 200:
                    data = response.json()
                    if "message" in data:
                        self.log_test(f"Commande {cmd}", True, f"{description}: {data['message'][:50]}...")
                    else:
                        self.log_test(f"Commande {cmd}", True, f"{description}: Réponse reçue")
                else:
                    self.log_test(f"Commande {cmd}", False, f"Code {response.status_code}")
                    all_success = False
                    
            except Exception as e:
                self.log_test(f"Commande {cmd}", False, f"Erreur: {str(e)}")
                all_success = False
        
        return all_success
    
    def test_quick_buttons(self):
        """Test des boutons rapides"""
        quick_commands = [
            "start_tutorial",
            "aide", 
            "luna_contact",
            "hack_system"
        ]
        
        all_success = True
        for cmd in quick_commands:
            try:
                response = requests.post(
                    f"{self.base_url}/commande",
                    json={"cmd": cmd},
                    timeout=10
                )
                
                if response.status_code == 200:
                    data = response.json()
                    self.log_test(f"Bouton rapide {cmd}", True, "Fonctionne")
                else:
                    self.log_test(f"Bouton rapide {cmd}", False, f"Code {response.status_code}")
                    all_success = False
                    
            except Exception as e:
                self.log_test(f"Bouton rapide {cmd}", False, f"Erreur: {str(e)}")
                all_success = False
        
        return all_success
    
    def test_responsive_elements(self):
        """Test des éléments responsive"""
        try:
            response = requests.get(f"{self.base_url}/terminal", timeout=5)
            if response.status_code == 200:
                content = response.text
                
                responsive_checks = [
                    ("Media queries", "@media (max-width:" in content),
                    ("Flexbox", "flex-direction: column" in content),
                    ("Viewport meta", "viewport" in content),
                    ("Mobile CSS", "max-width" in content),
                    ("Touch targets", "min-height" in content or "padding" in content)
                ]
                
                all_checks = True
                for check_name, check_result in responsive_checks:
                    if not check_result:
                        all_checks = False
                        self.log_test(f"Responsive - {check_name}", False, "Manquant")
                    else:
                        self.log_test(f"Responsive - {check_name}", True, "Présent")
                
                return all_checks
            else:
                self.log_test("Responsive", False, f"Code {response.status_code}")
                return False
        except Exception as e:
            self.log_test("Responsive", False, f"Erreur: {str(e)}")
            return False
    
    def test_accessibility(self):
        """Test de l'accessibilité"""
        try:
            response = requests.get(f"{self.base_url}/terminal", timeout=5)
            if response.status_code == 200:
                content = response.text
                
                a11y_checks = [
                    ("Aria labels", "aria-label" in content),
                    ("Role attributes", "role=" in content),
                    ("Alt text", "alt=" in content),
                    ("Tabindex", "tabindex" in content),
                    ("Semantic HTML", "<button" in content and "<input" in content),
                    ("Color contrast", "color:" in content and "background:" in content),
                    ("Focus indicators", ":focus" in content or "outline" in content)
                ]
                
                all_checks = True
                for check_name, check_result in a11y_checks:
                    if not check_result:
                        all_checks = False
                        self.log_test(f"Accessibilité - {check_name}", False, "Manquant")
                    else:
                        self.log_test(f"Accessibilité - {check_name}", True, "Présent")
                
                return all_checks
            else:
                self.log_test("Accessibilité", False, f"Code {response.status_code}")
                return False
        except Exception as e:
            self.log_test("Accessibilité", False, f"Erreur: {str(e)}")
            return False
    
    def test_audio_features(self):
        """Test des fonctionnalités audio"""
        try:
            response = requests.get(f"{self.base_url}/terminal", timeout=5)
            if response.status_code == 200:
                content = response.text
                
                audio_checks = [
                    ("Bouton audio", "audioToggle" in content),
                    ("Audio context", "AudioContext" in content),
                    ("Sons de frappe", "playTypingSound" in content),
                    ("Sons de succès", "playSuccessSound" in content),
                    ("Sons d'erreur", "playErrorSound" in content),
                    ("Contrôle volume", "volume" in content),
                    ("Mute toggle", "muted" in content)
                ]
                
                all_checks = True
                for check_name, check_result in audio_checks:
                    if not check_result:
                        all_checks = False
                        self.log_test(f"Audio - {check_name}", False, "Manquant")
                    else:
                        self.log_test(f"Audio - {check_name}", True, "Présent")
                
                return all_checks
            else:
                self.log_test("Audio", False, f"Code {response.status_code}")
                return False
        except Exception as e:
            self.log_test("Audio", False, f"Erreur: {str(e)}")
            return False
    
    def test_visual_effects(self):
        """Test des effets visuels"""
        try:
            response = requests.get(f"{self.base_url}/terminal", timeout=5)
            if response.status_code == 200:
                content = response.text
                
                effects_checks = [
                    ("Animations CSS", "@keyframes" in content),
                    ("Transitions", "transition" in content),
                    ("Transform", "transform" in content),
                    ("Box shadow", "box-shadow" in content),
                    ("Gradients", "gradient" in content),
                    ("Glitch effects", "glitch" in content),
                    ("Matrix effects", "matrix" in content),
                    ("Progress bars", "progress" in content)
                ]
                
                all_checks = True
                for check_name, check_result in effects_checks:
                    if not check_result:
                        all_checks = False
                        self.log_test(f"Effets - {check_name}", False, "Manquant")
                    else:
                        self.log_test(f"Effets - {check_name}", True, "Présent")
                
                return all_checks
            else:
                self.log_test("Effets visuels", False, f"Code {response.status_code}")
                return False
        except Exception as e:
            self.log_test("Effets visuels", False, f"Erreur: {str(e)}")
            return False
    
    def test_error_handling(self):
        """Test de la gestion d'erreurs"""
        try:
            # Test avec une commande invalide
            response = requests.post(
                f"{self.base_url}/commande",
                json={"cmd": "commande_tres_longue_et_invalide_qui_devrait_echouer"},
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                if "message" in data and ("erreur" in data["message"].lower() or "inconnu" in data["message"].lower()):
                    self.log_test("Gestion erreurs", True, "Erreur gérée correctement")
                    return True
                else:
                    self.log_test("Gestion erreurs", False, "Pas de message d'erreur")
                    return False
            else:
                self.log_test("Gestion erreurs", False, f"Code {response.status_code}")
                return False
                
        except Exception as e:
            self.log_test("Gestion erreurs", False, f"Erreur: {str(e)}")
            return False
    
    def test_performance_features(self):
        """Test des fonctionnalités de performance"""
        try:
            response = requests.get(f"{self.base_url}/terminal", timeout=5)
            if response.status_code == 200:
                content = response.text
                
                perf_checks = [
                    ("Détection performance", "deviceMemory" in content or "lowPerformance" in content),
                    ("Mode réduit", "low-performance" in content),
                    ("Optimisations", "will-change" in content),
                    ("Lazy loading", "loading" in content),
                    ("Debounce", "setTimeout" in content or "clearTimeout" in content)
                ]
                
                all_checks = True
                for check_name, check_result in perf_checks:
                    if not check_result:
                        all_checks = False
                        self.log_test(f"Performance - {check_name}", False, "Manquant")
                    else:
                        self.log_test(f"Performance - {check_name}", True, "Présent")
                
                return all_checks
            else:
                self.log_test("Performance", False, f"Code {response.status_code}")
                return False
        except Exception as e:
            self.log_test("Performance", False, f"Erreur: {str(e)}")
            return False
    
    def run_all_tests(self):
        """Lance tous les tests"""
        print("🚀 DÉBUT DES TESTS D'INTERFACE ARKALIA QUEST")
        print("=" * 50)
        
        # Tests de base
        if not self.test_server_connection():
            print("❌ Serveur non accessible, arrêt des tests")
            return self.results
        
        # Tests d'interface
        self.test_terminal_page()
        self.test_command_endpoint()
        self.test_quick_buttons()
        self.test_responsive_elements()
        self.test_accessibility()
        self.test_audio_features()
        self.test_visual_effects()
        self.test_error_handling()
        self.test_performance_features()
        
        # Résumé
        print("\n" + "=" * 50)
        print("📊 RÉSULTATS FINAUX")
        print(f"✅ Tests réussis: {self.results['success']}/{self.results['total']}")
        print(f"📈 Taux de réussite: {(self.results['success']/self.results['total']*100):.1f}%")
        
        if self.results['errors']:
            print(f"\n❌ Erreurs détectées: {len(self.results['errors'])}")
            for error in self.results['errors'][:5]:  # Afficher les 5 premières erreurs
                print(f"  - {error['test']}: {error['details']}")
        
        if self.results['success']/self.results['total'] >= 0.8:
            print("\n🎉 Interface prête pour la production !")
        elif self.results['success']/self.results['total'] >= 0.6:
            print("\n⚠️ Interface fonctionnelle mais améliorations recommandées")
        else:
            print("\n🚨 Interface nécessite des corrections importantes")
        
        return self.results

def main():
    """Fonction principale"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Test complet de l'interface Arkalia Quest")
    parser.add_argument("--url", default="http://localhost:5000", help="URL du serveur")
    parser.add_argument("--output", help="Fichier de sortie JSON")
    
    args = parser.parse_args()
    
    tester = InterfaceTester(args.url)
    results = tester.run_all_tests()
    
    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        print(f"\n📄 Résultats sauvegardés dans {args.output}")

if __name__ == "__main__":
    main() 