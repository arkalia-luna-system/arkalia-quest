"""
Tests pour le système de configuration
Version 2.0.0
"""

import pytest
import os
import tempfile
from pathlib import Path
from unittest.mock import patch, MagicMock

from config import (
    Config, COMMANDES_AUTORISEES, TYPES_PERSONNALITE,
    MISSIONS_CONFIG, BADGES_CONFIG, EFFECTS_CONFIG,
    ensure_directories, get_config
)


class TestConfig:
    """Tests pour la classe Config"""
    
    def test_config_default_values(self):
        """Test des valeurs par défaut de la configuration"""
        config = Config()
        
        # Test des valeurs de base
        assert config.SECRET_KEY == 'arkalia-quest-secret-key-2025'
        assert config.PORT == 5001
        assert config.HOST == '127.0.0.1'
        
        # DEBUG dépend de l'environnement, on teste juste que c'est un booléen
        assert isinstance(config.DEBUG, bool)
    
    def test_config_environment_variables(self):
        """Test de la configuration avec variables d'environnement"""
        config = Config()
        
        # Test que SECRET_KEY a une valeur par défaut si non définie
        assert config.SECRET_KEY is not None
        assert len(config.SECRET_KEY) > 0
        
        # Test que DEBUG peut être True ou False selon l'environnement
        assert isinstance(config.DEBUG, bool)
    
    def test_config_port_and_host(self):
        """Test de la configuration du port et de l'hôte"""
        config = Config()
        
        # Test que PORT et HOST ont des valeurs valides
        assert isinstance(config.PORT, int)
        assert config.PORT > 0
        assert isinstance(config.HOST, str)
        assert len(config.HOST) > 0


class TestCommandesAutorisees:
    """Tests pour les commandes autorisées"""
    
    def test_commandes_autorisees_structure(self):
        """Test de la structure des commandes autorisées"""
        assert isinstance(COMMANDES_AUTORISEES, dict)
        assert len(COMMANDES_AUTORISEES) > 0
        
        # Vérification que toutes les commandes ont une description
        for commande, description in COMMANDES_AUTORISEES.items():
            assert isinstance(commande, str)
            assert isinstance(description, str)
            assert len(description) > 0
    
    def test_commandes_immersives_presentes(self):
        """Test de la présence des commandes immersives principales"""
        commandes_requises = [
            'unlock_universe',
            'scan_persona',
            'load_mission',
            'reboot_world',
            'aide'
        ]
        
        for commande in commandes_requises:
            assert commande in COMMANDES_AUTORISEES
    
    def test_commandes_compatibilite_presentes(self):
        """Test de la présence des commandes de compatibilité"""
        commandes_compatibilite = [
            'decoder_message',
            'invoquer_dragon',
            'choisir_dragon'
        ]
        
        for commande in commandes_compatibilite:
            assert commande in COMMANDES_AUTORISEES


class TestTypesPersonnalite:
    """Tests pour les types de personnalité"""
    
    def test_types_personnalite_structure(self):
        """Test de la structure des types de personnalité"""
        assert isinstance(TYPES_PERSONNALITE, dict)
        assert len(TYPES_PERSONNALITE) > 0
        
        types_requis = [
            'hacker_creatif',
            'hacker_analytique',
            'hacker_social',
            'hacker_equilibre'
        ]
        
        for type_perso in types_requis:
            assert type_perso in TYPES_PERSONNALITE
    
    def test_type_personnalite_complet(self):
        """Test de la complétude d'un type de personnalité"""
        for type_perso, config in TYPES_PERSONNALITE.items():
            assert 'nom' in config
            assert 'description' in config
            assert 'traits' in config
            assert 'emoji' in config
            assert 'couleur' in config
            
            assert isinstance(config['nom'], str)
            assert isinstance(config['description'], str)
            assert isinstance(config['traits'], list)
            assert isinstance(config['emoji'], str)
            assert isinstance(config['couleur'], str)
            
            assert len(config['traits']) > 0
            assert config['couleur'].startswith('#')


class TestMissionsConfig:
    """Tests pour la configuration des missions"""
    
    def test_missions_config_structure(self):
        """Test de la structure de la configuration des missions"""
        assert 'difficultes' in MISSIONS_CONFIG
        assert 'types' in MISSIONS_CONFIG
        assert 'recompenses_base' in MISSIONS_CONFIG
    
    def test_difficultes_missions(self):
        """Test des difficultés de missions"""
        difficultes = MISSIONS_CONFIG['difficultes']
        assert isinstance(difficultes, list)
        assert len(difficultes) > 0
        
        difficultes_requises = ['facile', 'moyen', 'difficile', 'expert']
        for difficulte in difficultes_requises:
            assert difficulte in difficultes
    
    def test_types_missions(self):
        """Test des types de missions"""
        types = MISSIONS_CONFIG['types']
        assert isinstance(types, list)
        assert len(types) > 0
        
        types_requis = ['hack', 'enigme', 'social', 'creatif', 'analytique']
        for type_mission in types_requis:
            assert type_mission in types
    
    def test_recompenses_base(self):
        """Test des récompenses de base"""
        recompenses = MISSIONS_CONFIG['recompenses_base']
        assert isinstance(recompenses, dict)
        
        for difficulte, score in recompenses.items():
            assert difficulte in MISSIONS_CONFIG['difficultes']
            assert isinstance(score, int)
            assert score > 0


