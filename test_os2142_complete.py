#!/usr/bin/env python3
"""
Test complet de l'OS 2142 - Arkalia Quest
Vérifie que toute l'interface OS 2142 fonctionne correctement
"""

import json
import os
import sys
from pathlib import Path

def test_os2142_files():
    """Test que tous les fichiers de l'OS 2142 existent"""
    print("🔍 Test des fichiers OS 2142...")
    
    required_files = [
        "templates/os2142.html",
        "static/js/os2142.js",
        "static/css/os2142.css"
    ]
    
    all_exist = True
    for file_path in required_files:
        if os.path.exists(file_path):
            print(f"  ✅ {file_path}")
        else:
            print(f"  ❌ {file_path} - MANQUANT")
            all_exist = False
    
    return all_exist

def test_os2142_html_structure():
    """Test de la structure HTML de l'OS 2142"""
    print("\n📄 Test de la structure HTML...")
    
    try:
        with open("templates/os2142.html", 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        # Vérifier les éléments essentiels
        required_elements = [
            'id="os2142"',
            'id="sidebar"',
            'id="desktop"',
            'id="hud"',
            'id="window-terminal"',
            'id="btn-files"',
            'id="btn-terminal"',
            'id="btn-mail"',
            'id="btn-audio"',
            'id="btn-web"'
        ]
        
        for element in required_elements:
            if element in html_content:
                print(f"  ✅ Élément {element}")
            else:
                print(f"  ❌ Élément {element} - MANQUANT")
                return False
        
        # Vérifier les scripts et CSS
        if 'os2142.css' in html_content:
            print("  ✅ CSS OS 2142 lié")
        else:
            print("  ❌ CSS OS 2142 non lié")
            return False
        
        if 'os2142.js' in html_content:
            print("  ✅ JS OS 2142 lié")
        else:
            print("  ❌ JS OS 2142 non lié")
            return False
        
        return True
        
    except Exception as e:
        print(f"  ❌ Erreur lecture HTML: {e}")
        return False

def test_os2142_js_structure():
    """Test de la structure JavaScript de l'OS 2142"""
    print("\n⚙️ Test de la structure JavaScript...")
    
    try:
        with open("static/js/os2142.js", 'r', encoding='utf-8') as f:
            js_content = f.read()
        
        # Vérifier les classes et méthodes essentielles
        required_classes = [
            'class OS2142',
            'constructor()',
            'init()',
            'setupSidebar()',
            'setupHUD()',
            'createExplorerWindow()',
            'createMailWindow()',
            'createAudioWindow()',
            'createWebWindow()'
        ]
        
        for class_method in required_classes:
            if class_method in js_content:
                print(f"  ✅ {class_method}")
            else:
                print(f"  ❌ {class_method} - MANQUANT")
                return False
        
        # Vérifier les modules
        modules = ['explorer', 'mail', 'audio', 'web']
        for module in modules:
            if f'create{module.capitalize()}Window' in js_content:
                print(f"  ✅ Module {module}")
            else:
                print(f"  ❌ Module {module} - MANQUANT")
                return False
        
        return True
        
    except Exception as e:
        print(f"  ❌ Erreur lecture JavaScript: {e}")
        return False

def test_os2142_css_structure():
    """Test de la structure CSS de l'OS 2142"""
    print("\n🎨 Test de la structure CSS...")
    
    try:
        with open("static/css/os2142.css", 'r', encoding='utf-8') as f:
            css_content = f.read()
        
        # Vérifier les styles essentiels
        required_styles = [
            '#os2142',
            '#sidebar',
            '#desktop',
            '#hud',
            '.window',
            '.window-header',
            '.window-content',
            '#explorer-content',
            '#mail-list',
            '#audio-player',
            '#web-simulator'
        ]
        
        for style in required_styles:
            if style in css_content:
                print(f"  ✅ Style {style}")
            else:
                print(f"  ❌ Style {style} - MANQUANT")
                return False
        
        # Vérifier les animations
        animations = ['windowOpen', 'notification']
        for animation in animations:
            if f'@keyframes {animation}' in css_content:
                print(f"  ✅ Animation {animation}")
            else:
                print(f"  ❌ Animation {animation} - MANQUANT")
                return False
        
        return True
        
    except Exception as e:
        print(f"  ❌ Erreur lecture CSS: {e}")
        return False

def test_app_integration():
    """Test de l'intégration dans l'application Flask"""
    print("\n🔗 Test de l'intégration Flask...")
    
    try:
        with open("app.py", 'r', encoding='utf-8') as f:
            app_content = f.read()
        
        # Vérifier la route OS 2142
        if '@app.route(\'/os2142\')' in app_content:
            print("  ✅ Route /os2142")
        else:
            print("  ❌ Route /os2142 - MANQUANT")
            return False
        
        if 'def os2142():' in app_content:
            print("  ✅ Fonction os2142()")
        else:
            print("  ❌ Fonction os2142() - MANQUANT")
            return False
        
        if 'render_template(\'os2142.html\')' in app_content:
            print("  ✅ Template os2142.html")
        else:
            print("  ❌ Template os2142.html - MANQUANT")
            return False
        
        return True
        
    except Exception as e:
        print(f"  ❌ Erreur lecture app.py: {e}")
        return False

def test_mission_integration():
    """Test de l'intégration avec le système de missions"""
    print("\n🎯 Test de l'intégration missions...")
    
    try:
        # Vérifier que le gestionnaire de missions existe
        if os.path.exists("core/mission_handler.py"):
            print("  ✅ MissionHandler existe")
        else:
            print("  ❌ MissionHandler manquant")
            return False
        
        # Vérifier que les missions existent
        missions_path = Path("data/missions")
        new_missions = ['prologue.json', 'acte_1.json', 'acte_2.json', 'acte_3.json', 
                       'acte_4.json', 'acte_5.json', 'acte_6.json', 'epilogue.json']
        
        for mission in new_missions:
            if (missions_path / mission).exists():
                print(f"  ✅ Mission {mission}")
            else:
                print(f"  ❌ Mission {mission} - MANQUANT")
                return False
        
        return True
        
    except Exception as e:
        print(f"  ❌ Erreur test missions: {e}")
        return False

def main():
    """Test principal de l'OS 2142"""
    print("🚀 TEST COMPLET DE L'OS 2142 - ARKALIA QUEST")
    print("=" * 50)
    
    tests = [
        ("Fichiers OS 2142", test_os2142_files),
        ("Structure HTML", test_os2142_html_structure),
        ("Structure JavaScript", test_os2142_js_structure),
        ("Structure CSS", test_os2142_css_structure),
        ("Intégration Flask", test_app_integration),
        ("Intégration Missions", test_mission_integration)
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n📋 {test_name}")
        print("-" * 30)
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"  ❌ Erreur dans {test_name}: {e}")
            results.append((test_name, False))
    
    # Résumé
    print("\n" + "=" * 50)
    print("📊 RÉSUMÉ DES TESTS")
    print("=" * 50)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASSÉ" if result else "❌ ÉCHOUÉ"
        print(f"{status} - {test_name}")
        if result:
            passed += 1
    
    print(f"\n🎯 Résultat: {passed}/{total} tests passés")
    
    if passed == total:
        print("🎉 TOUS LES TESTS PASSÉS ! L'OS 2142 est opérationnel !")
        return True
    else:
        print("⚠️ Certains tests ont échoué. Vérifiez les erreurs ci-dessus.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 