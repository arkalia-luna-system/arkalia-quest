import pytest
import sys
import os
import json
import tempfile
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

@pytest.fixture
def profil_temp():
    """Crée un profil temporaire pour les tests"""
    profil = {
        "score": 0,
        "badges": [],
        "preferences": {},
        "personnalite": {
            "type": "non_detecte",
            "traits": [],
            "missions_completees": [],
            "monde_debloque": "arkalia_base"
        },
        "progression": {
            "niveau": 1,
            "univers_debloques": ["arkalia_base"],
            "portails_ouverts": []
        }
    }
    
    # Sauvegarde temporaire
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        json.dump(profil, f)
        temp_path = f.name
    
    # Sauvegarde l'ancien chemin
    import app
    old_path = app.PROFIL_PATH
    app.PROFIL_PATH = temp_path
    
    yield temp_path
    
    # Restaure l'ancien chemin
    app.PROFIL_PATH = old_path
    os.unlink(temp_path)

def test_unlock_universe(client, profil_temp):
    """Test de la commande unlock_universe"""
    response = client.post('/commande', 
                          json={'cmd': 'unlock_universe'})
    
    assert response.status_code == 200
    data = response.get_json()
    
    assert data['réussite'] == True
    assert 'UNIVERS DÉBLOQUÉ' in data['message']
    assert data['score_gagne'] == 100
    assert data['badge'] == 'Explorateur d\'Univers'
    assert data['debloque_monde'] == True

def test_scan_persona(client, profil_temp):
    """Test de la commande scan_persona"""
    response = client.post('/commande', 
                          json={'cmd': 'scan_persona'})
    
    assert response.status_code == 200
    data = response.get_json()
    
    assert data['réussite'] == True
    assert 'PROFIL DÉTECTÉ' in data['message']
    assert data['score_gagne'] == 50
    assert data['personnalite_detectee'] == True

def test_load_mission(client, profil_temp):
    """Test de la commande load_mission"""
    response = client.post('/commande', 
                          json={'cmd': 'load_mission'})
    
    assert response.status_code == 200
    data = response.get_json()
    
    assert data['réussite'] == True
    assert 'NOUVELLE MISSION CHARGÉE' in data['message']
    assert data['score_gagne'] == 25
    assert 'mission' in data

def test_reboot_world(client, profil_temp):
    """Test de la commande reboot_world"""
    response = client.post('/commande', 
                          json={'cmd': 'reboot_world'})
    
    assert response.status_code == 200
    data = response.get_json()
    
    assert data['réussite'] == True
    assert 'MONDE REDÉMARRÉ' in data['message']
    assert data['score_gagne'] == 30
    assert data['badge'] == 'Reboot Master'

def test_decode_portal(client, profil_temp):
    """Test de la commande decode_portal"""
    response = client.post('/commande', 
                          json={'cmd': 'decode_portal'})
    
    assert response.status_code == 200
    data = response.get_json()
    
    assert data['réussite'] == True
    assert 'PORTAIL DÉCHIFFRÉ' in data['message']
    assert data['score_gagne'] == 75
    assert data['badge'] == 'Déchiffreur de Portails'
    assert 'portail_debloque' in data

def test_aide_amelioree(client, profil_temp):
    """Test de la commande aide améliorée"""
    response = client.post('/commande', 
                          json={'cmd': 'aide'})
    
    assert response.status_code == 200
    data = response.get_json()
    
    assert data['réussite'] == True
    assert 'COMMANDES DISPONIBLES' in data['message']
    assert 'unlock_universe' in data['message']
    assert 'scan_persona' in data['message']
    assert 'load_mission' in data['message']

def test_profil_ameliore(client, profil_temp):
    """Test de la commande profil améliorée"""
    response = client.post('/commande', 
                          json={'cmd': 'profil'})
    
    assert response.status_code == 200
    data = response.get_json()
    
    assert data['réussite'] == True
    assert 'PROFIL ARKALIA' in data['message']
    assert 'Score : 0' in data['message']
    assert 'Type : Non Detecte' in data['message']

def test_commande_non_autorisee(client, profil_temp):
    """Test de rejet des commandes non autorisées"""
    response = client.post('/commande', 
                          json={'cmd': 'commande_dangereuse'})
    
    assert response.status_code == 200
    data = response.get_json()
    
    assert data['réussite'] == False
    assert 'Commande non autorisée' in data['message']

def test_commande_avec_arguments(client, profil_temp):
    """Test des commandes avec arguments"""
    response = client.post('/commande', 
                          json={'cmd': 'assistant_pirate salut'})
    
    assert response.status_code == 200
    data = response.get_json()
    
    assert data['ascii_art'] == '🤖'
    assert 'message' in data

def test_route_monde(client, profil_temp):
    """Test de la route /monde"""
    response = client.get('/monde')
    
    assert response.status_code == 200
    assert b'Monde Arkalia D' in response.data
    assert b'Portails Ouverts' in response.data
    assert b'Profil D' in response.data 