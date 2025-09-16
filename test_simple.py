#!/usr/bin/env python3
"""
Test simple pour isoler le problème
"""

import requests
import json

def test_simple():
    """Test simple de la route /commande"""
    try:
        response = requests.post(
            "http://localhost:5001/commande",
            json={"commande": "aide"},
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        
        print(f"Status: {response.status_code}")
        print(f"Headers: {dict(response.headers)}")
        print(f"Content: {response.text}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"JSON: {json.dumps(data, indent=2)}")
        
    except Exception as e:
        print(f"Erreur: {e}")

if __name__ == "__main__":
    test_simple()
