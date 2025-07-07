#!/usr/bin/env python3
"""
Test complet de la suite Arkalia Quest v2.0
Valide toutes les nouvelles fonctionnalités
"""

import os
import json
import urllib.request
import urllib.parse
import urllib.error
from pathlib import Path

class CompleteSuiteTester:
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
        
    def test_ascii_effects_complete(self):
        """Teste tous les effets ASCII"""
        print("\n🎭 Test complet des effets ASCII...")
        
        ascii_files = [
            "data/effects/ascii/success.txt",
            "data/effects/ascii/luna_contact.txt",
            "data/effects/ascii/error.txt",
            "data/effects/ascii/level_up.txt"
        ]
        
        for ascii_file in ascii_files:
            if os.path.exists(ascii_file):
                with open(ascii_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    
                if content.strip():
                    # Analyse détaillée
                    has_unicode = any(ord(c) > 127 for c in content)
                    has_emoji = any(c in "🌙✅❌🎉🌟🎯🔍🤝⚖️🎨💡" for c in content)
                    has_art = any(c in "╔╗╚╝║═█░" for c in content)
                    has_text = any(c.isalpha() for c in content)
                    
                    self.log(f"ASCII {ascii_file}", True, f"{len(content)} chars")
                    self.log(f"  - Unicode", has_unicode, "Caractères spéciaux")
                    self.log(f"  - Emojis", has_emoji, "Emojis présents")
                    self.log(f"  - Art", has_art, "ASCII art")
                    self.log(f"  - Texte", has_text, "Texte descriptif")
                else:
                    self.log(f"ASCII {ascii_file}", False, "Fichier vide")
            else:
                self.log(f"ASCII {ascii_file}", False, "Fichier manquant")
                
    def test_dashboard_css(self):
        """Teste le CSS du dashboard"""
        print("\n🎨 Test du CSS Dashboard...")
        
        css_file = "static/css/dashboard.css"
        if os.path.exists(css_file):
            with open(css_file, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # Vérifications CSS
            checks = [
                ("Variables CSS", ":root" in content),
                ("Grid Layout", "grid-template-columns" in content),
                ("Animations", "@keyframes" in content),
                ("Responsive", "@media" in content),
                ("Cards", ".stat-card" in content),
                ("Badges", ".badge" in content),
                ("Progress bars", ".progress-bar" in content),
                ("Hover effects", ":hover" in content)
            ]
            
            for name, check in checks:
                self.log(f"Dashboard CSS {name}", check, "Trouvé" if check else "Manquant")
        else:
            self.log("Dashboard CSS", False, "Fichier manquant")
            
    def test_effects_js(self):
        """Teste le JavaScript des effets"""
        print("\n🎵 Test du JavaScript des effets...")
        
        js_file = "static/js/effects.js"
        if os.path.exists(js_file):
            with open(js_file, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # Vérifications JS
            checks = [
                ("Class EffectsEngine", "class EffectsEngine" in content),
                ("Audio Context", "AudioContext" in content),
                ("Sound creation", "createBeep" in content),
                ("Matrix rain", "createMatrixRain" in content),
                ("Glow effects", "createGlowEffect" in content),
                ("Typing effect", "createTypingEffect" in content),
                ("Shake effect", "createShakeEffect" in content),
                ("Success animation", "createSuccessAnimation" in content),
                ("Error animation", "createErrorAnimation" in content),
                ("Level up animation", "createLevelUpAnimation" in content)
            ]
            
            for name, check in checks:
                self.log(f"Effects JS {name}", check, "Trouvé" if check else "Manquant")
        else:
            self.log("Effects JS", False, "Fichier manquant")
            
    def test_luna_ai_v2(self):
        """Teste LUNA AI v2"""
        print("\n🤖 Test de LUNA AI v2...")
        
        luna_file = "utils/luna_ai_v2.py"
        if os.path.exists(luna_file):
            with open(luna_file, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # Vérifications LUNA
            checks = [
                ("Class LunaAI", "class LunaAI" in content),
                ("Personnalité", "personnalite" in content),
                ("Analyse contexte", "analyser_contexte" in content),
                ("Génération réponse", "generer_reponse" in content),
                ("Analyse progression", "analyser_progression" in content),
                ("Mission personnalisée", "generer_mission_personnalisee" in content),
                ("Statut", "get_statut" in content),
                ("Phrases personnalité", "phrases_personnalite" in content),
                ("Historique", "historique_conversations" in content)
            ]
            
            for name, check in checks:
                self.log(f"LUNA v2 {name}", check, "Trouvé" if check else "Manquant")
        else:
            self.log("LUNA v2", False, "Fichier manquant")
            
    def test_missions_json(self):
        """Teste les missions JSON avancées"""
        print("\n🎯 Test des missions JSON avancées...")
        
        mission_file = "data/missions/hacker_challenge.json"
        if os.path.exists(mission_file):
            try:
                with open(mission_file, 'r', encoding='utf-8') as f:
                    mission = json.load(f)
                    
                # Vérifications mission
                required_fields = ["id", "titre", "description", "difficulte", "choix", "recompenses"]
                for field in required_fields:
                    if field in mission:
                        self.log(f"Mission {field}", True, f"Présent: {type(mission[field]).__name__}")
                    else:
                        self.log(f"Mission {field}", False, "Manquant")
                        
                # Vérification des choix
                if "choix" in mission:
                    choices = mission["choix"]
                    self.log(f"Mission choix", True, f"{len(choices)} choix disponibles")
                    
                    for i, choice in enumerate(choices):
                        if "id" in choice and "texte" in choice and "consequences" in choice:
                            self.log(f"  Choix {i+1}", True, f"'{choice['id']}' - {choice['texte'][:30]}...")
                        else:
                            self.log(f"  Choix {i+1}", False, "Structure invalide")
                            
                # Vérification des récompenses
                if "recompenses" in mission:
                    rewards = mission["recompenses"]
                    self.log(f"Mission récompenses", True, f"Score: {rewards.get('score_base', 'N/A')}")
                    
            except json.JSONDecodeError as e:
                self.log("Mission JSON", False, f"Erreur JSON: {e}")
        else:
            self.log("Mission JSON", False, "Fichier manquant")
            
    def test_static_files_accessibility(self):
        """Teste l'accessibilité des fichiers statiques"""
        print("\n📂 Test d'accessibilité des fichiers statiques...")
        
        static_files = [
            "/static/css/terminal.css",
            "/static/css/dashboard.css",
            "/static/js/terminal.js",
            "/static/js/effects.js"
        ]
        
        for static_file in static_files:
            try:
                response = urllib.request.urlopen(f"{self.base_url}{static_file}", timeout=5)
                if response.getcode() == 200:
                    content = response.read().decode('utf-8')
                    self.log(f"Statique {static_file}", True, f"Accessible ({len(content)} chars)")
                else:
                    self.log(f"Statique {static_file}", False, f"Status {response.getcode()}")
            except Exception as e:
                self.log(f"Statique {static_file}", False, f"Erreur: {e}")
                
    def test_advanced_commands(self):
        """Teste les commandes avancées"""
        print("\n⌨️ Test des commandes avancées...")
        
        # Test avec la nouvelle mission
        try:
            # Simule une commande qui pourrait charger la mission
            req = urllib.request.Request(
                f"{self.base_url}/commande",
                data=json.dumps({"cmd": "load_mission"}).encode('utf-8'),
                headers={'Content-Type': 'application/json'}
            )
            response = urllib.request.urlopen(req, timeout=10)
            
            if response.getcode() == 200:
                data = json.loads(response.read().decode('utf-8'))
                self.log("Commande load_mission", True, f"Réponse: {data.get('message', '')[:50]}...")
            else:
                self.log("Commande load_mission", False, f"Status {response.getcode()}")
        except Exception as e:
            self.log("Commande load_mission", False, f"Erreur: {e}")
            
    def test_file_structure(self):
        """Teste la structure complète des fichiers"""
        print("\n📁 Test de la structure des fichiers...")
        
        required_structure = [
            "static/css/terminal.css",
            "static/css/dashboard.css", 
            "static/js/terminal.js",
            "static/js/effects.js",
            "templates/terminal.html",
            "data/effects/ascii/success.txt",
            "data/effects/ascii/luna_contact.txt",
            "data/effects/ascii/error.txt",
            "data/effects/ascii/level_up.txt",
            "data/missions/hacker_challenge.json",
            "utils/luna_ai_v2.py",
            "tests/test_suite_complete.py"
        ]
        
        for file_path in required_structure:
            if os.path.exists(file_path):
                size = os.path.getsize(file_path)
                self.log(f"Structure {file_path}", True, f"Trouvé ({size} bytes)")
            else:
                self.log(f"Structure {file_path}", False, "Manquant")
                
    def run_complete_suite(self):
        """Lance la suite complète de tests"""
        print("🚀 SUITE COMPLÈTE DE TESTS - Arkalia Quest v2.0")
        print("=" * 60)
        
        self.test_ascii_effects_complete()
        self.test_dashboard_css()
        self.test_effects_js()
        self.test_luna_ai_v2()
        self.test_missions_json()
        self.test_static_files_accessibility()
        self.test_advanced_commands()
        self.test_file_structure()
        
        # Résumé complet
        print("\n" + "=" * 60)
        print("📊 RÉSUMÉ COMPLET DE LA SUITE")
        print("=" * 60)
        
        passed = sum(1 for r in self.results if r["success"])
        total = len(self.results)
        
        print(f"✅ Tests réussis: {passed}/{total}")
        print(f"❌ Tests échoués: {total - passed}/{total}")
        print(f"📈 Taux de réussite: {(passed/total)*100:.1f}%")
        
        if passed == total:
            print("\n🎉 SUITE COMPLÈTE VALIDÉE !")
            print("🌟 Arkalia Quest v2.0 est prêt pour la production !")
        elif passed >= total * 0.9:
            print("\n⚠️ SUITE PRESQUE COMPLÈTE")
            print("🔧 Quelques ajustements mineurs nécessaires")
        else:
            print("\n🔧 SUITE INCOMPLÈTE")
            print("⚠️ Des corrections importantes sont nécessaires")
            
        return passed == total

def main():
    """Fonction principale"""
    tester = CompleteSuiteTester()
    success = tester.run_complete_suite()
    
    if success:
        print("\n🎮 La suite complète est opérationnelle !")
        print("🌐 Prêt pour le déploiement et les ados de 13 ans !")
    else:
        print("\n🔧 Des corrections sont nécessaires avant la production.")
        
    return 0 if success else 1

if __name__ == "__main__":
    exit(main()) 