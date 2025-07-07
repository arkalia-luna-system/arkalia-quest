"""
Effects Engine - Moteur d'effets visuels et audio
"""

import os
import random
from typing import Dict, Any, Optional


class EffectsEngine:
    """Moteur d'effets visuels et audio pour Arkalia Quest"""
    
    def __init__(self, effects_dir: str = "data/effects"):
        self.effects_dir = effects_dir
        self.ascii_arts = self.load_ascii_arts()
        self.sounds = self.load_sounds()
        self.animations = self.load_animations()
        
        # Effets par défaut
        self.default_effects = {
            "success": {
                "ascii_art": self.get_default_ascii("success"),
                "sound": "success.mp3",
                "animation": "pulse_green",
                "color": "#00ff88",
                "duration": 2000
            },
            "error": {
                "ascii_art": self.get_default_ascii("error"),
                "sound": "error.mp3", 
                "animation": "shake",
                "color": "#ff4444",
                "duration": 1500
            },
            "luna": {
                "ascii_art": self.get_default_ascii("luna"),
                "sound": "luna_voice.mp3",
                "animation": "typing_effect",
                "color": "#00ffff",
                "duration": 3000
            },
            "mission": {
                "ascii_art": self.get_default_ascii("mission"),
                "sound": "mission_start.mp3",
                "animation": "fade_in",
                "color": "#ffaa00",
                "duration": 2500
            },
            "unlock": {
                "ascii_art": self.get_default_ascii("unlock"),
                "sound": "unlock.mp3",
                "animation": "glow_pulse",
                "color": "#00ff00",
                "duration": 4000
            }
        }
    
    def load_ascii_arts(self) -> Dict[str, str]:
        """Charge tous les ASCII arts depuis les fichiers"""
        
        ascii_arts = {}
        ascii_dir = os.path.join(self.effects_dir, "ascii")
        
        if os.path.exists(ascii_dir):
            for filename in os.listdir(ascii_dir):
                if filename.endswith('.txt'):
                    name = filename.replace('.txt', '')
                    try:
                        with open(os.path.join(ascii_dir, filename), 'r', encoding='utf-8') as f:
                            ascii_arts[name] = f.read()
                    except Exception:
                        ascii_arts[name] = self.get_default_ascii(name)
        
        return ascii_arts
    
    def load_sounds(self) -> Dict[str, str]:
        """Charge la liste des sons disponibles"""
        
        sounds = {}
        sounds_dir = os.path.join(self.effects_dir, "sounds")
        
        if os.path.exists(sounds_dir):
            for filename in os.listdir(sounds_dir):
                if filename.endswith(('.mp3', '.wav', '.ogg')):
                    name = filename.split('.')[0]
                    sounds[name] = filename
        
        return sounds
    
    def load_animations(self) -> Dict[str, Dict[str, Any]]:
        """Charge les définitions d'animations"""
        
        return {
            "pulse_green": {
                "type": "pulse",
                "color": "#00ff88",
                "duration": 2000,
                "easing": "ease-in-out"
            },
            "shake": {
                "type": "shake",
                "intensity": 10,
                "duration": 500,
                "easing": "ease-in-out"
            },
            "typing_effect": {
                "type": "typing",
                "speed": 50,
                "duration": 3000,
                "easing": "linear"
            },
            "fade_in": {
                "type": "fade",
                "direction": "in",
                "duration": 1000,
                "easing": "ease-in"
            },
            "glow_pulse": {
                "type": "glow",
                "color": "#00ff00",
                "duration": 2000,
                "easing": "ease-in-out"
            },
            "matrix_glitch": {
                "type": "glitch",
                "intensity": 5,
                "duration": 1500,
                "easing": "ease-in-out"
            }
        }
    
    def generate_effect(self, effect_type: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Génère un effet selon le type et le contexte
        
        Args:
            effect_type: Type d'effet (success, error, luna, mission, unlock)
            context: Contexte supplémentaire pour personnaliser l'effet
            
        Returns:
            Dict contenant l'effet complet
        """
        
        if context is None:
            context = {}
        
        # Récupérer l'effet de base
        base_effect = self.default_effects.get(effect_type, self.default_effects["success"]).copy()
        
        # Personnaliser selon le contexte
        if context.get("user_personality"):
            base_effect = self.personalize_effect(base_effect, context["user_personality"])
        
        # Ajouter des variations aléatoires
        base_effect = self.add_random_variations(base_effect)
        
        return base_effect
    
    def personalize_effect(self, effect: Dict[str, Any], personality: str) -> Dict[str, Any]:
        """Personnalise un effet selon la personnalité de l'utilisateur"""
        
        personality_colors = {
            "hacker_creatif": "#ff6b9d",  # Rose créatif
            "hacker_analytique": "#4ecdc4",  # Bleu analytique
            "hacker_social": "#45b7d1",  # Bleu social
            "hacker_rebelle": "#ff6b35",  # Orange rebelle
            "hacker_equilibre": "#96ceb4"  # Vert équilibré
        }
        
        if personality in personality_colors:
            effect["color"] = personality_colors[personality]
        
        return effect
    
    def add_random_variations(self, effect: Dict[str, Any]) -> Dict[str, Any]:
        """Ajoute des variations aléatoires à un effet"""
        
        # Variation de durée (±20%)
        duration_variation = random.uniform(0.8, 1.2)
        effect["duration"] = int(effect["duration"] * duration_variation)
        
        # Variation d'intensité pour certains effets
        if effect["animation"] == "shake":
            effect["intensity"] = random.randint(8, 15)
        elif effect["animation"] == "glow_pulse":
            effect["glow_intensity"] = random.uniform(0.5, 1.5)
        
        return effect
    
    def get_ascii_art(self, name: str) -> str:
        """Récupère un ASCII art par nom"""
        
        if name in self.ascii_arts:
            return self.ascii_arts[name]
        else:
            return self.get_default_ascii(name)
    
    def get_default_ascii(self, name: str) -> str:
        """Retourne un ASCII art par défaut"""
        
        default_ascii = {
            "success": """
    ╔══════════════════════════════════════════════════════════╗
    ║                    ✅ SUCCÈS ✅                          ║
    ║                                                          ║
    ║  ████████████████████████████████████████████████████████  ║
    ║  █░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░██  ║
    ║  █░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░██  ║
    ║  █░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░██  ║
    ║  █░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░██  ║
    ║  ████████████████████████████████████████████████████████  ║
    ╚══════════════════════════════════════════════════════════╝""",
            
            "error": """
    ╔══════════════════════════════════════════════════════════╗
    ║                    ❌ ERREUR ❌                          ║
    ║                                                          ║
    ║  ████████████████████████████████████████████████████████  ║
    ║  █░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░██  ║
    ║  █░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░██  ║
    ║  █░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░██  ║
    ║  █░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░██  ║
    ║  ████████████████████████████████████████████████████████  ║
    ╚══════════════════════════════════════════════════════════╝""",
            
            "luna": """
    ╔══════════════════════════════════════════════════════════╗
    ║                    🌙 LUNA AI 🌙                         ║
    ║                                                          ║
    ║  ████████████████████████████████████████████████████████  ║
    ║  █░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░██  ║
    ║  █░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░██  ║
    ║  █░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░██  ║
    ║  █░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░██  ║
    ║  ████████████████████████████████████████████████████████  ║
    ╚══════════════════════════════════════════════════════════╝""",
            
            "mission": """
    ╔══════════════════════════════════════════════════════════╗
    ║                    🎯 MISSION 🎯                         ║
    ║                                                          ║
    ║  ████████████████████████████████████████████████████████  ║
    ║  █░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░██  ║
    ║  █░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░██  ║
    ║  █░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░██  ║
    ║  █░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░██  ║
    ║  ████████████████████████████████████████████████████████  ║
    ╚══════════════════════════════════════════════════════════╝""",
            
            "unlock": """
    ╔══════════════════════════════════════════════════════════╗
    ║                    🔓 DÉBLOQUÉ 🔓                        ║
    ║                                                          ║
    ║  ████████████████████████████████████████████████████████  ║
    ║  █░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░██  ║
    ║  █░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░██  ║
    ║  █░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░██  ║
    ║  █░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░██  ║
    ║  ████████████████████████████████████████████████████████  ║
    ╚══════════════════════════════════════════════════════════╝"""
        }
        
        return default_ascii.get(name, "🎮")
    
    def get_animation_config(self, animation_name: str) -> Dict[str, Any]:
        """Récupère la configuration d'une animation"""
        
        return self.animations.get(animation_name, {
            "type": "fade",
            "duration": 1000,
            "easing": "ease-in-out"
        })
    
    def get_sound_path(self, sound_name: str) -> Optional[str]:
        """Récupère le chemin d'un son"""
        
        if sound_name in self.sounds:
            return os.path.join(self.effects_dir, "sounds", self.sounds[sound_name])
        return None
    
    def create_custom_effect(self, effect_config: Dict[str, Any]) -> Dict[str, Any]:
        """Crée un effet personnalisé"""
        
        # Fusionner avec les valeurs par défaut
        default_effect = self.default_effects["success"].copy()
        default_effect.update(effect_config)
        
        return default_effect 