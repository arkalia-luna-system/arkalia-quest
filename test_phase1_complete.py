#!/usr/bin/env python3
"""
Test complet de la PHASE 1 - Arkalia Quest
Vérifie que toute la nouvelle structure narrative fonctionne
"""

import json
import os
import sys
from pathlib import Path

# Ajouter le dossier core au path
sys.path.append('core')

try:
    from mission_handler import MissionHandler
except ImportError:
    print("❌ Erreur: Impossible d'importer MissionHandler")
    sys.exit(1)

def test_structure_files():
    """Test que tous les fichiers de structure existent"""
    print("🔍 Test des fichiers de structure...")
    
    required_files = [
        "data/story.json",
        "data/dialogues_dynamiques.json",
        "data/missions/prologue.json",
        "data/missions/acte_1.json",
        "data/missions/acte_2.json",
        "data/missions/acte_3.json",
        "data/missions/acte_4.json",
        "data/missions/acte_5.json",
        "data/missions/acte_6.json",
        "data/missions/epilogue.json",
        "core/mission_handler.py"
    ]
    
    all_exist = True
    for file_path in required_files:
        if os.path.exists(file_path):
            print(f"  ✅ {file_path}")
        else:
            print(f"  ❌ {file_path} - MANQUANT")
            all_exist = False
    
    return all_exist

def test_story_structure():
    """Test de la structure du fichier story.json"""
    print("\n📖 Test de la structure story.json...")
    
    try:
        with open("data/story.json", 'r', encoding='utf-8') as f:
            story = json.load(f)
        
        # Vérifier les personnages
        personnages = story.get('personnages', {})
        required_personnages = ['luna', 'nexus', 'althea', 'joueur', 'la_corp', 'shadow_13', 'pandora']
        
        for perso in required_personnages:
            if perso in personnages:
                print(f"  ✅ Personnage {perso}")
            else:
                print(f"  ❌ Personnage {perso} - MANQUANT")
                return False
        
        # Vérifier les actes
        actes = story.get('actes', {})
        required_actes = ['prologue', 'acte_1', 'acte_2', 'acte_3', 'acte_4', 'acte_5', 'acte_6', 'epilogue']
        
        for acte in required_actes:
            if acte in actes:
                print(f"  ✅ Acte {acte}")
            else:
                print(f"  ❌ Acte {acte} - MANQUANT")
                return False
        
        return True
        
    except Exception as e:
        print(f"  ❌ Erreur lecture story.json: {e}")
        return False

def test_dialogues_structure():
    """Test de la structure des dialogues"""
    print("\n💬 Test de la structure dialogues...")
    
    try:
        with open("data/dialogues_dynamiques.json", 'r', encoding='utf-8') as f:
            dialogues = json.load(f)
        
        # Vérifier les dialogues par acte
        dialogues_par_acte = dialogues.get('dialogues_par_acte', {})
        required_actes = ['prologue', 'acte_1', 'acte_2', 'acte_3', 'acte_4', 'acte_5', 'acte_6', 'epilogue']
        
        for acte in required_actes:
            if acte in dialogues_par_acte:
                acte_dialogues = dialogues_par_acte[acte]
                if acte_dialogues:
                    print(f"  ✅ Dialogues pour {acte} ({len(acte_dialogues)} personnages)")
                else:
                    print(f"  ⚠️ Dialogues vides pour {acte}")
            else:
                print(f"  ❌ Dialogues manquants pour {acte}")
                return False
        
        # Vérifier les réactions émotionnelles
        reactions = dialogues.get('reactions_emotionnelles', {})
        if reactions:
            print(f"  ✅ Réactions émotionnelles ({len(reactions)} personnages)")
        else:
            print(f"  ❌ Réactions émotionnelles manquantes")
            return False
        
        return True
        
    except Exception as e:
        print(f"  ❌ Erreur lecture dialogues: {e}")
        return False

