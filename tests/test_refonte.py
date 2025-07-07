"""
Tests pour la refonte Arkalia Quest
Tests unitaires et d'intégration pour la nouvelle architecture
"""

import pytest
import json
import os
import tempfile
from unittest.mock import Mock, patch

# Import des modules à tester
from core.game_engine import GameEngine
from core.profile_manager import ProfileManager
from core.command_handler import CommandHandler
from engines.luna_ai import LunaAI
from engines.effects_engine import EffectsEngine


class TestProfileManager:
    """Tests pour le gestionnaire de profils"""
    
    def setup_method(self):
        """Setup avant chaque test"""
        self.temp_dir = tempfile.mkdtemp()
        self.profile_manager = ProfileManager(self.temp_dir)
    
    def teardown_method(self):
        """Cleanup après chaque test"""
        import shutil
        shutil.rmtree(self.temp_dir)
    
    def test_create_default_profile(self):
        """Test de création d'un profil par défaut"""
        profile = self.profile_manager.create_default_profile()
        
        assert profile["id"] == "default"
        assert profile["score"] == 0
        assert profile["level"] == 1
        assert "arkalia_base" in profile["progression"]["univers_debloques"]
        assert profile["personnalite"]["type"] == "non_detecte"
    
    def test_load_nonexistent_profile(self):
        """Test de chargement d'un profil inexistant"""
        profile = self.profile_manager.load_profile("test_user")
        
        assert profile["id"] == "default"
        assert profile["score"] == 0
    
    def test_save_and_load_profile(self):
        """Test de sauvegarde et chargement d'un profil"""
        user_id = "test_user"
        original_profile = self.profile_manager.load_profile(user_id)
        original_profile["score"] = 100
        original_profile["name"] = "TestUser"
        
        self.profile_manager.save_profile(user_id, original_profile)
        loaded_profile = self.profile_manager.load_profile(user_id)
        
        assert loaded_profile["score"] == 100
        assert loaded_profile["name"] == "TestUser"
    
    def test_add_badge(self):
        """Test d'ajout de badge"""
        user_id = "test_user"
        self.profile_manager.add_badge(user_id, "Test Badge")
        
        profile = self.profile_manager.load_profile(user_id)
        assert "Test Badge" in profile["badges"]
    
    def test_add_score(self):
        """Test d'ajout de score"""
        user_id = "test_user"
        self.profile_manager.add_score(user_id, 50)
        
        profile = self.profile_manager.load_profile(user_id)
        assert profile["score"] == 50
        assert profile["level"] == 1  # Niveau 1 pour 50 points
    
    def test_add_score_level_up(self):
        """Test de montée de niveau"""
        user_id = "test_user"
        self.profile_manager.add_score(user_id, 150)
        
        profile = self.profile_manager.load_profile(user_id)
        assert profile["score"] == 150
        assert profile["level"] == 2  # Niveau 2 pour 150 points


class TestCommandHandler:
    """Tests pour le gestionnaire de commandes"""
    
    def setup_method(self):
        """Setup avant chaque test"""
        self.command_handler = CommandHandler()
        self.mock_profile = {
            "score": 0,
            "badges": [],
            "personnalite": {"type": "non_detecte", "traits": []},
            "progression": {
                "univers_debloques": ["arkalia_base"],
                "portails_ouverts": []
            }
        }
    
    def test_normalize_command(self):
        """Test de normalisation des commandes"""
        assert self.command_handler.normalize_command("  AIDE  ") == "aide"
        assert self.command_handler.normalize_command("unlock   universe") == "unlock universe"
    
    def test_find_authorized_command(self):
        """Test de recherche de commande autorisée"""
        assert self.command_handler.find_authorized_command("aide") == "aide"
        assert self.command_handler.find_authorized_command("assistant_pirate salut") == "assistant_pirate"
        assert self.command_handler.find_authorized_command("commande_inconnue") == ""
    
    def test_handle_aide(self):
        """Test de la commande aide"""
        result = self.command_handler.handle_aide()
        
        assert result["réussite"] == True
        assert "COMMANDES DISPONIBLES" in result["message"]
        assert result["profile_updated"] == False
    
    def test_handle_unlock_universe(self):
        """Test de la commande unlock_universe"""
        result = self.command_handler.handle_unlock_universe(self.mock_profile)
        
        assert result["réussite"] == True
        assert "UNIVERS DÉBLOQUÉ" in result["message"]
        assert result["score_gagne"] == 100
        assert "Explorateur d'Univers" in result["badge"]
        assert result["profile_updated"] == True
        assert "arkalia_complet" in self.mock_profile["progression"]["univers_debloques"]
    
    def test_handle_scan_persona(self):
        """Test de la commande scan_persona"""
        with patch('mission_utils.personality_engine.analyser_personnalite') as mock_analyze:
            mock_analyze.return_value = "hacker_creatif"
            
            result = self.command_handler.handle_scan_persona(self.mock_profile)
            
            assert result["réussite"] == True
            assert "PROFIL DÉTECTÉ" in result["message"]
            assert result["score_gagne"] == 50
            assert result["personnalite_detectee"] == True
            assert self.mock_profile["personnalite"]["type"] == "hacker_creatif"
    
    def test_handle_monde_locked(self):
        """Test de la commande monde quand verrouillé"""
        result = self.command_handler.handle_monde(self.mock_profile)
        
        assert result["réussite"] == False
        assert "MONDE VERROUILLÉ" in result["message"]
    
    def test_handle_monde_unlocked(self):
        """Test de la commande monde quand débloqué"""
        self.mock_profile["progression"]["univers_debloques"].append("arkalia_complet")
        
        result = self.command_handler.handle_monde(self.mock_profile)
        
        assert result["réussite"] == True
        assert "MONDE ARKALIA DÉBLOQUÉ" in result["message"]


