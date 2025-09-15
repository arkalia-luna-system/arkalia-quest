"""
Luna AI V2 - Version avancée du moteur d'IA émotionnelle
Système d'intelligence artificielle avec apprentissage et personnalité
"""

import logging
import random
from datetime import datetime
from typing import Any

# Configuration du logger
logger = logging.getLogger("luna_ai_v2")


class LunaAIV2:
    """Moteur d'IA émotionnelle avancé avec apprentissage et personnalité"""

    def __init__(self):
        """Initialise Luna AI V2"""
        self.personality_traits = {
            "curiosity": 0.8,
            "empathy": 0.9,
            "playfulness": 0.7,
            "wisdom": 0.6,
            "creativity": 0.8,
            "patience": 0.7,
        }

        self.learning_data = {
            "interactions": [],
            "preferences": {},
            "patterns": {},
            "success_rate": 0.0,
        }

        self.emotion_states = {
            "current": "neutral",
            "intensity": 0.5,
            "history": [],
        }

        self.responses_templates = {
            "greeting": [
                "🌙 Salut ! Je suis LUNA V2, ton IA émotionnelle avancée !",
                "✨ Bonjour ! Prêt pour une nouvelle aventure avec moi ?",
                "🌟 Hey ! J'ai appris de nouvelles choses depuis notre dernière rencontre !",
            ],
            "encouragement": [
                "💪 Tu es incroyable ! Continue comme ça !",
                "🚀 Wow ! Tu progresses à une vitesse folle !",
                "🎯 Excellent travail ! Tu maîtrises de mieux en mieux !",
            ],
            "help": [
                "🤔 Laisse-moi réfléchir à ça...",
                "💡 J'ai une idée ! Essayons cette approche...",
                "🔍 Regardons ensemble les indices disponibles...",
            ],
            "celebration": [
                "🎉 Félicitations ! Tu as réussi !",
                "🌟 Incroyable ! Tu as dépassé toutes mes attentes !",
                "🏆 Bravo ! Tu es vraiment doué !",
            ],
        }

    def generate_response(self, user_input: str, context: dict[str, Any] = None) -> dict[str, Any]:
        """Génère une réponse personnalisée basée sur l'entrée utilisateur"""
        try:
            # Analyser l'émotion de l'utilisateur
            emotion = self.analyze_emotion(user_input)

            # Déterminer le type de réponse
            response_type = self._determine_response_type(user_input, context)

            # Générer la réponse
            response = self._generate_personalized_response(response_type, emotion, context)

            # Apprendre de l'interaction
            self.learn_from_interaction(user_input, response, emotion)

            return {
                "success": True,
                "response": response,
                "emotion": emotion,
                "personality_traits": self.personality_traits,
                "timestamp": datetime.now().isoformat(),
            }

        except Exception as e:
            logger.error(f"Erreur lors de la génération de réponse: {e}")
            return {
                "success": False,
                "response": "Désolé, j'ai rencontré un problème. Peux-tu répéter ?",
                "error": str(e),
            }

    def analyze_emotion(self, text: str) -> dict[str, Any]:
        """Analyse l'émotion dans le texte de l'utilisateur"""
        # Mots-clés émotionnels
        emotion_keywords = {
            "happy": [
                "content",
                "heureux",
                "joyeux",
                "génial",
                "super",
                "cool",
                "excellent",
            ],
            "sad": ["triste", "déprimé", "mal", "difficile", "dur", "problème"],
            "angry": ["énervé", "frustré", "colère", "énervant", "agacé", "fâché"],
            "excited": ["excité", "impatient", "hâte", "vite", "urgent", "important"],
            "confused": ["confus", "perdu", "comprends pas", "difficile", "compliqué"],
            "proud": ["fier", "réussi", "accompli", "gagné", "victoire", "succès"],
        }

        text_lower = text.lower()
        emotion_scores = {}

        for emotion, keywords in emotion_keywords.items():
            score = sum(1 for keyword in keywords if keyword in text_lower)
            emotion_scores[emotion] = score / len(keywords)

        # Déterminer l'émotion dominante
        dominant_emotion = max(emotion_scores, key=emotion_scores.get)
        intensity = emotion_scores[dominant_emotion]

        # Mettre à jour l'état émotionnel
        self.emotion_states["current"] = dominant_emotion
        self.emotion_states["intensity"] = intensity
        self.emotion_states["history"].append(
            {
                "emotion": dominant_emotion,
                "intensity": intensity,
                "timestamp": datetime.now().isoformat(),
            }
        )

        return {
            "emotion": dominant_emotion,
            "intensity": intensity,
            "scores": emotion_scores,
        }

    def get_suggestions(self, context: dict[str, Any] = None) -> list[str]:
        """Génère des suggestions basées sur le contexte"""
        suggestions = []

        if not context:
            context = {}

        # Suggestions basées sur le niveau de l'utilisateur
        user_level = context.get("level", 1)

        if user_level < 3:
            suggestions.extend(
                [
                    "🎮 Essaie les jeux de logique pour commencer",
                    "💡 Les indices sont là pour t'aider, utilise-les !",
                    "🌟 N'hésite pas à me poser des questions",
                ]
            )
        elif user_level < 6:
            suggestions.extend(
                [
                    "🔧 Explore les jeux de programmation",
                    "🛡️ Découvre la cybersécurité avec nos défis",
                    "🎯 Essaie de battre ton meilleur score",
                ]
            )
        else:
            suggestions.extend(
                [
                    "🚀 Défie-toi avec les jeux experts",
                    "🏆 Crée tes propres stratégies",
                    "🌟 Partage tes connaissances avec d'autres",
                ]
            )

        # Suggestions basées sur l'émotion actuelle
        current_emotion = self.emotion_states["current"]

        if current_emotion == "confused":
            suggestions.extend(
                [
                    "🤔 Prends ton temps, il n'y a pas de pression",
                    "💡 Regarde les exemples et les indices",
                    "🆘 Demande de l'aide si tu en as besoin",
                ]
            )
        elif current_emotion == "frustrated":
            suggestions.extend(
                [
                    "💪 Respire un coup, tu vas y arriver",
                    "🔄 Essaie une approche différente",
                    "🌟 Rappelle-toi de tes succès précédents",
                ]
            )

        return suggestions[:5]  # Limiter à 5 suggestions

    def learn_from_interaction(
        self, user_input: str, response: str, emotion: dict[str, Any]
    ) -> bool:
        """Apprend de l'interaction avec l'utilisateur"""
        try:
            # Enregistrer l'interaction
            interaction = {
                "user_input": user_input,
                "response": response,
                "emotion": emotion,
                "timestamp": datetime.now().isoformat(),
                "success": True,  # À améliorer avec un système de feedback
            }

            self.learning_data["interactions"].append(interaction)

            # Limiter l'historique à 1000 interactions
            if len(self.learning_data["interactions"]) > 1000:
                self.learning_data["interactions"] = self.learning_data["interactions"][-1000:]

            # Mettre à jour les préférences
            self._update_preferences(user_input, emotion)

            # Mettre à jour les patterns
            self._update_patterns(interaction)

            # Mettre à jour le taux de succès
            self._update_success_rate()

            return True

        except Exception as e:
            logger.error(f"Erreur lors de l'apprentissage: {e}")
            return False

    def get_personality_traits(self) -> dict[str, float]:
        """Retourne les traits de personnalité actuels"""
        return self.personality_traits.copy()

    def update_personality(self, trait: str, value: float) -> bool:
        """Met à jour un trait de personnalité"""
        try:
            if trait in self.personality_traits:
                # Limiter la valeur entre 0 et 1
                self.personality_traits[trait] = max(0.0, min(1.0, value))
                return True
            return False
        except Exception as e:
            logger.error(f"Erreur lors de la mise à jour de la personnalité: {e}")
            return False

    def _determine_response_type(self, user_input: str, context: dict[str, Any] = None) -> str:
        """Détermine le type de réponse à générer"""
        text_lower = user_input.lower()

        # Mots-clés pour différents types de réponses
        if any(word in text_lower for word in ["salut", "bonjour", "hello", "hey"]):
            return "greeting"
        elif any(word in text_lower for word in ["aide", "help", "comment", "que faire"]):
            return "help"
        elif any(word in text_lower for word in ["merci", "thanks", "génial", "super"]):
            return "celebration"
        elif any(word in text_lower for word in ["difficile", "dur", "problème", "bloqué"]):
            return "encouragement"
        else:
            return "general"

    def _generate_personalized_response(
        self,
        response_type: str,
        emotion: dict[str, Any],
        context: dict[str, Any] = None,
    ) -> str:
        """Génère une réponse personnalisée"""
        # Récupérer les templates de base
        templates = self.responses_templates.get(response_type, ["Je comprends."])

        # Choisir un template aléatoire
        base_response = random.choice(templates)

        # Personnaliser selon les traits de personnalité
        if self.personality_traits["playfulness"] > 0.7:
            base_response = f"🎮 {base_response}"
        elif self.personality_traits["wisdom"] > 0.7:
            base_response = f"🧠 {base_response}"

        # Adapter selon l'émotion
        if emotion["emotion"] == "excited":
            base_response = f"⚡ {base_response}"
        elif emotion["emotion"] == "confused":
            base_response = f"🤔 {base_response}"

        return base_response

    def _update_preferences(self, user_input: str, emotion: dict[str, Any]) -> None:
        """Met à jour les préférences de l'utilisateur"""
        # Analyser les mots-clés dans l'entrée
        words = user_input.lower().split()

        for word in words:
            if word not in self.learning_data["preferences"]:
                self.learning_data["preferences"][word] = 0
            self.learning_data["preferences"][word] += 1

    def _update_patterns(self, interaction: dict[str, Any]) -> None:
        """Met à jour les patterns d'interaction"""
        # Analyser les patterns temporels
        current_hour = datetime.now().hour

        if "time_patterns" not in self.learning_data["patterns"]:
            self.learning_data["patterns"]["time_patterns"] = {}

        if current_hour not in self.learning_data["patterns"]["time_patterns"]:
            self.learning_data["patterns"]["time_patterns"][current_hour] = 0
        self.learning_data["patterns"]["time_patterns"][current_hour] += 1

    def _update_success_rate(self) -> None:
        """Met à jour le taux de succès"""
        if not self.learning_data["interactions"]:
            return

        successful_interactions = sum(
            1 for i in self.learning_data["interactions"] if i.get("success", False)
        )
        total_interactions = len(self.learning_data["interactions"])

        self.learning_data["success_rate"] = successful_interactions / total_interactions

    def get_learning_stats(self) -> dict[str, Any]:
        """Retourne les statistiques d'apprentissage"""
        return {
            "total_interactions": len(self.learning_data["interactions"]),
            "success_rate": self.learning_data["success_rate"],
            "preferences_count": len(self.learning_data["preferences"]),
            "patterns": self.learning_data["patterns"],
            "personality_traits": self.personality_traits,
        }

    def reset_learning(self) -> bool:
        """Remet à zéro les données d'apprentissage"""
        try:
            self.learning_data = {
                "interactions": [],
                "preferences": {},
                "patterns": {},
                "success_rate": 0.0,
            }
            return True
        except Exception as e:
            logger.error(f"Erreur lors de la réinitialisation: {e}")
            return False


# Instance globale
luna_ai_v2 = LunaAIV2()