def test_missions_structure():
    """Test de la structure des missions"""
    print("\n🎯 Test de la structure des missions...")
    
    missions_path = Path("data/missions")
    mission_files = list(missions_path.glob("*.json"))
    
    # Filtrer seulement les nouvelles missions (prologue, acte_1 à acte_6, epilogue)
    new_missions = [f for f in mission_files if f.name in ['prologue.json', 'acte_1.json', 'acte_2.json', 'acte_3.json', 'acte_4.json', 'acte_5.json', 'acte_6.json', 'epilogue.json']]
    
    if len(new_missions) != 8:  # 7 actes + épilogue
        print(f"  ❌ Nombre de nouvelles missions incorrect: {len(new_missions)} au lieu de 8")
        return False
    
    for mission_file in new_missions:
        try:
            with open(mission_file, 'r', encoding='utf-8') as f:
                mission = json.load(f)
            
            # Vérifier les champs requis
            required_fields = ['id', 'titre', 'description', 'difficulte', 'recompense', 'etapes', 'objectifs', 'conseils', 'personnages', 'objet_symbolique', 'cliffhanger']
            
            for field in required_fields:
                if field not in mission:
                    print(f"  ❌ Champ '{field}' manquant dans {mission_file.name}")
                    return False
            
            # Vérifier qu'il y a des étapes
            if not mission['etapes']:
                print(f"  ❌ Aucune étape dans {mission_file.name}")
                return False
            
            print(f"  ✅ {mission_file.name} - {len(mission['etapes'])} étapes")
            
        except Exception as e:
            print(f"  ❌ Erreur lecture {mission_file.name}: {e}")
            return False
    
    return True

def test_mission_handler():
    """Test du gestionnaire de missions"""
    print("\n⚙️ Test du gestionnaire de missions...")
    
    try:
        handler = MissionHandler()
        
        # Test de chargement des données
        if handler.missions:
            print(f"  ✅ {len(handler.missions)} missions chargées")
        else:
            print("  ❌ Aucune mission chargée")
            return False
        
        if handler.dialogues:
            print("  ✅ Dialogues chargés")
        else:
            print("  ❌ Dialogues non chargés")
            return False
        
        if handler.story:
            print("  ✅ Histoire chargée")
        else:
            print("  ❌ Histoire non chargée")
            return False
        
        # Test avec un profil fictif
        profil_test = {
            'points': 0,
            'missions_completed': [],
            'etapes_completed': {}
        }
        
        # Test récupération de l'acte actuel
        current_acte = handler.get_current_acte(profil_test)
        if current_acte == 'prologue':
            print("  ✅ Acte actuel correct (prologue)")
        else:
            print(f"  ❌ Acte actuel incorrect: {current_acte}")
            return False
        
        # Test récupération des missions disponibles
        available_missions = handler.get_available_missions(profil_test)
        if available_missions:
            print(f"  ✅ {len(available_missions)} missions disponibles")
        else:
            print("  ❌ Aucune mission disponible")
            return False
        
        # Test dialogue
        dialogue = handler.get_dialogue('luna', 'prologue', 'accueil')
        if dialogue and ('luna' in dialogue.lower() or '🌙' in dialogue):
            print("  ✅ Dialogue récupéré")
        else:
            print(f"  ❌ Dialogue non récupéré: '{dialogue}'")
            return False
        
        return True
        
    except Exception as e:
        print(f"  ❌ Erreur MissionHandler: {e}")
        return False

def test_assets():
    """Test des assets créés"""
    print("\n🎨 Test des assets...")
    
    required_assets = [
        "data/effects/ascii/fusion_arkalia.txt",
        "data/effects/ascii/pandora_reveil.txt",
        "data/objets_symboliques/Frag_Althea_SOS.txt"
    ]
    
    all_exist = True
    for asset_path in required_assets:
        if os.path.exists(asset_path):
            print(f"  ✅ {asset_path}")
        else:
            print(f"  ❌ {asset_path} - MANQUANT")
            all_exist = False
    
    return all_exist

def main():
    """Test principal de la PHASE 1"""
    print("🚀 TEST COMPLET DE LA PHASE 1 - ARKALIA QUEST")
    print("=" * 50)
    
    tests = [
        ("Fichiers de structure", test_structure_files),
        ("Structure story.json", test_story_structure),
        ("Structure dialogues", test_dialogues_structure),
        ("Structure missions", test_missions_structure),
        ("Gestionnaire de missions", test_mission_handler),
        ("Assets", test_assets)
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
        print("🎉 TOUS LES TESTS PASSÉS ! La PHASE 1 est opérationnelle !")
        return True
    else:
        print("⚠️ Certains tests ont échoué. Vérifiez les erreurs ci-dessus.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 