class TestLunaAI:
    """Tests pour l'IA LUNA"""
    
    def setup_method(self):
        """Setup avant chaque test"""
        self.luna = LunaAI()
        self.mock_profile = {
            "personnalite": {"type": "hacker_creatif"},
            "score": 100,
            "badges": ["Test Badge"]
        }
    
    def test_classify_message(self):
        """Test de classification des messages"""
        assert self.luna.classify_message("salut") == "greeting"
        assert self.luna.classify_message("aide") == "help_request"
        assert self.luna.classify_message("mission") == "mission_related"
        assert self.luna.classify_message("merci") == "gratitude"
        assert self.luna.classify_message("qui es-tu") == "identity_question"
        assert self.luna.classify_message("test") == "general"
    
    def test_generate_greeting_creative(self):
        """Test des salutations pour un hacker créatif"""
        context = {"user_personality": "hacker_creatif"}
        response = self.luna.generate_greeting(context)
        
        assert "créatif" in response.lower() or "artiste" in response.lower()
    
    def test_generate_greeting_analytical(self):
        """Test des salutations pour un hacker analytique"""
        context = {"user_personality": "hacker_analytique"}
        response = self.luna.generate_greeting(context)
        
        assert "logique" in response.lower() or "analytique" in response.lower()
    
    def test_respond_with_context(self):
        """Test de réponse avec contexte"""
        result = self.luna.respond("salut", self.mock_profile)
        
        assert "message" in result
        assert "mood" in result
        assert "relationship_level" in result
        assert "context" in result
        assert len(self.luna.conversation_history) == 1
    
    def test_relationship_status(self):
        """Test du statut de relation"""
        self.luna.relationship_level = 8
        assert self.luna.get_relationship_status() == "Ami très proche"
        
        self.luna.relationship_level = 5
        assert self.luna.get_relationship_status() == "Ami"
        
        self.luna.relationship_level = 2
        assert self.luna.get_relationship_status() == "Étranger"
    
    def test_mood_description(self):
        """Test de description d'humeur"""
        self.luna.mood = "joyeux"
        assert "joyeuse" in self.luna.get_mood_description().lower()
        
        self.luna.mood = "inquiet"
        assert "inquiète" in self.luna.get_mood_description().lower()


class TestEffectsEngine:
    """Tests pour le moteur d'effets"""
    
    def setup_method(self):
        """Setup avant chaque test"""
        self.temp_dir = tempfile.mkdtemp()
        self.effects_engine = EffectsEngine(self.temp_dir)
    
    def teardown_method(self):
        """Cleanup après chaque test"""
        import shutil
        shutil.rmtree(self.temp_dir)
    
    def test_generate_effect_success(self):
        """Test de génération d'effet de succès"""
        effect = self.effects_engine.generate_effect("success")
        
        assert "ascii_art" in effect
        assert "sound" in effect
        assert "animation" in effect
        assert "color" in effect
        assert "duration" in effect
        assert effect["color"] == "#00ff88"
    
    def test_generate_effect_error(self):
        """Test de génération d'effet d'erreur"""
        effect = self.effects_engine.generate_effect("error")
        
        assert effect["color"] == "#ff4444"
        assert effect["animation"] == "shake"
    
    def test_generate_effect_luna(self):
        """Test de génération d'effet LUNA"""
        effect = self.effects_engine.generate_effect("luna")
        
        assert effect["color"] == "#00ffff"
        assert effect["animation"] == "typing_effect"
    
    def test_personalize_effect(self):
        """Test de personnalisation d'effet"""
        base_effect = {"color": "#ffffff"}
        personalized = self.effects_engine.personalize_effect(base_effect, "hacker_creatif")
        
        assert personalized["color"] == "#ff6b9d"
    
    def test_get_default_ascii(self):
        """Test de récupération d'ASCII art par défaut"""
        ascii_art = self.effects_engine.get_default_ascii("success")
        assert "SUCCÈS" in ascii_art
        
        ascii_art = self.effects_engine.get_default_ascii("luna")
        assert "LUNA" in ascii_art
    
    def test_get_animation_config(self):
        """Test de récupération de configuration d'animation"""
        config = self.effects_engine.get_animation_config("pulse_green")
        
        assert config["type"] == "pulse"
        assert config["color"] == "#00ff88"
        assert "duration" in config


