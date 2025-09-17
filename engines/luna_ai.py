"""
Compatibilité LunaAI (shim)

Fournit une API simple attendue par les tests historiques en
se basant sur l'implémentation moderne `LunaAIV3`.
"""

from typing import Any

from .luna_ai_v3 import LunaAIV3


class LunaAI:
    """Adaptateur simple vers LunaAIV3 pour compatibilité tests.

    Expose les attributs et méthodes utilisés par tests/test_engines_coverage.py
    : personality, mood, relationship_level, respond(), classify_message(),
      generate_response(context), generate_general_response()
    """

    def __init__(self) -> None:
        self._engine = LunaAIV3()
        # Valeurs par défaut requises par les tests
        self.personality: str = "friendly"
        self.mood: str = "neutral"
        self.relationship_level: int = 0

    def respond(
        self, text: str, user_context: dict[str, Any], game_ctx: dict[str, Any],
    ) -> dict[str, Any]:
        """API historique: renvoie un dict contenant au moins 'message'."""
        result = self._engine.generate_response(text, user_context, game_ctx)
        message = result.get("response") if isinstance(result, dict) else None
        if not isinstance(message, str):
            message = "Je t'écoute. Continuons l'aventure !"
        return {
            "message": message,
            "success": bool(result and result.get("success", True)),
        }

    def classify_message(self, text: str) -> str:
        """Retourne un type de message d'après LUNA V3."""
        context = self._engine._analyze_advanced_context(text, {}, None)
        return str(context.get("message_type", "general"))

    def generate_response(self, context: dict[str, Any]) -> str:  # type: ignore[override]
        """API historique: retourne un texte, basée sur _generate_personalized_response.
        Ici on réutilise respond() avec un input dérivé du contexte.
        """
        text = (
            context.get("prompt", "Salut LUNA !") if isinstance(context, dict) else "Salut LUNA !"
        )
        result = self._engine.generate_response(
            text, {"level": 1}, context if isinstance(context, dict) else None,
        )
        return str(result.get("response", "Prête à t'aider !"))

    def generate_general_response(self) -> str:
        """Réponse générique pour tests d'erreurs."""
        return "LUNA est là pour t'aider. Tape 'aide' pour commencer."
