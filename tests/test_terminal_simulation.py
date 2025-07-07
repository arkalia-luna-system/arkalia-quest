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

def send_cmd(client, cmd):
    return client.post('/commande', json={'cmd': cmd})

def test_commandes_terminal_success(client):
    # Commandes principales
    commandes = [
        'unlock_universe',
        'scan_persona',
        'load_mission',
        'reboot_world',
        'decode_portal',
        'hacker_coffre',
        'aide',
        'profil',
        'assistant_pirate Salut IA',
        'generer_meme Arkalia rocks!',
        'decoder_message',
        'invoquer_dragon',
        'choisir_dragon bleu',
        'choisir_dragon rouge',
    ]
    for cmd in commandes:
        r = send_cmd(client, cmd)
        assert r.status_code == 200
        data = r.get_json()
        assert 'message' in data or 'ascii_art' in data
        # On vérifie qu'aucune commande ne fait planter

def test_commandes_terminal_erreurs(client):
    # Commandes inconnues, fautes, variantes
    erreurs = [
        '',
        '   ',
        'unloc_universe',
        'scan persona',
        'load-mission',
        'hacker_coffre_extra',
        'generer_meme',
        'dragon',
        'unknown_command',
    ]
    for cmd in erreurs:
        r = send_cmd(client, cmd)
        assert r.status_code == 200
        data = r.get_json()
        assert not data.get('réussite', False)
        assert 'message' in data

def test_progression_profil(client):
    # On débloque l'univers, puis on scanne la personnalité, puis on charge une mission
    send_cmd(client, 'unlock_universe')
    send_cmd(client, 'scan_persona')
    send_cmd(client, 'load_mission')
    # Vérifie la progression dans le profil
    with open(PROFIL_PATH, 'r', encoding='utf-8') as f:
        profil = json.load(f)
    assert profil['score'] > 0
    assert len(profil['badges']) >= 1
    assert profil['personnalite']['type'] != 'non_detecte'
    assert len(profil['personnalite']['missions_completees']) >= 1
    assert 'arkalia_complet' in profil['progression']['univers_debloques']

def test_variantes_commandes(client):
    variantes = [
        '  UNLOCK_universe  ',
        'Scan_Persona',
        'LoAd_Mission',
        '  reboot_world ',
        'DECODE_PORTAL',
        'HACKER_COFFRE',
        'Assistant_Pirate   Salut',
        'Generer_Meme   test',
    ]
    for cmd in variantes:
        r = send_cmd(client, cmd)
        assert r.status_code == 200
        data = r.get_json()
        assert 'message' in data or 'ascii_art' in data
