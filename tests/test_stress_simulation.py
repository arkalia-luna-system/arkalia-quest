#!/usr/bin/env python3
"""
Test de Stress Arkalia Quest
Simule plusieurs joueurs connectés simultanément
et teste la robustesse du système
"""

import os
import pytest
import json
import time
import threading
import random
from datetime import datetime
from typing import Dict, List, Any
from app import app, PROFIL_PATH, sauvegarder_profil

def reset_profil():
    if os.path.exists(PROFIL_PATH):
        os.remove(PROFIL_PATH)

@pytest.fixture(autouse=True)
def client():
    reset_profil()
    with app.test_client() as client:
        yield client

def send_cmd(client, cmd):
    return client.post('/commande', json={'cmd': cmd})

def test_commandes_tres_longues(client):
    """Test avec des commandes très longues"""
    commandes_longues = [
        'A' * 1000,  # 1000 caractères
        'unlock_universe ' + 'x' * 500,
        'scan_persona' + ' ' * 200 + 'extra',
        'aide' + '?' * 300,
    ]
    
    for cmd in commandes_longues:
        r = send_cmd(client, cmd)
        assert r.status_code == 200
        data = r.get_json()
        assert 'message' in data

def test_commandes_caracteres_speciaux(client):
    """Test avec des caractères spéciaux"""
    commandes_speciales = [
        'unlock_universe!@#$%^&*()',
        'scan_persona\n\t\r',
        'aide<script>alert("xss")</script>',
        'profil"\'\\',
        'assistant_pirate 💻🚀🎮',
        'generer_meme 🎯🔥💪',
    ]
    
    for cmd in commandes_speciales:
        r = send_cmd(client, cmd)
        assert r.status_code == 200
        data = r.get_json()
        assert 'message' in data

def test_spam_commandes(client):
    """Test de spam de commandes"""
    commandes = ['aide', 'profil', 'unlock_universe', 'scan_persona']
    
    # Envoie chaque commande 10 fois rapidement
    for _ in range(10):
        for cmd in commandes:
            r = send_cmd(client, cmd)
            assert r.status_code == 200
            data = r.get_json()
            assert 'message' in data

def test_commandes_vides_et_espaces(client):
    """Test avec des commandes vides ou pleines d'espaces"""
    commandes_vides = [
        '',
        ' ',
        '   ',
        '\t',
        '\n',
        '\r\n',
        ' \t \n \r ',
    ]
    
    for cmd in commandes_vides:
        r = send_cmd(client, cmd)
        assert r.status_code == 200
        data = r.get_json()
        assert 'message' in data

def test_commandes_malformees_json(client):
    """Test avec des données JSON malformées"""
    # Test sans JSON
    r = client.post('/commande')
    assert r.status_code == 415  # Unsupported Media Type
    
    # Test avec JSON invalide
    r = client.post('/commande', data='{"cmd": "aide"', content_type='application/json')
    assert r.status_code == 400  # Bad Request
    
    # Test avec JSON vide
    r = client.post('/commande', json={})
    assert r.status_code == 200

def test_commandes_unicode(client):
    """Test avec des caractères Unicode"""
    commandes_unicode = [
        'unlock_universe éèàçù',
        'scan_persona 中文',
        'aide 日本語',
        'profil русский',
        'assistant_pirate العربية',
    ]
    
    for cmd in commandes_unicode:
        r = send_cmd(client, cmd)
        assert r.status_code == 200
        data = r.get_json()
        assert 'message' in data

def test_commandes_injection(client):
    """Test d'injection de commandes"""
    commandes_injection = [
        'unlock_universe; rm -rf /',
        'scan_persona && echo "hack"',
        'aide | cat /etc/passwd',
        'profil || exit',
        'assistant_pirate $(whoami)',
    ]
    
    for cmd in commandes_injection:
        r = send_cmd(client, cmd)
        assert r.status_code == 200
        data = r.get_json()
        assert 'message' in data

def test_commandes_recursion(client):
    """Test de commandes qui pourraient causer une récursion"""
    commandes_recursion = [
        'aide aide aide aide',
        'profil profil profil',
        'unlock_universe unlock_universe',
    ]
    
    for cmd in commandes_recursion:
        r = send_cmd(client, cmd)
        assert r.status_code == 200
        data = r.get_json()
        assert 'message' in data

