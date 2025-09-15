"""
Daily Challenges Engine - Moteur de défis quotidiens
Système de contenu renouvelé quotidiennement pour maintenir l'engagement
"""

import logging
import random
from datetime import datetime, timedelta
from enum import Enum
from typing import Any, Optional

# Configuration du logger
logger = logging.getLogger("daily_challenges")


class ChallengeType(Enum):
    """Types de défis quotidiens"""

    HACKING = "hacking"
    PROGRAMMING = "programming"
    LOGIC = "logic"
    CYBERSECURITY = "cybersecurity"
    EXPLORATION = "exploration"
    SOCIAL = "social"
    CREATIVE = "creative"


class DifficultyLevel(Enum):
    """Niveaux de difficulté"""

    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"
    EXPERT = "expert"


class DailyChallengesEngine:
    """Moteur de défis quotidiens pour Arkalia Quest"""

    def __init__(self):
        self.challenges = {}
        self.challenges_data = {}  # Alias pour compatibilité
        self.user_progress = {}
        self.streak_data = {}
        self.rewards = {}

        # Initialiser les défis
        self._initialize_challenges()
        self._initialize_rewards()

        # Synchroniser challenges_data avec challenges
        self.challenges_data = self.challenges

        logger.info("✅ Moteur de défis quotidiens initialisé")

    def generate_challenge(
        self, challenge_type: str, frequency: str, difficulty: str
    ) -> dict[str, Any]:
        """Génère un défi aléatoire"""
        try:
            # Convertir le type de défi
            type_mapping = {
                "hack": ChallengeType.HACKING,
                "program": ChallengeType.PROGRAMMING,
                "logic": ChallengeType.LOGIC,
                "cybersecurity": ChallengeType.CYBERSECURITY,
                "explore": ChallengeType.EXPLORATION,
                "social": ChallengeType.SOCIAL,
                "creative": ChallengeType.CREATIVE,
            }

            challenge_type_enum = type_mapping.get(
                challenge_type.lower(), ChallengeType.HACKING
            )

            # Convertir la difficulté
            difficulty_mapping = {
                "facile": "easy",
                "moyen": "medium",
                "difficile": "hard",
                "expert": "expert",
            }
            difficulty_key = difficulty_mapping.get(difficulty.lower(), "easy")

            # Récupérer les défis disponibles
            available_challenges = self.challenges.get(challenge_type_enum, {}).get(
                difficulty_key, []
            )

            if not available_challenges:
                # Fallback vers easy si pas de défis pour cette difficulté
                available_challenges = self.challenges.get(challenge_type_enum, {}).get(
                    "easy", []
                )

            if not available_challenges:
                # Défi par défaut
                return {
                    "id": f"{challenge_type}_default_1",
                    "title": f"🎯 Défi {challenge_type.title()}",
                    "description": f"Un défi de {challenge_type} pour toi !",
                    "objective": "Réussir ce défi",
                    "hints": ["Pense différemment", "Utilise ta créativité"],
                    "reward_points": 50,
                    "reward_badge": "Défieur",
                    "time_limit": 300,
                    "attempts_limit": 3,
                    "difficulty": difficulty,
                    "type": challenge_type,
                    "answer": "solution_par_defaut",
                }

            # Sélectionner un défi aléatoire
            challenge = random.choice(available_challenges).copy()
            challenge["difficulty"] = difficulty
            challenge["type"] = challenge_type
            challenge["answer"] = f"solution_{challenge['id']}"

            return challenge

        except Exception as e:
            logger.error(f"Erreur génération défi: {e}")
            return {
                "id": "error_challenge",
                "title": "❌ Erreur",
                "description": "Impossible de générer un défi",
                "objective": "Réessayer plus tard",
                "hints": [],
                "reward_points": 0,
                "reward_badge": "Aucun",
                "time_limit": 0,
                "attempts_limit": 0,
                "difficulty": "easy",
                "type": "error",
                "answer": "error",
            }

    def _initialize_challenges(self):
        """Initialise la base de données des défis"""
        self.challenges = {
            ChallengeType.HACKING: {
                "easy": [
                    {
                        "id": "hack_daily_1",
                        "title": "🔓 Défi Hacking Facile",
                        "description": "Trouve le mot de passe caché dans ce fichier système",
                        "objective": "Décrypter le mot de passe 'ARKALIA2025'",
                        "hints": ["Regarde les commentaires", "Cherche les patterns"],
                        "reward_points": 50,
                        "reward_badge": "Hacker Débutant",
                        "time_limit": 300,  # 5 minutes
                        "attempts_limit": 3,
                    },
                    {
                        "id": "hack_daily_2",
                        "title": "🌐 Scan de Ports",
                        "description": "Scanne les ports ouverts de ce serveur",
                        "objective": "Identifier les ports 22, 80, 443",
                        "hints": ["Utilise nmap", "Ports communs"],
                        "reward_points": 75,
                        "reward_badge": "Scanner",
                        "time_limit": 180,
                        "attempts_limit": 2,
                    },
                ],
                "medium": [
                    {
                        "id": "hack_daily_3",
                        "title": "🛡️ Bypass de Sécurité",
                        "description": "Contourne ce système de sécurité basique",
                        "objective": "Accéder au système sans déclencher l'alarme",
                        "hints": ["Évite les capteurs", "Timing précis"],
                        "reward_points": 150,
                        "reward_badge": "Ninja Hacker",
                        "time_limit": 600,
                        "attempts_limit": 2,
                    }
                ],
                "hard": [
                    {
                        "id": "hack_daily_4",
                        "title": "⚡ Exploit Zero-Day",
                        "description": "Développe un exploit pour cette vulnérabilité",
                        "objective": "Créer un payload fonctionnel",
                        "hints": ["Buffer overflow", "ROP chain"],
                        "reward_points": 300,
                        "reward_badge": "Elite Hacker",
                        "time_limit": 1200,
                        "attempts_limit": 1,
                    }
                ],
            },
            ChallengeType.PROGRAMMING: {
                "easy": [
                    {
                        "id": "code_daily_1",
                        "title": "🐍 Défi Python",
                        "description": "Écris une fonction pour calculer la suite de Fibonacci",
                        "objective": "Implémenter fib(n) efficacement",
                        "hints": ["Récursion", "Mémoisation"],
                        "reward_points": 60,
                        "reward_badge": "Codeur Python",
                        "time_limit": 300,
                        "attempts_limit": 3,
                    }
                ],
                "medium": [
                    {
                        "id": "code_daily_2",
                        "title": "🔧 Debug Avancé",
                        "description": "Corrige ce code JavaScript bugué",
                        "objective": "Rendre le code fonctionnel",
                        "hints": ["Closures", "Hoisting"],
                        "reward_points": 120,
                        "reward_badge": "Debug Master",
                        "time_limit": 450,
                        "attempts_limit": 2,
                    }
                ],
            },
            ChallengeType.LOGIC: {
                "easy": [
                    {
                        "id": "logic_daily_1",
                        "title": "🧩 Puzzle Logique",
                        "description": "Résous ce puzzle de logique mathématique",
                        "objective": "Trouver la valeur de X dans l'équation",
                        "hints": ["Algèbre", "Propriétés"],
                        "reward_points": 40,
                        "reward_badge": "Logique Pure",
                        "time_limit": 240,
                        "attempts_limit": 3,
                    }
                ],
                "medium": [
                    {
                        "id": "logic_daily_2",
                        "title": "🎯 Dédduction Complexe",
                        "description": "Déduis la solution à partir des indices",
                        "objective": "Identifier le coupable",
                        "hints": ["Élimination", "Preuves"],
                        "reward_points": 100,
                        "reward_badge": "Détective",
                        "time_limit": 600,
                        "attempts_limit": 2,
                    }
                ],
            },
            ChallengeType.CYBERSECURITY: {
                "easy": [
                    {
                        "id": "cyber_daily_1",
                        "title": "🔒 Audit de Sécurité",
                        "description": "Identifie les vulnérabilités dans ce code",
                        "objective": "Trouver 3 vulnérabilités",
                        "hints": ["Injection", "XSS", "CSRF"],
                        "reward_points": 80,
                        "reward_badge": "Auditeur",
                        "time_limit": 360,
                        "attempts_limit": 2,
                    }
                ],
                "hard": [
                    {
                        "id": "cyber_daily_2",
                        "title": "🛡️ Incident Response",
                        "description": "Réponds à cette attaque en cours",
                        "objective": "Contenir et éliminer la menace",
                        "hints": ["Isolation", "Analyse", "Récupération"],
                        "reward_points": 250,
                        "reward_badge": "Incident Commander",
                        "time_limit": 900,
                        "attempts_limit": 1,
                    }
                ],
            },
            ChallengeType.EXPLORATION: {
                "easy": [
                    {
                        "id": "explore_daily_1",
                        "title": "🗺️ Exploration Urbaine",
                        "description": "Explore cette zone urbaine virtuelle",
                        "objective": "Trouver 5 objets cachés",
                        "hints": ["Regarde partout", "Interagit avec l'environnement"],
                        "reward_points": 70,
                        "reward_badge": "Explorateur",
                        "time_limit": 480,
                        "attempts_limit": 2,
                    }
                ]
            },
            ChallengeType.SOCIAL: {
                "medium": [
                    {
                        "id": "social_daily_1",
                        "title": "🤝 Défi Collaboratif",
                        "description": "Travaille avec d'autres joueurs",
                        "objective": "Compléter une mission en équipe",
                        "hints": ["Communication", "Coordination"],
                        "reward_points": 150,
                        "reward_badge": "Team Player",
                        "time_limit": 1800,
                        "attempts_limit": 1,
                    }
                ]
            },
            ChallengeType.CREATIVE: {
                "easy": [
                    {
                        "id": "creative_daily_1",
                        "title": "🎨 Création Artistique",
                        "description": "Crée une œuvre d'art numérique",
                        "objective": "Générer un pattern ASCII unique",
                        "hints": ["Symétrie", "Couleurs", "Originalité"],
                        "reward_points": 90,
                        "reward_badge": "Artiste Digital",
                        "time_limit": 600,
                        "attempts_limit": 2,
                    }
                ]
            },
        }

    def _initialize_rewards(self):
        """Initialise le système de récompenses"""
        self.rewards = {
            "daily_completion": {
                "points": 100,
                "badge": "Daily Warrior",
                "streak_bonus": True,
            },
            "weekly_completion": {
                "points": 500,
                "badge": "Weekly Champion",
                "special_reward": "Thème exclusif",
            },
            "monthly_completion": {
                "points": 2000,
                "badge": "Monthly Legend",
                "special_reward": "Avatar légendaire",
            },
            "streak_rewards": {
                3: {"points": 50, "badge": "Streak 3"},
                7: {"points": 150, "badge": "Streak 7"},
                15: {"points": 400, "badge": "Streak 15"},
                30: {"points": 1000, "badge": "Streak 30"},
                100: {"points": 5000, "badge": "Streak Master"},
            },
        }

    def get_daily_challenges(
        self, user_id: str, date: Optional[str] = None
    ) -> dict[str, Any]:
        """Récupère les défis quotidiens pour un utilisateur"""
        if date is None:
            date = datetime.now().strftime("%Y-%m-%d")

        # Vérifier si les défis existent déjà pour cette date
        if date not in self.user_progress:
            self.user_progress[date] = {}

        if user_id not in self.user_progress[date]:
            self.user_progress[date][user_id] = {
                "challenges": self._generate_daily_challenges(user_id, date),
                "completed": [],
                "attempts": {},
                "start_time": datetime.now().isoformat(),
            }

        user_data = self.user_progress[date][user_id]

        return {
            "date": date,
            "user_id": user_id,
            "challenges": user_data["challenges"],
            "completed": user_data["completed"],
            "streak": self._get_user_streak(user_id),
            "total_points": self._calculate_daily_points(user_id, date),
            "time_remaining": self._get_time_remaining(user_data["start_time"]),
        }

    def _generate_daily_challenges(
        self, user_id: str, date: str
    ) -> list[dict[str, Any]]:
        """Génère les défis quotidiens personnalisés"""
        # Utiliser la date comme seed pour la reproductibilité
        random.seed(hash(date + user_id))

        challenges = []

        # Sélectionner 3 défis de difficultés variées
        difficulty_weights = {"easy": 0.5, "medium": 0.3, "hard": 0.2}

        for challenge_type in ChallengeType:
            if random.random() < 0.7:  # 70% de chance d'avoir ce type
                difficulty = random.choices(
                    list(difficulty_weights.keys()),
                    weights=list(difficulty_weights.values()),
                )[0]

                if (
                    challenge_type in self.challenges
                    and difficulty in self.challenges[challenge_type]
                ):
                    available_challenges = self.challenges[challenge_type][difficulty]
                    if available_challenges:
                        challenge = random.choice(available_challenges).copy()
                        challenge["type"] = challenge_type.value
                        challenge["difficulty"] = difficulty
                        challenge["daily_id"] = f"{date}_{challenge['id']}"
                        challenge["answer"] = f"solution_{challenge['id']}"
                        challenges.append(challenge)

        # S'assurer qu'il y a au moins 3 défis
        while len(challenges) < 3:
            challenge_type = random.choice(list(ChallengeType))
            difficulty = "easy"
            if (
                challenge_type in self.challenges
                and difficulty in self.challenges[challenge_type]
            ):
                available_challenges = self.challenges[challenge_type][difficulty]
                if available_challenges:
                    challenge = random.choice(available_challenges).copy()
                    challenge["type"] = challenge_type.value
                    challenge["difficulty"] = difficulty
                    challenge["daily_id"] = f"{date}_{challenge['id']}"
                    challenge["answer"] = f"solution_{challenge['id']}"
                    challenges.append(challenge)

        random.seed()  # Reset seed
        return challenges[:3]  # Maximum 3 défis par jour

    def attempt_challenge(
        self, user_id: str, challenge_id: str, answer: str, date: Optional[str] = None
    ) -> dict[str, Any]:
        """Tente de résoudre un défi quotidien"""
        if date is None:
            date = datetime.now().strftime("%Y-%m-%d")

        if date not in self.user_progress or user_id not in self.user_progress[date]:
            return {
                "success": False,
                "error": "Défis quotidiens non trouvés",
                "points_earned": 0,
            }

        user_data = self.user_progress[date][user_id]

        # Trouver le défi (chercher par id ou daily_id)
        challenge = None
        for c in user_data["challenges"]:
            if c["id"] == challenge_id or c["daily_id"] == challenge_id:
                challenge = c
                break

        if not challenge:
            return {"success": False, "error": "Défi non trouvé", "points_earned": 0}

        # Vérifier les tentatives
        attempts = user_data["attempts"].get(challenge_id, 0)
        if attempts >= challenge["attempts_limit"]:
            return {
                "success": False,
                "error": "Limite de tentatives atteinte",
                "points_earned": 0,
            }

        # Vérifier le temps
        if self._is_time_expired(user_data["start_time"], challenge["time_limit"]):
            return {"success": False, "error": "Temps écoulé", "points_earned": 0}

        # Incrémenter les tentatives
        user_data["attempts"][challenge_id] = attempts + 1

        # Vérifier la réponse (logique simplifiée)
        is_correct = self._check_answer(challenge, answer)

        if is_correct:
            # Marquer comme complété
            if challenge_id not in user_data["completed"]:
                user_data["completed"].append(challenge_id)

            # Calculer les récompenses
            rewards = self._calculate_rewards(challenge, user_id, date)

            # Mettre à jour la série
            self._update_streak(user_id, date)

            return {
                "success": True,
                "correct": True,
                "points_earned": rewards.get("points", 0),
                "message": f"🎉 Excellent ! Tu as résolu le défi ! +{rewards.get('points', 0)} points !",
                "streak": self._get_user_streak(user_id),
                "rewards": rewards,
            }
        else:
            remaining_attempts = challenge["attempts_limit"] - (attempts + 1)
            return {
                "success": True,
                "correct": False,
                "points_earned": 0,
                "message": f"❌ Incorrect. Il te reste {remaining_attempts} tentative(s).",
                "hint": random.choice(challenge.get("hints", ["Essaie encore !"])),
                "remaining_attempts": remaining_attempts,
            }

    def _check_answer(self, challenge: dict[str, Any], answer: str) -> bool:
        """Vérifie si la réponse est correcte (logique simplifiée)"""
        # Dans un vrai système, ceci serait plus sophistiqué
        objective = challenge.get("objective", "").lower()
        answer_lower = answer.lower()

        # Logique de vérification basique
        if "arkalia" in objective and "arkalia" in answer_lower:
            return True
        elif "fibonacci" in objective and any(
            word in answer_lower for word in ["fib", "récursion", "memo"]
        ):
            return True
        elif "vulnérabilité" in objective and any(
            word in answer_lower for word in ["injection", "xss", "csrf"]
        ):
            return True
        elif "port" in objective and any(char.isdigit() for char in answer):
            return True
        else:
            # Vérification par similarité simple
            return len(set(objective.split()) & set(answer_lower.split())) >= 2

    def _calculate_rewards(
        self, challenge: dict[str, Any], user_id: str, date: str
    ) -> dict[str, Any]:
        """Calcule les récompenses pour un défi complété"""
        base_points = challenge.get("reward_points", 50)
        badge = challenge.get("reward_badge", "Daily Warrior")

        # Bonus de série
        streak = self._get_user_streak(user_id)
        streak_bonus = min(streak * 10, 100)  # Maximum 100 points de bonus

        # Bonus de difficulté
        difficulty_bonus = {"easy": 0, "medium": 25, "hard": 50, "expert": 100}.get(
            challenge.get("difficulty", "easy"), 0
        )

        total_points = base_points + streak_bonus + difficulty_bonus

        return {
            "points": total_points,
            "badge": badge,
            "streak_bonus": streak_bonus,
            "difficulty_bonus": difficulty_bonus,
            "base_points": base_points,
        }

    def _get_user_streak(self, user_id: str) -> int:
        """Calcule la série de jours consécutifs"""
        if user_id not in self.streak_data:
            self.streak_data[user_id] = {"current_streak": 0, "last_date": None}

        return self.streak_data[user_id]["current_streak"]

    def _update_streak(self, user_id: str, date: str):
        """Met à jour la série de l'utilisateur"""
        if user_id not in self.streak_data:
            self.streak_data[user_id] = {"current_streak": 0, "last_date": None}

        last_date = self.streak_data[user_id]["last_date"]
        current_date = datetime.strptime(date, "%Y-%m-%d")

        if last_date:
            last_date_obj = datetime.strptime(last_date, "%Y-%m-%d")
            if (current_date - last_date_obj).days == 1:
                # Jour consécutif
                self.streak_data[user_id]["current_streak"] += 1
            elif (current_date - last_date_obj).days > 1:
                # Série brisée
                self.streak_data[user_id]["current_streak"] = 1
        else:
            # Premier jour
            self.streak_data[user_id]["current_streak"] = 1

        self.streak_data[user_id]["last_date"] = date

    def _calculate_daily_points(self, user_id: str, date: str) -> int:
        """Calcule le total de points pour la journée"""
        if date not in self.user_progress or user_id not in self.user_progress[date]:
            return 0

        user_data = self.user_progress[date][user_id]
        total_points = 0

        for challenge_id in user_data["completed"]:
            for challenge in user_data["challenges"]:
                if challenge["daily_id"] == challenge_id:
                    total_points += challenge.get("reward_points", 50)
                    break

        return total_points

    def _get_time_remaining(self, start_time: str) -> int:
        """Calcule le temps restant en secondes"""
        start = datetime.fromisoformat(start_time)
        elapsed = (datetime.now() - start).total_seconds()
        return max(0, 86400 - int(elapsed))  # 24 heures en secondes

    def _is_time_expired(self, start_time: str, time_limit: int) -> bool:
        """Vérifie si le temps est écoulé pour un défi"""
        start = datetime.fromisoformat(start_time)
        elapsed = (datetime.now() - start).total_seconds()
        return elapsed > time_limit

    def get_leaderboard(self, date: Optional[str] = None) -> list[dict[str, Any]]:
        """Retourne le classement des défis quotidiens"""
        if date is None:
            date = datetime.now().strftime("%Y-%m-%d")

        if date not in self.user_progress:
            return []

        leaderboard = []
        for user_id, user_data in self.user_progress[date].items():
            points = self._calculate_daily_points(user_id, date)
            completed = len(user_data["completed"])
            total = len(user_data["challenges"])

            leaderboard.append(
                {
                    "user_id": user_id,
                    "points": points,
                    "completed": completed,
                    "total": total,
                    "completion_rate": completed / total if total > 0 else 0,
                    "streak": self._get_user_streak(user_id),
                }
            )

        # Trier par points décroissants
        leaderboard.sort(key=lambda x: x["points"], reverse=True)
        return leaderboard

    def get_weekly_stats(self, user_id: str) -> dict[str, Any]:
        """Retourne les statistiques hebdomadaires d'un utilisateur"""
        today = datetime.now()
        week_start = today - timedelta(days=today.weekday())

        total_points = 0
        total_completed = 0
        total_challenges = 0
        days_active = 0

        for i in range(7):
            date = (week_start + timedelta(days=i)).strftime("%Y-%m-%d")
            if date in self.user_progress and user_id in self.user_progress[date]:
                user_data = self.user_progress[date][user_id]
                total_points += self._calculate_daily_points(user_id, date)
                total_completed += len(user_data["completed"])
                total_challenges += len(user_data["challenges"])
                days_active += 1

        return {
            "user_id": user_id,
            "week_start": week_start.strftime("%Y-%m-%d"),
            "week_end": (week_start + timedelta(days=6)).strftime("%Y-%m-%d"),
            "total_points": total_points,
            "completed_challenges": total_completed,
            "total_challenges": total_challenges,
            "completion_rate": (
                total_completed / total_challenges if total_challenges > 0 else 0
            ),
            "streak_days": self._get_user_streak(user_id),
            "days_active": days_active,
            "average_daily_points": total_points / 7 if days_active > 0 else 0,
        }
