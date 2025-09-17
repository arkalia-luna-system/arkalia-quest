#!/usr/bin/env python3
"""
🎨 MOTEUR DE CUSTOMISATION - ARKALIA QUEST
==========================================

Système de personnalisation avancée pour Arkalia Quest.
Gère les avatars, skins, thèmes, voix IA, et personnalisation complète.

Auteur: Assistant IA
Version: 1.0
"""

import json
import logging
import os
import uuid
from datetime import datetime
from typing import Any

# Configuration du logging
logger = logging.getLogger(__name__)


class CustomizationEngine:
    """Moteur de customisation pour la personnalisation avancée"""

    def __init__(self):
        self.avatars = {}
        self.themes = {}
        self.skins = {}
        self.voice_profiles = {}
        self.player_customizations = {}

        # Configuration
        self.default_theme = "matrix"
        self.default_avatar = "hacker_default"
        self.default_voice = "luna_neutral"

        # Initialiser les données
        self.load_customization_data()
        self.init_default_assets()

    def load_customization_data(self):
        """Charge les données de customisation"""
        try:
            # Charger les customisations des joueurs
            customizations_file = os.path.join("data", "player_customizations.json")
            if os.path.exists(customizations_file):
                with open(customizations_file, encoding="utf-8") as f:
                    self.player_customizations = json.load(f)

            logger.info("✅ Données de customisation chargées")
        except Exception as e:
            logger.error(f"❌ Erreur chargement customisation: {e}")

    def save_customization_data(self):
        """Sauvegarde les données de customisation"""
        try:
            os.makedirs("data", exist_ok=True)

            with open(
                os.path.join("data", "player_customizations.json"),
                "w",
                encoding="utf-8",
            ) as f:
                json.dump(self.player_customizations, f, indent=2, ensure_ascii=False)

            logger.info("✅ Données de customisation sauvegardées")
        except Exception as e:
            logger.error(f"❌ Erreur sauvegarde customisation: {e}")

    def init_default_assets(self):
        """Initialise les assets par défaut"""
        # Thèmes par défaut
        self.themes = {
            "matrix": {
                "id": "matrix",
                "name": "Matrix",
                "description": "Thème cyberpunk classique",
                "colors": {
                    "primary": "#00ff00",
                    "secondary": "#0066ff",
                    "accent": "#ff6600",
                    "background": "#000000",
                    "text": "#00ff00",
                    "success": "#00ff88",
                    "error": "#ff0044",
                    "warning": "#ffaa00",
                },
                "fonts": {"primary": "IBM Plex Mono", "secondary": "Courier New"},
                "effects": {
                    "glitch": True,
                    "particles": True,
                    "scanlines": True,
                    "terminal_glow": True,
                },
                "unlocked": True,
                "premium": False,
            },
            "luna_vision": {
                "id": "luna_vision",
                "name": "Luna Vision",
                "description": "Thème lunaire mystique",
                "colors": {
                    "primary": "#6b46c1",
                    "secondary": "#3b82f6",
                    "accent": "#f59e0b",
                    "background": "#1e1b4b",
                    "text": "#e0e7ff",
                    "success": "#10b981",
                    "error": "#ef4444",
                    "warning": "#f59e0b",
                },
                "fonts": {"primary": "Inter", "secondary": "JetBrains Mono"},
                "effects": {
                    "aurora": True,
                    "stars": True,
                    "moon_phases": True,
                    "cosmic_glow": True,
                },
                "unlocked": True,
                "premium": False,
            },
            "neon_city": {
                "id": "neon_city",
                "name": "Neon City",
                "description": "Métropole cyberpunk",
                "colors": {
                    "primary": "#ff0080",
                    "secondary": "#00ffff",
                    "accent": "#ffff00",
                    "background": "#0a0a0a",
                    "text": "#ffffff",
                    "success": "#00ff00",
                    "error": "#ff0000",
                    "warning": "#ffff00",
                },
                "fonts": {"primary": "Orbitron", "secondary": "Roboto Mono"},
                "effects": {
                    "neon_glow": True,
                    "rain": True,
                    "city_lights": True,
                    "hologram": True,
                },
                "unlocked": False,
                "premium": True,
            },
            "retro_wave": {
                "id": "retro_wave",
                "name": "Retro Wave",
                "description": "Synthwave des années 80",
                "colors": {
                    "primary": "#ff00ff",
                    "secondary": "#00ffff",
                    "accent": "#ffff00",
                    "background": "#1a0033",
                    "text": "#ffffff",
                    "success": "#00ff00",
                    "error": "#ff0000",
                    "warning": "#ffaa00",
                },
                "fonts": {"primary": "Orbitron", "secondary": "Courier New"},
                "effects": {
                    "grid": True,
                    "sunset": True,
                    "vaporwave": True,
                    "retro_glow": True,
                },
                "unlocked": False,
                "premium": True,
            },
        }

        # Avatars par défaut
        self.avatars = {
            "hacker_default": {
                "id": "hacker_default",
                "name": "Hacker Classique",
                "description": "Avatar cyberpunk basique",
                "image": "/static/images/avatars/hacker_default.png",
                "unlocked": True,
                "premium": False,
                "category": "basic",
            },
            "luna_avatar": {
                "id": "luna_avatar",
                "name": "LUNA",
                "description": "Avatar de l'IA LUNA",
                "image": "/static/images/avatars/luna_avatar.png",
                "unlocked": True,
                "premium": False,
                "category": "special",
            },
            "cyber_ninja": {
                "id": "cyber_ninja",
                "name": "Cyber Ninja",
                "description": "Ninja numérique",
                "image": "/static/images/avatars/cyber_ninja.png",
                "unlocked": False,
                "premium": True,
                "category": "premium",
            },
            "quantum_hacker": {
                "id": "quantum_hacker",
                "name": "Quantum Hacker",
                "description": "Hacker quantique",
                "image": "/static/images/avatars/quantum_hacker.png",
                "unlocked": False,
                "premium": True,
                "category": "premium",
            },
        }

        # Skins par défaut
        self.skins = {
            "terminal_basic": {
                "id": "terminal_basic",
                "name": "Terminal Basique",
                "description": "Interface terminal standard",
                "type": "terminal",
                "unlocked": True,
                "premium": False,
            },
            "terminal_neon": {
                "id": "terminal_neon",
                "name": "Terminal Neon",
                "description": "Terminal avec effets néon",
                "type": "terminal",
                "unlocked": False,
                "premium": True,
            },
            "terminal_hologram": {
                "id": "terminal_hologram",
                "name": "Terminal Hologramme",
                "description": "Interface holographique",
                "type": "terminal",
                "unlocked": False,
                "premium": True,
            },
        }

        # Profils vocaux par défaut
        self.voice_profiles = {
            "luna_neutral": {
                "id": "luna_neutral",
                "name": "LUNA Neutre",
                "description": "Voix standard de LUNA",
                "voice_type": "neutral",
                "speed": 1.0,
                "pitch": 1.0,
                "unlocked": True,
                "premium": False,
            },
            "luna_energetic": {
                "id": "luna_energetic",
                "name": "LUNA Énergique",
                "description": "LUNA avec plus d'énergie",
                "voice_type": "energetic",
                "speed": 1.2,
                "pitch": 1.1,
                "unlocked": False,
                "premium": False,
            },
            "luna_mysterious": {
                "id": "luna_mysterious",
                "name": "LUNA Mystérieuse",
                "description": "LUNA avec une voix mystérieuse",
                "voice_type": "mysterious",
                "speed": 0.8,
                "pitch": 0.9,
                "unlocked": False,
                "premium": True,
            },
        }

    # ===== GESTION DES THÈMES =====

    def get_available_themes(self, player_id: str) -> list[dict[str, Any]]:
        """Retourne les thèmes disponibles pour un joueur"""
        available_themes = []

        for theme_id, theme in self.themes.items():
            if theme["unlocked"] or self.is_theme_unlocked(player_id, theme_id):
                available_themes.append(theme)

        return available_themes

    def get_theme(self, theme_id: str) -> dict[str, Any]:
        """Retourne un thème spécifique"""
        return self.themes.get(theme_id, {})

    def get_player_theme(self, player_id: str) -> dict[str, Any]:
        """Retourne le thème actuel d'un joueur"""
        if player_id not in self.player_customizations:
            return self.themes.get(self.default_theme, {})

        current_theme_id = self.player_customizations[player_id].get(
            "current_theme", self.default_theme
        )
        return self.themes.get(current_theme_id, {})

    def is_theme_unlocked(self, player_id: str, theme_id: str) -> bool:
        """Vérifie si un thème est débloqué pour un joueur"""
        if player_id not in self.player_customizations:
            return False

        unlocked_themes = self.player_customizations[player_id].get("unlocked_themes", [])
        return theme_id in unlocked_themes

    def unlock_theme(self, player_id: str, theme_id: str) -> dict[str, Any]:
        """Débloque un thème pour un joueur"""
        if theme_id not in self.themes:
            return {"success": False, "error": "Thème introuvable"}

        if self.is_theme_unlocked(player_id, theme_id):
            return {"success": False, "error": "Thème déjà débloqué"}

        if player_id not in self.player_customizations:
            self.player_customizations[player_id] = {
                "unlocked_themes": [],
                "unlocked_avatars": [],
                "unlocked_skins": [],
                "unlocked_voices": [],
                "current_theme": self.default_theme,
                "current_avatar": self.default_avatar,
                "current_skin": "terminal_basic",
                "current_voice": self.default_voice,
            }

        self.player_customizations[player_id]["unlocked_themes"].append(theme_id)
        self.save_customization_data()

        return {
            "success": True,
            "message": f"Thème '{self.themes[theme_id]['name']}' débloqué !",
        }

    def set_player_theme(self, player_id: str, theme_id: str) -> dict[str, Any]:
        """Définit le thème d'un joueur"""
        if theme_id not in self.themes:
            return {"success": False, "error": "Thème introuvable"}

        if not self.is_theme_unlocked(player_id, theme_id):
            return {"success": False, "error": "Thème non débloqué"}

        if player_id not in self.player_customizations:
            self.player_customizations[player_id] = {
                "unlocked_themes": [theme_id],
                "unlocked_avatars": [],
                "unlocked_skins": [],
                "unlocked_voices": [],
                "current_theme": theme_id,
                "current_avatar": self.default_avatar,
                "current_skin": "terminal_basic",
                "current_voice": self.default_voice,
            }

        self.player_customizations[player_id]["current_theme"] = theme_id
        self.save_customization_data()

        return {
            "success": True,
            "message": f"Thème changé vers '{self.themes[theme_id]['name']}' !",
        }

    # ===== GESTION DES AVATARS =====

    def get_available_avatars(self, player_id: str) -> list[dict[str, Any]]:
        """Retourne les avatars disponibles pour un joueur"""
        available_avatars = []

        for avatar_id, avatar in self.avatars.items():
            if avatar["unlocked"] or self.is_avatar_unlocked(player_id, avatar_id):
                available_avatars.append(avatar)

        return available_avatars

    def get_avatar(self, avatar_id: str) -> dict[str, Any]:
        """Retourne un avatar spécifique"""
        return self.avatars.get(avatar_id, {})

    def get_player_avatar(self, player_id: str) -> dict[str, Any]:
        """Retourne l'avatar actuel d'un joueur"""
        if player_id not in self.player_customizations:
            return self.avatars.get(self.default_avatar, {})

        current_avatar_id = self.player_customizations[player_id].get(
            "current_avatar", self.default_avatar
        )
        return self.avatars.get(current_avatar_id, {})

    def is_avatar_unlocked(self, player_id: str, avatar_id: str) -> bool:
        """Vérifie si un avatar est débloqué pour un joueur"""
        if player_id not in self.player_customizations:
            return False

        unlocked_avatars = self.player_customizations[player_id].get("unlocked_avatars", [])
        return avatar_id in unlocked_avatars

    def unlock_avatar(self, player_id: str, avatar_id: str) -> dict[str, Any]:
        """Débloque un avatar pour un joueur"""
        if avatar_id not in self.avatars:
            return {"success": False, "error": "Avatar introuvable"}

        if self.is_avatar_unlocked(player_id, avatar_id):
            return {"success": False, "error": "Avatar déjà débloqué"}

        if player_id not in self.player_customizations:
            self.player_customizations[player_id] = {
                "unlocked_themes": [],
                "unlocked_avatars": [],
                "unlocked_skins": [],
                "unlocked_voices": [],
                "current_theme": self.default_theme,
                "current_avatar": self.default_avatar,
                "current_skin": "terminal_basic",
                "current_voice": self.default_voice,
            }

        self.player_customizations[player_id]["unlocked_avatars"].append(avatar_id)
        self.save_customization_data()

        return {
            "success": True,
            "message": f"Avatar '{self.avatars[avatar_id]['name']}' débloqué !",
        }

    def set_player_avatar(self, player_id: str, avatar_id: str) -> dict[str, Any]:
        """Définit l'avatar d'un joueur"""
        if avatar_id not in self.avatars:
            return {"success": False, "error": "Avatar introuvable"}

        if not self.is_avatar_unlocked(player_id, avatar_id):
            return {"success": False, "error": "Avatar non débloqué"}

        if player_id not in self.player_customizations:
            self.player_customizations[player_id] = {
                "unlocked_themes": [],
                "unlocked_avatars": [avatar_id],
                "unlocked_skins": [],
                "unlocked_voices": [],
                "current_theme": self.default_theme,
                "current_avatar": avatar_id,
                "current_skin": "terminal_basic",
                "current_voice": self.default_voice,
            }

        self.player_customizations[player_id]["current_avatar"] = avatar_id
        self.save_customization_data()

        return {
            "success": True,
            "message": f"Avatar changé vers '{self.avatars[avatar_id]['name']}' !",
        }

    # ===== GESTION DES SKINS =====

    def get_available_skins(self, player_id: str, skin_type: str = None) -> list[dict[str, Any]]:
        """Retourne les skins disponibles pour un joueur"""
        available_skins = []

        for skin_id, skin in self.skins.items():
            if skin_type and skin["type"] != skin_type:
                continue

            if skin["unlocked"] or self.is_skin_unlocked(player_id, skin_id):
                available_skins.append(skin)

        return available_skins

    def get_skin(self, skin_id: str) -> dict[str, Any]:
        """Retourne un skin spécifique"""
        return self.skins.get(skin_id, {})

    def get_player_skin(self, player_id: str) -> dict[str, Any]:
        """Retourne le skin actuel d'un joueur"""
        if player_id not in self.player_customizations:
            return self.skins.get("terminal_basic", {})

        current_skin_id = self.player_customizations[player_id].get(
            "current_skin", "terminal_basic"
        )
        return self.skins.get(current_skin_id, {})

    def is_skin_unlocked(self, player_id: str, skin_id: str) -> bool:
        """Vérifie si un skin est débloqué pour un joueur"""
        if player_id not in self.player_customizations:
            return False

        unlocked_skins = self.player_customizations[player_id].get("unlocked_skins", [])
        return skin_id in unlocked_skins

    def unlock_skin(self, player_id: str, skin_id: str) -> dict[str, Any]:
        """Débloque un skin pour un joueur"""
        if skin_id not in self.skins:
            return {"success": False, "error": "Skin introuvable"}

        if self.is_skin_unlocked(player_id, skin_id):
            return {"success": False, "error": "Skin déjà débloqué"}

        if player_id not in self.player_customizations:
            self.player_customizations[player_id] = {
                "unlocked_themes": [],
                "unlocked_avatars": [],
                "unlocked_skins": [],
                "unlocked_voices": [],
                "current_theme": self.default_theme,
                "current_avatar": self.default_avatar,
                "current_skin": "terminal_basic",
                "current_voice": self.default_voice,
            }

        self.player_customizations[player_id]["unlocked_skins"].append(skin_id)
        self.save_customization_data()

        return {
            "success": True,
            "message": f"Skin '{self.skins[skin_id]['name']}' débloqué !",
        }

    def set_player_skin(self, player_id: str, skin_id: str) -> dict[str, Any]:
        """Définit le skin d'un joueur"""
        if skin_id not in self.skins:
            return {"success": False, "error": "Skin introuvable"}

        # Débloquer le skin s'il ne l'est pas déjà
        if not self.is_skin_unlocked(player_id, skin_id):
            unlock_result = self.unlock_skin(player_id, skin_id)
            if not unlock_result["success"]:
                return unlock_result

        if player_id not in self.player_customizations:
            self.player_customizations[player_id] = {
                "unlocked_themes": [],
                "unlocked_avatars": [],
                "unlocked_skins": [skin_id],
                "unlocked_voices": [],
                "current_theme": self.default_theme,
                "current_avatar": self.default_avatar,
                "current_skin": skin_id,
                "current_voice": self.default_voice,
            }

        self.player_customizations[player_id]["current_skin"] = skin_id
        self.save_customization_data()

        return {
            "success": True,
            "message": f"Skin changé vers '{self.skins[skin_id]['name']}' !",
        }

    # ===== GESTION DES VOIX =====

    def get_available_voices(self, player_id: str) -> list[dict[str, Any]]:
        """Retourne les voix disponibles pour un joueur"""
        available_voices = []

        for voice_id, voice in self.voice_profiles.items():
            if voice["unlocked"] or self.is_voice_unlocked(player_id, voice_id):
                available_voices.append(voice)

        return available_voices

    def get_voice(self, voice_id: str) -> dict[str, Any]:
        """Retourne une voix spécifique"""
        return self.voice_profiles.get(voice_id, {})

    def get_player_voice(self, player_id: str) -> dict[str, Any]:
        """Retourne la voix actuelle d'un joueur"""
        if player_id not in self.player_customizations:
            return self.voice_profiles.get(self.default_voice, {})

        current_voice_id = self.player_customizations[player_id].get(
            "current_voice", self.default_voice
        )
        return self.voice_profiles.get(current_voice_id, {})

    def is_voice_unlocked(self, player_id: str, voice_id: str) -> bool:
        """Vérifie si une voix est débloquée pour un joueur"""
        if player_id not in self.player_customizations:
            return False

        unlocked_voices = self.player_customizations[player_id].get("unlocked_voices", [])
        return voice_id in unlocked_voices

    def unlock_voice(self, player_id: str, voice_id: str) -> dict[str, Any]:
        """Débloque une voix pour un joueur"""
        if voice_id not in self.voice_profiles:
            return {"success": False, "error": "Voix introuvable"}

        if self.is_voice_unlocked(player_id, voice_id):
            return {"success": False, "error": "Voix déjà débloquée"}

        if player_id not in self.player_customizations:
            self.player_customizations[player_id] = {
                "unlocked_themes": [],
                "unlocked_avatars": [],
                "unlocked_skins": [],
                "unlocked_voices": [],
                "current_theme": self.default_theme,
                "current_avatar": self.default_avatar,
                "current_skin": "terminal_basic",
                "current_voice": self.default_voice,
            }

        self.player_customizations[player_id]["unlocked_voices"].append(voice_id)
        self.save_customization_data()

        return {
            "success": True,
            "message": f"Voix '{self.voice_profiles[voice_id]['name']}' débloquée !",
        }

    def set_player_voice(self, player_id: str, voice_id: str) -> dict[str, Any]:
        """Définit la voix d'un joueur"""
        if voice_id not in self.voice_profiles:
            return {"success": False, "error": "Voix introuvable"}

        # Débloquer la voix si elle ne l'est pas déjà
        if not self.is_voice_unlocked(player_id, voice_id):
            unlock_result = self.unlock_voice(player_id, voice_id)
            if not unlock_result["success"]:
                return unlock_result

        if player_id not in self.player_customizations:
            self.player_customizations[player_id] = {
                "unlocked_themes": [],
                "unlocked_avatars": [],
                "unlocked_skins": [],
                "unlocked_voices": [voice_id],
                "current_theme": self.default_theme,
                "current_avatar": self.default_avatar,
                "current_skin": "terminal_basic",
                "current_voice": voice_id,
            }

        self.player_customizations[player_id]["current_voice"] = voice_id
        self.save_customization_data()

        return {
            "success": True,
            "message": f"Voix changée vers '{self.voice_profiles[voice_id]['name']}' !",
        }

    # ===== CUSTOMISATION AVANCÉE =====

    def create_custom_theme(
        self, player_id: str, theme_name: str, theme_data: dict[str, Any]
    ) -> dict[str, Any]:
        """Crée un thème personnalisé"""
        theme_id = f"custom_{player_id}_{uuid.uuid4().hex[:8]}"

        custom_theme = {
            "id": theme_id,
            "name": theme_name,
            "description": theme_data.get("description", "Thème créé par l'utilisateur"),
            "colors": theme_data.get("colors", {}),
            "fonts": theme_data.get("fonts", {}),
            "effects": theme_data.get("effects", {}),
            "unlocked": True,
            "premium": False,
            "custom": True,
            "creator": player_id,
            "created_at": datetime.now().isoformat(),
        }

        # Ajouter aux thèmes disponibles
        self.themes[theme_id] = custom_theme

        # Débloquer pour le créateur
        self.unlock_theme(player_id, theme_id)

        return {
            "success": True,
            "theme": custom_theme,
            "message": "Thème personnalisé créé !",
        }

    def get_custom_themes(self, player_id: str) -> list[dict[str, Any]]:
        """Retourne les thèmes personnalisés d'un joueur"""
        custom_themes = []
        for theme in self.themes.values():
            if theme.get("custom", False) and theme.get("creator") == player_id:
                custom_themes.append(theme)
        return custom_themes

    def reset_player_customization(self, player_id: str) -> dict[str, Any]:
        """Réinitialise la customisation d'un joueur"""
        if player_id in self.player_customizations:
            self.player_customizations[player_id] = {
                "unlocked_themes": [self.default_theme],
                "unlocked_avatars": [self.default_avatar],
                "unlocked_skins": ["terminal_basic"],
                "unlocked_voices": [self.default_voice],
                "current_theme": self.default_theme,
                "current_avatar": self.default_avatar,
                "current_skin": "terminal_basic",
                "current_voice": self.default_voice,
            }
            self.save_customization_data()
            return {"success": True, "message": "Customisation réinitialisée !"}
        return {"success": False, "error": "Joueur introuvable"}

    def get_unlocked_items(self, player_id: str) -> dict[str, list[dict[str, Any]]]:
        """Retourne tous les objets débloqués d'un joueur"""
        if player_id not in self.player_customizations:
            return {"themes": [], "avatars": [], "skins": [], "voices": []}

        customization = self.player_customizations[player_id]

        return {
            "themes": [
                self.themes[t] for t in customization.get("unlocked_themes", []) if t in self.themes
            ],
            "avatars": [
                self.avatars[a]
                for a in customization.get("unlocked_avatars", [])
                if a in self.avatars
            ],
            "skins": [
                self.skins[s] for s in customization.get("unlocked_skins", []) if s in self.skins
            ],
            "voices": [
                self.voice_profiles[v]
                for v in customization.get("unlocked_voices", [])
                if v in self.voice_profiles
            ],
        }

    def export_customization(self, player_id: str) -> dict[str, Any]:
        """Exporte la customisation d'un joueur"""
        customization = self.get_player_customization(player_id)
        return {
            "success": True,
            "player_id": player_id,
            "customization": customization,
            "exported_at": datetime.now().isoformat(),
        }

    def import_customization(self, player_id: str, import_data: dict[str, Any]) -> dict[str, Any]:
        """Importe une customisation pour un joueur"""
        try:
            if "customization" not in import_data:
                return {"success": False, "error": "Données d'import invalides"}

            # Appliquer la customisation importée
            self.player_customizations[player_id] = {
                "unlocked_themes": [
                    t["id"] for t in import_data["customization"].get("unlocked_themes", [])
                ],
                "unlocked_avatars": [
                    a["id"] for a in import_data["customization"].get("unlocked_avatars", [])
                ],
                "unlocked_skins": [
                    s["id"] for s in import_data["customization"].get("unlocked_skins", [])
                ],
                "unlocked_voices": [
                    v["id"] for v in import_data["customization"].get("unlocked_voices", [])
                ],
                "current_theme": import_data["customization"]
                .get("current_theme", {})
                .get("id", self.default_theme),
                "current_avatar": import_data["customization"]
                .get("current_avatar", {})
                .get("id", self.default_avatar),
                "current_skin": import_data["customization"]
                .get("current_skin", {})
                .get("id", "terminal_basic"),
                "current_voice": import_data["customization"]
                .get("current_voice", {})
                .get("id", self.default_voice),
            }

            self.save_customization_data()
            return {"success": True, "message": "Customisation importée !"}
        except Exception as e:
            return {"success": False, "error": f"Erreur d'import: {str(e)}"}

    def get_player_customization(self, player_id: str) -> dict[str, Any]:
        """Retourne la customisation complète d'un joueur"""
        if player_id not in self.player_customizations:
            # Créer une customisation par défaut
            self.player_customizations[player_id] = {
                "unlocked_themes": [self.default_theme],
                "unlocked_avatars": [self.default_avatar],
                "unlocked_skins": ["terminal_basic"],
                "unlocked_voices": [self.default_voice],
                "current_theme": self.default_theme,
                "current_avatar": self.default_avatar,
                "current_skin": "terminal_basic",
                "current_voice": self.default_voice,
            }
            self.save_customization_data()

        customization = self.player_customizations[player_id]

        return {
            "player_id": player_id,
            "theme": self.themes.get(customization["current_theme"], {}),
            "avatar": self.avatars.get(customization["current_avatar"], {}),
            "skin": self.skins.get(customization["current_skin"], {}),
            "voice": self.voice_profiles.get(customization["current_voice"], {}),
            "current_theme": self.themes.get(customization["current_theme"], {}),
            "current_avatar": self.avatars.get(customization["current_avatar"], {}),
            "current_skin": self.skins.get(customization["current_skin"], {}),
            "current_voice": self.voice_profiles.get(customization["current_voice"], {}),
            "unlocked_themes": [
                self.themes[t] for t in customization["unlocked_themes"] if t in self.themes
            ],
            "unlocked_avatars": [
                self.avatars[a] for a in customization["unlocked_avatars"] if a in self.avatars
            ],
            "unlocked_skins": [
                self.skins[s] for s in customization["unlocked_skins"] if s in self.skins
            ],
            "unlocked_voices": [
                self.voice_profiles[v]
                for v in customization["unlocked_voices"]
                if v in self.voice_profiles
            ],
        }

    def apply_customization(self, player_id: str) -> dict[str, Any]:
        """Applique la customisation d'un joueur"""
        customization = self.get_player_customization(player_id)

        return {
            "success": True,
            "customization": customization,
            "css_variables": self.generate_css_variables(customization["current_theme"]),
            "message": "Customisation appliquée !",
        }

    def generate_css_variables(self, theme: dict[str, Any]) -> dict[str, str]:
        """Génère les variables CSS pour un thème"""
        if not theme:
            return {}

        css_vars = {}

        # Variables de couleur
        colors = theme.get("colors", {})
        for color_name, color_value in colors.items():
            css_vars[f"--theme-{color_name}"] = color_value

        # Variables de police
        fonts = theme.get("fonts", {})
        for font_name, font_value in fonts.items():
            css_vars[f"--theme-font-{font_name}"] = font_value

        return css_vars

    # ===== SYSTÈME DE RÉCOMPENSES =====

    def unlock_random_customization(
        self, player_id: str, category: str = "random"
    ) -> dict[str, Any]:
        """Débloque une customisation aléatoire"""
        if category == "random":
            categories = ["themes", "avatars", "skins", "voices"]
            category = categories[hash(player_id + str(datetime.now().date())) % len(categories)]

        if category == "themes":
            available = [
                t
                for t in self.themes.values()
                if not t.get("unlocked", False) and not self.is_theme_unlocked(player_id, t["id"])
            ]
        elif category == "avatars":
            available = [
                a
                for a in self.avatars.values()
                if not a.get("unlocked", False) and not self.is_avatar_unlocked(player_id, a["id"])
            ]
        elif category == "skins":
            available = [
                s
                for s in self.skins.values()
                if not s.get("unlocked", False) and not self.is_skin_unlocked(player_id, s["id"])
            ]
        elif category == "voices":
            available = [
                v
                for v in self.voice_profiles.values()
                if not v.get("unlocked", False) and not self.is_voice_unlocked(player_id, v["id"])
            ]
        else:
            return {"success": False, "error": "Catégorie invalide"}

        if not available:
            return {
                "success": False,
                "error": "Aucune customisation disponible à débloquer",
            }

        # Sélectionner aléatoirement
        selected = available[hash(player_id + str(datetime.now())) % len(available)]

        # Débloquer
        if category == "themes":
            result = self.unlock_theme(player_id, selected["id"])
        elif category == "avatars":
            result = self.unlock_avatar(player_id, selected["id"])
        elif category == "skins":
            result = self.unlock_skin(player_id, selected["id"])
        elif category == "voices":
            result = self.unlock_voice(player_id, selected["id"])

        if result["success"]:
            result["unlocked_item"] = selected

        return result


# Instance globale
customization_engine = CustomizationEngine()
