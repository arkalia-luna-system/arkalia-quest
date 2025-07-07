import os
import json
import tempfile
import pytest
import sys
sys.path.append('.')
from app import app, PROFIL_PATH

def setup_module(module):
    # Sauvegarder l'ancien profil
    if os.path.exists(PROFIL_PATH):
        os.rename(PROFIL_PATH, PROFIL_PATH + '.bak')
    # Créer un profil vierge
    with open(PROFIL_PATH, 'w', encoding='utf-8') as f:
        json.dump({"score": 0, "badges": [], "preferences": {}}, f)

def teardown_module(module):
    # Restaurer l'ancien profil
    if os.path.exists(PROFIL_PATH + '.bak'):
        os.remove(PROFIL_PATH)
        os.rename(PROFIL_PATH + '.bak', PROFIL_PATH)

def test_hacker_coffre():
    client = app.test_client()
    # Envoyer la commande hacker_coffre
    response = client.post('/commande', json={"cmd": "hacker_coffre"})
    data = response.get_json()
    assert data["réussite"] is True
    assert "Bravo" in data["message"]
    # Vérifier l'incrémentation du score
    with open(PROFIL_PATH, 'r', encoding='utf-8') as f:
        profil = json.load(f)
    assert profil["score"] >= 50
    assert "Pirate débutant" in profil["badges"]

def test_decoder_message():
    client = app.test_client()
    response = client.post("/commande", json={"cmd": "decoder_message"})
    data = response.get_json()
    assert data["réussite"] is True
    assert "Espion confirmé" in data["badge"]
    # Vérifier l'incrémentation du score
    with open(PROFIL_PATH, 'r', encoding='utf-8') as f:
        profil = json.load(f)
    assert profil["score"] >= 30

def test_invoquer_dragon():
    client = app.test_client()
    response = client.post("/commande", json={"cmd": "invoquer_dragon"})
    data = response.get_json()
    assert data["réussite"] is True
    assert "Maître du feu" in data["badge"]
    # Vérifier l'incrémentation du score
    with open(PROFIL_PATH, 'r', encoding='utf-8') as f:
        profil = json.load(f)
    assert profil["score"] >= 70

def test_choisir_dragon_prompt():
    client = app.test_client()
    r = client.post("/commande", json={"cmd": "choisir_dragon"})
    assert b"Quel dragon choisis-tu ?" in r.data

def test_choisir_dragon_bleu():
    client = app.test_client()
    r = client.post("/commande", json={"cmd": "choisir_dragon bleu"})
    assert b"Dragon de glace" in r.data
    # Vérifie que le choix est bien stocké
    with open(PROFIL_PATH, 'r', encoding='utf-8') as f:
        profil = json.load(f)
    assert profil["preferences"].get("dragon_choisi") == "bleu"

def test_choisir_dragon_rouge():
    client = app.test_client()
    r = client.post("/commande", json={"cmd": "choisir_dragon rouge"})
    assert b"Dragon de feu" in r.data
    with open(PROFIL_PATH, 'r', encoding='utf-8') as f:
        profil = json.load(f)
    assert profil["preferences"].get("dragon_choisi") == "rouge" 