class TestGameEngine:
    """Tests d'intégration pour le moteur de jeu"""
    
    def setup_method(self):
        """Setup avant chaque test"""
        self.temp_dir = tempfile.mkdtemp()
        self.game_engine = GameEngine()
        # Rediriger les profils vers le dossier temporaire
        self.game_engine.profile_manager.profiles_dir = self.temp_dir
    
    def teardown_method(self):
        """Cleanup après chaque test"""
        import shutil
        shutil.rmtree(self.temp_dir)
    
    def test_process_command_aide(self):
        """Test de traitement de la commande aide"""
        result = self.game_engine.process_command("aide", "test_user")
        
        assert result["réussite"] == True
        assert "effect" in result
        assert result["effect"]["type"] == "success"
    
    def test_process_command_unknown(self):
        """Test de traitement d'une commande inconnue"""
        result = self.game_engine.process_command("commande_inconnue", "test_user")
        
        assert result["réussite"] == False
        assert "effect" in result
        assert result["effect"]["type"] == "error"
    
    def test_process_command_with_luna(self):
        """Test de traitement avec intervention de LUNA"""
        result = self.game_engine.process_command("luna salut", "test_user")
        
        assert result["réussite"] == True
        assert "effect" in result
        # L'effet devrait être de type "luna" car contient "luna" dans le message
        assert "luna" in result.get("message", "").lower()
    
    def test_start_mission(self):
        """Test de démarrage de mission"""
        # Créer un fichier de mission temporaire
        mission_file = os.path.join(self.temp_dir, "test_mission.json")
        with open(mission_file, 'w') as f:
            json.dump({
                "id": "test_mission",
                "prerequis": []
            }, f)
        
        # Rediriger le moteur vers le dossier temporaire
        original_missions_dir = "data/missions"
        with patch.object(self.game_engine, 'can_start_mission') as mock_can_start:
            mock_can_start.return_value = True
            
            result = self.game_engine.start_mission("test_mission", "test_user")
            
            assert result["réussite"] == True
            assert "démarrée" in result["message"]
            assert "mission_context" in result
    
    def test_get_available_missions(self):
        """Test de récupération des missions disponibles"""
        missions = self.game_engine.get_available_missions("test_user")
        
        # Devrait retourner une liste (même vide)
        assert isinstance(missions, list)


# Tests de performance
class TestPerformance:
    """Tests de performance"""
    
    def test_command_processing_speed(self):
        """Test de vitesse de traitement des commandes"""
        import time
        
        game_engine = GameEngine()
        start_time = time.time()
        
        for _ in range(100):
            game_engine.process_command("aide", "test_user")
        
        end_time = time.time()
        processing_time = end_time - start_time
        
        # Devrait traiter 100 commandes en moins de 1 seconde
        assert processing_time < 1.0
    
    def test_luna_response_speed(self):
        """Test de vitesse de réponse de LUNA"""
        import time
        
        luna = LunaAI()
        mock_profile = {"personnalite": {"type": "hacker_creatif"}}
        
        start_time = time.time()
        
        for _ in range(50):
            luna.respond("salut", mock_profile)
        
        end_time = time.time()
        processing_time = end_time - start_time
        
        # Devrait traiter 50 réponses en moins de 0.5 seconde
        assert processing_time < 0.5


# Tests de compatibilité
class TestCompatibility:
    """Tests de compatibilité"""
    
    def test_profile_backward_compatibility(self):
        """Test de compatibilité avec les anciens profils"""
        profile_manager = ProfileManager()
        
        # Ancien format de profil
        old_profile = {
            "score": 100,
            "badges": ["Old Badge"]
            # Manque les nouvelles clés
        }
        
        # Devrait être corrigé automatiquement
        corrected_profile = profile_manager.ensure_profile_structure(old_profile)
        
        assert "personnalite" in corrected_profile
        assert "progression" in corrected_profile
        assert corrected_profile["score"] == 100
        assert "Old Badge" in corrected_profile["badges"]
    
    def test_command_backward_compatibility(self):
        """Test de compatibilité avec les anciennes commandes"""
        command_handler = CommandHandler()
        mock_profile = {
            "score": 0,
            "badges": [],
            "personnalite": {"type": "non_detecte"},
            "progression": {"univers_debloques": ["arkalia_base"], "portails_ouverts": []}
        }
        
        # Anciennes commandes devraient toujours fonctionner
        result = command_handler.handle_command("hacker_coffre", mock_profile)
        assert result["réussite"] == True
        
        result = command_handler.handle_command("aide", mock_profile)
        assert result["réussite"] == True


if __name__ == "__main__":
    # Exécuter les tests
    pytest.main([__file__, "-v"]) 