"""
WebSocket Manager - Gestionnaire de WebSockets pour défis temps réel
"""

import time
from typing import Any, Callable, Dict, Optional


class WebSocketManager:
    """Gestionnaire de WebSockets pour défis temps réel (version simulée)"""

    def __init__(self):
        self.active_connections = {}  # {session_id: connection_info}
        self.challenge_rooms = {}  # {room_id: [session_ids]}
        self.challenge_data = {}  # {room_id: challenge_info}
        self.message_handlers = {}  # {event_type: handler_function}

        # Enregistrer les handlers par défaut
        self.register_default_handlers()

    def register_default_handlers(self):
        """Enregistre les handlers par défaut"""
        self.register_handler("join_challenge", self.handle_join_challenge)
        self.register_handler("leave_challenge", self.handle_leave_challenge)
        self.register_handler("challenge_action", self.handle_challenge_action)
        self.register_handler("chat_message", self.handle_chat_message)
        self.register_handler("ping", self.handle_ping)

    def register_handler(self, event_type: str, handler: Callable):
        """Enregistre un handler pour un type d'événement"""
        self.message_handlers[event_type] = handler

    def handle_join_challenge(
        self, session_id: str, data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Gère l'arrivée d'un joueur dans un défi"""
        room_id = data.get("room_id")
        if not room_id:
            return {"type": "error", "message": "Room ID required"}

        player_name = data.get("player_name", "Anonymous")

        if room_id not in self.challenge_rooms:
            self.challenge_rooms[room_id] = []

        if session_id not in self.challenge_rooms[room_id]:
            self.challenge_rooms[room_id].append(session_id)

        # Informer les autres joueurs
        self.broadcast_to_room(
            room_id,
            {
                "type": "player_joined",
                "player_name": player_name,
                "players_count": len(self.challenge_rooms[room_id]),
            },
            exclude_session=session_id,
        )

        return {
            "type": "join_success",
            "room_id": room_id,
            "players_count": len(self.challenge_rooms[room_id]),
            "challenge_info": self.challenge_data.get(room_id, {}),
        }

    def handle_leave_challenge(
        self, session_id: str, data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Gère le départ d'un joueur d'un défi"""
        room_id = data.get("room_id")
        if not room_id:
            return {"type": "error", "message": "Room ID required"}

        if (
            room_id in self.challenge_rooms
            and session_id in self.challenge_rooms[room_id]
        ):
            self.challenge_rooms[room_id].remove(session_id)

            # Informer les autres joueurs
            self.broadcast_to_room(
                room_id,
                {
                    "type": "player_left",
                    "players_count": len(self.challenge_rooms[room_id]),
                },
            )

        return {"type": "leave_success"}

    def handle_challenge_action(
        self, session_id: str, data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Gère une action dans un défi"""
        room_id = data.get("room_id")
        if not room_id:
            return {"type": "error", "message": "Room ID required"}

        action = data.get("action")
        player_name = data.get("player_name", "Anonymous")

        # Traiter l'action selon le type
        if action == "start_challenge":
            return self.start_challenge(room_id, session_id)
        elif action == "complete_mission":
            return self.complete_mission(room_id, session_id, data)
        elif action == "timeout":
            return self.handle_timeout(room_id, session_id)

        # Diffuser l'action aux autres joueurs
        self.broadcast_to_room(
            room_id,
            {
                "type": "player_action",
                "player_name": player_name,
                "action": action,
                "timestamp": time.time(),
            },
            exclude_session=session_id,
        )

        return {"type": "action_processed"}

    def handle_chat_message(
        self, session_id: str, data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Gère un message de chat"""
        room_id = data.get("room_id")
        if not room_id:
            return {"type": "error", "message": "Room ID required"}

        message = data.get("message", "")
        player_name = data.get("player_name", "Anonymous")

        # Diffuser le message à tous les joueurs de la room
        self.broadcast_to_room(
            room_id,
            {
                "type": "chat_message",
                "player_name": player_name,
                "message": message,
                "timestamp": time.time(),
            },
        )

        return {"type": "message_sent"}

    def handle_ping(self, session_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Gère un ping pour maintenir la connexion"""
        return {"type": "pong", "timestamp": time.time()}

    def start_challenge(self, room_id: str, session_id: str) -> Dict[str, Any]:
        """Démarre un défi"""
        if room_id in self.challenge_data:
            challenge = self.challenge_data[room_id]
            challenge["status"] = "active"
            challenge["start_time"] = time.time()
            challenge["timer"] = challenge.get("timer", 30)

            # Informer tous les joueurs
            self.broadcast_to_room(
                room_id,
                {
                    "type": "challenge_started",
                    "timer": challenge["timer"],
                    "start_time": challenge["start_time"],
                },
            )

            return {
                "type": "challenge_started",
                "timer": challenge["timer"],
                "mission": challenge.get("mission", {}),
            }

        return {"type": "error", "message": "Challenge not found"}

    def complete_mission(
        self, room_id: str, session_id: str, data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Marque une mission comme complétée"""
        player_name = data.get("player_name", "Anonymous")
        completion_time = data.get("completion_time", 0)

        # Enregistrer le résultat
        if room_id not in self.challenge_data:
            self.challenge_data[room_id] = {}

        if "results" not in self.challenge_data[room_id]:
            self.challenge_data[room_id]["results"] = {}

        self.challenge_data[room_id]["results"][player_name] = {
            "completion_time": completion_time,
            "timestamp": time.time(),
        }

        # Vérifier si tous les joueurs ont fini
        players_in_room = self.challenge_rooms.get(room_id, [])
        completed_players = len(self.challenge_data[room_id]["results"])

        if completed_players >= len(players_in_room):
            return self.end_challenge(room_id)

        # Informer les autres joueurs
        self.broadcast_to_room(
            room_id,
            {
                "type": "player_completed",
                "player_name": player_name,
                "completion_time": completion_time,
                "remaining_players": len(players_in_room) - completed_players,
            },
            exclude_session=session_id,
        )

        return {"type": "mission_completed"}

    def handle_timeout(self, room_id: str, session_id: str) -> Dict[str, Any]:
        """Gère un timeout dans un défi"""
        player_name = self.get_player_name(session_id)

        # Marquer le joueur comme ayant échoué
        if room_id not in self.challenge_data:
            self.challenge_data[room_id] = {}

        if "results" not in self.challenge_data[room_id]:
            self.challenge_data[room_id]["results"] = {}

        self.challenge_data[room_id]["results"][player_name] = {
            "status": "timeout",
            "timestamp": time.time(),
        }

        # Informer les autres joueurs
        self.broadcast_to_room(
            room_id,
            {"type": "player_timeout", "player_name": player_name},
            exclude_session=session_id,
        )

        return {"type": "timeout_processed"}

    def end_challenge(self, room_id: str) -> Dict[str, Any]:
        """Termine un défi et calcule les résultats"""
        results = self.challenge_data[room_id].get("results", {})

        # Calculer le classement
        ranking = []
        for player_name, result in results.items():
            if isinstance(result, dict) and "completion_time" in result:
                ranking.append(
                    {
                        "player_name": player_name,
                        "completion_time": result["completion_time"],
                        "status": "completed",
                    }
                )
            else:
                ranking.append({"player_name": player_name, "status": "timeout"})

        # Trier par temps de completion
        ranking.sort(key=lambda x: x.get("completion_time", float("inf")))

        # Déterminer le gagnant
        winner = (
            ranking[0]["player_name"]
            if ranking and ranking[0]["status"] == "completed"
            else None
        )

        # Informer tous les joueurs
        self.broadcast_to_room(
            room_id, {"type": "challenge_ended", "ranking": ranking, "winner": winner}
        )

        return {"type": "challenge_ended", "ranking": ranking, "winner": winner}

    def broadcast_to_room(
        self,
        room_id: str,
        message: Dict[str, Any],
        exclude_session: Optional[str] = None,
    ):
        """Diffuse un message à tous les joueurs d'une room"""
        if room_id in self.challenge_rooms:
            for session_id in self.challenge_rooms[room_id]:
                if session_id != exclude_session:
                    # En mode simulé, on stocke juste le message
                    if session_id not in self.active_connections:
                        self.active_connections[session_id] = {"messages": []}

                    self.active_connections[session_id]["messages"].append(message)

    def get_player_name(self, session_id: str) -> str:
        """Récupère le nom d'un joueur par session_id"""
        if session_id in self.active_connections:
            return self.active_connections[session_id].get("player_name", "Anonymous")
        return "Anonymous"

    def create_challenge_room(self, challenge_data: Dict[str, Any]) -> str:
        """Crée une nouvelle room de défi"""
        room_id = f"challenge_{int(time.time())}"
        self.challenge_data[room_id] = challenge_data
        self.challenge_rooms[room_id] = []
        return room_id

    def get_room_info(self, room_id: str) -> Optional[Dict[str, Any]]:
        """Récupère les informations d'une room"""
        if room_id in self.challenge_data:
            return {
                "room_id": room_id,
                "challenge": self.challenge_data[room_id],
                "players": self.challenge_rooms.get(room_id, []),
                "players_count": len(self.challenge_rooms.get(room_id, [])),
            }
        return None


# Instance globale
websocket_manager = WebSocketManager()
