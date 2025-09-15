#!/usr/bin/env python3
"""
🌐 MOTEUR SOCIAL - ARKALIA QUEST
================================

Système d'interactions sociales et communautaires pour Arkalia Quest.
Gère les guildes, défis coopératifs, chat sécurisé, et événements collectifs.

Auteur: Assistant IA
Version: 1.0
"""

import json
import logging
import os
import uuid
from datetime import datetime, timedelta
from typing import Any, Optional

# Configuration du logging
logger = logging.getLogger(__name__)


class SocialEngine:
    """Moteur social pour les interactions communautaires"""

    def __init__(self):
        self.guilds = {}
        self.challenges = {}
        self.events = {}
        self.chat_messages = []
        self.player_relationships = {}
        self.season_data = {}

        # Configuration
        self.max_chat_messages = 1000
        self.max_guild_size = 50
        self.challenge_cooldown = 3600  # 1 heure

        # Initialiser les données
        self.load_social_data()
        self.init_season_system()

    def load_social_data(self):
        """Charge les données sociales depuis les fichiers"""
        try:
            # Charger les guildes
            guilds_file = os.path.join("data", "guilds.json")
            if os.path.exists(guilds_file):
                with open(guilds_file, encoding="utf-8") as f:
                    self.guilds = json.load(f)

            # Charger les défis
            challenges_file = os.path.join("data", "challenges.json")
            if os.path.exists(challenges_file):
                with open(challenges_file, encoding="utf-8") as f:
                    self.challenges = json.load(f)

            # Charger les événements
            events_file = os.path.join("data", "events.json")
            if os.path.exists(events_file):
                with open(events_file, encoding="utf-8") as f:
                    self.events = json.load(f)

            logger.info("✅ Données sociales chargées")
        except Exception as e:
            logger.error(f"❌ Erreur chargement données sociales: {e}")

    def save_social_data(self):
        """Sauvegarde les données sociales"""
        try:
            os.makedirs("data", exist_ok=True)

            # Sauvegarder les guildes
            with open(os.path.join("data", "guilds.json"), "w", encoding="utf-8") as f:
                json.dump(self.guilds, f, indent=2, ensure_ascii=False)

            # Sauvegarder les défis
            with open(os.path.join("data", "challenges.json"), "w", encoding="utf-8") as f:
                json.dump(self.challenges, f, indent=2, ensure_ascii=False)

            # Sauvegarder les événements
            with open(os.path.join("data", "events.json"), "w", encoding="utf-8") as f:
                json.dump(self.events, f, indent=2, ensure_ascii=False)

            logger.info("✅ Données sociales sauvegardées")
        except Exception as e:
            logger.error(f"❌ Erreur sauvegarde données sociales: {e}")

    def init_season_system(self):
        """Initialise le système de saisons"""
        current_season = self.get_current_season()

        if current_season not in self.season_data:
            self.season_data[current_season] = {
                "start_date": datetime.now().isoformat(),
                "end_date": (datetime.now() + timedelta(days=30)).isoformat(),
                "leaderboard": {},
                "special_badges": [],
                "seasonal_events": [],
                "guild_competitions": {},
            }

            logger.info(f"🌱 Nouvelle saison {current_season} initialisée")

    def get_current_season(self) -> str:
        """Retourne la saison actuelle"""
        now = datetime.now()
        year = now.year
        month = now.month

        if month <= 3:
            return f"Spring_{year}"
        elif month <= 6:
            return f"Summer_{year}"
        elif month <= 9:
            return f"Autumn_{year}"
        else:
            return f"Winter_{year}"

    # ===== SYSTÈME DE GUILDES =====

    def create_guild(
        self, creator_id: str, guild_name: str, description: str = ""
    ) -> dict[str, Any]:
        """Crée une nouvelle guilde"""
        guild_id = str(uuid.uuid4())

        guild = {
            "id": guild_id,
            "name": guild_name,
            "description": description,
            "creator": creator_id,
            "members": [creator_id],
            "officers": [],
            "created_at": datetime.now().isoformat(),
            "level": 1,
            "experience": 0,
            "badges": [],
            "achievements": [],
            "chat_history": [],
            "settings": {"public": True, "auto_accept": False, "min_level": 1},
        }

        self.guilds[guild_id] = guild
        self.save_social_data()

        logger.info(f"🏰 Guilde '{guild_name}' créée par {creator_id}")

        return {
            "success": True,
            "guild": guild,
            "message": f"Guilde '{guild_name}' créée avec succès !",
        }

    def join_guild(self, player_id: str, guild_id: str) -> dict[str, Any]:
        """Rejoint une guilde"""
        if guild_id not in self.guilds:
            return {"success": False, "error": "Guilde introuvable"}

        guild = self.guilds[guild_id]

        if player_id in guild["members"]:
            return {"success": False, "error": "Vous êtes déjà membre de cette guilde"}

        if len(guild["members"]) >= self.max_guild_size:
            return {"success": False, "error": "La guilde est pleine"}

        guild["members"].append(player_id)
        self.save_social_data()

        # Ajouter message de bienvenue
        self.add_guild_message(guild_id, "system", f"🎉 {player_id} a rejoint la guilde !")

        return {
            "success": True,
            "message": f"Bienvenue dans la guilde {guild['name']} !",
        }

    def leave_guild(self, player_id: str, guild_id: str) -> dict[str, Any]:
        """Quitte une guilde"""
        if guild_id not in self.guilds:
            return {"success": False, "error": "Guilde introuvable"}

        guild = self.guilds[guild_id]

        if player_id not in guild["members"]:
            return {"success": False, "error": "Vous n'êtes pas membre de cette guilde"}

        guild["members"].remove(player_id)

        if player_id in guild["officers"]:
            guild["officers"].remove(player_id)

        # Si c'était le créateur, transférer la guilde
        if guild["creator"] == player_id and guild["members"]:
            guild["creator"] = guild["members"][0]
            guild["officers"].append(guild["creator"])

        self.save_social_data()

        return {"success": True, "message": "Vous avez quitté la guilde"}

    def add_guild_message(
        self, guild_id: str, sender: str, message: str, message_type: str = "chat"
    ):
        """Ajoute un message au chat de guilde"""
        if guild_id not in self.guilds:
            return

        guild = self.guilds[guild_id]

        chat_message = {
            "id": str(uuid.uuid4()),
            "sender": sender,
            "message": message,
            "type": message_type,
            "timestamp": datetime.now().isoformat(),
        }

        guild["chat_history"].append(chat_message)

        # Limiter l'historique
        if len(guild["chat_history"]) > 500:
            guild["chat_history"] = guild["chat_history"][-500:]

        self.save_social_data()

    def get_guild_info(self, guild_id: str) -> Optional[dict[str, Any]]:
        """Retourne les informations d'une guilde"""
        return self.guilds.get(guild_id)

    def get_player_guilds(self, player_id: str) -> list[dict[str, Any]]:
        """Retourne les guildes d'un joueur"""
        player_guilds = []

        for guild_id, guild in self.guilds.items():
            if player_id in guild["members"]:
                player_guilds.append(
                    {
                        "id": guild_id,
                        "name": guild["name"],
                        "role": (
                            "creator"
                            if guild["creator"] == player_id
                            else ("officer" if player_id in guild["officers"] else "member")
                        ),
                        "level": guild["level"],
                        "member_count": len(guild["members"]),
                    }
                )

        return player_guilds

    # ===== SYSTÈME DE DÉFIS COOPÉRATIFS =====

    def create_coop_challenge(
        self, creator_id: str, challenge_data: dict[str, Any]
    ) -> dict[str, Any]:
        """Crée un défi coopératif"""
        challenge_id = str(uuid.uuid4())

        challenge = {
            "id": challenge_id,
            "creator": creator_id,
            "title": challenge_data.get("title", "Défi Coopératif"),
            "description": challenge_data.get("description", ""),
            "type": challenge_data.get("type", "mission"),
            "difficulty": challenge_data.get("difficulty", "medium"),
            "max_participants": challenge_data.get("max_participants", 4),
            "participants": [creator_id],
            "status": "open",
            "created_at": datetime.now().isoformat(),
            "expires_at": (datetime.now() + timedelta(hours=24)).isoformat(),
            "rewards": challenge_data.get("rewards", {}),
            "progress": {},
            "chat": [],
        }

        self.challenges[challenge_id] = challenge
        self.save_social_data()

        return {
            "success": True,
            "challenge": challenge,
            "message": "Défi coopératif créé !",
        }

    def join_challenge(self, player_id: str, challenge_id: str) -> dict[str, Any]:
        """Rejoint un défi coopératif"""
        if challenge_id not in self.challenges:
            return {"success": False, "error": "Défi introuvable"}

        challenge = self.challenges[challenge_id]

        if challenge["status"] != "open":
            return {"success": False, "error": "Ce défi n'est plus disponible"}

        if player_id in challenge["participants"]:
            return {"success": False, "error": "Vous participez déjà à ce défi"}

        if len(challenge["participants"]) >= challenge["max_participants"]:
            return {"success": False, "error": "Le défi est complet"}

        challenge["participants"].append(player_id)
        challenge["progress"][player_id] = {"status": "active", "contribution": 0}

        # Message dans le chat du défi
        self.add_challenge_message(challenge_id, "system", f"🎯 {player_id} a rejoint le défi !")

        self.save_social_data()

        return {"success": True, "message": "Vous avez rejoint le défi !"}

    def add_challenge_message(self, challenge_id: str, sender: str, message: str):
        """Ajoute un message au chat du défi"""
        if challenge_id not in self.challenges:
            return

        challenge = self.challenges[challenge_id]

        chat_message = {
            "id": str(uuid.uuid4()),
            "sender": sender,
            "message": message,
            "timestamp": datetime.now().isoformat(),
        }

        challenge["chat"].append(chat_message)

        # Limiter l'historique
        if len(challenge["chat"]) > 200:
            challenge["chat"] = challenge["chat"][-200:]

        self.save_social_data()

    def update_challenge_progress(
        self, challenge_id: str, player_id: str, progress_data: dict[str, Any]
    ) -> dict[str, Any]:
        """Met à jour le progrès d'un joueur dans un défi"""
        if challenge_id not in self.challenges:
            return {"success": False, "error": "Défi introuvable"}

        challenge = self.challenges[challenge_id]

        if player_id not in challenge["participants"]:
            return {"success": False, "error": "Vous ne participez pas à ce défi"}

        if player_id not in challenge["progress"]:
            challenge["progress"][player_id] = {"status": "active", "contribution": 0}

        # Mettre à jour le progrès
        challenge["progress"][player_id].update(progress_data)

        # Vérifier si le défi est terminé
        completed_count = sum(
            1 for p in challenge["progress"].values() if p.get("status") == "completed"
        )

        if completed_count >= len(challenge["participants"]):
            challenge["status"] = "completed"
            self.distribute_challenge_rewards(challenge)

        self.save_social_data()

        return {"success": True, "message": "Progrès mis à jour !"}

    def distribute_challenge_rewards(self, challenge: dict[str, Any]):
        """Distribue les récompenses d'un défi terminé"""
        # rewards = challenge.get("rewards", {})  # TODO: Implémenter la distribution des récompenses

        for participant in challenge["participants"]:
            # Ici, on pourrait intégrer avec le système de gamification
            # pour distribuer les récompenses
            logger.info(
                f"🎁 Récompenses distribuées à {participant} pour le défi {challenge['id']}"
            )

    # ===== SYSTÈME D'ÉVÉNEMENTS COLLECTIFS =====

    def create_seasonal_event(self, event_data: dict[str, Any]) -> dict[str, Any]:
        """Crée un événement saisonnier"""
        event_id = str(uuid.uuid4())
        current_season = self.get_current_season()

        event = {
            "id": event_id,
            "season": current_season,
            "title": event_data.get("title", "Événement Saisonnier"),
            "description": event_data.get("description", ""),
            "type": event_data.get("type", "community"),
            "start_date": datetime.now().isoformat(),
            "end_date": (datetime.now() + timedelta(days=7)).isoformat(),
            "participants": [],
            "global_progress": 0,
            "target": event_data.get("target", 1000),
            "rewards": event_data.get("rewards", {}),
            "leaderboard": {},
            "achievements": event_data.get("achievements", []),
        }

        if current_season not in self.season_data:
            self.season_data[current_season] = {}

        if "seasonal_events" not in self.season_data[current_season]:
            self.season_data[current_season]["seasonal_events"] = []

        self.season_data[current_season]["seasonal_events"].append(event)
        self.save_social_data()

        return {
            "success": True,
            "event": event,
            "message": "Événement saisonnier créé !",
        }

    def join_seasonal_event(self, player_id: str, event_id: str) -> dict[str, Any]:
        """Rejoint un événement saisonnier"""
        current_season = self.get_current_season()

        if current_season not in self.season_data:
            return {"success": False, "error": "Aucune saison active"}

        events = self.season_data[current_season].get("seasonal_events", [])
        event = next((e for e in events if e["id"] == event_id), None)

        if not event:
            return {"success": False, "error": "Événement introuvable"}

        if player_id in event["participants"]:
            return {"success": False, "error": "Vous participez déjà à cet événement"}

        event["participants"].append(player_id)
        event["leaderboard"][player_id] = {"score": 0, "contributions": 0}

        self.save_social_data()

        return {"success": True, "message": "Vous avez rejoint l'événement !"}

    def update_event_progress(
        self, event_id: str, player_id: str, contribution: int
    ) -> dict[str, Any]:
        """Met à jour le progrès d'un joueur dans un événement"""
        current_season = self.get_current_season()

        if current_season not in self.season_data:
            return {"success": False, "error": "Aucune saison active"}

        events = self.season_data[current_season].get("seasonal_events", [])
        event = next((e for e in events if e["id"] == event_id), None)

        if not event:
            return {"success": False, "error": "Événement introuvable"}

        if player_id not in event["participants"]:
            return {"success": False, "error": "Vous ne participez pas à cet événement"}

        # Mettre à jour le score du joueur
        if player_id not in event["leaderboard"]:
            event["leaderboard"][player_id] = {"score": 0, "contributions": 0}

        event["leaderboard"][player_id]["score"] += contribution
        event["leaderboard"][player_id]["contributions"] += 1
        event["global_progress"] += contribution

        # Vérifier si l'objectif global est atteint
        if event["global_progress"] >= event["target"]:
            self.complete_seasonal_event(event)

        self.save_social_data()

        return {
            "success": True,
            "message": "Progrès mis à jour !",
            "global_progress": event["global_progress"],
            "target": event["target"],
        }

    def complete_seasonal_event(self, event: dict[str, Any]):
        """Marque un événement comme terminé et distribue les récompenses"""
        event["status"] = "completed"
        event["completed_at"] = datetime.now().isoformat()

        # Distribuer les récompenses
        logger.info(f"🎉 Événement {event['title']} terminé !")

        # Ici, on pourrait distribuer des récompenses spéciales
        # et des badges saisonniers

    # ===== SYSTÈME DE CHAT SÉCURISÉ =====

    def send_global_message(
        self, sender_id: str, message: str, message_type: str = "chat"
    ) -> dict[str, Any]:
        """Envoie un message dans le chat global"""
        # Validation du message
        if not self.validate_message(message):
            return {"success": False, "error": "Message invalide"}

        chat_message = {
            "id": str(uuid.uuid4()),
            "sender": sender_id,
            "message": message,
            "type": message_type,
            "timestamp": datetime.now().isoformat(),
        }

        self.chat_messages.append(chat_message)

        # Limiter l'historique
        if len(self.chat_messages) > self.max_chat_messages:
            self.chat_messages = self.chat_messages[-self.max_chat_messages :]

        self.save_social_data()

        return {"success": True, "message": "Message envoyé !"}

    def validate_message(self, message: str) -> bool:
        """Valide un message (anti-spam, contenu inapproprié, etc.)"""
        if not message or len(message.strip()) == 0:
            return False

        if len(message) > 500:
            return False

        # Liste de mots interdits (à étendre)
        forbidden_words = ["spam", "hack", "cheat", "exploit"]

        message_lower = message.lower()
        for word in forbidden_words:
            if word in message_lower:
                return False

        return True

    def get_recent_messages(self, limit: int = 50) -> list[dict[str, Any]]:
        """Retourne les messages récents"""
        return self.chat_messages[-limit:] if self.chat_messages else []

    # ===== SYSTÈME DE RELATIONS =====

    def add_friend(self, player_id: str, friend_id: str) -> dict[str, Any]:
        """Ajoute un ami"""
        if player_id not in self.player_relationships:
            self.player_relationships[player_id] = {
                "friends": [],
                "blocked": [],
                "rivals": [],
            }

        if friend_id not in self.player_relationships[player_id]["friends"]:
            self.player_relationships[player_id]["friends"].append(friend_id)
            self.save_social_data()

            return {"success": True, "message": f"{friend_id} ajouté comme ami !"}

        return {"success": False, "error": "Déjà ami avec ce joueur"}

    def add_rival(self, player_id: str, rival_id: str) -> dict[str, Any]:
        """Ajoute un rival"""
        if player_id not in self.player_relationships:
            self.player_relationships[player_id] = {
                "friends": [],
                "blocked": [],
                "rivals": [],
            }

        if rival_id not in self.player_relationships[player_id]["rivals"]:
            self.player_relationships[player_id]["rivals"].append(rival_id)
            self.save_social_data()

            return {"success": True, "message": f"{rival_id} ajouté comme rival !"}

        return {"success": False, "error": "Déjà rival avec ce joueur"}

    def get_player_relationships(self, player_id: str) -> dict[str, Any]:
        """Retourne les relations d'un joueur"""
        return self.player_relationships.get(
            player_id, {"friends": [], "blocked": [], "rivals": []}
        )

    # ===== API PUBLIQUE =====

    def get_social_dashboard(self, player_id: str) -> dict[str, Any]:
        """Retourne le tableau de bord social d'un joueur"""
        current_season = self.get_current_season()

        return {
            "player_id": player_id,
            "guilds": self.get_player_guilds(player_id),
            "relationships": self.get_player_relationships(player_id),
            "active_challenges": [
                c
                for c in self.challenges.values()
                if player_id in c["participants"] and c["status"] == "open"
            ],
            "seasonal_events": [
                e
                for e in self.season_data.get(current_season, {}).get("seasonal_events", [])
                if player_id in e["participants"]
            ],
            "recent_messages": self.get_recent_messages(20),
            "current_season": current_season,
        }


# Instance globale
social_engine = SocialEngine()
