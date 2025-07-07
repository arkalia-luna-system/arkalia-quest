import os
import pytest
import json
from app import app, PROFIL_PATH, sauvegarder_profil, charger_profil

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

def test_parcours_joueur_complet(client):
    """Test du parcours complet d'un joueur Arkalia Quest"""
    
    # ÉTAPE 1: Accès initial
    r = client.get('/')
    assert r.status_code == 200
    
    r = client.get('/terminal')
    assert r.status_code == 200
    
    # Vérification du profil initial
    profil_initial = charger_profil()
    assert profil_initial['score'] >= 0
    assert len(profil_initial['badges']) == 0
    assert profil_initial['personnalite']['type'] == 'non_detecte'
    
    # ÉTAPE 2: Déblocage de l'univers
    r = send_cmd(client, 'unlock_universe')
    assert r.status_code == 200
    data = r.get_json()
    assert data['réussite'] == True
    assert 'UNIVERS DÉBLOQUÉ' in data['message']
    assert data['score_gagne'] == 100
    assert data['badge'] == 'Explorateur d\'Univers'
    
    # ÉTAPE 3: Scan de personnalité
    r = send_cmd(client, 'scan_persona')
    assert r.status_code == 200
    data = r.get_json()
    assert data['réussite'] == True
    assert 'PROFIL DÉTECTÉ' in data['message']
    assert data['score_gagne'] == 50
    assert data['personnalite_detectee'] == True
    
    # ÉTAPE 4: Chargement de mission
    r = send_cmd(client, 'load_mission')
    assert r.status_code == 200
    data = r.get_json()
    assert data['réussite'] == True
    assert 'NOUVELLE MISSION CHARGÉE' in data['message']
    assert data['score_gagne'] == 25
    assert 'mission' in data
    
    # ÉTAPE 5: Utilisation de l'assistant pirate
    r = send_cmd(client, 'assistant_pirate Salut IA pirate !')
    assert r.status_code == 200
    data = r.get_json()
    assert 'message' in data
    
    # ÉTAPE 6: Génération de meme
    r = send_cmd(client, 'generer_meme Arkalia Quest est génial !')
    assert r.status_code == 200
    data = r.get_json()
    # La génération de meme peut échouer selon l'environnement, vérifions juste la réponse
    assert 'message' in data
    if data.get('réussite'):
        assert data['score_gagne'] == 25
        assert data['badge'] == 'Pirate visuel'
    
    # ÉTAPE 7: Déchiffrement de portail
    r = send_cmd(client, 'decode_portal')
    assert r.status_code == 200
    data = r.get_json()
    assert data['réussite'] == True
    assert 'PORTAIL DÉCHIFFRÉ' in data['message']
    assert data['score_gagne'] == 75
    assert data['badge'] == 'Déchiffreur de Portails'
    assert 'portail_debloque' in data
    
    # ÉTAPE 8: Redémarrage du monde
    r = send_cmd(client, 'reboot_world')
    assert r.status_code == 200
    data = r.get_json()
    assert data['réussite'] == True
    assert 'MONDE REDÉMARRÉ' in data['message']
    assert data['score_gagne'] == 30
    assert data['badge'] == 'Reboot Master'
    
    # ÉTAPE 9: Missions classiques
    r = send_cmd(client, 'hacker_coffre')
    assert r.status_code == 200
    data = r.get_json()
    assert data['réussite'] == True
    assert data['score_gagne'] > 0
    assert data['badge'] == 'Pirate débutant'
    
    r = send_cmd(client, 'decoder_message')
    assert r.status_code == 200
    data = r.get_json()
    assert data['réussite'] == True
    assert data['score_gagne'] > 0
    assert data['badge'] == 'Espion confirmé'
    
    r = send_cmd(client, 'invoquer_dragon')
    assert r.status_code == 200
    data = r.get_json()
    assert data['réussite'] == True
    assert data['score_gagne'] > 0
    assert data['badge'] == 'Maître du feu'
    
    # ÉTAPE 10: Choix de dragon
    r = send_cmd(client, 'choisir_dragon bleu')
    assert r.status_code == 200
    data = r.get_json()
    assert data['réussite'] == True
    assert data['score_gagne'] == 40
    assert data['badge'] == 'Dragon de glace'
    assert data['dragon_choisi'] == 'bleu'
    
    r = send_cmd(client, 'choisir_dragon rouge')
    assert r.status_code == 200
    data = r.get_json()
    assert data['réussite'] == True
    assert data['score_gagne'] == 50
    assert data['badge'] == 'Dragon de feu'
    assert data['dragon_choisi'] == 'rouge'
    
    # ÉTAPE 11: Navigation dans les pages
    r = client.get('/profil')
    assert r.status_code == 200
    
    r = client.get('/monde')
    assert r.status_code == 200
    
    r = client.get('/mission')
    assert r.status_code == 200
    
    r = client.get('/oracle')
    assert r.status_code == 200
    
    # ÉTAPE 12: Utilisation de l'oracle
    r = client.post('/oracle', data={'question': 'Comment progresser dans Arkalia Quest ?'})
    assert r.status_code == 200
    
    # ÉTAPE 13: Vérification finale du profil
    profil_final = charger_profil()
    
    # Vérifications de progression
    assert profil_final['score'] > 300  # Au moins 300 points gagnés
    assert len(profil_final['badges']) >= 8  # Au moins 8 badges
    assert profil_final['personnalite']['type'] != 'non_detecte'
    assert len(profil_final['personnalite']['traits']) > 0
    assert len(profil_final['personnalite']['missions_completees']) >= 1
    assert 'arkalia_complet' in profil_final['progression']['univers_debloques']
    assert len(profil_final['progression']['portails_ouverts']) >= 1
    assert 'dragon_choisi' in profil_final['preferences']
    
    # ÉTAPE 14: Affichage du profil final
    r = send_cmd(client, 'profil')
    assert r.status_code == 200
    data = r.get_json()
    assert data['réussite'] == True
    assert 'PROFIL ARKALIA' in data['message']
    assert str(profil_final['score']) in data['message']
    
    # ÉTAPE 15: Affichage de l'aide
    r = send_cmd(client, 'aide')
    assert r.status_code == 200
    data = r.get_json()
    assert data['réussite'] == True
    assert 'COMMANDES DISPONIBLES' in data['message']

