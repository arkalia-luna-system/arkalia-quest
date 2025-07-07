import os
import pytest
import json
from app import app, PROFIL_PATH, sauvegarder_profil

def reset_profil():
    if os.path.exists(PROFIL_PATH):
        os.remove(PROFIL_PATH)

@pytest.fixture(autouse=True)
def client():
    reset_profil()
    with app.test_client() as client:
        yield client

def test_route_accueil(client):
    """Test de la page d'accueil"""
    r = client.get('/')
    assert r.status_code == 200
    assert b'arkalia' in r.data.lower() or b'terminal' in r.data.lower()

def test_route_terminal(client):
    """Test de la page terminal"""
    r = client.get('/terminal')
    assert r.status_code == 200
    assert b'terminal' in r.data.lower() or b'commande' in r.data.lower()

def test_route_profil(client):
    """Test de la page profil"""
    r = client.get('/profil')
    assert r.status_code == 200
    assert b'profil' in r.data.lower() or b'score' in r.data.lower()

def test_route_monde(client):
    """Test de la page monde"""
    r = client.get('/monde')
    assert r.status_code == 200
    assert b'monde' in r.data.lower() or b'univers' in r.data.lower()

def test_route_mission(client):
    """Test de la page mission"""
    r = client.get('/mission')
    assert r.status_code == 200
    assert b'mission' in r.data.lower()

def test_route_oracle(client):
    """Test de la page oracle"""
    r = client.get('/oracle')
    assert r.status_code == 200
    assert b'oracle' in r.data.lower()

def test_navigation_complete(client):
    """Test de navigation complète : accueil -> terminal -> profil -> monde"""
    # Accueil
    r = client.get('/')
    assert r.status_code == 200
    
    # Terminal
    r = client.get('/terminal')
    assert r.status_code == 200
    
    # Profil
    r = client.get('/profil')
    assert r.status_code == 200
    
    # Monde
    r = client.get('/monde')
    assert r.status_code == 200
    
    # Mission
    r = client.get('/mission')
    assert r.status_code == 200
    
    # Oracle
    r = client.get('/oracle')
    assert r.status_code == 200

def test_assets_static(client):
    """Test que les fichiers CSS se chargent"""
    r = client.get('/static/style.css')
    assert r.status_code == 200
    
    r = client.get('/static/oracle.css')
    assert r.status_code == 200
    
    r = client.get('/static/mission.css')
    assert r.status_code == 200

def test_404_route(client):
    """Test des routes inexistantes"""
    r = client.get('/route_inexistante')
    assert r.status_code == 404 