def test_stress_missions(client):
    """Test de stress sur les missions"""
    # Spam de soumissions de missions
    for i in range(50):
        r = client.post('/mission', data={'choix': f'choix{i}'})
        assert r.status_code == 200

def test_stress_oracle(client):
    """Test de stress sur l'oracle"""
    # Spam de questions à l'oracle
    for i in range(50):
        r = client.post('/oracle', data={'question': f'Question {i} ?'})
        assert r.status_code == 200

def test_concurrent_access(client):
    """Simulation d'accès concurrent"""
    # Accès rapide à différentes routes
    routes = ['/', '/terminal', '/profil', '/monde', '/mission', '/oracle']
    
    for _ in range(10):
        for route in routes:
            r = client.get(route)
            assert r.status_code == 200 

class ArkaliaStressTester:
    def __init__(self, base_url="http://localhost:5001"):
        self.base_url = base_url
        self.results = {
            "total_requests": 0,
            "successful_requests": 0,
            "failed_requests": 0,
            "average_response_time": 0,
            "max_concurrent_users": 0,
            "errors": []
        }
        self.lock = threading.Lock()
        
        # Commandes populaires pour le stress test
        self.popular_commands = [
            "aide", "kill_virus", "hack_system", "find_shadow", 
            "load_mission", "badges", "profil", "luna_contact",
            "start_tutorial", "unlock_universe", "scan_persona"
        ]
    
    def send_request(self, command: str) -> Dict[str, Any]:
        """Envoie une requête au serveur avec mesure du temps"""
        start_time = time.time()
        
        try:
            import requests
            response = requests.post(
                f"{self.base_url}/commande",
                json={"cmd": command},
                timeout=5
            )
            
            end_time = time.time()
            response_time = end_time - start_time
            
            with self.lock:
                self.results["total_requests"] += 1
                self.results["average_response_time"] = (
                    (self.results["average_response_time"] * (self.results["total_requests"] - 1) + response_time) 
                    / self.results["total_requests"]
                )
                
                if response.status_code == 200:
                    self.results["successful_requests"] += 1
                    return {"success": True, "response_time": response_time, "data": response.json()}
                else:
                    self.results["failed_requests"] += 1
                    self.results["errors"].append(f"HTTP {response.status_code}")
                    return {"success": False, "response_time": response_time, "error": f"HTTP {response.status_code}"}
                    
        except Exception as e:
            end_time = time.time()
            response_time = end_time - start_time
            
            with self.lock:
                self.results["total_requests"] += 1
                self.results["failed_requests"] += 1
                self.results["errors"].append(str(e))
                self.results["average_response_time"] = (
                    (self.results["average_response_time"] * (self.results["total_requests"] - 1) + response_time) 
                    / self.results["total_requests"]
                )
            
            return {"success": False, "response_time": response_time, "error": str(e)}
    
    def simulate_user(self, user_id: int, duration: int = 30):
        """Simule un utilisateur qui envoie des commandes pendant une durée donnée"""
        print(f"👤 Utilisateur {user_id} connecté")
        
        start_time = time.time()
        commands_sent = 0
        
        while time.time() - start_time < duration:
            # Choisir une commande aléatoire
            command = random.choice(self.popular_commands)
            
            # Envoyer la requête
            result = self.send_request(command)
            commands_sent += 1
            
            if result["success"]:
                print(f"  ✅ User {user_id}: {command} ({result['response_time']:.2f}s)")
            else:
                print(f"  ❌ User {user_id}: {command} - {result.get('error', 'Erreur')}")
            
            # Pause aléatoire entre les commandes
            time.sleep(random.uniform(0.5, 2.0))
        
        print(f"👤 Utilisateur {user_id} déconnecté ({commands_sent} commandes)")
    
    def run_stress_test(self, num_users: int = 5, duration: int = 30):
        """Lance le test de stress avec plusieurs utilisateurs simultanés"""
        print(f"🚀 DÉMARRAGE DU TEST DE STRESS")
        print(f"👥 {num_users} utilisateurs simultanés")
        print(f"⏱️  Durée: {duration} secondes")
        print("=" * 50)
        
        start_time = time.time()
        
        # Créer les threads pour chaque utilisateur
        threads = []
        for i in range(num_users):
            thread = threading.Thread(
                target=self.simulate_user,
                args=(i + 1, duration)
            )
            threads.append(thread)
        
        # Démarrer tous les threads
        for thread in threads:
            thread.start()
        
        # Attendre que tous les threads se terminent
        for thread in threads:
            thread.join()
        
        end_time = time.time()
        total_duration = end_time - start_time
        
        # Calculer les statistiques
        success_rate = (self.results["successful_requests"] / self.results["total_requests"]) * 100 if self.results["total_requests"] > 0 else 0
        requests_per_second = self.results["total_requests"] / total_duration if total_duration > 0 else 0
        
        # Rapport final
        print("\n" + "=" * 50)
        print("📊 RAPPORT DU TEST DE STRESS")
        print("=" * 50)
        print(f"⏱️  Durée totale: {total_duration:.2f} secondes")
        print(f"👥 Utilisateurs simultanés: {num_users}")
        print(f"📡 Requêtes totales: {self.results['total_requests']}")
        print(f"✅ Requêtes réussies: {self.results['successful_requests']}")
        print(f"❌ Requêtes échouées: {self.results['failed_requests']}")
        print(f"📈 Taux de réussite: {success_rate:.1f}%")
        print(f"⚡ Requêtes/seconde: {requests_per_second:.1f}")
        print(f"⏳ Temps de réponse moyen: {self.results['average_response_time']:.2f}s")
        
        if self.results["errors"]:
            print(f"\n🚨 Erreurs rencontrées:")
            for error in set(self.results["errors"]):
                count = self.results["errors"].count(error)
                print(f"  • {error}: {count} fois")
        
        return {
            "duration": total_duration,
            "num_users": num_users,
            "total_requests": self.results["total_requests"],
            "successful_requests": self.results["successful_requests"],
            "failed_requests": self.results["failed_requests"],
            "success_rate": success_rate,
            "requests_per_second": requests_per_second,
            "average_response_time": self.results["average_response_time"],
            "errors": list(set(self.results["errors"]))
        }

