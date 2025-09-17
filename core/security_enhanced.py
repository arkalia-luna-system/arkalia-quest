#!/usr/bin/env python3
"""
Système de sécurité amélioré pour Arkalia Quest
"""

import hashlib
import re
import secrets
import time
from collections import defaultdict, deque
from datetime import datetime
from typing import Optional


class SecurityEnhanced:
    """Système de sécurité avancé avec rate limiting et validation"""

    def __init__(self):
        """Initialise le système de sécurité"""
        self.rate_limits = defaultdict(lambda: deque())
        self.blocked_ips = {}
        self.suspicious_activities = defaultdict(list)
        self.login_attempts = defaultdict(list)

        # Configuration de sécurité
        self.config = {
            "max_requests_per_minute": 120,  # Augmenté pour éviter les blocages en développement
            "max_requests_per_hour": 2000,  # Augmenté proportionnellement
            "max_login_attempts": 5,
            "block_duration_minutes": 5,  # Réduit de 15 à 5 minutes
            "suspicious_threshold": 20,  # Augmenté de 10 à 20
            "max_session_duration_hours": 24,
        }

        # Patterns de validation renforcés
        self.validation_patterns = {
            "username": re.compile(r"^[a-zA-Z0-9_-]{3,20}$"),
            "email": re.compile(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"),
            "password": re.compile(
                r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$",
            ),
            "game_id": re.compile(r"^[a-zA-Z0-9_-]+$"),
            "command": re.compile(
                r"^[a-zA-Z0-9_\s\-\.]+$"
            ),  # Ajout du point pour les commandes
            "api_key": re.compile(r"^[a-zA-Z0-9]{32,64}$"),
            "session_id": re.compile(r"^[a-zA-Z0-9_-]{24,48}$"),
        }

    def validate_input(self, input_type: str, value: str) -> tuple[bool, str]:
        """
        Valide une entrée utilisateur

        Args:
            input_type: Type d'entrée (username, email, password, etc.)
            value: Valeur à valider

        Returns:
            Tuple (is_valid, error_message)
        """
        if not value or not isinstance(value, str):
            return False, "Valeur invalide"

        # Vérifier la longueur
        if len(value) > 1000:  # Limite de sécurité
            return False, "Valeur trop longue"

        # Vérifier les caractères dangereux (liste étendue)
        dangerous_chars = [
            "<",
            ">",
            '"',
            "'",
            "&",
            ";",
            "(",
            ")",
            "|",
            "`",
            "$",
            "{",
            "}",
            "[",
            "]",
            "\\",
            "/",
            "*",
            "?",
            "!",
            "@",
            "#",
            "%",
            "^",
            "+",
            "=",
            "~",
            "`",
        ]
        if any(char in value for char in dangerous_chars):
            return False, "Caractères non autorisés détectés"

        # Vérifier les patterns d'injection
        injection_patterns = [
            "script",
            "javascript",
            "vbscript",
            "onload",
            "onerror",
            "onclick",
            "eval",
            "function",
            "alert",
            "confirm",
            "prompt",
        ]
        value_lower = value.lower()
        for pattern in injection_patterns:
            if pattern in value_lower:
                return False, f"Pattern suspect détecté: {pattern}"

        # Validation spécifique par type
        if input_type in self.validation_patterns:
            pattern = self.validation_patterns[input_type]
            if not pattern.match(value):
                return False, f"Format {input_type} invalide"

        return True, ""

    def check_rate_limit(self, ip_address: str) -> tuple[bool, str]:
        """
        Vérifie si une IP respecte les limites de taux

        Args:
            ip_address: Adresse IP à vérifier

        Returns:
            Tuple (is_allowed, message)
        """
        # Liste blanche pour les IPs de développement - pas de rate limiting
        dev_ips = ["127.0.0.1", "localhost", "::1"]
        if ip_address in dev_ips:
            return True, ""

        current_time = time.time()

        # Nettoyer les anciennes requêtes
        while (
            self.rate_limits[ip_address]
            and current_time - self.rate_limits[ip_address][0] > 60
        ):
            self.rate_limits[ip_address].popleft()

        # Vérifier la limite par minute
        if len(self.rate_limits[ip_address]) >= self.config["max_requests_per_minute"]:
            self._log_suspicious_activity(ip_address, "rate_limit_exceeded")
            return False, "Trop de requêtes. Veuillez patienter."

        # Ajouter la requête actuelle
        self.rate_limits[ip_address].append(current_time)

        return True, ""

    def check_login_attempts(self, ip_address: str, username: str) -> tuple[bool, str]:
        """
        Vérifie les tentatives de connexion

        Args:
            ip_address: Adresse IP
            username: Nom d'utilisateur

        Returns:
            Tuple (is_allowed, message)
        """
        current_time = time.time()
        key = f"{ip_address}:{username}"

        # Nettoyer les anciennes tentatives
        self.login_attempts[key] = [
            attempt
            for attempt in self.login_attempts[key]
            if current_time - attempt < 3600  # 1 heure
        ]

        # Vérifier la limite
        if len(self.login_attempts[key]) >= self.config["max_login_attempts"]:
            self._log_suspicious_activity(ip_address, "login_brute_force", username)
            return False, "Trop de tentatives de connexion. Veuillez patienter."

        return True, ""

    def record_login_attempt(self, ip_address: str, username: str, success: bool):
        """
        Enregistre une tentative de connexion

        Args:
            ip_address: Adresse IP
            username: Nom d'utilisateur
            success: Succès de la connexion
        """
        current_time = time.time()
        key = f"{ip_address}:{username}"

        if not success:
            self.login_attempts[key].append(current_time)
        else:
            # Réinitialiser les tentatives en cas de succès
            self.login_attempts[key] = []

    def is_ip_blocked(self, ip_address: str) -> bool:
        """
        Vérifie si une IP est bloquée

        Args:
            ip_address: Adresse IP à vérifier

        Returns:
            True si l'IP est bloquée
        """
        if ip_address in self.blocked_ips:
            block_until = self.blocked_ips[ip_address]
            if time.time() < block_until:
                return True
            # Débloquer l'IP
            del self.blocked_ips[ip_address]

        return False

    def block_ip(self, ip_address: str, duration_minutes: Optional[int] = None):
        """
        Bloque une adresse IP

        Args:
            ip_address: Adresse IP à bloquer
            duration_minutes: Durée du blocage en minutes
        """
        # Ne pas bloquer les IPs de développement
        dev_ips = ["127.0.0.1", "localhost", "::1"]
        if ip_address in dev_ips:
            self._log_security_event(
                "dev_ip_block_attempt",
                {
                    "ip": ip_address,
                    "message": "Tentative de blocage d'IP de développement ignorée",
                },
            )
            return

        if duration_minutes is None:
            duration_minutes = self.config["block_duration_minutes"]

        block_until = time.time() + (duration_minutes * 60)
        self.blocked_ips[ip_address] = block_until

        self._log_security_event(
            "ip_blocked",
            {
                "ip": ip_address,
                "duration_minutes": duration_minutes,
                "blocked_until": datetime.fromtimestamp(block_until).isoformat(),
            },
        )

    def _log_suspicious_activity(
        self, ip_address: str, activity_type: str, details: str = ""
    ):
        """
        Enregistre une activité suspecte

        Args:
            ip_address: Adresse IP
            activity_type: Type d'activité
            details: Détails supplémentaires
        """
        current_time = time.time()

        self.suspicious_activities[ip_address].append(
            {"timestamp": current_time, "type": activity_type, "details": details},
        )

        # Nettoyer les anciennes activités
        self.suspicious_activities[ip_address] = [
            activity
            for activity in self.suspicious_activities[ip_address]
            if current_time - activity["timestamp"] < 3600  # 1 heure
        ]

        # Vérifier si l'IP doit être bloquée
        if (
            len(self.suspicious_activities[ip_address])
            >= self.config["suspicious_threshold"]
        ):
            self.block_ip(ip_address)

        self._log_security_event(
            "suspicious_activity",
            {
                "ip": ip_address,
                "activity_type": activity_type,
                "details": details,
                "total_activities": len(self.suspicious_activities[ip_address]),
            },
        )

    def _log_security_event(self, event_type: str, data: dict):
        """
        Enregistre un événement de sécurité

        Args:
            event_type: Type d'événement
            data: Données de l'événement
        """
        # Log l'événement de sécurité
        game_logger.info(f"🔒 SECURITY EVENT: {event_type} - {data}")

    def generate_secure_token(self, length: int = 32) -> str:
        """
        Génère un token sécurisé

        Args:
            length: Longueur du token

        Returns:
            Token sécurisé
        """
        return secrets.token_urlsafe(length)

    def hash_password(self, password: str) -> str:
        """
        Hache un mot de passe de manière sécurisée

        Args:
            password: Mot de passe en clair

        Returns:
            Mot de passe haché
        """
        salt = secrets.token_hex(16)
        password_hash = hashlib.pbkdf2_hmac(
            "sha256", password.encode(), salt.encode(), 100000
        )
        return f"{salt}:{password_hash.hex()}"

    def verify_password(self, password: str, hashed_password: str) -> bool:
        """
        Vérifie un mot de passe

        Args:
            password: Mot de passe en clair
            hashed_password: Mot de passe haché

        Returns:
            True si le mot de passe est correct
        """
        try:
            salt, stored_hash = hashed_password.split(":")
            password_hash = hashlib.pbkdf2_hmac(
                "sha256", password.encode(), salt.encode(), 100000
            )
            return password_hash.hex() == stored_hash
        except (ValueError, AttributeError):
            return False

    def get_security_stats(self) -> dict:
        """
        Retourne les statistiques de sécurité

        Returns:
            Dictionnaire avec les statistiques
        """
        current_time = time.time()

        # Compter les IPs actives
        active_ips = len(
            [
                ip
                for ip, requests in self.rate_limits.items()
                if requests and current_time - requests[-1] < 3600
            ],
        )

        # Compter les IPs bloquées
        blocked_ips = len(
            [
                ip
                for ip, block_until in self.blocked_ips.items()
                if current_time < block_until
            ],
        )

        # Compter les activités suspectes
        suspicious_ips = len(
            [
                ip
                for ip, activities in self.suspicious_activities.items()
                if activities and current_time - activities[-1]["timestamp"] < 3600
            ],
        )

        return {
            "active_ips": active_ips,
            "blocked_ips": blocked_ips,
            "suspicious_ips": suspicious_ips,
            "total_rate_limits": len(self.rate_limits),
            "total_login_attempts": len(self.login_attempts),
            "config": self.config,
        }


# Instance globale du système de sécurité
security_enhanced = SecurityEnhanced()