def test_parcours_joueur_erreurs(client):
    """Test du parcours avec des erreurs et récupération"""
    
    # Commandes incorrectes puis correctes
    r = send_cmd(client, 'unloc_universe')  # Faute de frappe
    assert r.status_code == 200
    data = r.get_json()
    assert not data['réussite']
    
    r = send_cmd(client, 'unlock_universe')  # Commande correcte
    assert r.status_code == 200
    data = r.get_json()
    assert data['réussite'] == True
    
    # Test de variantes
    r = send_cmd(client, '  SCAN_PERSONA  ')  # Espaces et majuscules
    assert r.status_code == 200
    data = r.get_json()
    assert data['réussite'] == True
    
    # Test de commandes avec arguments
    r = send_cmd(client, 'assistant_pirate   Comment ça va ?   ')  # Espaces multiples
    assert r.status_code == 200
    data = r.get_json()
    assert 'message' in data

def test_persistence_donnees(client):
    """Test de persistance des données après redémarrage"""
    
    # Première session
    send_cmd(client, 'unlock_universe')
    send_cmd(client, 'scan_persona')
    send_cmd(client, 'load_mission')
    
    # Vérification du profil
    profil_session1 = charger_profil()
    
    score_session1 = profil_session1['score']
    badges_session1 = len(profil_session1['badges'])
    
    # Simulation de redémarrage (nouveau client)
    with app.test_client() as client2:
        # Vérification que les données persistent
        r = send_cmd(client2, 'profil')
        assert r.status_code == 200
        data = r.get_json()
        assert data['réussite'] == True
        
        # Vérification que le score et les badges persistent
        profil_session2 = charger_profil()
        assert profil_session2['score'] == score_session1
        assert len(profil_session2['badges']) == badges_session1 