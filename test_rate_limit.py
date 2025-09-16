#!/usr/bin/env python3
"""
Test simple pour vérifier que le rate limiting est supprimé
"""

import requests
import time
import json

def test_rate_limit_removal():
    """Test que le rate limiting est bien supprimé"""
    base_url = "http://localhost:5001"
    
    print("🧪 Test de suppression du rate limiting...")
    
    # Faire plusieurs requêtes rapides
    for i in range(10):
        try:
            response = requests.post(
                f"{base_url}/commande",
                json={"commande": "aide"},
                headers={"Content-Type": "application/json"},
                timeout=5
            )
            
            print(f"Requête {i+1}: Status {response.status_code}")
            
            if response.status_code == 429:
                print("❌ Rate limiting encore actif !")
                return False
                
            if response.status_code == 200:
                data = response.json()
                if "reponse" in data and "réussite" in data["reponse"]:
                    print(f"✅ Réponse {i+1}: {data['reponse']['message'][:50]}...")
                else:
                    print(f"⚠️  Réponse {i+1}: Format inattendu")
            
            # Petite pause pour éviter de surcharger
            time.sleep(0.1)
            
        except requests.exceptions.RequestException as e:
            print(f"❌ Erreur requête {i+1}: {e}")
            return False
    
    print("✅ Test terminé - Aucun rate limiting détecté !")
    return True

if __name__ == "__main__":
    test_rate_limit_removal()
