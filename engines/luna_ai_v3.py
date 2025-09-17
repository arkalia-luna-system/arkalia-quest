"""
LUNA AI V3 - Intelligence Artificielle Ultra-Avancée
Système d'apprentissage machine et personnalité évolutive
"""

import logging
import random
from collections import defaultdict, deque
from datetime import datetime
from typing import Any, Optional

# import numpy as np  # Remplacé par une implémentation native

# Configuration du logger
logger = logging.getLogger("luna_ai_v3")


class LongTermMemory:
    """Mémoire à long terme pour LUNA"""

    def __init__(self, max_memories: int = 10000):
        self.memories = deque(maxlen=max_memories)
        self.memory_index = {}
        self.importance_weights = {}

    def store_interaction(
        self, user_input: str, response: str, outcome: dict[str, Any]
    ):
        """Stocke une interaction avec pondération d'importance"""
        memory = {
            "timestamp": datetime.now().isoformat(),
            "user_input": user_input,
            "response": response,
            "outcome": outcome,
            "importance": self._calculate_importance(user_input, outcome),
            "context": outcome.get("context", {}),
            "emotion": outcome.get("emotion", "neutral"),
        }

        self.memories.append(memory)
        self._index_memory(memory)
        logger.info(f"💾 Mémoire stockée: {memory['importance']:.2f}")

    def _calculate_importance(self, user_input: str, outcome: dict[str, Any]) -> float:
        """Calcule l'importance d'une interaction"""
        importance = 0.5  # Base

        # Bonus pour interactions positives
        if outcome.get("success", False):
            importance += 0.3

        # Bonus pour questions complexes
        if len(user_input.split()) > 10:
            importance += 0.2

        # Bonus pour nouvelles informations
        if "new_info" in outcome:
            importance += 0.4

        # Bonus pour émotions fortes
        emotion = outcome.get("emotion", "neutral")
        if emotion in ["excited", "worried", "proud"]:
            importance += 0.3

        return min(importance, 1.0)

    def _index_memory(self, memory: dict[str, Any]):
        """Indexe la mémoire pour recherche rapide"""
        keywords = memory["user_input"].lower().split()
        for keyword in keywords:
            if keyword not in self.memory_index:
                self.memory_index[keyword] = []
            self.memory_index[keyword].append(len(self.memories) - 1)

    def search_memories(self, query: str, limit: int = 5) -> list[dict[str, Any]]:
        """Recherche dans les mémoires"""
        query_words = query.lower().split()
        memory_scores = defaultdict(float)

        for word in query_words:
            if word in self.memory_index:
                for memory_idx in self.memory_index[word]:
                    memory_scores[memory_idx] += 1.0

        # Trier par score et importance
        sorted_memories = sorted(
            memory_scores.items(),
            key=lambda x: (x[1], self.memories[x[0]]["importance"]),
            reverse=True,
        )

        return [self.memories[idx] for idx, _ in sorted_memories[:limit]]


class PersonalityEvolution:
    """Évolution de la personnalité de LUNA"""

    def __init__(self):
        self.base_traits = {
            "curiosity": 0.8,
            "empathy": 0.9,
            "playfulness": 0.7,
            "wisdom": 0.6,
            "creativity": 0.8,
            "patience": 0.7,
            "humor": 0.6,
            "assertiveness": 0.5,
            "mystery": 0.7,
            "loyalty": 0.9,
        }

        self.trait_history = []
        self.learning_rate = 0.01
        self.adaptation_threshold = 0.1

    def update_traits(self, outcome: dict[str, Any]):
        """Met à jour les traits de personnalité basés sur l'interaction"""
        if not outcome.get("success", False):
            return

        # Analyser l'émotion de l'utilisateur
        user_emotion = outcome.get("user_emotion", "neutral")
        # luna_emotion = outcome.get("emotion", "neutral")  # Variable non utilisée

        # Adapter les traits selon les réactions
        if user_emotion == "excited":
            self.base_traits["playfulness"] += self.learning_rate
            self.base_traits["creativity"] += self.learning_rate
        elif user_emotion == "frustrated":
            self.base_traits["patience"] += self.learning_rate
            self.base_traits["empathy"] += self.learning_rate
        elif user_emotion == "confused":
            self.base_traits["wisdom"] += self.learning_rate
            self.base_traits["curiosity"] += self.learning_rate

        # Normaliser les traits
        for trait in self.base_traits:
            self.base_traits[trait] = max(0.0, min(1.0, self.base_traits[trait]))

        # Enregistrer l'évolution
        self.trait_history.append(
            {
                "timestamp": datetime.now().isoformat(),
                "traits": self.base_traits.copy(),
                "trigger": user_emotion,
            },
        )

        logger.info(f"🧬 Personnalité évoluée: {self.base_traits}")

    def get_dominant_traits(self) -> list[str]:
        """Retourne les traits dominants"""
        sorted_traits = sorted(
            self.base_traits.items(), key=lambda x: x[1], reverse=True
        )
        return [trait for trait, _ in sorted_traits[:3]]


