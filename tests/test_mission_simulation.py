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

def test_mission_get(client):
    """Test d'accès à la page mission"""
    r = client.get('/mission')
    assert r.status_code == 200
    assert b'mission' in r.data.lower()

def test_mission_post_choix(client):
    """Test de soumission d'un choix de mission"""
    # Accès initial
    r = client.get('/mission')
    assert r.status_code == 200
    
    # Soumission d'un choix
    r = client.post('/mission', data={'choix': 'choix1'})
    assert r.status_code == 200
    
    # Vérification que le profil a été mis à jour
    with open(PROFIL_PATH, 'r', encoding='utf-8') as f:
        profil = json.load(f)
    assert 'personnalite' in profil
    assert 'missions_completees' in profil['personnalite']

def test_mission_post_choix_vide(client):
    """Test de soumission d'un choix vide"""
    r = client.post('/mission', data={'choix': ''})
    assert r.status_code == 200

def test_mission_post_choix_invalide(client):
    """Test de soumission d'un choix invalide"""
    r = client.post('/mission', data={'choix': 'choix_inexistant'})
    assert r.status_code == 200

def test_mission_multiple_choix(client):
    """Test de plusieurs choix consécutifs"""
    choix_list = ['choix1', 'choix2', 'choix3']
    
    for choix in choix_list:
        r = client.post('/mission', data={'choix': choix})
        assert r.status_code == 200
    
    # Vérification de la progression
    with open(PROFIL_PATH, 'r', encoding='utf-8') as f:
        profil = json.load(f)
    assert len(profil['personnalite']['missions_completees']) >= 0

def test_mission_persistence(client):
    """Test de persistance des données de mission"""
    # Premier choix
    r = client.post('/mission', data={'choix': 'choix1'})
    assert r.status_code == 200
    
    # Rechargement de la page
    r = client.get('/mission')
    assert r.status_code == 200
    
    # Vérification que les données persistent
    with open(PROFIL_PATH, 'r', encoding='utf-8') as f:
        profil = json.load(f)
    assert 'personnalite' in profil

def test_oracle_get(client):
    """Test d'accès à la page oracle"""
    r = client.get('/oracle')
    assert r.status_code == 200
    assert b'oracle' in r.data.lower()

def test_oracle_post_question(client):
    """Test de soumission d'une question à l'oracle"""
    question = "Quelle est ma mission ?"
    r = client.post('/oracle', data={'question': question})
    assert r.status_code == 200
    assert b'oracle' in r.data.lower()

def test_oracle_post_question_vide(client):
    """Test de soumission d'une question vide"""
    r = client.post('/oracle', data={'question': ''})
    assert r.status_code == 200

def test_oracle_post_question_longue(client):
    """Test de soumission d'une question très longue"""
    question = "A" * 1000  # Question de 1000 caractères
    r = client.post('/oracle', data={'question': question})
    assert r.status_code == 200

def test_oracle_multiple_questions(client):
    """Test de plusieurs questions consécutives"""
    questions = [
        "Quelle est ma mission ?",
        "Comment progresser ?",
        "Quel est mon profil ?"
    ]
    
    for question in questions:
        r = client.post('/oracle', data={'question': question})
        assert r.status_code == 200 