#!/usr/bin/env python3
"""
Test frontend simplifié Arkalia Quest
Sans dépendances externes - vérification basique
"""

import os
import json
import urllib.request
import urllib.parse
import urllib.error
from pathlib import Path

class SimpleFrontendTester:
    def __init__(self, base_url="http://127.0.0.1:5001"):
        self.base_url = base_url
        self.results = []
        
    def log(self, test_name, success, message=""):
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} {test_name}: {message}")
        self.results.append({
            "test": test_name,
            "success": success,
            "message": message
        })
        
    def test_files_exist(self):
        """Teste l'existence des fichiers frontend"""
        print("\n📁 Test de l'existence des fichiers...")
        
        files_to_check = [
            "static/css/terminal.css",
            "static/js/terminal.js", 
            "templates/terminal.html",
            "data/effects/ascii/success.txt",
            "data/effects/ascii/luna_contact.txt"
        ]
        
        for file_path in files_to_check:
            if os.path.exists(file_path):
                size = os.path.getsize(file_path)
                self.log(f"Fichier {file_path}", True, f"Trouvé ({size} bytes)")
            else:
                self.log(f"Fichier {file_path}", False, "Fichier manquant")
                
    def test_css_content(self):
        """Teste le contenu du CSS"""
        print("\n🎨 Test du contenu CSS...")
        
        css_file = "static/css/terminal.css"
        if os.path.exists(css_file):
            with open(css_file, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # Vérifications CSS
            checks = [
                ("Variables CSS", ":root" in content),
                ("Couleurs néon", "#00ff88" in content or "#ffea00" in content),
                ("Animations", "@keyframes" in content),
                ("Media queries", "@media" in content),
                ("Terminal container", ".terminal-container" in content),
                ("Responsive", "max-width" in content)
            ]
            
            for name, check in checks:
                self.log(f"CSS {name}", check, "Trouvé" if check else "Manquant")
        else:
            self.log("CSS terminal.css", False, "Fichier manquant")
            
    def test_js_content(self):
        """Teste le contenu du JavaScript"""
        print("\n⚡ Test du contenu JavaScript...")
        
        js_file = "static/js/terminal.js"
        if os.path.exists(js_file):
            with open(js_file, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # Vérifications JS
            checks = [
                ("Event listener", "addEventListener" in content),
                ("Fetch API", "fetch" in content),
                ("DOM manipulation", "getElementById" in content),
                ("Form handling", "preventDefault" in content),
                ("JSON handling", "JSON.stringify" in content)
            ]
            
            for name, check in checks:
                self.log(f"JS {name}", check, "Trouvé" if check else "Manquant")
        else:
            self.log("JS terminal.js", False, "Fichier manquant")
            
    def test_html_content(self):
        """Teste le contenu du HTML"""
        print("\n🌐 Test du contenu HTML...")
        
        html_file = "templates/terminal.html"
        if os.path.exists(html_file):
            with open(html_file, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # Vérifications HTML
            checks = [
                ("DOCTYPE", "<!DOCTYPE html>" in content),
                ("Meta viewport", "viewport" in content),
                ("CSS link", "terminal.css" in content),
                ("JS script", "terminal.js" in content),
                ("Terminal container", "terminal-container" in content),
                ("Input field", "terminal-input" in content),
                ("Prompt LUNA", "LUNA" in content)
            ]
            
            for name, check in checks:
                self.log(f"HTML {name}", check, "Trouvé" if check else "Manquant")
        else:
            self.log("HTML terminal.html", False, "Fichier manquant")
            
    def test_ascii_effects(self):
        """Teste les effets ASCII"""
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
                    # Vérifications ASCII
                    has_unicode = any(ord(c) > 127 for c in content)
                    has_emoji = "🌙" in content or "✅" in content
                    has_art = "╔" in content or ".-" in content
                    
                    self.log(f"ASCII {ascii_file}", True, f"Contenu: {len(content)} chars")
                    self.log(f"  - Unicode", has_unicode, "Caractères spéciaux trouvés")
                    self.log(f"  - Emojis", has_emoji, "Emojis trouvés")
                    self.log(f"  - Art", has_art, "ASCII art trouvé")
                else:
                    self.log(f"ASCII {ascii_file}", False, "Fichier vide")
            else:
                self.log(f"ASCII {ascii_file}", False, "Fichier manquant")
                
    def test_server_connection(self):
        """Teste la connexion au serveur"""
        print("\n🌐 Test de connexion au serveur...")
        
        try:
            # Test de base
            response = urllib.request.urlopen(f"{self.base_url}/", timeout=5)
            if response.getcode() == 200:
                self.log("Serveur accessible", True, f"Status: {response.getcode()}")
            else:
                self.log("Serveur accessible", False, f"Status: {response.getcode()}")
        except Exception as e:
            self.log("Serveur accessible", False, f"Erreur: {e}")
            
    def test_terminal_endpoint(self):
        """Teste l'endpoint terminal"""
        print("\n🖥️ Test de l'endpoint terminal...")
        
        try:
            response = urllib.request.urlopen(f"{self.base_url}/terminal", timeout=5)
            if response.getcode() == 200:
                content = response.read().decode('utf-8')
                
                # Vérifications basiques
                checks = [
                    ("HTML structure", "<html" in content and "</html>" in content),
                    ("CSS link", "terminal.css" in content),
                    ("JS script", "terminal.js" in content),
                    ("Terminal container", "terminal-container" in content),
                    ("LUNA prompt", "LUNA" in content)
                ]
                
                for name, check in checks:
                    self.log(f"Terminal {name}", check, "Trouvé" if check else "Manquant")
            else:
                self.log("Endpoint terminal", False, f"Status: {response.getcode()}")
        except Exception as e:
            self.log("Endpoint terminal", False, f"Erreur: {e}")
            
    def test_static_files(self):
        """Teste l'accessibilité des fichiers statiques"""
        print("\n📂 Test des fichiers statiques...")
        
        static_files = [
            "/static/css/terminal.css",
            "/static/js/terminal.js"
        ]
        
        for static_file in static_files:
            try:
                response = urllib.request.urlopen(f"{self.base_url}{static_file}", timeout=5)
                if response.getcode() == 200:
                    content = response.read().decode('utf-8')
                    self.log(f"Statique {static_file}", True, f"Accessible ({len(content)} chars)")
                else:
                    self.log(f"Statique {static_file}", False, f"Status: {response.getcode()}")
            except Exception as e:
                self.log(f"Statique {static_file}", False, f"Erreur: {e}")
                
    def run_all_tests(self):
        """Lance tous les tests"""
        print("🚀 Démarrage des tests Frontend Simplifiés")
        print("=" * 50)
        
        self.test_files_exist()
        self.test_css_content()
        self.test_js_content()
        self.test_html_content()
        self.test_ascii_effects()
        self.test_server_connection()
        self.test_terminal_endpoint()
        self.test_static_files()
        
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
            print("🎮 Le frontend est prêt pour la démo !")
        else:
            print("\n⚠️ Certains tests ont échoué. Vérifiez les erreurs ci-dessus.")
            
        return passed == total

def main():
    """Fonction principale"""
    tester = SimpleFrontendTester()
    success = tester.run_all_tests()
    
    if success:
        print("\n🌐 Ouvrez http://127.0.0.1:5001/terminal dans votre navigateur")
        print("📖 Consultez DEMO_GUIDEE.md pour la démo complète")
    else:
        print("\n🔧 Des corrections sont nécessaires avant la démo.")
        
    return 0 if success else 1

if __name__ == "__main__":
    exit(main()) 