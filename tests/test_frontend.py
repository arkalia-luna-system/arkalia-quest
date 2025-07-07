#!/usr/bin/env python3
"""
Test automatisé du frontend Arkalia Quest
Vérifie : CSS, JS, Terminal, Responsive, Effets ASCII
"""

import requests
import time
import json
import os
from bs4 import BeautifulSoup

class FrontendTester:
    def __init__(self, base_url="http://127.0.0.1:5001"):
        self.base_url = base_url
        self.session = requests.Session()
        self.results = []
        
    def log(self, test_name, success, message=""):
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} {test_name}: {message}")
        self.results.append({
            "test": test_name,
            "success": success,
            "message": message
        })
        
    def test_css_files(self):
        """Teste l'existence et l'accessibilité des fichiers CSS"""
        print("\n🎨 Test des fichiers CSS...")
        
        css_files = [
            "/static/css/terminal.css",
            "/static/style.css"  # Ancien CSS pour compatibilité
        ]
        
        for css_file in css_files:
            try:
                response = self.session.get(f"{self.base_url}{css_file}")
                if response.status_code == 200:
                    self.log(f"CSS {css_file}", True, f"Status: {response.status_code}")
                else:
                    self.log(f"CSS {css_file}", False, f"Status: {response.status_code}")
            except Exception as e:
                self.log(f"CSS {css_file}", False, f"Erreur: {e}")
                
    def test_js_files(self):
        """Teste l'existence et l'accessibilité des fichiers JS"""
        print("\n⚡ Test des fichiers JavaScript...")
        
        js_files = [
            "/static/js/terminal.js"
        ]
        
        for js_file in js_files:
            try:
                response = self.session.get(f"{self.base_url}{js_file}")
                if response.status_code == 200:
                    self.log(f"JS {js_file}", True, f"Status: {response.status_code}")
                else:
                    self.log(f"JS {js_file}", False, f"Status: {response.status_code}")
            except Exception as e:
                self.log(f"JS {js_file}", False, f"Erreur: {e}")
                
    def test_terminal_page(self):
        """Teste la page terminal et ses éléments"""
        print("\n🖥️ Test de la page Terminal...")
        
        try:
            response = self.session.get(f"{self.base_url}/terminal")
            if response.status_code == 200:
                self.log("Page Terminal", True, "Page accessible")
                
                # Parse HTML
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # Vérifie les éléments essentiels
                elements_to_check = [
                    ("#terminal-output", "Zone de sortie"),
                    ("#terminal-input", "Zone de saisie"),
                    ("#terminal-form", "Formulaire"),
                    (".prompt", "Prompt LUNA"),
                    (".submit-btn", "Bouton d'envoi")
                ]
                
                for selector, name in elements_to_check:
                    element = soup.select_one(selector)
                    if element:
                        self.log(f"Élément {name}", True, f"Trouvé: {selector}")
                    else:
                        self.log(f"Élément {name}", False, f"Manquant: {selector}")
                        
                # Vérifie les liens CSS/JS
                css_links = soup.find_all('link', rel='stylesheet')
                js_scripts = soup.find_all('script', src=True)
                
                self.log("Liens CSS", True, f"{len(css_links)} fichiers CSS trouvés")
                self.log("Scripts JS", True, f"{len(js_scripts)} fichiers JS trouvés")
                
            else:
                self.log("Page Terminal", False, f"Status: {response.status_code}")
                
        except Exception as e:
            self.log("Page Terminal", False, f"Erreur: {e}")
            
    def test_terminal_commands(self):
        """Teste les commandes du terminal"""
        print("\n⌨️ Test des commandes Terminal...")
        
        test_commands = [
            "aide",
            "profil", 
            "unlock_universe",
            "scan_persona"
        ]
        
        for cmd in test_commands:
            try:
                response = self.session.post(
                    f"{self.base_url}/commande",
                    json={"cmd": cmd},
                    headers={"Content-Type": "application/json"}
                )
                
                if response.status_code == 200:
                    data = response.json()
                    if data.get("réussite") is not None:
                        self.log(f"Commande '{cmd}'", True, f"Réponse: {data.get('message', '')[:50]}...")
                    else:
                        self.log(f"Commande '{cmd}'", False, "Format de réponse invalide")
                else:
                    self.log(f"Commande '{cmd}'", False, f"Status: {response.status_code}")
                    
            except Exception as e:
                self.log(f"Commande '{cmd}'", False, f"Erreur: {e}")
                
    def test_ascii_effects(self):
        """Teste l'existence des effets ASCII"""
        print("\n🎭 Test des effets ASCII...")
        
        ascii_files = [
            "data/effects/ascii/success.txt",
            "data/effects/ascii/luna_contact.txt"
        ]
        
        for ascii_file in ascii_files:
            if os.path.exists(ascii_file):
                with open(ascii_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    if content.strip():
                        self.log(f"Effet ASCII {ascii_file}", True, f"Contenu: {len(content)} caractères")
                    else:
                        self.log(f"Effet ASCII {ascii_file}", False, "Fichier vide")
            else:
                self.log(f"Effet ASCII {ascii_file}", False, "Fichier manquant")
                
    def test_responsive_design(self):
        """Teste la responsivité (simulation)"""
        print("\n📱 Test de la responsivité...")
        
        # Simule différents viewports
        viewports = [
            ("Desktop", "1200x800"),
            ("Tablet", "768x1024"), 
            ("Mobile", "375x667")
        ]
        
        for device, resolution in viewports:
            # Vérifie que le CSS contient des media queries
            try:
                response = self.session.get(f"{self.base_url}/static/css/terminal.css")
                if response.status_code == 200:
                    css_content = response.text
                    if "@media" in css_content:
                        self.log(f"Responsive {device}", True, f"Media queries trouvées pour {resolution}")
                    else:
                        self.log(f"Responsive {device}", False, "Aucune media query trouvée")
                else:
                    self.log(f"Responsive {device}", False, "CSS non accessible")
            except Exception as e:
                self.log(f"Responsive {device}", False, f"Erreur: {e}")
                
    def run_all_tests(self):
        """Lance tous les tests"""
        print("🚀 Démarrage des tests Frontend Arkalia Quest")
        print("=" * 50)
        
        self.test_css_files()
        self.test_js_files()
        self.test_terminal_page()
        self.test_terminal_commands()
        self.test_ascii_effects()
        self.test_responsive_design()
        
        # Résumé
        print("\n" + "=" * 50)
        print("📊 RÉSUMÉ DES TESTS")
        print("=" * 50)
        
        passed = sum(1 for r in self.results if r["success"])
        total = len(self.results)
        
        print(f"✅ Tests réussis: {passed}/{total}")
        print(f"❌ Tests échoués: {total - passed}/{total}")
        print(f"📈 Taux de réussite: {(passed/total)*100:.1f}%")
        
        if passed == total:
            print("\n🎉 TOUS LES TESTS SONT PASSÉS !")
        else:
            print("\n⚠️ Certains tests ont échoué. Vérifiez les erreurs ci-dessus.")
            
        return passed == total

def main():
    """Fonction principale"""
    tester = FrontendTester()
    success = tester.run_all_tests()
    
    if success:
        print("\n🎮 Le frontend est prêt pour la démo !")
        print("🌐 Ouvrez http://127.0.0.1:5001/terminal dans votre navigateur")
    else:
        print("\n🔧 Des corrections sont nécessaires avant la démo.")
        
    return 0 if success else 1

if __name__ == "__main__":
    exit(main()) 