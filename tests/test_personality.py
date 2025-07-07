import pytest
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mission_utils.personality_engine import analyser_personnalite, generer_mission_personnalisee, obtenir_conseils_personnalite

def test_analyser_personnalite_creatif():
    """Test de détection d'un profil créatif"""
    profil = {
        "badges": ["Pirate visuel", "Créateur d'art"],
        "score": 250,
        "personnalite": {
            "missions_completees": ["creatif_1"]
        }
    }
    
    resultat = analyser_personnalite(profil)
    assert resultat == "hacker_creatif"

def test_analyser_personnalite_analytique():
    """Test de détection d'un profil analytique"""
    profil = {
        "badges": ["Espion confirmé", "Déchiffreur de Portails"],
        "score": 350,
        "personnalite": {
            "missions_completees": ["analytique_1", "analytique_2"]
        }
    }
    
    resultat = analyser_personnalite(profil)
    assert resultat == "hacker_analytique"

def test_analyser_personnalite_social():
    """Test de détection d'un profil social"""
    profil = {
        "badges": ["Assistant Social", "Communicateur"],
        "score": 200,
        "personnalite": {
            "missions_completees": ["social_1"]
        }
    }
    
    resultat = analyser_personnalite(profil)
    assert resultat == "hacker_social"

def test_analyser_personnalite_equilibre():
    """Test de détection d'un profil équilibré (par défaut)"""
    profil = {
        "badges": [],
        "score": 0,
        "personnalite": {
            "missions_completees": []
        }
    }
    
    resultat = analyser_personnalite(profil)
    assert resultat == "hacker_equilibre"

def test_generer_mission_personnalisee():
    """Test de génération de mission personnalisée"""
    profil = {
        "personnalite": {
            "type": "hacker_creatif",
            "missions_completees": []
        }
    }
    
    mission = generer_mission_personnalisee(profil)
    assert "id" in mission
    assert "titre" in mission
    assert "description" in mission
    assert "difficulte" in mission
    assert "recompense" in mission
    assert mission["id"].startswith("creatif_")

def test_generer_mission_speciale():
    """Test de génération de mission spéciale quand toutes sont complétées"""
    profil = {
        "personnalite": {
            "type": "hacker_creatif",
            "missions_completees": ["creatif_1", "creatif_2"]
        }
    }
    
    mission = generer_mission_personnalisee(profil)
    assert mission["id"] == "hacker_creatif_special"
    assert "Mission Maître" in mission["titre"]
    assert mission["difficulte"] == "expert"

def test_obtenir_conseils_personnalite():
    """Test d'obtention de conseils personnalisés"""
    conseils = obtenir_conseils_personnalite("hacker_creatif")
    assert isinstance(conseils, list)
    assert len(conseils) > 0
    assert all(isinstance(conseil, str) for conseil in conseils)

def test_obtenir_conseils_type_inconnu():
    """Test d'obtention de conseils pour un type inconnu"""
    conseils = obtenir_conseils_personnalite("type_inconnu")
    assert isinstance(conseils, list)
    assert len(conseils) > 0 