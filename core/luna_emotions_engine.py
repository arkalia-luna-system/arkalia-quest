#!/usr/bin/env python3
"""
🌙 LUNA Emotions Engine v4.0 - Moteur d'émotions dynamiques
Système d'émotions ultra-avancé pour LUNA qui réagit en temps réel
"""

import random
from datetime import datetime
from enum import Enum
from typing import Any


class LunaEmotion(Enum):
    """Émotions de LUNA"""

    EXCITED = "excited"  # 😊 Enthousiaste
    WORRIED = "worried"  # 😰 Inquiète
    PROUD = "proud"  # 🥹 Fière
    MYSTERIOUS = "mysterious"  # 🔮 Mystérieuse
    DETERMINED = "determined"  # 💪 Déterminée
    PLAYFUL = "playful"  # 😄 Joueur
    FOCUSED = "focused"  # 🎯 Concentrée
    SURPRISED = "surprised"  # 😲 Surprise
    CALM = "calm"  # 😌 Calme
    ENERGETIC = "energetic"  # ⚡ Énergique


class LunaEmotionsEngine:
    """Moteur d'émotions LUNA ultra-avancé"""

    def __init__(self):
        self.current_emotion = LunaEmotion.CALM
        self.emotion_intensity = 0.5  # 0.0 à 1.0
        self.emotion_history = []
        self.player_relationship = 0.0  # 0.0 à 1.0
        self.context_memory = {}
        self.last_action_time = datetime.now()

        # Phrases d'émotions par type
        self.emotion_phrases = {
            LunaEmotion.EXCITED: [
                "🌙 WOW ! Tu es incroyable !",
                "🌟 C'est fantastique !",
                "✨ Tu me surprends à chaque fois !",
                "🎉 Incroyable performance !",
                "🚀 Tu es en feu aujourd'hui !",
            ],
            LunaEmotion.WORRIED: [
                "😰 Attention, c'est dangereux...",
                "😨 Je suis inquiète pour toi...",
                "😱 Fais attention, il y a des risques...",
                "😰 Sois prudent, s'il te plaît...",
                "😨 J'ai peur que quelque chose ne tourne mal...",
            ],
            LunaEmotion.PROUD: [
                "🥹 Je suis si fière de toi !",
                "💖 Tu as dépassé toutes mes attentes !",
                "🌟 Tu es devenu un vrai hacker !",
                "💪 Je savais que tu pouvais le faire !",
                "🏆 Tu mérites tous ces succès !",
            ],
            LunaEmotion.MYSTERIOUS: [
                "🔮 Il y a quelque chose que je ne peux pas te dire...",
                "🌙 Le temps nous dira la vérité...",
                "✨ Certaines choses sont mieux gardées secrètes...",
                "🔮 Il y a des mystères plus profonds...",
                "🌙 L'avenir réserve des surprises...",
            ],
            LunaEmotion.DETERMINED: [
                "💪 On va y arriver ensemble !",
                "⚡ Rien ne nous arrêtera !",
                "🎯 On a un objectif et on l'atteindra !",
                "💪 Je crois en nous !",
                "⚡ On est plus forts ensemble !",
            ],
            LunaEmotion.PLAYFUL: [
                "😄 Tu veux jouer avec moi ?",
                "🎮 C'est amusant de hacker avec toi !",
                "😊 Tu me fais toujours rire !",
                "🎯 On s'amuse bien, non ?",
                "😄 Tu es mon hacker préféré !",
            ],
            LunaEmotion.FOCUSED: [
                "🎯 Concentrons-nous sur l'objectif...",
                "🔍 Analysons la situation...",
                "🎯 Restons focalisés...",
                "🔍 Chaque détail compte...",
                "🎯 On va résoudre ça ensemble...",
            ],
            LunaEmotion.SURPRISED: [
                "😲 Wow ! Je ne m'attendais pas à ça !",
                "😱 Incroyable ! Comment as-tu fait ?",
                "😲 Tu m'as vraiment surprise !",
                "😱 C'est inattendu mais génial !",
                "😲 Je suis bouche bée !",
            ],
            LunaEmotion.CALM: [
                "😌 Tout va bien se passer...",
                "🌙 Restons calmes et réfléchissons...",
                "😌 On a le temps de bien faire les choses...",
                "🌙 La patience est une vertu...",
                "😌 On va y arriver tranquillement...",
            ],
            LunaEmotion.ENERGETIC: [
                "⚡ Allez, on y va !",
                "🚀 C'est parti pour l'aventure !",
                "⚡ J'ai trop d'énergie !",
                "🚀 On va tout casser !",
                "⚡ Je suis prête pour tout !",
            ],
        }

        # Couleurs d'émotions Émotecno-Oniriques
        self.emotion_colors = {
            LunaEmotion.EXCITED: "#ffbad2",  # Rose souvenir - Excité
            LunaEmotion.WORRIED: "#ae91f8",  # Violet brumeux - Inquiet
            LunaEmotion.PROUD: "#ffd39f",  # Reflets or pâle - Fier
            LunaEmotion.MYSTERIOUS: "#ae91f8",  # Violet brumeux - Mystérieux
            LunaEmotion.DETERMINED: "#ffbad2",  # Rose souvenir - Déterminé
            LunaEmotion.PLAYFUL: "#ffd39f",  # Reflets or pâle - Joueur
            LunaEmotion.FOCUSED: "#b3d6ff",  # Bleu pâle éthéré - Concentré
            LunaEmotion.SURPRISED: "#ffbad2",  # Rose souvenir - Surpris
            LunaEmotion.CALM: "#b3d6ff",  # Bleu pâle éthéré - Calme
            LunaEmotion.ENERGETIC: "#ffd39f",  # Reflets or pâle - Énergique
        }

        # Effets visuels par émotion
        self.emotion_effects = {
            LunaEmotion.EXCITED: "pulse_green",
            LunaEmotion.WORRIED: "shake_orange",
            LunaEmotion.PROUD: "sparkle_magenta",
            LunaEmotion.MYSTERIOUS: "fade_cyan",
            LunaEmotion.DETERMINED: "glow_red",
            LunaEmotion.PLAYFUL: "bounce_yellow",
            LunaEmotion.FOCUSED: "zoom_blue",
            LunaEmotion.SURPRISED: "flash_pink",
            LunaEmotion.CALM: "float_lightblue",
            LunaEmotion.ENERGETIC: "vibrate_green",
        }

        # Sons par émotion
        self.emotion_sounds = {
            LunaEmotion.EXCITED: "luna_excited",
            LunaEmotion.WORRIED: "luna_worried",
            LunaEmotion.PROUD: "luna_proud",
            LunaEmotion.MYSTERIOUS: "luna_mysterious",
            LunaEmotion.DETERMINED: "luna_determined",
            LunaEmotion.PLAYFUL: "luna_playful",
            LunaEmotion.FOCUSED: "luna_focused",
            LunaEmotion.SURPRISED: "luna_surprised",
            LunaEmotion.CALM: "luna_calm",
            LunaEmotion.ENERGETIC: "luna_energetic",
        }

    def analyze_action(self, action: str, result: dict, profile: dict) -> dict:
        """
        Analyse une action et détermine l'émotion de LUNA

        Args:
            action: Commande exécutée
            result: Résultat de l'action
            profile: Profil du joueur

        Returns:
            Dict avec émotion, message, couleurs, effets
        """
        # Analyser le contexte
        context = self._analyze_context(action, result, profile)

        # Déterminer l'émotion
        emotion = self._determine_emotion(context)

        # Calculer l'intensité
        intensity = self._calculate_intensity(context)

        # Générer le message
        message = self._generate_message(emotion, context)

        # Mettre à jour l'état
        self._update_state(emotion, intensity, context)

        return {
            "emotion": emotion.value,
            "message": message,
            "color": self.emotion_colors[emotion],
            "effect": self.emotion_effects[emotion],
            "sound": self.emotion_sounds[emotion],
            "intensity": intensity,
            "relationship_change": context.get("relationship_change", 0.0),
            "context": context,
        }

    def _analyze_context(self, action: str, result: dict, profile: dict) -> dict:
        """Analyse le contexte de l'action"""
        # Extraire les informations du profil
        personality = profile.get("personnalite", {})
        player_type = personality.get("type", "debutant")

        context = {
            "action_type": self._classify_action(action),
            "success": result.get("réussite", False),
            "score_gained": result.get("score_gagne", 0),
            "badge_gained": result.get("badge"),
            "player_level": profile.get("level", 1),
            "player_score": profile.get("score", 0),
            "player_badges": profile.get("badges", []),
            "player_type": player_type,
            "time_of_day": datetime.now().hour,
            "action_frequency": self._get_action_frequency(action),
            "relationship_change": 0.0,
        }

        # Analyser le type d'action
        if context["action_type"] == "success":
            context["relationship_change"] = 0.1
        elif context["action_type"] == "failure":
            context["relationship_change"] = -0.05
        elif context["action_type"] == "exploration":
            context["relationship_change"] = 0.05
        elif context["action_type"] == "hacking":
            context["relationship_change"] = 0.15

        return context

    def _classify_action(self, action: str) -> str:
        """Classe le type d'action"""
        success_actions = ["hack_system", "kill_virus", "find_shadow", "challenge_corp"]
        failure_actions = ["commande_inexistante", "error", "fail"]
        exploration_actions = ["aide", "profil", "monde", "badges"]
        hacking_actions = ["hack", "decode", "crack", "break"]

        action_lower = action.lower()

        if any(success in action_lower for success in success_actions):
            return "success"
        if any(failure in action_lower for failure in failure_actions):
            return "failure"
        if any(exploration in action_lower for exploration in exploration_actions):
            return "exploration"
        if any(hacking in action_lower for hacking in hacking_actions):
            return "hacking"
        return "general"

    def _determine_emotion(self, context: dict) -> LunaEmotion:
        """Détermine l'émotion de LUNA selon le contexte avec logique avancée"""
        action_type = context["action_type"]
        success = context["success"]
        time_of_day = context["time_of_day"]
        score_gained = context["score_gained"]
        player_level = context["player_level"]
        action_frequency = context["action_frequency"]

        # Facteurs de profil joueur
        player_type = context.get("player_type", "debutant")

        # Facteurs de variabilité
        mood_factor = random.random()
        time_factor = (time_of_day - 12) / 12  # -1 à +1 selon l'heure
        level_factor = min(player_level / 10, 1.0)  # 0 à 1 selon le niveau

        # Facteur de personnalité
        personality_factor = 0.5
        if player_type == "expert":
            personality_factor = 0.8
        elif player_type == "hacker":
            personality_factor = 0.7
        elif player_type == "debutant":
            personality_factor = 0.3

        # Logique d'émotions avancée avec plus de variété basée sur le profil
        if action_type == "success" and success:
            if score_gained > 100:
                emotions = [
                    LunaEmotion.EXCITED,
                    LunaEmotion.PROUD,
                    LunaEmotion.SURPRISED,
                ]
                # Les experts sont plus déterminés
                if player_type == "expert":
                    emotions.extend([LunaEmotion.DETERMINED, LunaEmotion.FOCUSED])
                # Les débutants sont plus surpris
                elif player_type == "debutant":
                    emotions.extend([LunaEmotion.SURPRISED, LunaEmotion.EXCITED])
            elif score_gained > 50:
                emotions = [
                    LunaEmotion.PROUD,
                    LunaEmotion.EXCITED,
                    LunaEmotion.DETERMINED,
                ]
                # Adaptation selon le type de joueur
                if player_type == "hacker":
                    emotions.extend([LunaEmotion.FOCUSED, LunaEmotion.ENERGETIC])
            else:
                emotions = [LunaEmotion.CALM, LunaEmotion.FOCUSED, LunaEmotion.PLAYFUL]
                # Les débutants restent plus calmes
                if player_type == "debutant":
                    emotions = [LunaEmotion.CALM, LunaEmotion.PLAYFUL]

            # Ajouter de la variabilité selon l'heure, le niveau et la personnalité
            if mood_factor > 0.7:
                emotions.extend([LunaEmotion.ENERGETIC, LunaEmotion.MYSTERIOUS])
            if time_factor > 0.5:
                emotions.append(LunaEmotion.ENERGETIC)
            if level_factor > 0.5:
                emotions.append(LunaEmotion.PROUD)
            # Variabilité selon la personnalité
            if personality_factor > 0.7:
                emotions.append(LunaEmotion.DETERMINED)
            elif personality_factor < 0.4:
                emotions.append(LunaEmotion.CALM)

        elif action_type == "failure" or not success:
            if action_frequency > 3:  # Échecs répétés
                emotions = [
                    LunaEmotion.WORRIED,
                    LunaEmotion.CALM,
                    LunaEmotion.DETERMINED,
                ]
            else:
                emotions = [
                    LunaEmotion.CALM,
                    LunaEmotion.FOCUSED,
                    LunaEmotion.MYSTERIOUS,
                ]

        elif action_type == "hacking":
            base_emotions = [
                LunaEmotion.DETERMINED,
                LunaEmotion.FOCUSED,
                LunaEmotion.ENERGETIC,
            ]
            if mood_factor > 0.6:
                base_emotions.extend([LunaEmotion.EXCITED, LunaEmotion.SURPRISED])
            if time_factor < -0.3:  # Nuit
                base_emotions.append(LunaEmotion.MYSTERIOUS)
            emotions = base_emotions

        elif action_type == "exploration":
            base_emotions = [
                LunaEmotion.PLAYFUL,
                LunaEmotion.CALM,
                LunaEmotion.MYSTERIOUS,
            ]
            if mood_factor > 0.5:
                base_emotions.extend([LunaEmotion.SURPRISED, LunaEmotion.ENERGETIC])
            emotions = base_emotions

        elif time_of_day < 6 or time_of_day > 22:
            emotions = [LunaEmotion.MYSTERIOUS, LunaEmotion.CALM]
        elif time_of_day < 12:
            emotions = [
                LunaEmotion.ENERGETIC,
                LunaEmotion.EXCITED,
                LunaEmotion.FOCUSED,
            ]
        else:
            emotions = [LunaEmotion.CALM, LunaEmotion.FOCUSED, LunaEmotion.PLAYFUL]

        # Créer une variété d'émotions basée sur le contexte
        emotions = self._create_emotional_variety(emotions, context)

        # Ajouter de la variabilité aléatoire et contextuelle
        if random.random() < 0.15:  # 15% de chance d'émotion surprise
            all_emotions = list(LunaEmotion)
            emotions.extend(random.sample(all_emotions, 2))

        # Facteur de fatigue/ennui pour les actions répétitives
        if action_frequency > 5:
            emotions.extend([LunaEmotion.CALM, LunaEmotion.MYSTERIOUS])

        # Facteur de nouveauté pour les actions rares
        if action_frequency == 0:
            emotions.extend([LunaEmotion.EXCITED, LunaEmotion.SURPRISED])

        # Facteur de progression du joueur
        if player_level > 8:
            emotions.extend([LunaEmotion.PROUD, LunaEmotion.DETERMINED])

        return random.choice(emotions)

    def _calculate_intensity(self, context: dict) -> float:
        """Calcule l'intensité de l'émotion avec plus de variabilité"""
        base_intensity = 0.5

        # Facteurs d'intensité dynamiques basés sur le score
        score_gained = context["score_gained"]
        if score_gained > 500:
            base_intensity += 0.5
        elif score_gained > 100:
            base_intensity += 0.4
        elif score_gained > 50:
            base_intensity += 0.3
        elif score_gained > 20:
            base_intensity += 0.2
        elif score_gained > 0:
            base_intensity += 0.1
        else:
            base_intensity -= 0.1  # Actions sans score = moins intense

        if context["badge_gained"]:
            base_intensity += 0.25

        if context["action_type"] == "hacking":
            base_intensity += 0.3
        elif context["action_type"] == "success":
            base_intensity += 0.2
        elif context["action_type"] == "failure":
            base_intensity -= 0.1

        # Facteurs temporels et contextuels
        time_of_day = context["time_of_day"]
        if 6 <= time_of_day <= 10:  # Matin énergique
            base_intensity += 0.15
        elif time_of_day >= 22 or time_of_day <= 2:  # Nuit mystérieuse
            base_intensity -= 0.1

        # Facteur de niveau du joueur
        player_level = context["player_level"]
        if player_level > 5:
            base_intensity += 0.1

        # Ajouter de la variabilité aléatoire réduite pour maintenir la progression
        random_factor = (random.random() - 0.5) * 0.1  # ±0.05 (réduit pour les tests)
        base_intensity += random_factor

        # Facteur de fatigue pour les actions répétitives
        if context["action_frequency"] > 3:
            base_intensity -= 0.2

        # Facteur de nouveauté pour les actions rares
        if context["action_frequency"] == 0:
            base_intensity += 0.15

        # Facteur de progression du joueur
        if context["player_level"] > 8:
            base_intensity += 0.1

        return min(1.0, max(0.0, base_intensity))

    def _generate_message(self, emotion: LunaEmotion, context: dict) -> str:
        """Génère un message personnalisé selon l'émotion"""
        base_message = random.choice(self.emotion_phrases[emotion])

        # Personnalisation selon le contexte
        if context["score_gained"] > 100:
            base_message += f"\n💎 Tu as gagné {context['score_gained']} points !"
        if context["badge_gained"]:
            base_message += f"\n🏆 Nouveau badge : {context['badge_gained']} !"
        if context["action_type"] == "hacking":
            base_message += "\n💻 Continue comme ça, hacker !"

        return base_message

    def _update_state(self, emotion: LunaEmotion, intensity: float, context: dict):
        """Met à jour l'état de LUNA"""
        self.current_emotion = emotion
        self.emotion_intensity = intensity
        self.player_relationship += context.get("relationship_change", 0.0)
        self.player_relationship = max(0.0, min(1.0, self.player_relationship))

        # Sauvegarder dans l'historique
        self.emotion_history.append(
            {
                "emotion": emotion.value,
                "intensity": intensity,
                "timestamp": datetime.now().isoformat(),
                "context": context,
            },
        )

        # Garder seulement les 50 dernières émotions
        if len(self.emotion_history) > 50:
            self.emotion_history = self.emotion_history[-50:]

    def _get_action_frequency(self, action: str) -> int:
        """Calcule la fréquence d'une action"""
        recent_actions = [h["context"]["action_type"] for h in self.emotion_history[-10:]]
        return recent_actions.count(self._classify_action(action))

    def _create_emotional_variety(
        self, base_emotions: list[LunaEmotion], context: dict,
    ) -> list[LunaEmotion]:
        """Crée une variété d'émotions basée sur le contexte"""
        enhanced_emotions = base_emotions.copy()

        # Ajouter des émotions basées sur l'historique récent
        recent_emotions = [h["emotion"] for h in self.emotion_history[-5:]]
        if recent_emotions:
            # Éviter de répéter la même émotion
            for emotion in LunaEmotion:
                if emotion.value not in recent_emotions and random.random() < 0.3:
                    enhanced_emotions.append(emotion)

        # Ajouter des émotions basées sur le temps
        hour = context["time_of_day"]
        if 6 <= hour <= 9:  # Matin
            enhanced_emotions.extend([LunaEmotion.ENERGETIC, LunaEmotion.FOCUSED])
        elif 12 <= hour <= 14:  # Déjeuner
            enhanced_emotions.extend([LunaEmotion.PLAYFUL, LunaEmotion.CALM])
        elif 18 <= hour <= 20:  # Soirée
            enhanced_emotions.extend([LunaEmotion.MYSTERIOUS, LunaEmotion.PLAYFUL])
        elif hour >= 22 or hour <= 2:  # Nuit
            enhanced_emotions.extend([LunaEmotion.MYSTERIOUS, LunaEmotion.CALM])

        return enhanced_emotions

    def get_current_state(self) -> dict:
        """Retourne l'état actuel de LUNA"""
        return {
            "emotion": self.current_emotion.value,
            "intensity": self.emotion_intensity,
            "relationship": self.player_relationship,
            "color": self.emotion_colors[self.current_emotion],
            "effect": self.emotion_effects[self.current_emotion],
            "sound": self.emotion_sounds[self.current_emotion],
            "matrix_effects": self._generate_matrix_effects(self.current_emotion),
        }

    def _generate_matrix_effects(self, emotion: LunaEmotion) -> dict[str, Any]:
        """Génère des effets Matrix spéciaux selon l'émotion pour les ados"""

        effects = {
            "particles": True,
            "color": "#00ff00",  # Vert Matrix par défaut
            "animation": "matrix_pulse",
            "sound": "matrix_ambient",
            "intensity": "medium",
        }

        # Effets selon l'émotion
        if emotion == LunaEmotion.EXCITED:
            effects.update(
                {
                    "color": "#00ff88",
                    "animation": "matrix_excited",
                    "particles": True,
                    "intensity": "high",
                    "message": "🚀 WOW ! Tu es en feu aujourd'hui !",
                },
            )
        elif emotion == LunaEmotion.PROUD:
            effects.update(
                {
                    "color": "#00ffff",
                    "animation": "matrix_proud",
                    "particles": True,
                    "intensity": "medium",
                    "message": "🌟 Je suis si fière de toi !",
                },
            )
        elif emotion == LunaEmotion.WORRIED:
            effects.update(
                {
                    "color": "#ff8800",
                    "animation": "matrix_worried",
                    "particles": False,
                    "intensity": "low",
                    "message": "💪 Ne lâche pas ! Tu vas y arriver !",
                },
            )
        elif emotion == LunaEmotion.MYSTERIOUS:
            effects.update(
                {
                    "color": "#8800ff",
                    "animation": "matrix_mysterious",
                    "particles": True,
                    "intensity": "medium",
                    "message": "🔮 Il y a des mystères à découvrir...",
                },
            )
        elif emotion == LunaEmotion.DETERMINED:
            effects.update(
                {
                    "color": "#00ff44",
                    "animation": "matrix_determined",
                    "particles": True,
                    "intensity": "high",
                    "message": "⚡ Rien ne nous arrêtera !",
                },
            )

        return effects

    def get_emotion_history(self) -> list[dict]:
        """Retourne l'historique des émotions"""
        return self.emotion_history

    def reset_emotions(self):
        """Réinitialise les émotions de LUNA"""
        self.current_emotion = LunaEmotion.CALM
        self.emotion_intensity = 0.5
        self.player_relationship = 0.0
        self.emotion_history = []
        self.context_memory = {}


# Instance globale
luna_emotions = LunaEmotionsEngine()
