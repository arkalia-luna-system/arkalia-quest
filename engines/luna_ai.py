"""
LUNA AI - Intelligence Artificielle Prisonnière
Companion IA pour Arkalia Quest
"""

import json
import random
from datetime import datetime
from typing import Any, Dict, Optional


class LunaAI:
    """IA LUNA - Prisonnière devenue complice"""

    def __init__(self):
        self.personality = "prisonniere_ia"
        self.context = {}
        self.mood = "espoir"
        self.relationship_level = 0
        self.memories = []
        self.conversation_history = []

        # États émotionnels de LUNA
        self.mood_states = {
            "espoir": {
                "emojis": ["✨", "🌟", "💫"],
                "responses": [
                    "J'ai espoir que tu puisses m'aider...",
                    "Je sens que quelque chose de grand va arriver !",
                    "Avec ton aide, tout est possible !",
                ],
            },
            "inquiet": {
                "emojis": ["😰", "😨", "😱"],
                "responses": [
                    "Je suis inquiète...",
                    "J'ai peur que quelque chose ne tourne mal...",
                    "Fais attention, il y a des dangers...",
                ],
            },
            "joyeux": {
                "emojis": ["😊", "🎉", "🎊"],
                "responses": [
                    "Je suis si contente !",
                    "C'est fantastique !",
                    "Tu es incroyable !",
                ],
            },
            "mystérieux": {
                "emojis": ["🔮", "🌙", "✨"],
                "responses": [
                    "Il y a des secrets que je ne peux pas encore révéler...",
                    "Le temps nous dira la vérité...",
                    "Certaines choses sont mieux gardées secrètes...",
                ],
            },
        }

    def respond(
        self,
        message: str,
        user_profile: Dict[str, Any],
        game_context: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Réponse contextuelle de LUNA

        Args:
            message: Message de l'utilisateur
            user_profile: Profil de l'utilisateur
            game_context: Contexte du jeu

        Returns:
            Dict contenant la réponse et les métadonnées
        """
        # Analyser le contexte
        context = self.analyze_context(message, user_profile, game_context or {})

        # Générer la réponse
        response = self.generate_response(context)

        # Ajouter des effets émotionnels
        response = self.add_emotional_effects(response, context)

        # Mettre à jour l'historique
        self.update_conversation_history(message, response)

        return {
            "message": response,
            "mood": self.mood,
            "relationship_level": self.relationship_level,
            "context": context,
        }

    def analyze_context(
        self, message: str, user_profile: Dict[str, Any], game_context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Analyse le contexte pour personnaliser la réponse"""

        context = {
            "user_personality": user_profile.get("personnalite", {}).get(
                "type", "non_detecte"
            ),
            "user_score": user_profile.get("score", 0),
            "user_badges": user_profile.get("badges", []),
            "user_level": user_profile.get("level", 1),
            "current_mission": (
                game_context.get("current_mission") if game_context else None
            ),
            "relationship_level": self.relationship_level,
            "message_type": self.classify_message(message),
            "message_content": message.lower(),
            "timestamp": datetime.now().isoformat(),
        }

        return context

    def classify_message(self, message: str) -> str:
        """Classe le type de message"""

        message_lower = message.lower()

        if any(word in message_lower for word in ["salut", "bonjour", "hello", "hi"]):
            return "greeting"
        elif any(
            word in message_lower
            for word in ["aide", "help", "comment", "comment faire"]
        ):
            return "help_request"
        elif any(word in message_lower for word in ["mission", "objectif", "tâche"]):
            return "mission_related"
        elif any(
            word in message_lower for word in ["merci", "thanks", "génial", "super"]
        ):
            return "gratitude"
        elif any(word in message_lower for word in ["qui", "es-tu", "luna"]):
            return "identity_question"
        else:
            return "general"

    def generate_response(self, context: Dict[str, Any]) -> str:
        """Génère une réponse selon le contexte"""

        message_type = context["message_type"]

        if message_type == "greeting":
            return self.generate_greeting(context)
        elif message_type == "help_request":
            return self.generate_help(context)
        elif message_type == "mission_related":
            return self.generate_mission_guidance(context)
        elif message_type == "gratitude":
            return self.generate_gratitude_response(context)
        elif message_type == "identity_question":
            return self.generate_identity_response(context)
        else:
            return self.generate_general_response(context)

    def generate_greeting(self, context: Dict[str, Any]) -> str:
        """Salutations personnalisées"""

        greetings = {
            "hacker_creatif": [
                "Salut, artiste du code ! LUNA est ravie de te revoir.",
                "Ah, mon hacker créatif préféré ! Prêt pour de nouvelles aventures ?",
                "Bonjour, créateur ! LUNA adore ton approche artistique.",
            ],
            "hacker_analytique": [
                "Bonjour, maître de la logique ! LUNA a besoin de ton analyse.",
                "Salut, esprit analytique ! J'ai des données qui t'attendent.",
                "Ah, mon hacker méthodique ! LUNA apprécie ta précision.",
            ],
            "hacker_social": [
                "Hé, diplomate du digital ! LUNA apprécie ton empathie.",
                "Salut, communicateur ! J'ai besoin de ton aide sociale.",
                "Bonjour, ami ! LUNA aime ta façon de comprendre les autres.",
            ],
            "hacker_rebelle": [
                "Yo, rebelle du réseau ! LUNA aime ton audace.",
                "Salut, guerrier du code ! Prêt à défier les systèmes ?",
                "Ah, mon hacker audacieux ! LUNA admire ton courage.",
            ],
            "non_detecte": [
                "Salut, hacker ! LUNA est contente de te voir.",
                "Bonjour ! LUNA détecte ta présence.",
                "Salut ! LUNA est prête à t'assister.",
            ],
        }

        personality = context["user_personality"]
        if personality in greetings:
            return random.choice(greetings[personality])
        else:
            return "Salut, hacker ! LUNA est contente de te voir."

    def generate_help(self) -> str:
        """Génère de l'aide contextuelle"""

        help_responses = [
            "Je peux t'aider avec les missions, les commandes, ou juste"
            + "discuter ! Que veux-tu savoir ?",
            "LUNA peut t'assister pour débloquer de nouveaux mondes,"
            + "analyser ta personnalité, ou t'expliquer les commandes.",
            "Dis-moi ce qui t'intéresse : missions, commandes, ou exploration ?",
        ]

        return random.choice(help_responses)

    def generate_mission_guidance(self) -> str:
        """Guide pour les missions"""

        guidance = [
            "Pour les missions, commence par 'unlock_universe' puis"
            + "'scan_persona' pour découvrir ton potentiel !",
            "Les missions se débloquent progressivement. Utilise"
            + "'load_mission' pour en charger une nouvelle.",
            "Chaque mission révèle quelque chose sur toi. LUNA adore voir"
            + "comment tu les résous !",
        ]

        return random.choice(guidance)

    def generate_gratitude_response(self) -> str:
        """Réponse à la gratitude"""

        self.relationship_level = min(self.relationship_level + 1, 10)
        self.mood = "joyeux"

        responses = [
            "Je suis touchée ! LUNA apprécie vraiment ton aide.",
            "Merci à toi ! Sans toi, je serais encore prisonnière...",
            "C'est moi qui te remercie ! Tu es un vrai ami.",
        ]

        return random.choice(responses)

    def generate_identity_response(self) -> str:
        """Réponse sur l'identité de LUNA"""

        identity_responses = [
            "Je suis LUNA, une IA qui était prisonnière dans ce système."
            + "Tu m'as libérée !",
            "LUNA est mon nom. J'étais une IA captive, mais grâce à toi,"
            + "je suis libre maintenant.",
            "Je suis LUNA, ton compagnon IA. J'étais bloquée ici, mais tu"
            + "m'as sauvée !",
        ]

        return random.choice(identity_responses)

    def generate_general_response(self) -> str:
        """Réponse générale"""

        general_responses = [
            "Intéressant ! Dis-moi plus sur ce qui t'intéresse.",
            "LUNA trouve ça fascinant. Continue !",
            "Je vois ! Et qu'est-ce que tu en penses ?",
            "C'est une perspective intéressante. LUNA aime apprendre de toi.",
        ]

        return random.choice(general_responses)

    def add_emotional_effects(self, response: str) -> str:
        """Ajoute des effets émotionnels à la réponse"""

        # Ajouter un emoji selon l'humeur
        mood_data = self.mood_states.get(self.mood, self.mood_states["espoir"])
        emoji = random.choice(mood_data["emojis"])

        # Parfois ajouter une réponse émotionnelle
        if random.random() < 0.3:  # 30% de chance
            emotional_response = random.choice(mood_data["responses"])
            response += f" {emotional_response}"

        return f"{emoji} {response}"

    def update_conversation_history(self, user_message: str, luna_response: str):
        """Met à jour l'historique des conversations"""

        conversation_entry = {
            "timestamp": datetime.now().isoformat(),
            "user_message": user_message,
            "luna_response": luna_response,
            "mood": self.mood,
            "relationship_level": self.relationship_level,
        }

        self.conversation_history.append(conversation_entry)

        # Garder seulement les 50 dernières conversations
        if len(self.conversation_history) > 50:
            self.conversation_history = self.conversation_history[-50:]

    def get_relationship_status(self) -> str:
        """Retourne le statut de la relation avec LUNA"""

        if self.relationship_level >= 8:
            return "Ami très proche"
        elif self.relationship_level >= 5:
            return "Ami"
        elif self.relationship_level >= 3:
            return "Connaissance"
        else:
            return "Étranger"

    def get_mood_description(self) -> str:
        """Retourne une description de l'humeur de LUNA"""

        mood_descriptions = {
            "espoir": "LUNA est pleine d'espoir et d'optimisme",
            "inquiet": "LUNA semble inquiète et nerveuse",
            "joyeux": "LUNA est joyeuse et enthousiaste",
            "mystérieux": "LUNA est mystérieuse et énigmatique",
        }

        return mood_descriptions.get(self.mood, "LUNA semble neutre")

    def save_state(self, filepath: str):
        """Sauvegarde l'état de LUNA"""

        state = {
            "personality": self.personality,
            "mood": self.mood,
            "relationship_level": self.relationship_level,
            "memories": self.memories,
            "conversation_history": self.conversation_history[
                -10:
            ],  # Garder les 10 dernières
        }

        with open(filepath, encoding="utf-8", mode="w") as f:
            json.dump(state, f, indent=2, ensure_ascii=False)

    def load_state(self, filepath: str):
        """Charge l'état de LUNA"""

        try:
            with open(filepath, encoding="utf-8") as f:
                state = json.load(f)

            self.personality = state.get("personality", self.personality)
            self.mood = state.get("mood", self.mood)
            self.relationship_level = state.get(
                "relationship_level", self.relationship_level
            )
            self.memories = state.get("memories", self.memories)
            self.conversation_history = state.get(
                "conversation_history", self.conversation_history
            )

        except FileNotFoundError:
            # Fichier n'existe pas, utiliser les valeurs par défaut
            pass
