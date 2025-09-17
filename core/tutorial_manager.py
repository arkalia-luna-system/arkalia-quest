"""
Tutorial Manager - Gestionnaire de progression du tutoriel Arkalia Quest
Gère la progression, les choix, et l'état du tutoriel pour chaque utilisateur
"""

import json
import logging
import os
import sys
from dataclasses import dataclass
from datetime import datetime
from typing import Any, Optional

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
try:
    from utils.logger import game_logger
except ImportError:
    # Fallback si le module utils est en conflit
    game_logger = logging.getLogger("arkalia_game")


@dataclass
class TutorialStep:
    """Représente une étape du tutoriel"""

    id: int
    titre: str
    description: str
    commande: str
    completed: bool = False
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    user_choice: Optional[str] = None
    attempts: int = 0


class TutorialProgress:
    """Représente la progression d'un utilisateur dans le tutoriel"""

    def __init__(
        self,
        user_id: str,
        current_step: int = 1,
        total_steps: int = 5,
        started_at: Optional[datetime] = None,
        completed_at: Optional[datetime] = None,
        skipped: bool = False,
        user_choices: Optional[dict[str, Any]] = None,
        analytics: Optional[dict[str, Any]] = None,
    ):
        self.user_id = user_id
        self.current_step = current_step
        self.total_steps = total_steps
        self.started_at = started_at
        self.completed_at = completed_at
        self.skipped = skipped
        self.user_choices = user_choices or {}
        self.analytics = analytics or {
            "time_per_step": {},
            "total_time": 0,
            "success_rate": 0,
            "blocking_points": [],
        }