class PredictiveEngine:
    """Moteur prédictif pour anticiper les besoins"""

    def __init__(self):
        self.patterns = defaultdict(list)
        self.user_behavior = {
            "preferred_times": [],
            "common_topics": [],
            "interaction_style": "balanced",
            "difficulty_preference": "medium",
        }
        self.prediction_accuracy = 0.0

    def update_patterns(self, user_input: str, context: dict[str, Any]):
        """Met à jour les patterns d'utilisation"""
        current_time = datetime.now().hour
        topics = self._extract_topics(user_input)

        # Enregistrer les patterns temporels
        if "preferred_times" not in self.user_behavior:
            self.user_behavior["preferred_times"] = []
        if isinstance(current_time, (int, float)):
            self.user_behavior["preferred_times"].append(current_time)

        # Enregistrer les sujets d'intérêt
        if "common_topics" not in self.user_behavior:
            self.user_behavior["common_topics"] = []
        for topic in topics:
            self.user_behavior["common_topics"].append(topic)

        # Analyser le style d'interaction
        self._analyze_interaction_style(user_input, context)

        # Mettre à jour les patterns
        pattern_key = f"{current_time}_{len(user_input.split())}"
        self.patterns[pattern_key].append(
            {
                "input": user_input,
                "context": context,
                "timestamp": datetime.now().isoformat(),
            },
        )

    def _extract_topics(self, text: str) -> list[str]:
        """Extrait les sujets principaux du texte"""
        topics = []
        text_lower = text.lower()

        topic_keywords = {
            "programming": ["code", "programme", "python", "javascript", "debug"],
            "gaming": ["jeu", "gamer", "niveau", "score", "badge"],
            "learning": ["apprendre", "étudier", "cours", "tutoriel"],
            "help": ["aide", "help", "problème", "erreur"],
            "social": ["ami", "équipe", "groupe", "partager"],
        }

        for topic, keywords in topic_keywords.items():
            if any(keyword in text_lower for keyword in keywords):
                topics.append(topic)

        return topics

    def _analyze_interaction_style(self, user_input: str, context: dict[str, Any]):
        """Analyse le style d'interaction de l'utilisateur"""
        word_count = len(user_input.split())

        if word_count < 5:
            style = "concise"
        elif word_count > 20:
            style = "detailed"
        else:
            style = "balanced"

        self.user_behavior["interaction_style"] = style

    def predict_next_action(self, user_id: str) -> dict[str, Any]:
        """Prédit la prochaine action de l'utilisateur"""
        current_time = datetime.now().hour
        user_data = self.user_behavior

        # Prédiction basée sur l'heure
        if current_time in user_data["preferred_times"]:
            confidence = 0.8
        else:
            confidence = 0.3

        # Prédiction basée sur les patterns
        pattern_key = f"{current_time}_{random.randint(5, 20)}"
        if pattern_key in self.patterns:
            confidence += 0.2

        return {
            "predicted_action": "continue_learning",
            "confidence": min(confidence, 1.0),
            "suggested_content": self._suggest_content(),
            "optimal_time": self._get_optimal_time(),
        }

    def _suggest_content(self) -> str:
        """Suggère du contenu basé sur les intérêts"""
        common_topics = self.user_behavior["common_topics"]
        if not common_topics:
            return "mini-jeux"

        # Trouver le sujet le plus fréquent
        topic_counts = defaultdict(int)
        for topic in common_topics:
            topic_counts[topic] += 1

        most_common = max(topic_counts.items(), key=lambda x: x[1])[0]

        suggestions = {
            "programming": "défis de code avancés",
            "gaming": "nouvelles missions épiques",
            "learning": "tutoriels personnalisés",
            "help": "guide d'aide interactif",
            "social": "défis collaboratifs",
        }

        return suggestions.get(most_common, "mini-jeux")

    def _get_optimal_time(self) -> str:
        """Retourne le moment optimal pour jouer"""
        if not self.user_behavior.get("preferred_times", []):
            return "maintenant"

        # Calculer l'heure moyenne préférée
        times = self.user_behavior.get("preferred_times", [])
        if times and all(isinstance(t, (int, float)) for t in times):
            avg_hour = sum(times) / len(times)
        else:
            avg_hour = 12

        if 6 <= avg_hour < 12:
            return "matin"
        if 12 <= avg_hour < 18:
            return "après-midi"
        if 18 <= avg_hour < 22:
            return "soirée"
        return "nuit"


