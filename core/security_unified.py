#!/usr/bin/env python3
"""
Système de sécurité unifié pour Arkalia Quest
Combine les meilleures fonctionnalités de security_manager.py et security_enhanced.py
"""

import logging
import re
import time
from collections import defaultdict, deque
from datetime import datetime
from pathlib import Path
from typing import Any

# Configuration du logger de sécurité
security_logger = logging.getLogger("arkalia_security")
security_logger.setLevel(logging.INFO)

# Créer le dossier logs s'il n'existe pas
logs_dir = Path("logs")
logs_dir.mkdir(exist_ok=True)

# Handler pour fichier de logs de sécurité
security_handler = logging.FileHandler(logs_dir / "security.log")
security_handler.setLevel(logging.INFO)

# Formatter pour les logs de sécurité
security_formatter = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
security_handler.setFormatter(security_formatter)
security_logger.addHandler(security_handler)


class SecurityUnified:
    """Système de sécurité unifié avec toutes les fonctionnalités"""

    def __init__(self):
        """Initialise le système de sécurité unifié"""
        # Rate limiting (de security_enhanced)
        self.rate_limits = defaultdict(lambda: deque())
        self.blocked_ips = {}
        self.suspicious_activities = defaultdict(list)
        self.login_attempts = defaultdict(list)
        self.rate_limit_violations = []

        # Configuration de sécurité
        self.config = {
            "max_requests_per_minute": 120,
            "max_requests_per_hour": 2000,
            "max_login_attempts": 5,
            "block_duration_minutes": 5,
            "suspicious_threshold": 10,
        }

        # Patterns de sécurité (de security_manager)
        self.dangerous_patterns = [
            r"rm\s+-rf",
            r"sudo\s+rm",
            r"chmod\s+777",
            r"passwd\s+",
            r"su\s+",
            r"sudo\s+",
            r"wget\s+.*\|.*sh",
            r"curl\s+.*\|.*sh",
            r"eval\s*\(",
            r"exec\s*\(",
            r"system\s*\(",
            r"shell_exec\s*\(",
            r"<script",
            r"javascript:",
            r"onload\s*=",
            r"onerror\s*=",
            r"onclick\s*=",
            r"onmouseover\s*=",
            r"onfocus\s*=",
            r"onblur\s*=",
            r"onchange\s*=",
            r"onsubmit\s*=",
            r"onreset\s*=",
            r"onselect\s*=",
            r"onkeydown\s*=",
            r"onkeyup\s*=",
            r"onkeypress\s*=",
            r"onmousedown\s*=",
            r"onmouseup\s*=",
            r"onmousemove\s*=",
            r"onmouseout\s*=",
            r"onmouseover\s*=",
            r"onmouseenter\s*=",
            r"onmouseleave\s*=",
            r"oncontextmenu\s*=",
            r"ondblclick\s*=",
            r"onwheel\s*=",
            r"onresize\s*=",
            r"onscroll\s*=",
            r"onunload\s*=",
            r"onbeforeunload\s*=",
            r"onpagehide\s*=",
            r"onpageshow\s*=",
            r"onpopstate\s*=",
            r"onhashchange\s*=",
            r"onstorage\s*=",
            r"onmessage\s*=",
            r"onerror\s*=",
            r"onabort\s*=",
            r"oncanplay\s*=",
            r"oncanplaythrough\s*=",
            r"onchange\s*=",
            r"onclick\s*=",
            r"oncontextmenu\s*=",
            r"ondblclick\s*=",
            r"ondrag\s*=",
            r"ondragend\s*=",
            r"ondragenter\s*=",
            r"ondragleave\s*=",
            r"ondragover\s*=",
            r"ondragstart\s*=",
            r"ondrop\s*=",
            r"ondurationchange\s*=",
            r"onemptied\s*=",
            r"onended\s*=",
            r"onerror\s*=",
            r"onfocus\s*=",
            r"oninput\s*=",
            r"oninvalid\s*=",
            r"onkeydown\s*=",
            r"onkeypress\s*=",
            r"onkeyup\s*=",
            r"onload\s*=",
            r"onloadeddata\s*=",
            r"onloadedmetadata\s*=",
            r"onloadstart\s*=",
            r"onmousedown\s*=",
            r"onmouseenter\s*=",
            r"onmouseleave\s*=",
            r"onmousemove\s*=",
            r"onmouseout\s*=",
            r"onmouseover\s*=",
            r"onmouseup\s*=",
            r"onmousewheel\s*=",
            r"onoffline\s*=",
            r"ononline\s*=",
            r"onpagehide\s*=",
            r"onpageshow\s*=",
            r"onpause\s*=",
            r"onplay\s*=",
            r"onplaying\s*=",
            r"onpopstate\s*=",
            r"onprogress\s*=",
            r"onratechange\s*=",
            r"onresize\s*=",
            r"onscroll\s*=",
            r"onseeked\s*=",
            r"onseeking\s*=",
            r"onselect\s*=",
            r"onstalled\s*=",
            r"onstorage\s*=",
            r"onsubmit\s*=",
            r"onsuspend\s*=",
            r"ontimeupdate\s*=",
            r"onunload\s*=",
            r"onvolumechange\s*=",
            r"onwaiting\s*=",
            r"onwheel\s*=",
        ]

        # Origines autorisées
        self.allowed_origins = [
            "http://localhost:5000",
            "http://localhost:5001",
            "http://127.0.0.1:5000",
            "http://127.0.0.1:5001",
            "https://arkalia-quest.com",
        ]

    # Méthodes de rate limiting (de security_enhanced)
    def is_ip_blocked(self, ip: str) -> bool:
        """Vérifie si une IP est bloquée"""
        if ip in self.blocked_ips:
            block_info = self.blocked_ips[ip]
            if time.time() - block_info["timestamp"] < block_info["duration"]:
                return True
            else:
                # Débloquer l'IP
                del self.blocked_ips[ip]
        return False

    def check_rate_limit(self, ip: str) -> bool:
        """Vérifie le rate limiting pour une IP"""
        now = time.time()

        # Nettoyer les anciennes requêtes
        while self.rate_limits[ip] and now - self.rate_limits[ip][0] > 60:
            self.rate_limits[ip].popleft()

        # Vérifier la limite par minute
        if len(self.rate_limits[ip]) >= self.config["max_requests_per_minute"]:
            self._block_ip(ip, "Rate limit dépassé")
            return False

        # Ajouter la requête actuelle
        self.rate_limits[ip].append(now)
        return True

    def check_rate_limit_violation(
        self, ip: str, current_count: int, limit: int
    ) -> bool:
        """Vérifie si une IP a violé le rate limit"""
        violated = current_count > limit
        if violated:
            self.rate_limit_violations.append(
                {
                    "ip": ip,
                    "current_count": current_count,
                    "limit": limit,
                    "timestamp": datetime.now().isoformat(),
                }
            )
        return violated

    def _block_ip(self, ip: str, reason: str):
        """Bloque une IP"""
        self.blocked_ips[ip] = {
            "timestamp": time.time(),
            "duration": self.config["block_duration_minutes"] * 60,
            "reason": reason,
        }
        security_logger.warning(f"IP {ip} bloquée: {reason}")

    # Méthodes de validation (de security_enhanced)
    def validate_input(self, input_type: str, value: str) -> tuple[bool, str]:
        """Valide une entrée utilisateur"""
        if not value or not isinstance(value, str):
            return False, "Valeur invalide"

        # Vérifier les patterns dangereux
        for pattern in self.dangerous_patterns:
            if re.search(pattern, value, re.IGNORECASE):
                return False, f"Pattern dangereux détecté: {pattern}"

        # Validation spécifique par type
        if input_type == "email":
            if not re.match(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", value):
                return False, "Format email invalide"

        elif input_type == "username":
            if not re.match(r"^[a-zA-Z0-9_-]{3,20}$", value):
                return False, "Nom d'utilisateur invalide"

        elif input_type == "command":
            if len(value) > 1000:
                return False, "Commande trop longue"

        return True, "Valide"

    # Méthodes de sécurité (de security_manager)
    def check_input_security(
        self, cmd: str, client_ip: str = None, ip_address: str = None
    ) -> dict[str, Any]:
        """Vérifie la sécurité d'une commande"""
        # Support des deux paramètres pour compatibilité
        if ip_address:
            client_ip = ip_address

        threats_detected = []
        risk_level = "low"

        # Vérifier les patterns dangereux
        for pattern in self.dangerous_patterns:
            if re.search(pattern, cmd, re.IGNORECASE):
                # Simplifier le nom du pattern pour les tests
                if pattern == r"<script":
                    threats_detected.append("pattern_script")
                else:
                    clean_pattern = (
                        pattern.replace("\\", "").replace("(", "").replace(")", "")
                    )
                    threats_detected.append(f"pattern_{clean_pattern}")
                risk_level = "critical"

        # Vérifier la longueur
        if len(cmd) > 1000:
            threats_detected.append("Commande trop longue")
            risk_level = "high"

        # Vérifier les caractères suspects
        if re.search(r"[<>\"'&]", cmd):
            threats_detected.append("Caractères suspects")
            risk_level = "medium"

        return {
            "is_safe": len(threats_detected) == 0,
            "threats_detected": threats_detected,
            "risk_level": risk_level,
            "client_ip": client_ip,
            "timestamp": datetime.now().isoformat(),
        }

    def block_ip(self, ip: str, reason: str, duration: int = None):
        """Bloque une IP avec une raison"""
        if duration:
            # Utiliser la durée spécifiée
            self.blocked_ips[ip] = {
                "timestamp": time.time(),
                "duration": duration * 60,  # Convertir en secondes
                "reason": reason,
            }
        else:
            self._block_ip(ip, reason)

    def check_origin_security(self, origin: str, client_ip: str = None) -> bool:
        """Vérifie la sécurité de l'origine"""
        if origin in self.allowed_origins:
            return True

        # Log de l'origine suspecte
        if client_ip:
            security_logger.warning(f"Origine suspecte: {origin} depuis {client_ip}")
        return False

    def get_security_report(self) -> dict[str, Any]:
        """Retourne un rapport de sécurité"""
        return {
            "blocked_ips_count": len(self.blocked_ips),
            "total_events_24h": len(self.rate_limit_violations),
            "security_status": "active",
            "suspicious_activities": len(self.suspicious_activities),
            "total_requests": sum(
                len(requests) for requests in self.rate_limits.values()
            ),
            "timestamp": datetime.now().isoformat(),
        }

    def get_security_stats(self) -> dict[str, Any]:
        """Retourne les statistiques de sécurité"""
        return {
            "blocked_ips_count": len(self.blocked_ips),
            "active_rate_limits": len(self.rate_limits),
            "suspicious_activities_count": len(self.suspicious_activities),
            "login_attempts_count": len(self.login_attempts),
            "timestamp": datetime.now().isoformat(),
        }

    def unblock_ip(self, ip: str) -> bool:
        """Débloque une IP"""
        if ip in self.blocked_ips:
            del self.blocked_ips[ip]
            security_logger.info(f"IP {ip} débloquée")
            return True
        return False

    def get_blocked_ips(self) -> list[dict[str, Any]]:
        """Retourne la liste des IPs bloquées"""
        return [
            {
                "ip": ip,
                "reason": info["reason"],
                "blocked_at": datetime.fromtimestamp(info["timestamp"]).isoformat(),
                "duration_minutes": info["duration"] / 60,
            }
            for ip, info in self.blocked_ips.items()
        ]

    def clear_old_blocks(self):
        """Nettoie les anciens blocages"""
        now = time.time()
        expired_ips = [
            ip
            for ip, info in self.blocked_ips.items()
            if now - info["timestamp"] > info["duration"]
        ]
        for ip in expired_ips:
            del self.blocked_ips[ip]
            security_logger.info(f"Blocage expiré pour IP {ip}")


# Instance globale
security_unified = SecurityUnified()