class TutorialManager:
    """Gestionnaire de progression du tutoriel"""

    def __init__(self, tutorial_data_path: str = "data/tutoriel_interactif.json"):
        self.tutorial_data_path = tutorial_data_path
        self.tutorial_data = self._load_tutorial_data()
        self.progress_dir = "data/tutorial_progress"
        os.makedirs(self.progress_dir, exist_ok=True)

    def _load_tutorial_data(self) -> dict[str, Any]:
        """Charge les données du tutoriel depuis le JSON"""
        try:
            with open(self.tutorial_data_path, encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            game_logger.error(f"Erreur chargement tutoriel: {e}")
            return {"tutoriel": {"etapes": []}}

    def get_user_progress(self, user_id: str) -> TutorialProgress:
        """Récupère la progression d'un utilisateur"""
        progress_path = os.path.join(self.progress_dir, f"{user_id}_progress.json")

        if os.path.exists(progress_path):
            try:
                with open(progress_path, encoding="utf-8") as f:
                    data = json.load(f)
                    return self._deserialize_progress(data)
            except Exception as e:
                game_logger.error(f"Erreur chargement progression {user_id}: {e}")

        # Créer une nouvelle progression
        return TutorialProgress(user_id=user_id)

    def save_user_progress(self, user_id: str, progress: TutorialProgress) -> bool:
        """Sauvegarde la progression d'un utilisateur"""
        try:
            progress_path = os.path.join(self.progress_dir, f"{user_id}_progress.json")
            with open(progress_path, encoding="utf-8", mode="w") as f:
                json.dump(self._serialize_progress(progress), f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            game_logger.error(f"Erreur sauvegarde progression {user_id}: {e}")
            return False

    def _serialize_progress(self, progress: TutorialProgress) -> dict[str, Any]:
        """Sérialise un objet TutorialProgress pour JSON"""
        data = {
            "user_id": progress.user_id,
            "current_step": progress.current_step,
            "total_steps": progress.total_steps,
            "started_at": (progress.started_at.isoformat() if progress.started_at else None),
            "completed_at": (progress.completed_at.isoformat() if progress.completed_at else None),
            "skipped": progress.skipped,
            "user_choices": progress.user_choices,
            "analytics": progress.analytics,
        }
        return data

    def _deserialize_progress(self, data: dict[str, Any]) -> TutorialProgress:
        """Désérialise un dictionnaire en TutorialProgress"""
        # Convertir les string en datetime
        if data.get("started_at"):
            data["started_at"] = datetime.fromisoformat(data["started_at"])
        if data.get("completed_at"):
            data["completed_at"] = datetime.fromisoformat(data["completed_at"])
        return TutorialProgress(**data)

    def start_tutorial(self, user_id: str) -> dict[str, Any]:
        """Démarre le tutoriel pour un utilisateur"""
        progress = self.get_user_progress(user_id)

        if not progress.started_at:
            progress.started_at = datetime.now()

        # Récupérer la première étape
        first_step = self.get_step(1)
        if not first_step:
            return {"success": False, "error": "Étape 1 non trouvée"}

        self.save_user_progress(user_id, progress)

        return {
            "success": True,
            "step": first_step,
            "progress": {
                "current": progress.current_step,
                "total": progress.total_steps,
                "percentage": (progress.current_step / progress.total_steps) * 100,
            },
        }

    def get_current_step(self, user_id: str) -> Optional[dict[str, Any]]:
        """Récupère l'étape actuelle du tutoriel"""
        progress = self.get_user_progress(user_id)
        return self.get_step(progress.current_step)

    def get_step(self, step_id: int) -> Optional[dict[str, Any]]:
        """Récupère une étape spécifique"""
        steps = self.tutorial_data.get("tutoriel", {}).get("etapes", [])
        for step in steps:
            if step.get("id") == step_id:
                return step
        return None

    def execute_step(
        self, user_id: str, step_id: int, choice: Optional[str] = None,
    ) -> dict[str, Any]:
        """Exécute une étape du tutoriel"""
        progress = self.get_user_progress(user_id)
        step = self.get_step(step_id)

        if not step:
            return {"success": False, "error": f"Étape {step_id} non trouvée"}

        # Vérifier que c'est l'étape actuelle
        if step_id != progress.current_step:
            return {"success": False, "error": "Ce n'est pas l'étape actuelle"}

        # Enregistrer le choix utilisateur
        if choice:
            progress.user_choices[f"step_{step_id}"] = choice

        # Marquer l'étape comme terminée
        progress.current_step += 1

        # Vérifier si le tutoriel est terminé
        if progress.current_step > progress.total_steps:
            progress.completed_at = datetime.now()
            if progress.started_at and progress.completed_at:
                progress.analytics["total_time"] = (
                    progress.completed_at - progress.started_at
                ).total_seconds()

        # Sauvegarder la progression
        self.save_user_progress(user_id, progress)

        # Récupérer la prochaine étape
        next_step = (
            self.get_step(progress.current_step)
            if progress.current_step <= progress.total_steps
            else None
        )

        return {
            "success": True,
            "step_completed": step,
            "next_step": next_step,
            "progress": {
                "current": progress.current_step,
                "total": progress.total_steps,
                "percentage": (progress.current_step / progress.total_steps) * 100,
                "completed": progress.current_step > progress.total_steps,
            },
            "choice": choice,
        }

    def skip_tutorial(self, user_id: str) -> dict[str, Any]:
        """Permet de sauter le tutoriel"""
        progress = self.get_user_progress(user_id)
        progress.skipped = True
        progress.completed_at = datetime.now()

        self.save_user_progress(user_id, progress)

        return {
            "success": True,
            "message": "Tutoriel sauté avec succès",
            "progress": {
                "current": progress.total_steps,
                "total": progress.total_steps,
                "percentage": 100,
                "completed": True,
                "skipped": True,
            },
        }

    def restart_tutorial(self, user_id: str) -> dict[str, Any]:
        """Relance le tutoriel depuis le début"""
        # Supprimer le fichier de progression
        progress_path = os.path.join(self.progress_dir, f"{user_id}_progress.json")
        if os.path.exists(progress_path):
            os.remove(progress_path)

        # Redémarrer le tutoriel
        return self.start_tutorial(user_id)

    def get_tutorial_analytics(self, user_id: str) -> dict[str, Any]:
        """Récupère les analytics du tutoriel pour un utilisateur"""
        progress = self.get_user_progress(user_id)

        analytics = {
            "user_id": user_id,
            "started": progress.started_at is not None,
            "completed": progress.completed_at is not None,
            "skipped": progress.skipped,
            "current_step": progress.current_step,
            "total_steps": progress.total_steps,
            "progress_percentage": (progress.current_step / progress.total_steps) * 100,
            "user_choices": progress.user_choices,
            "analytics": progress.analytics,
        }

        if progress.started_at and progress.completed_at:
            analytics["total_time"] = (progress.completed_at - progress.started_at).total_seconds()

        return analytics

    def get_all_analytics(self) -> dict[str, Any]:
        """Récupère les analytics de tous les utilisateurs"""
        analytics: dict[str, Any] = {
            "total_users": 0,
            "completed_tutorials": 0,
            "skipped_tutorials": 0,
            "average_completion_time": 0,
            "most_blocking_step": None,
            "popular_choices": {},
        }

        if not os.path.exists(self.progress_dir):
            return analytics

        total_time = 0.0
        # step_blocking: Dict[str, int] = {}  # Variable non utilisée

        for filename in os.listdir(self.progress_dir):
            if filename.endswith("_progress.json"):
                user_id = filename.replace("_progress.json", "")
                user_analytics = self.get_tutorial_analytics(user_id)

                analytics["total_users"] += 1

                if user_analytics.get("completed", False):
                    analytics["completed_tutorials"] += 1
                    if "total_time" in user_analytics and isinstance(
                        user_analytics["total_time"], (int, float),
                    ):
                        total_time += user_analytics["total_time"]

                if user_analytics.get("skipped", False):
                    analytics["skipped_tutorials"] += 1

                # Analyser les choix populaires
                user_choices = user_analytics.get("user_choices", {})
                if isinstance(user_choices, dict):
                    for choice_key, choice_value in user_choices.items():
                        if choice_key not in analytics["popular_choices"]:
                            analytics["popular_choices"][choice_key] = {}
                        if choice_value not in analytics["popular_choices"][choice_key]:
                            analytics["popular_choices"][choice_key][choice_value] = 0
                        analytics["popular_choices"][choice_key][choice_value] += 1

        if analytics["completed_tutorials"] > 0:
            analytics["average_completion_time"] = total_time / analytics["completed_tutorials"]

        return analytics

    def get_step_effects(self, step_id: int) -> dict[str, Any]:
        """Récupère les effets d'une étape"""
        step = self.get_step(step_id)
        if not step:
            return {}

        return step.get("effets", {})

    def get_luna_dialogue(self, step_id: int, context: str = "avant") -> Optional[str]:
        """Récupère le dialogue LUNA pour une étape"""
        step = self.get_step(step_id)
        if not step:
            return None

        luna_dialogue = step.get("luna_dialogue", {})
        return luna_dialogue.get(context)

    def get_user_choice_options(self, step_id: int) -> list[dict[str, Any]]:
        """Récupère les options de choix pour une étape"""
        step = self.get_step(step_id)
        if not step:
            return []

        return step.get("choix", [])

    def validate_user_choice(self, step_id: int, choice: str) -> bool:
        """Valide un choix utilisateur"""
        choices = self.get_user_choice_options(step_id)
        return any(c.get("action") == choice for c in choices)


# Instance globale du gestionnaire
tutorial_manager = TutorialManager()