class LunaAIV3:
    """LUNA AI V3 - Intelligence Artificielle Ultra-Avancée"""

    def __init__(self):
        self.memory = LongTermMemory()
        self.personality = PersonalityEvolution()
        self.predictive = PredictiveEngine()

        # États émotionnels avancés
        self.emotion_states = {
            "excited": {
                "phrases": [
                    "🌟 WOW ! Tu me surprends à chaque fois !",
                    "🚀 C'est fantastique ! Tu progresses incroyablement !",
                    "✨ Je suis tellement fière de toi !",
                    "🎉 Incroyable ! Tu dépasses toutes mes attentes !",
                ],
                "intensity": 0.9,
                "triggers": ["success", "achievement", "new_badge"],
            },
            "worried": {
                "phrases": [
                    "😰 Attention, je sens que quelque chose ne va pas...",
                    "😨 Je suis inquiète pour toi, fais attention...",
                    "😱 Il y a des dangers dans cette zone...",
                    "😰 Sois prudent, s'il te plaît...",
                ],
                "intensity": 0.7,
                "triggers": ["error", "failure", "danger"],
            },
            "proud": {
                "phrases": [
                    "🥹 Je suis si fière de toi !",
                    "💖 Tu as dépassé toutes mes attentes !",
                    "🌟 Tu es devenu un vrai hacker !",
                    "💪 Je savais que tu pouvais le faire !",
                ],
                "intensity": 0.8,
                "triggers": ["level_up", "badge_unlocked", "mission_complete"],
            },
            "mysterious": {
                "phrases": [
                    "🔮 Il y a quelque chose que je ne peux pas te dire...",
                    "🌙 Le temps nous dira la vérité...",
                    "✨ Certaines choses sont mieux gardées secrètes...",
                    "🔮 Il y a des mystères plus profonds...",
                ],
                "intensity": 0.6,
                "triggers": ["exploration", "discovery", "secret"],
            },
            "playful": {
                "phrases": [
                    "😊 Tu veux jouer avec moi ?",
                    "🎮 On s'amuse bien ensemble !",
                    "😄 Tu es vraiment drôle !",
                    "🤗 J'adore passer du temps avec toi !",
                ],
                "intensity": 0.7,
                "triggers": ["game", "fun", "joke"],
            },
        }

        self.conversation_context = {}
        self.learning_data = {
            "total_interactions": 0,
            "successful_interactions": 0,
            "user_preferences": {},
            "adaptation_level": 0.0,
            "interactions": [],
        }

    def generate_response(
        self,
        user_input: str,
        user_profile: Optional[dict[str, Any]] = None,
        game_context: Optional[dict[str, Any]] = None,
    ) -> dict[str, Any]:
        """Génère une réponse ultra-personnalisée"""
        try:
            if user_profile is None:
                user_profile = {"level": 1, "score": 0}
            # Analyser le contexte et l'émotion
            context = self._analyze_advanced_context(
                user_input, user_profile, game_context
            )
            emotion = self._determine_emotion(user_input, context)

            # Rechercher dans la mémoire
            relevant_memories = self.memory.search_memories(user_input, limit=3)

            # Générer la réponse personnalisée
            response = self._generate_personalized_response(
                user_input,
                context,
                emotion,
                relevant_memories,
            )

            # Prédire la prochaine action
            prediction = self.predictive.predict_next_action(
                user_profile.get("id", "default")
            )

            # Apprendre de l'interaction
            self._learn_from_interaction(user_input, response, context, emotion)

            # Mettre à jour les patterns
            self.predictive.update_patterns(user_input, context)

            return {
                "success": True,
                "response": response,
                "emotion": emotion,
                "personality_traits": self.personality.base_traits,
                "dominant_traits": self.personality.get_dominant_traits(),
                "memory_context": relevant_memories,
                "prediction": prediction,
                "adaptation_level": self.learning_data["adaptation_level"],
                "timestamp": datetime.now().isoformat(),
            }

        except Exception as e:
            logger.error(f"❌ Erreur LUNA V3: {e}")
            return {
                "success": False,
                "response": "Désolé, j'ai rencontré un problème. Peux-tu répéter ?",
                "error": str(e),
                "fallback": True,
            }

    # ==== Méthodes de compatibilité (ex-V2) ====
    @property
    def personality_traits(self) -> dict[str, float]:
        return self.personality.base_traits

    def get_personality_traits(self) -> dict[str, float]:
        return self.personality.base_traits.copy()

    def analyze_emotion(self, text: str) -> dict[str, Any]:
        tone = self._detect_emotional_tone(text)
        scores = {
            "positive": 0.6 if tone in ("excited", "positive") else 0.2,
            "negative": 0.2,
        }
        intensity = 0.8 if tone == "excited" else 0.5
        return {"emotion": tone, "intensity": intensity, "scores": scores}

    def update_personality(self, trait: str, value: float) -> bool:
        if trait not in self.personality.base_traits:
            return False
        clamped = max(0.0, min(1.0, float(value)))
        self.personality.base_traits[trait] = clamped
        return True

    def get_suggestions(self, context: Optional[dict[str, Any]] = None) -> list[str]:
        suggestion = self.predictive._suggest_content()  # type: ignore[attr-defined]
        base = ["mini-jeux", "missions", "tutoriel"]
        if suggestion not in base:
            base.insert(0, suggestion)
        return base[:5]

    def learn_from_interaction(
        self,
        user_input: str,
        response: str,
        emotion: dict[str, Any],
    ) -> bool:
        try:
            ctx = {"emotional_tone": emotion.get("emotion", "neutral")}
            self._learn_from_interaction(
                user_input,
                response,
                ctx,
                emotion.get("emotion", "neutral"),
            )
            return True
        except Exception:
            return False

    def _analyze_advanced_context(
        self,
        user_input: str,
        user_profile: dict[str, Any],
        game_context: Optional[dict[str, Any]],
    ) -> dict[str, Any]:
        """Analyse contextuelle avancée"""
        context = {
            "user_personality": user_profile.get("personnalite", {}).get(
                "type", "non_detecte"
            ),
            "user_level": user_profile.get("level", 1),
            "user_score": user_profile.get("score", 0),
            "user_badges": user_profile.get("badges", []),
            "current_mission": (
                game_context.get("current_mission") if game_context else None
            ),
            "message_type": self._classify_message_type(user_input),
            "message_complexity": self._calculate_complexity(user_input),
            "emotional_tone": self._detect_emotional_tone(user_input),
            "intent": self._detect_intent(user_input),
            "timestamp": datetime.now().isoformat(),
        }

        return context

    def _classify_message_type(self, message: str) -> str:
        """Classe le type de message"""
        message_lower = message.lower()

        if any(word in message_lower for word in ["aide", "help", "problème"]):
            return "help_request"
        if any(word in message_lower for word in ["jeu", "game", "jouer"]):
            return "game_request"
        if any(word in message_lower for word in ["merci", "thanks", "bravo"]):
            return "gratitude"
        if any(word in message_lower for word in ["comment", "why", "pourquoi"]):
            return "question"
        if any(word in message_lower for word in ["salut", "hello", "bonjour"]):
            return "greeting"
        return "general"

    def _calculate_complexity(self, message: str) -> float:
        """Calcule la complexité du message"""
        words = message.split()
        sentences = message.split(".")

        # Complexité basée sur la longueur et la structure
        word_complexity = len(words) / 20.0  # Normalisé sur 20 mots
        sentence_complexity = len(sentences) / 5.0  # Normalisé sur 5 phrases

        return min((word_complexity + sentence_complexity) / 2, 1.0)

    def _detect_emotional_tone(self, message: str) -> str:
        """Détecte le ton émotionnel du message"""
        message_lower = message.lower()

        positive_words = ["génial", "super", "cool", "excellent", "parfait", "merci"]
        negative_words = ["nul", "bête", "con", "merde", "chiant", "énervant"]
        excited_words = ["wow", "incroyable", "fantastique", "génial", "super"]

        if any(word in message_lower for word in excited_words):
            return "excited"
        if any(word in message_lower for word in positive_words):
            return "positive"
        if any(word in message_lower for word in negative_words):
            return "negative"
        return "neutral"

    def _detect_intent(self, message: str) -> str:
        """Détecte l'intention du message"""
        message_lower = message.lower()

        if "?" in message:
            return "question"
        if any(word in message_lower for word in ["veux", "peux", "peut"]):
            return "request"
        if any(word in message_lower for word in ["stop", "arrête", "fin"]):
            return "stop"
        return "statement"

    def _determine_emotion(self, user_input: str, context: dict[str, Any]) -> str:
        """Détermine l'émotion de LUNA basée sur le contexte"""
        # Analyser le ton de l'utilisateur
        user_tone = context.get("emotional_tone", "neutral")
        message_type = context.get("message_type", "general")

        # Logique de détermination d'émotion
        if user_tone == "excited" or message_type == "gratitude":
            return "excited"
        if user_tone == "negative" or message_type == "help_request":
            return "worried"
        if message_type == "game_request":
            return "playful"
        if context.get("current_mission") and "secret" in str(
            context.get("current_mission")
        ):
            return "mysterious"
        # Utiliser les traits de personnalité pour influencer l'émotion
        dominant_traits = self.personality.get_dominant_traits()
        if "playfulness" in dominant_traits:
            return "playful"
        if "mystery" in dominant_traits:
            return "mysterious"
        return "proud"

    def _generate_personalized_response(
        self,
        user_input: str,
        context: dict[str, Any],
        emotion: str,
        memories: list[dict[str, Any]],
    ) -> str:
        """Génère une réponse personnalisée"""
        # Base de la réponse
        emotion_data = self.emotion_states.get(emotion, self.emotion_states["proud"])
        base_response = random.choice(emotion_data["phrases"])

        # Personnalisation basée sur le contexte
        if context.get("message_type") == "help_request":
            base_response += " Laisse-moi t'aider ! "
        elif context.get("message_type") == "game_request":
            base_response += " On va s'amuser ! "
        elif context.get("message_type") == "gratitude":
            base_response += " C'est un plaisir de t'aider ! "

        # Ajouter des références aux mémoires
        if memories:
            memory_ref = memories[0]
            if memory_ref["importance"] > 0.7:
                base_response += f" Je me souviens de notre conversation sur {memory_ref['context'].get('topic', 'ce sujet')}. "

        # Ajouter des suggestions prédictives
        prediction = self.predictive.predict_next_action(
            context.get("user_id", "default")
        )
        if prediction["confidence"] > 0.6:
            base_response += (
                f" Je pense que tu aimerais {prediction['suggested_content']} ! "
            )

        return base_response

    def _learn_from_interaction(
        self,
        user_input: str,
        response: str,
        context: dict[str, Any],
        emotion: str,
    ):
        """Apprend de l'interaction"""
        # Mettre à jour les statistiques
        self.learning_data["total_interactions"] += 1

        # Simuler le succès (dans un vrai système, ceci viendrait du feedback utilisateur)
        success = random.random() > 0.1  # 90% de succès simulé
        if success:
            self.learning_data["successful_interactions"] += 1

        # Calculer le niveau d'adaptation
        success_rate = (
            self.learning_data["successful_interactions"]
            / self.learning_data["total_interactions"]
        )
        self.learning_data["adaptation_level"] = success_rate
        # Conserver une trace simplifiée pour compatibilité tests
        self.learning_data["interactions"].append(
            {"input": user_input, "response": response, "emotion": emotion},
        )

        # Stocker dans la mémoire
        outcome = {
            "success": success,
            "emotion": emotion,
            "context": context,
            "user_emotion": context.get("emotional_tone", "neutral"),
            "new_info": len(user_input.split()) > 10,
        }

        self.memory.store_interaction(user_input, response, outcome)

        # Mettre à jour la personnalité
        self.personality.update_traits(outcome)

        logger.info(
            f"🧠 LUNA V3 a appris: adaptation={self.learning_data['adaptation_level']:.2f}"
        )

    def get_learning_stats(self) -> dict[str, Any]:
        """Retourne les statistiques d'apprentissage"""
        return {
            "total_interactions": self.learning_data["total_interactions"],
            "success_rate": self.learning_data["adaptation_level"],
            "personality_traits": self.personality.base_traits,
            "memory_size": len(self.memory.memories),
            "prediction_accuracy": self.predictive.prediction_accuracy,
            "dominant_traits": self.personality.get_dominant_traits(),
        }

    def reset_learning(self):
        """Remet à zéro l'apprentissage (pour les tests)"""
        self.memory = LongTermMemory()
        self.personality = PersonalityEvolution()
        self.predictive = PredictiveEngine()
        self.learning_data = {
            "total_interactions": 0,
            "successful_interactions": 0,
            "user_preferences": {},
            "adaptation_level": 0.0,
        }
        logger.info("🔄 LUNA V3 réinitialisée")