class TestBadgesConfig:
    """Tests pour la configuration des badges"""
    
    def test_badges_config_structure(self):
        """Test de la structure de la configuration des badges"""
        assert isinstance(BADGES_CONFIG, dict)
        assert len(BADGES_CONFIG) > 0
    
    def test_badge_complet(self):
        """Test de la complétude d'un badge"""
        for badge_id, config in BADGES_CONFIG.items():
            assert 'nom' in config
            assert 'description' in config
            assert 'score_requis' in config
            
            assert isinstance(config['nom'], str)
            assert isinstance(config['description'], str)
            assert isinstance(config['score_requis'], int)
            
            assert config['score_requis'] >= 0


class TestEffectsConfig:
    """Tests pour la configuration des effets visuels"""
    
    def test_effects_config_structure(self):
        """Test de la structure de la configuration des effets"""
        assert 'ascii_art' in EFFECTS_CONFIG
        assert isinstance(EFFECTS_CONFIG['ascii_art'], dict)
    
    def test_ascii_art_present(self):
        """Test de la présence des ASCII art"""
        ascii_arts = EFFECTS_CONFIG['ascii_art']
        
        arts_requis = ['unlock_universe', 'scan_persona', 'reboot_world']
        for art in arts_requis:
            assert art in ascii_arts
            assert isinstance(ascii_arts[art], str)
            assert len(ascii_arts[art]) > 0


class TestFonctionsUtilitaires:
    """Tests pour les fonctions utilitaires"""
    
    def test_ensure_directories(self, tmp_path):
        """Test de la création des répertoires"""
        with patch('config.BASE_DIR', tmp_path):
            with patch('config.DATA_DIR', tmp_path / "data"):
                with patch('config.MISSIONS_DIR', tmp_path / "missions"):
                    with patch('config.LOGS_DIR', tmp_path / "logs"):
                        with patch('config.BADGES_DIR', tmp_path / "badges"):
                            ensure_directories()
                            
                            assert (tmp_path / "data").exists()
                            assert (tmp_path / "missions").exists()
                            assert (tmp_path / "logs").exists()
                            assert (tmp_path / "badges").exists()
    
    @patch.dict(os.environ, {'FLASK_ENV': 'development'})
    def test_get_config_development(self):
        """Test de la configuration en mode développement"""
        config = get_config()
        assert isinstance(config, Config)
        assert config.DEBUG is True
    
    def test_get_config_production(self):
        """Test de la configuration en mode production"""
        # Sauvegarde de l'environnement actuel
        original_env = os.environ.get('FLASK_ENV')
        
        # Force le mode production
        os.environ['FLASK_ENV'] = 'production'
        
        try:
            config = get_config()
            assert isinstance(config, Config)
            assert config.DEBUG is False
        finally:
            # Restauration de l'environnement
            if original_env:
                os.environ['FLASK_ENV'] = original_env
            else:
                del os.environ['FLASK_ENV']


class TestIntegration:
    """Tests d'intégration de la configuration"""
    
    def test_configuration_coherence(self):
        """Test de la cohérence globale de la configuration"""
        # Vérification que les types de personnalité sont cohérents
        for type_perso in TYPES_PERSONNALITE:
            assert type_perso in ['hacker_creatif', 'hacker_analytique', 
                                'hacker_social', 'hacker_equilibre']
        
        # Vérification que les difficultés sont cohérentes
        for difficulte in MISSIONS_CONFIG['difficultes']:
            assert difficulte in MISSIONS_CONFIG['recompenses_base']
        
        # Vérification que les commandes ont des descriptions uniques
        descriptions = list(COMMANDES_AUTORISEES.values())
        assert len(descriptions) == len(set(descriptions))
    
    def test_configuration_complete(self):
        """Test de la complétude de la configuration"""
        # Tous les composants principaux doivent être présents
        assert COMMANDES_AUTORISEES is not None
        assert TYPES_PERSONNALITE is not None
        assert MISSIONS_CONFIG is not None
        assert BADGES_CONFIG is not None
        assert EFFECTS_CONFIG is not None
        
        # Aucun composant ne doit être vide
        assert len(COMMANDES_AUTORISEES) > 0
        assert len(TYPES_PERSONNALITE) > 0
        assert len(MISSIONS_CONFIG) > 0
        assert len(BADGES_CONFIG) > 0
        assert len(EFFECTS_CONFIG) > 0 