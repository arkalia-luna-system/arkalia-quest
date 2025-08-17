"""
Educational Games Engine - Moteur de mini-jeux éducatifs pour Arkalia Quest
Jeux de logique, code et cybersécurité pour apprendre en s'amusant
"""

from datetime import datetime
from enum import Enum
from typing import Any, Dict, List


class GameType(Enum):
    """Types de jeux éducatifs disponibles"""

    LOGIC = "logic"
    CODE = "code"
    CYBERSECURITY = "cybersecurity"
    CRYPTOGRAPHY = "cryptography"
    NETWORK = "network"


class Difficulty(Enum):
    """Niveaux de difficulté"""

    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"
    EXPERT = "expert"


class EducationalGamesEngine:
    """Moteur de mini-jeux éducatifs pour Arkalia Quest"""

    def __init__(self):
        self.games_data = self._load_games_data()
        self.user_progress = {}
        self.game_sessions = {}

    def _load_games_data(self) -> Dict[str, Any]:
        """Charge les données des jeux depuis les fichiers JSON"""
        games = {
            "logic": self._get_logic_games(),
            "code": self._get_code_games(),
            "cybersecurity": self._get_cybersecurity_games(),
            "cryptography": self._get_cryptography_games(),
            "network": self._get_network_games(),
        }
        return games

    def _get_logic_games(self) -> List[Dict[str, Any]]:
        """Jeux de logique et déduction"""
        return [
            {
                "id": "logic_1",
                "title": "🔍 Décrypte le Mot de Passe",
                "description": "Trouve le mot de passe en analysant les indices",
                "type": GameType.LOGIC.value,
                "difficulty": Difficulty.BEGINNER.value,
                "hints": [
                    "Le mot fait 6 lettres",
                    "Il contient 2 voyelles",
                    "C'est un animal",
                    "Il commence par 'C'",
                ],
                "solution": "CHAT",
                "explanation": "C = première lettre, HAT = 3 lettres restantes, animal = CHAT",
                "points": 50,
                "badge": "Déducteur",
            },
            {
                "id": "logic_2",
                "title": "🧩 Puzzle de Portes",
                "description": "Ouvre la bonne porte en suivant la logique",
                "type": GameType.LOGIC.value,
                "difficulty": Difficulty.INTERMEDIATE.value,
                "rules": [
                    "Porte 1 : Ouverte si nombre pair",
                    "Porte 2 : Ouverte si nombre > 10",
                    "Porte 3 : Ouverte si nombre divisible par 3",
                ],
                "numbers": [6, 15, 9, 12, 7],
                "solution": [1, 2, 3],  # Portes 1, 2, 3
                "explanation": "6 (pair), 15 (>10 et divisible par 3), 9 (divisible par 3)",
                "points": 75,
                "badge": "Logique",
            },
        ]

    def _get_code_games(self) -> List[Dict[str, Any]]:
        """Jeux de programmation et code"""
        return [
            {
                "id": "code_1",
                "title": "💻 Débogue le Code",
                "description": "Trouve et corrige l'erreur dans ce code Python",
                "type": GameType.CODE.value,
                "difficulty": Difficulty.BEGINNER.value,
                "code": """
def calculer_moyenne(nombres):
    total = 0
    for nombre in nombres:
        total += nombre
    return total / len(nombres)

# Test
resultat = calculer_moyenne([10, 20, 30])
print("Moyenne:", resultat)
""",
                "error": "Division par zéro si liste vide",
                "solution": "Ajouter une vérification de liste vide",
                "fixed_code": """
def calculer_moyenne(nombres):
    if not nombres:
        return 0
    total = 0
    for nombre in nombres:
        total += nombre
    return total / len(nombres)
""",
                "points": 60,
                "badge": "Débogueur",
            },
            {
                "id": "code_2",
                "title": "🔐 Crée un Hash",
                "description": "Écris une fonction pour créer un hash MD5",
                "type": GameType.CODE.value,
                "difficulty": Difficulty.INTERMEDIATE.value,
                "challenge": "Crée une fonction qui prend une chaîne et retourne son hash MD5",
                "test_input": "hello",
                "expected_output": "5d41402abc4b2a76b9719d911017c592",
                "solution": """
import hashlib

def create_md5_hash(text):
    return hashlib.md5(text.encode()).hexdigest()
""",
                "points": 80,
                "badge": "Codeur",
            },
        ]

    def _get_cybersecurity_games(self) -> List[Dict[str, Any]]:
        """Jeux de cybersécurité"""
        return [
            {
                "id": "cyber_1",
                "title": "🛡️ Détecte l'Attaque",
                "description": "Identifie le type d'attaque dans ces logs",
                "type": GameType.CYBERSECURITY.value,
                "difficulty": Difficulty.BEGINNER.value,
                "logs": [
                    "192.168.1.100 - - [GET /admin HTTP/1.1] 404",
                    "192.168.1.100 - - [GET /admin.php HTTP/1.1] 404",
                    "192.168.1.100 - - [GET /administrator HTTP/1.1] 404",
                    "192.168.1.100 - - [GET /wp-admin HTTP/1.1] 404",
                ],
                "options": [
                    "DDoS",
                    "Brute Force",
                    "Directory Traversal",
                    "SQL Injection",
                ],
                "solution": "Directory Traversal",
                "explanation": "L'attaquant teste différents chemins d'administration",
                "points": 70,
                "badge": "Détective",
            },
            {
                "id": "cyber_2",
                "title": "🔒 Sécurise le Mot de Passe",
                "description": "Choisis le mot de passe le plus sécurisé",
                "type": GameType.CYBERSECURITY.value,
                "difficulty": Difficulty.INTERMEDIATE.value,
                "passwords": [
                    "password123",
                    "P@ssw0rd!",
                    "MyDogName2024",
                    "K9#mN2$pL8@vX",
                ],
                "solution": 3,  # Index du mot de passe le plus sécurisé
                "explanation": "Longueur, complexité, caractères spéciaux, pas d'infos personnelles",
                "points": 65,
                "badge": "Sécurisé",
            },
        ]

    def _get_cryptography_games(self) -> List[Dict[str, Any]]:
        """Jeux de cryptographie"""
        return [
            {
                "id": "crypto_1",
                "title": "🔐 Décode le Message",
                "description": "Décode ce message en Base64",
                "type": GameType.CRYPTOGRAPHY.value,
                "difficulty": Difficulty.BEGINNER.value,
                "encoded_message": "SGVsbG8gQXJraGFsaWE=",
                "solution": "Hello Arkalia",
                "explanation": "Base64 est un encodage, pas un chiffrement",
                "points": 45,
                "badge": "Décodeur",
            },
            {
                "id": "crypto_2",
                "title": "🔄 César Cipher",
                "description": "Décode ce message chiffré avec le code de César (décalage de 3)",
                "type": GameType.CRYPTOGRAPHY.value,
                "difficulty": Difficulty.INTERMEDIATE.value,
                "encrypted": "KHOOR DUNOLD",
                "shift": 3,
                "solution": "HELLO ARKALIA",
                "explanation": "Chaque lettre est décalée de 3 positions dans l'alphabet",
                "points": 55,
                "badge": "Cryptographe",
            },
        ]

    def _get_network_games(self) -> List[Dict[str, Any]]:
        """Jeux de réseaux"""
        return [
            {
                "id": "network_1",
                "title": "🌐 Analyse le Réseau",
                "description": "Identifie le type de réseau à partir de l'adresse IP",
                "type": GameType.NETWORK.value,
                "difficulty": Difficulty.BEGINNER.value,
                "ip_addresses": ["192.168.1.1", "10.0.0.1", "172.16.0.1", "8.8.8.8"],
                "options": ["Réseau privé", "Réseau public", "DNS Google"],
                "solution": [0, 0, 0, 2],  # Indices des bonnes réponses
                "explanation": "192.168.x.x et 10.x.x.x sont des réseaux privés, 8.8.8.8 est DNS Google",
                "points": 50,
                "badge": "Réseau",
            }
        ]

    def get_available_games(self, user_level: int = 1) -> List[Dict[str, Any]]:
        """Récupère les jeux disponibles selon le niveau de l'utilisateur"""
        available_games = []

        for _game_type, games in self.games_data.items():
            for game in games:
                # Déterminer la difficulté selon le niveau
                if user_level >= 3 and game["difficulty"] == Difficulty.EXPERT.value:
                    available_games.append(game)
                elif (
                    user_level >= 2 and game["difficulty"] == Difficulty.ADVANCED.value
                ):
                    available_games.append(game)
                elif user_level >= 1 and game["difficulty"] in [
                    Difficulty.BEGINNER.value,
                    Difficulty.INTERMEDIATE.value,
                ]:
                    available_games.append(game)

        return available_games

    def start_game(self, game_id: str, user_id: str) -> Dict[str, Any]:
        """Démarre un jeu éducatif"""
        # Trouver le jeu
        game = None
        for _game_type, games in self.games_data.items():
            for g in games:
                if g["id"] == game_id:
                    game = g
                    break
            if game:
                break

        if not game:
            return {"success": False, "message": "❌ Jeu non trouvé"}

        # Créer une session de jeu
        session_id = f"{user_id}_{game_id}_{datetime.now().timestamp()}"
        self.game_sessions[session_id] = {
            "user_id": user_id,
            "game_id": game_id,
            "start_time": datetime.now(),
            "attempts": 0,
            "completed": False,
            "score": 0,
        }

        # Préparer le jeu selon son type
        game_data = self._prepare_game(game)

        return {
            "success": True,
            "session_id": session_id,
            "game": game_data,
            "message": f"🎮 {game['title']} démarré !",
        }

    def _prepare_game(self, game: Dict[str, Any]) -> Dict[str, Any]:
        """Prépare les données du jeu pour l'affichage"""
        game_data = {
            "id": game["id"],
            "title": game["title"],
            "description": game["description"],
            "type": game["type"],
            "difficulty": game["difficulty"],
            "points": game["points"],
            "badge": game["badge"],
        }

        # Ajouter les données spécifiques au type de jeu
        if game["type"] == GameType.LOGIC.value:
            if "hints" in game:
                game_data["hints"] = game["hints"]
            if "rules" in game:
                game_data["rules"] = game["rules"]
                game_data["numbers"] = game["numbers"]
        elif game["type"] == GameType.CODE.value:
            if "code" in game:
                game_data["code"] = game["code"]
            if "challenge" in game:
                game_data["challenge"] = game["challenge"]
                game_data["test_input"] = game["test_input"]
        elif game["type"] == GameType.CYBERSECURITY.value:
            if "logs" in game:
                game_data["logs"] = game["logs"]
                game_data["options"] = game["options"]
            if "passwords" in game:
                game_data["passwords"] = game["passwords"]
        elif game["type"] == GameType.CRYPTOGRAPHY.value:
            if "encoded_message" in game:
                game_data["encoded_message"] = game["encoded_message"]
            if "encrypted" in game:
                game_data["encrypted"] = game["encrypted"]
                game_data["shift"] = game["shift"]
        elif game["type"] == GameType.NETWORK.value:
            if "ip_addresses" in game:
                game_data["ip_addresses"] = game["ip_addresses"]
                game_data["options"] = game["options"]

        return game_data

    def submit_answer(self, session_id: str, answer: Any) -> Dict[str, Any]:
        """Soumet une réponse pour un jeu"""
        if session_id not in self.game_sessions:
            return {"success": False, "message": "❌ Session de jeu non trouvée"}

        session = self.game_sessions[session_id]
        game_id = session["game_id"]

        # Trouver le jeu
        game = None
        for _game_type, games in self.games_data.items():
            for g in games:
                if g["id"] == game_id:
                    game = g
                    break
            if game:
                break

        if not game:
            return {"success": False, "message": "❌ Jeu non trouvé"}

        # Incrémenter les tentatives
        session["attempts"] += 1

        # Vérifier la réponse
        is_correct = self._check_answer(game, answer)

        if is_correct:
            session["completed"] = True
            session["score"] = game["points"]

            # SYSTÈME DE RÉCOMPENSES MATRIX AMÉLIORÉ
            matrix_bonus = self._calculate_matrix_bonus(user_id, game, session["attempts"])
            total_score = game["points"] + matrix_bonus["total"]

            return {
                "success": True,
                "correct": True,
                "score": total_score,
                "badge": game["badge"],
                "explanation": game.get("explanation", "Bravo ! Tu as réussi !"),
                "message": f"🎉 Correct ! +{total_score} points !",
                "matrix_bonus": matrix_bonus,
                "celebration": True,
                "particles": True,
                "matrix_effect": "success_pulse"
            }
        else:
            # Donner un indice après 2 tentatives
            hint = ""
            if session["attempts"] >= 2:
                if game["type"] == GameType.LOGIC.value and "hints" in game:
                    hint = f"💡 Indice : {game['hints'][min(session['attempts']-2, len(game['hints'])-1)]}"
                elif game["type"] == GameType.CODE.value:
                    hint = "💡 Vérifie la syntaxe et la logique du code"
                elif game["type"] == GameType.CYBERSECURITY.value:
                    hint = "💡 Analyse les patterns dans les données"
                elif game["type"] == GameType.CRYPTOGRAPHY.value:
                    hint = "💡 Pense à la méthode de chiffrement utilisée"
                elif game["type"] == GameType.NETWORK.value:
                    hint = "💡 Regarde les plages d'adresses IP"

            return {
                "success": True,
                "correct": False,
                "attempts": session["attempts"],
                "hint": hint,
                "message": "❌ Incorrect. Essaie encore !",
            }

    def _check_answer(self, game: Dict[str, Any], answer: Any) -> bool:
        """Vérifie si la réponse est correcte"""
        solution = game["solution"]

        # Normaliser la réponse
        if isinstance(answer, str):
            answer = answer.strip().upper()
        if isinstance(solution, str):
            solution = solution.strip().upper()

        # Vérification selon le type de jeu
        if game["type"] == GameType.LOGIC.value:
            return answer == solution
        elif game["type"] == GameType.CODE.value:
            # Pour les jeux de code, vérifier si la réponse contient les éléments clés
            if isinstance(solution, str) and isinstance(answer, str):
                return solution.lower() in answer.lower()
            return answer == solution
        elif game["type"] == GameType.CYBERSECURITY.value:
            if isinstance(solution, list):
                return answer in solution
            return answer == solution
        elif game["type"] == GameType.CRYPTOGRAPHY.value:
            return answer == solution
        elif game["type"] == GameType.NETWORK.value:
            if isinstance(solution, list):
                # Pour les jeux réseau, vérifier l'égalité des listes
                return answer == solution
            return answer == solution

        return False

    def get_user_progress(self, user_id: str) -> Dict[str, Any]:
        """Récupère la progression d'un utilisateur"""
        if user_id not in self.user_progress:
            self.user_progress[user_id] = {
                "games_completed": 0,
                "total_score": 0,
                "badges_earned": [],
                "favorite_type": None,
                "last_played": None,
            }

        return self.user_progress[user_id]

    def get_leaderboard(self) -> List[Dict[str, Any]]:
        """Récupère le classement des joueurs"""
        leaderboard = []

        for user_id, progress in self.user_progress.items():
            leaderboard.append(
                {
                    "user_id": user_id,
                    "games_completed": progress["games_completed"],
                    "total_score": progress["total_score"],
                    "badges_count": len(progress["badges_earned"]),
                }
            )

        # Trier par score décroissant
        leaderboard.sort(key=lambda x: x["total_score"], reverse=True)

        return leaderboard[:10]  # Top 10

    def get_game_statistics(self) -> Dict[str, Any]:
        """Récupère les statistiques globales des jeux"""
        total_games = sum(len(games) for games in self.games_data.values())
        total_players = len(self.user_progress)
        total_sessions = len(self.game_sessions)

        # Compter les jeux par type
        games_by_type = {}
        for game_type, games in self.games_data.items():
            games_by_type[game_type] = len(games)

        return {
            "total_games": total_games,
            "total_players": total_players,
            "total_sessions": total_sessions,
            "games_by_type": games_by_type,
            "last_updated": datetime.now().isoformat(),
        }


# Instance globale
educational_games = EducationalGamesEngine()
