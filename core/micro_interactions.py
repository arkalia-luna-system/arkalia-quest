#!/usr/bin/env python3
"""
✨ MOTEUR DE MICRO-INTERACTIONS - ARKALIA QUEST
==============================================

Système de micro-interactions et feedback avancé pour une UX exceptionnelle.
Gère les animations, sons, vibrations, et notifications contextuelles.

Auteur: Assistant IA
Version: 1.0
"""

import json
import logging
import os
import uuid
from datetime import datetime
from typing import Any, Dict, List

# Configuration du logging
logger = logging.getLogger(__name__)


class MicroInteractionsEngine:
    """Moteur de micro-interactions pour l'UX"""

    def __init__(self):
        self.interaction_templates = {}
        self.feedback_systems = {}
        self.animation_queue = []
        self.sound_queue = []
        self.notification_queue = []
        self.user_preferences = {}

        # Configuration
        self.max_queue_size = 100
        self.animation_duration = 300  # ms
        self.sound_volume = 0.7

        # Initialiser les données
        self.load_interaction_data()
        self.init_default_interactions()

    def load_interaction_data(self):
        """Charge les données d'interactions"""
        try:
            # Charger les préférences utilisateur
            preferences_file = os.path.join("data", "user_preferences.json")
            if os.path.exists(preferences_file):
                with open(preferences_file, encoding="utf-8") as f:
                    self.user_preferences = json.load(f)

            logger.info("✅ Données d'interactions chargées")
        except Exception as e:
            logger.error(f"❌ Erreur chargement interactions: {e}")

    def save_interaction_data(self):
        """Sauvegarde les données d'interactions"""
        try:
            os.makedirs("data", exist_ok=True)

            with open(
                os.path.join("data", "user_preferences.json"), "w", encoding="utf-8"
            ) as f:
                json.dump(self.user_preferences, f, indent=2, ensure_ascii=False)

            logger.info("✅ Données d'interactions sauvegardées")
        except Exception as e:
            logger.error(f"❌ Erreur sauvegarde interactions: {e}")

    def init_default_interactions(self):
        """Initialise les interactions par défaut"""
        # Templates d'interactions
        self.interaction_templates = {
            "button_click": {
                "id": "button_click",
                "type": "click",
                "animations": [
                    {
                        "element": "target",
                        "animation": "scale",
                        "duration": 150,
                        "easing": "ease-out",
                        "params": {"scale": 0.95},
                    },
                    {
                        "element": "target",
                        "animation": "ripple",
                        "duration": 300,
                        "easing": "ease-out",
                        "params": {"color": "rgba(0, 255, 0, 0.3)"},
                    },
                ],
                "sounds": [{"sound": "click", "volume": 0.3, "delay": 0}],
                "haptic": {"type": "light", "duration": 50},
            },
            "success_action": {
                "id": "success_action",
                "type": "success",
                "animations": [
                    {
                        "element": "target",
                        "animation": "success_pulse",
                        "duration": 600,
                        "easing": "ease-out",
                        "params": {"color": "#00ff88", "glow": True},
                    },
                    {
                        "element": "body",
                        "animation": "confetti",
                        "duration": 2000,
                        "easing": "ease-out",
                        "params": {
                            "count": 20,
                            "colors": ["#00ff88", "#0066ff", "#ff6600"],
                        },
                    },
                ],
                "sounds": [{"sound": "success", "volume": 0.5, "delay": 0}],
                "haptic": {"type": "success", "duration": 200},
                "notifications": [
                    {
                        "type": "toast",
                        "message": "Action réussie !",
                        "duration": 3000,
                        "position": "top-right",
                    }
                ],
            },
            "error_action": {
                "id": "error_action",
                "type": "error",
                "animations": [
                    {
                        "element": "target",
                        "animation": "error_shake",
                        "duration": 500,
                        "easing": "ease-in-out",
                        "params": {"intensity": 10},
                    },
                    {
                        "element": "target",
                        "animation": "error_glow",
                        "duration": 1000,
                        "easing": "ease-out",
                        "params": {"color": "#ff0044"},
                    },
                ],
                "sounds": [{"sound": "error", "volume": 0.4, "delay": 0}],
                "haptic": {"type": "error", "duration": 300},
                "notifications": [
                    {
                        "type": "toast",
                        "message": "Erreur détectée",
                        "duration": 4000,
                        "position": "top-right",
                        "style": "error",
                    }
                ],
            },
            "level_up": {
                "id": "level_up",
                "type": "achievement",
                "animations": [
                    {
                        "element": "target",
                        "animation": "level_up_glow",
                        "duration": 1000,
                        "easing": "ease-out",
                        "params": {"color": "#ffaa00", "size": 1.2},
                    },
                    {
                        "element": "body",
                        "animation": "level_up_particles",
                        "duration": 3000,
                        "easing": "ease-out",
                        "params": {"count": 50, "type": "stars"},
                    },
                ],
                "sounds": [
                    {"sound": "level_up", "volume": 0.6, "delay": 0},
                    {"sound": "fanfare", "volume": 0.4, "delay": 200},
                ],
                "haptic": {"type": "success", "duration": 500},
                "notifications": [
                    {
                        "type": "modal",
                        "title": "Niveau Supérieur !",
                        "message": "Félicitations ! Vous avez atteint un nouveau niveau !",
                        "duration": 5000,
                        "style": "celebration",
                    }
                ],
            },
            "badge_earned": {
                "id": "badge_earned",
                "type": "achievement",
                "animations": [
                    {
                        "element": "target",
                        "animation": "badge_reveal",
                        "duration": 800,
                        "easing": "ease-out",
                        "params": {"rotation": 360, "scale": 1.1},
                    },
                    {
                        "element": "body",
                        "animation": "badge_glow",
                        "duration": 2000,
                        "easing": "ease-out",
                        "params": {"color": "#6b46c1", "intensity": 0.8},
                    },
                ],
                "sounds": [{"sound": "badge_earned", "volume": 0.5, "delay": 0}],
                "haptic": {"type": "medium", "duration": 300},
                "notifications": [
                    {
                        "type": "badge_popup",
                        "title": "Nouveau Badge !",
                        "message": "Vous avez gagné un nouveau badge !",
                        "duration": 4000,
                        "style": "badge",
                    }
                ],
            },
            "mission_complete": {
                "id": "mission_complete",
                "type": "achievement",
                "animations": [
                    {
                        "element": "target",
                        "animation": "mission_complete",
                        "duration": 1200,
                        "easing": "ease-out",
                        "params": {"type": "checkmark", "color": "#00ff88"},
                    },
                    {
                        "element": "body",
                        "animation": "mission_particles",
                        "duration": 3000,
                        "easing": "ease-out",
                        "params": {"count": 30, "type": "sparkles"},
                    },
                ],
                "sounds": [{"sound": "mission_complete", "volume": 0.6, "delay": 0}],
                "haptic": {"type": "success", "duration": 400},
                "notifications": [
                    {
                        "type": "mission_popup",
                        "title": "Mission Accomplie !",
                        "message": "Félicitations ! Mission terminée avec succès !",
                        "duration": 5000,
                        "style": "mission",
                    }
                ],
            },
        }

        # Systèmes de feedback
        self.feedback_systems = {
            "visual": {
                "enabled": True,
                "intensity": "medium",
                "animations": True,
                "particles": True,
                "glow_effects": True,
            },
            "audio": {
                "enabled": True,
                "volume": 0.7,
                "sound_effects": True,
                "ambient_sounds": True,
                "voice_feedback": True,
            },
            "haptic": {
                "enabled": True,
                "intensity": "medium",
                "vibration_patterns": True,
                "tactile_feedback": True,
            },
            "notifications": {
                "enabled": True,
                "toast_notifications": True,
                "modal_notifications": True,
                "badge_notifications": True,
                "sound_notifications": True,
            },
        }

    # ===== GESTION DES INTERACTIONS =====

    def trigger_interaction(
        self,
        player_id: str,
        interaction_type: str,
        target_element: str = None,
        context: Dict[str, Any] = None,
    ) -> Dict[str, Any]:
        """Déclenche une interaction avec feedback immédiat"""
        if interaction_type not in self.interaction_templates:
            return {"success": False, "error": "Type d'interaction non trouvé"}

        # Vérifier les préférences utilisateur
        if not self.check_user_preferences(player_id, interaction_type):
            return {
                "success": False,
                "error": "Interaction désactivée par l'utilisateur",
            }

        template = self.interaction_templates[interaction_type]
        interaction_id = str(uuid.uuid4())

        # Générer des effets immédiats
        immediate_effects = self._generate_immediate_effects(interaction_type, context)

        interaction = {
            "id": interaction_id,
            "type": interaction_type,
            "target_element": target_element,
            "context": context or {},
            "timestamp": datetime.now().isoformat(),
            "template": template,
            "immediate_effects": immediate_effects,
        }

        # Ajouter à la queue d'exécution
        self.add_to_animation_queue(interaction)
        self.add_to_sound_queue(interaction)
        self.add_to_notification_queue(interaction)

        return {
            "success": True,
            "interaction_id": interaction_id,
            "interaction": interaction,
        }

    def _generate_immediate_effects(
        self, interaction_type: str, context: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """Génère des effets immédiats selon le type d'interaction"""

        effects = {
            "visual": True,
            "audio": True,
            "haptic": True,
            "particles": True,
            "animation": True,
        }

        # Effets spécifiques selon le type
        if interaction_type == "button_click":
            effects.update(
                {
                    "ripple_effect": True,
                    "scale_animation": True,
                    "sound": "click",
                    "vibration": [50],
                }
            )
        elif interaction_type == "success":
            effects.update(
                {
                    "glow_effect": True,
                    "particle_burst": True,
                    "sound": "success",
                    "vibration": [100, 50, 100],
                    "screen_flash": True,
                }
            )
        elif interaction_type == "error":
            effects.update(
                {
                    "shake_effect": True,
                    "red_flash": True,
                    "sound": "error",
                    "vibration": [200],
                }
            )
        elif interaction_type == "hover":
            effects.update(
                {
                    "glow_effect": True,
                    "scale_animation": True,
                    "sound": "hover",
                }
            )
        elif interaction_type == "luna_interaction":
            effects.update(
                {
                    "luna_glow": True,
                    "sparkle_effect": True,
                    "sound": "luna_chime",
                    "vibration": [75, 25, 75],
                }
            )
        elif interaction_type == "hack_success":
            effects.update(
                {
                    "matrix_effect": True,
                    "green_glow": True,
                    "sound": "hack_success",
                    "vibration": [100, 50, 100, 50, 100],
                    "text_effect": "ACCESS GRANTED",
                }
            )
        elif interaction_type == "badge_unlock":
            effects.update(
                {
                    "badge_glow": True,
                    "celebration": True,
                    "confetti": True,
                    "sound": "badge_unlock",
                    "vibration": [150, 100, 150],
                    "screen_flash": True,
                }
            )

        # Intensité selon le contexte
        if context and context.get("intensity") == "high":
            effects.update(
                {
                    "intensity": "high",
                    "duration": 2000,
                    "screen_flash": True,
                    "vibration": [200, 100, 200],
                }
            )
        elif context and context.get("intensity") == "low":
            effects.update(
                {
                    "intensity": "low",
                    "duration": 500,
                    "vibration": [50],
                }
            )
        else:
            effects.update(
                {
                    "intensity": "medium",
                    "duration": 1000,
                }
            )

        return effects

    def check_user_preferences(self, player_id: str, interaction_type: str) -> bool:
        """Vérifie les préférences utilisateur pour une interaction"""
        if player_id not in self.user_preferences:
            return True  # Par défaut, tout est activé

        preferences = self.user_preferences[player_id]

        # Vérifier les préférences globales
        if not preferences.get("interactions_enabled", True):
            return False

        # Vérifier les préférences spécifiques au type
        disabled_types = preferences.get("disabled_interaction_types", [])
        if interaction_type in disabled_types:
            return False

        return True

    def add_to_animation_queue(self, interaction: Dict[str, Any]):
        """Ajoute une interaction à la queue d'animations"""
        if len(self.animation_queue) >= self.max_queue_size:
            self.animation_queue.pop(0)  # Supprimer le plus ancien

        self.animation_queue.append(
            {
                "interaction": interaction,
                "type": "animation",
                "priority": self.get_animation_priority(interaction["type"]),
            }
        )

    def add_to_sound_queue(self, interaction: Dict[str, Any]):
        """Ajoute une interaction à la queue de sons"""
        if len(self.sound_queue) >= self.max_queue_size:
            self.sound_queue.pop(0)

        self.sound_queue.append(
            {
                "interaction": interaction,
                "type": "sound",
                "priority": self.get_sound_priority(interaction["type"]),
            }
        )

    def add_to_notification_queue(self, interaction: Dict[str, Any]):
        """Ajoute une interaction à la queue de notifications"""
        if len(self.notification_queue) >= self.max_queue_size:
            self.notification_queue.pop(0)

        self.notification_queue.append(
            {
                "interaction": interaction,
                "type": "notification",
                "priority": self.get_notification_priority(interaction["type"]),
            }
        )

    def get_animation_priority(self, interaction_type: str) -> int:
        """Retourne la priorité d'animation"""
        priorities = {
            "level_up": 10,
            "badge_earned": 9,
            "mission_complete": 8,
            "success_action": 7,
            "error_action": 6,
            "button_click": 1,
        }
        return priorities.get(interaction_type, 5)

    def get_sound_priority(self, interaction_type: str) -> int:
        """Retourne la priorité de son"""
        priorities = {
            "level_up": 10,
            "badge_earned": 9,
            "mission_complete": 8,
            "success_action": 7,
            "error_action": 6,
            "button_click": 1,
        }
        return priorities.get(interaction_type, 5)

    def get_notification_priority(self, interaction_type: str) -> int:
        """Retourne la priorité de notification"""
        priorities = {
            "level_up": 10,
            "badge_earned": 9,
            "mission_complete": 8,
            "success_action": 7,
            "error_action": 6,
            "button_click": 1,
        }
        return priorities.get(interaction_type, 5)

    # ===== GESTION DES ANIMATIONS =====

    def process_animation_queue(self) -> List[Dict[str, Any]]:
        """Traite la queue d'animations"""
        if not self.animation_queue:
            return []

        # Trier par priorité
        self.animation_queue.sort(key=lambda x: x["priority"], reverse=True)

        # Traiter les animations
        processed_animations = []
        for item in self.animation_queue[:5]:  # Traiter max 5 animations à la fois
            animation_data = self.generate_animation_data(item["interaction"])
            processed_animations.append(animation_data)

        # Vider la queue traitée
        self.animation_queue = self.animation_queue[5:]

        return processed_animations

    def generate_animation_data(self, interaction: Dict[str, Any]) -> Dict[str, Any]:
        """Génère les données d'animation pour une interaction"""
        template = interaction["template"]
        animations = template.get("animations", [])

        animation_data = {
            "interaction_id": interaction["id"],
            "target_element": interaction["target_element"],
            "animations": [],
        }

        for anim in animations:
            animation_data["animations"].append(
                {
                    "element": anim["element"],
                    "animation": anim["animation"],
                    "duration": anim["duration"],
                    "easing": anim["easing"],
                    "params": anim.get("params", {}),
                    "delay": anim.get("delay", 0),
                }
            )

        return animation_data

    # ===== GESTION DES SONS =====

    def process_sound_queue(self) -> List[Dict[str, Any]]:
        """Traite la queue de sons"""
        if not self.sound_queue:
            return []

        # Trier par priorité
        self.sound_queue.sort(key=lambda x: x["priority"], reverse=True)

        # Traiter les sons
        processed_sounds = []
        for item in self.sound_queue[:3]:  # Traiter max 3 sons à la fois
            sound_data = self.generate_sound_data(item["interaction"])
            processed_sounds.append(sound_data)

        # Vider la queue traitée
        self.sound_queue = self.sound_queue[3:]

        return processed_sounds

    def generate_sound_data(self, interaction: Dict[str, Any]) -> Dict[str, Any]:
        """Génère les données de son pour une interaction"""
        template = interaction["template"]
        sounds = template.get("sounds", [])

        sound_data = {"interaction_id": interaction["id"], "sounds": []}

        for sound in sounds:
            sound_data["sounds"].append(
                {
                    "sound": sound["sound"],
                    "volume": sound["volume"] * self.sound_volume,
                    "delay": sound.get("delay", 0),
                    "loop": sound.get("loop", False),
                }
            )

        return sound_data

    # ===== GESTION DES NOTIFICATIONS =====

    def process_notification_queue(self) -> List[Dict[str, Any]]:
        """Traite la queue de notifications"""
        if not self.notification_queue:
            return []

        # Trier par priorité
        self.notification_queue.sort(key=lambda x: x["priority"], reverse=True)

        # Traiter les notifications
        processed_notifications = []
        for item in self.notification_queue[
            :2
        ]:  # Traiter max 2 notifications à la fois
            notification_data = self.generate_notification_data(item["interaction"])
            processed_notifications.append(notification_data)

        # Vider la queue traitée
        self.notification_queue = self.notification_queue[2:]

        return processed_notifications

    def generate_notification_data(self, interaction: Dict[str, Any]) -> Dict[str, Any]:
        """Génère les données de notification pour une interaction"""
        template = interaction["template"]
        notifications = template.get("notifications", [])

        notification_data = {"interaction_id": interaction["id"], "notifications": []}

        for notif in notifications:
            notification_data["notifications"].append(
                {
                    "type": notif["type"],
                    "title": notif.get("title", ""),
                    "message": notif["message"],
                    "duration": notif["duration"],
                    "position": notif.get("position", "top-right"),
                    "style": notif.get("style", "default"),
                    "delay": notif.get("delay", 0),
                }
            )

        return notification_data

    # ===== GESTION DES PRÉFÉRENCES =====

    def update_user_preferences(
        self, player_id: str, preferences: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Met à jour les préférences d'un utilisateur"""
        if player_id not in self.user_preferences:
            self.user_preferences[player_id] = {}

        self.user_preferences[player_id].update(preferences)
        self.save_interaction_data()

        return {"success": True, "message": "Préférences mises à jour !"}

    def get_user_preferences(self, player_id: str) -> Dict[str, Any]:
        """Retourne les préférences d'un utilisateur"""
        if player_id not in self.user_preferences:
            # Créer des préférences par défaut
            self.user_preferences[player_id] = {
                "interactions_enabled": True,
                "disabled_interaction_types": [],
                "animation_intensity": "medium",
                "sound_volume": 0.7,
                "haptic_enabled": True,
                "notifications_enabled": True,
            }
            self.save_interaction_data()

        return self.user_preferences[player_id]

    # ===== INTERACTIONS CONTEXTUELLES =====

    def create_contextual_interaction(
        self, player_id: str, context: str, target_element: str = None
    ) -> Dict[str, Any]:
        """Crée une interaction contextuelle basée sur la situation"""
        contextual_templates = {
            "first_mission": "success_action",
            "level_up": "level_up",
            "badge_earned": "badge_earned",
            "mission_complete": "mission_complete",
            "error_occurred": "error_action",
            "button_click": "button_click",
            "hover_element": "button_click",
            "form_submit": "success_action",
            "data_load": "success_action",
        }

        interaction_type = contextual_templates.get(context, "button_click")

        return self.trigger_interaction(
            player_id, interaction_type, target_element, {"context": context}
        )

    def create_custom_interaction(
        self, player_id: str, interaction_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Crée une interaction personnalisée"""
        interaction_id = str(uuid.uuid4())

        custom_interaction = {
            "id": interaction_id,
            "type": "custom",
            "target_element": interaction_data.get("target_element"),
            "context": interaction_data.get("context", {}),
            "timestamp": datetime.now().isoformat(),
            "template": {
                "animations": interaction_data.get("animations", []),
                "sounds": interaction_data.get("sounds", []),
                "haptic": interaction_data.get("haptic", {}),
                "notifications": interaction_data.get("notifications", []),
            },
        }

        # Ajouter aux queues
        self.add_to_animation_queue(custom_interaction)
        self.add_to_sound_queue(custom_interaction)
        self.add_to_notification_queue(custom_interaction)

        return {
            "success": True,
            "interaction_id": interaction_id,
            "interaction": custom_interaction,
        }

    # ===== SYSTÈME DE FEEDBACK ADAPTATIF =====

    def analyze_user_behavior(self, player_id: str) -> Dict[str, Any]:
        """Analyse le comportement de l'utilisateur pour adapter les interactions"""
        # Cette fonction pourrait analyser les interactions passées
        # et adapter les préférences automatiquement

        behavior_analysis = {
            "preferred_intensity": "medium",
            "interaction_frequency": "normal",
            "sensitivity_to_feedback": "medium",
            "preferred_animation_style": "smooth",
            "sound_preference": "balanced",
        }

        return behavior_analysis

    def adapt_interactions_to_user(self, player_id: str) -> Dict[str, Any]:
        """Adapte les interactions aux préférences de l'utilisateur"""
        behavior = self.analyze_user_behavior(player_id)

        # Adapter les paramètres selon l'analyse
        adapted_preferences = {
            "animation_intensity": behavior["preferred_intensity"],
            "sound_volume": 0.7 if behavior["sound_preference"] == "balanced" else 0.5,
            "haptic_intensity": behavior["sensitivity_to_feedback"],
            "interaction_frequency": behavior["interaction_frequency"],
        }

        self.update_user_preferences(player_id, adapted_preferences)

        return {
            "success": True,
            "adapted_preferences": adapted_preferences,
            "message": "Interactions adaptées à vos préférences !",
        }

    # ===== API PUBLIQUE =====

    def get_interaction_status(self, player_id: str) -> Dict[str, Any]:
        """Retourne le statut des interactions pour un joueur"""
        preferences = self.get_user_preferences(player_id)
        behavior = self.analyze_user_behavior(player_id)

        return {
            "player_id": player_id,
            "preferences": preferences,
            "behavior_analysis": behavior,
            "queue_status": {
                "animations": len(self.animation_queue),
                "sounds": len(self.sound_queue),
                "notifications": len(self.notification_queue),
            },
            "available_interactions": list(self.interaction_templates.keys()),
        }

    def process_all_queues(self) -> Dict[str, Any]:
        """Traite toutes les queues d'interactions"""
        animations = self.process_animation_queue()
        sounds = self.process_sound_queue()
        notifications = self.process_notification_queue()

        return {
            "success": True,
            "processed": {
                "animations": animations,
                "sounds": sounds,
                "notifications": notifications,
            },
            "timestamp": datetime.now().isoformat(),
        }


# Instance globale
micro_interactions = MicroInteractionsEngine()
