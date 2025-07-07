#!/usr/bin/env python3
"""
Script de test pour le tutoriel Arkalia Quest
Teste le tutoriel complet depuis le début
"""

import requests
import json
import time

def get_profile():
    """Récupère le profil actuel"""
    try:
        response = requests.get("http://localhost:5001/data/profil_joueur.json")
        if response.status_code == 200:
            return response.json()
    except:
        pass
    return {}

def test_tutoriel():
    """Teste le tutoriel complet"""
    
    base_url = "http://localhost:5001"
    
    # Réinitialiser le profil (supprimer tutorial_step)
    print("🔄 Réinitialisation du profil...")
    try:
        profil = get_profile()
        if "tutorial_step" in profil:
            del profil["tutorial_step"]
            # Sauvegarder le profil modifié
            with open("data/profil_joueur.json", "w", encoding="utf-8") as f:
                json.dump(profil, f, indent=2, ensure_ascii=False)
            print("✅ Profil réinitialisé")
    except Exception as e:
        print(f"⚠️ Erreur lors de la réinitialisation: {e}")
    
    # Test des étapes du tutoriel
    etapes = [
        ("start_tutorial", "🎯 ÉTAPE 1/5 - Démarrage du tutoriel"),
        ("luna_contact", "🌙 ÉTAPE 2/5 - Contact avec LUNA"),
        ("scan_persona", "🔍 ÉTAPE 3/5 - Analyse personnalité"),
        ("unlock_universe", "🌌 ÉTAPE 4/5 - Déblocage univers"),
        ("load_mission", "🏆 ÉTAPE 5/5 - Fin du tutoriel")
    ]
    
    for commande, description in etapes:
        print(f"\n{description}")
        print(f"📤 Envoi de la commande: {commande}")
        
        # Afficher le tutorial_step avant la commande
        profil_avant = get_profile()
        tutorial_step_avant = profil_avant.get("tutorial_step", "Non défini")
        print(f"📊 Tutorial step avant: {tutorial_step_avant}")
        
        try:
            response = requests.post(
                f"{base_url}/commande",
                headers={"Content-Type": "application/json"},
                json={"cmd": commande}
            )
            
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Succès: {data.get('réussite', False)}")
                print(f"📝 Message: {data.get('message', 'Aucun message')[:100]}...")
                print(f"🎯 Score gagné: {data.get('score_gagne', 0)}")
                print(f"🏆 Badge: {data.get('badge', 'Aucun')}")
                print(f"🎮 Mode tutoriel: {data.get('tutorial_mode', False)}")
                print(f"➡️ Prochaine commande: {data.get('next_command', 'Aucune')}")
                
                # Afficher le tutorial_step après la commande
                time.sleep(0.5)  # Attendre que le profil soit sauvegardé
                profil_apres = get_profile()
                tutorial_step_apres = profil_apres.get("tutorial_step", "Non défini")
                print(f"📊 Tutorial step après: {tutorial_step_apres}")
                
                if data.get('tutorial_completed'):
                    print("🎉 TUTORIEL TERMINÉ AVEC SUCCÈS !")
                    break
                    
            else:
                print(f"❌ Erreur HTTP: {response.status_code}")
                print(f"📄 Réponse: {response.text}")
                
        except Exception as e:
            print(f"❌ Erreur: {e}")
        
        time.sleep(1)  # Pause entre les commandes
    
    print("\n🎮 Test du tutoriel terminé !")

if __name__ == "__main__":
    test_tutoriel() 