def main():
    """Fonction principale pour lancer le test de stress"""
    tester = ArkaliaStressTester()
    
    # Test avec différents nombres d'utilisateurs
    test_scenarios = [
        {"users": 3, "duration": 20, "name": "Test Léger"},
        {"users": 5, "duration": 30, "name": "Test Moyen"},
        {"users": 8, "duration": 25, "name": "Test Intense"}
    ]
    
    all_results = {}
    
    for scenario in test_scenarios:
        print(f"\n🎯 {scenario['name']}")
        print("=" * 30)
        
        # Réinitialiser les résultats
        tester.results = {
            "total_requests": 0,
            "successful_requests": 0,
            "failed_requests": 0,
            "average_response_time": 0,
            "max_concurrent_users": 0,
            "errors": []
        }
        
        # Lancer le test
        result = tester.run_stress_test(scenario["users"], scenario["duration"])
        all_results[scenario["name"]] = result
        
        # Pause entre les tests
        time.sleep(2)
    
    # Rapport global
    print("\n" + "=" * 60)
    print("🌍 RAPPORT GLOBAL DES TESTS DE STRESS")
    print("=" * 60)
    
    for scenario_name, result in all_results.items():
        print(f"\n📊 {scenario_name}:")
        print(f"  👥 {result['num_users']} utilisateurs")
        print(f"  📡 {result['total_requests']} requêtes")
        print(f"  ✅ {result['success_rate']:.1f}% de réussite")
        print(f"  ⚡ {result['requests_per_second']:.1f} req/s")
        print(f"  ⏳ {result['average_response_time']:.2f}s de réponse moyenne")
    
    # Sauvegarder les résultats
    with open("stress_test_results.json", "w", encoding="utf-8") as f:
        json.dump(all_results, f, indent=2, ensure_ascii=False, default=str)
    
    print(f"\n💾 Résultats sauvegardés dans stress_test_results.json")
    
    # Évaluation finale
    overall_success_rate = sum(r["success_rate"] for r in all_results.values()) / len(all_results)
    
    if overall_success_rate >= 90:
        print("🎉 TESTS DE STRESS RÉUSSIS ! Le système est robuste !")
        return 0
    elif overall_success_rate >= 70:
        print("⚠️  TESTS DE STRESS PARTIELS - Le système tient la charge mais peut être optimisé")
        return 1
    else:
        print("❌ TESTS DE STRESS ÉCHOUÉS - Le système a des problèmes de performance")
        return 1

if __name__ == "__main__":
    exit(main()) 