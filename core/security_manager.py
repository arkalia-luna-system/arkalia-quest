"""
Security Manager - Gestionnaire de sécurité professionnel pour Arkalia Quest
Gère la sécurité, les logs, le monitoring et la protection contre les attaques
"""

import json
import logging
import time
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Optional

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

# Handler pour console (en mode debug)
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(security_formatter)
security_logger.addHandler(console_handler)


class SecurityManager:
    """Gestionnaire de sécurité professionnel pour Arkalia Quest"""

    def __init__(self):
        self.security_events = []
        self.blocked_ips = set()
        self.suspicious_activities = []
        self.rate_limit_violations = []
        self.security_config = {
            "max_failed_attempts": 5,
            "block_duration": 3600,  # 1 heure
            "suspicious_patterns": [
                "script",
                "javascript",
                "onload",
                "onerror",
                "union select",
                "drop table",
                "insert into",
                "exec(",
                "eval(",
                "document.cookie",
            ],
            "max_request_size": 1024 * 1024,  # 1MB
            "allowed_origins": ["localhost", "127.0.0.1"],
        }

        # Charger la configuration depuis un fichier si disponible
        self._load_security_config()

    def _load_security_config(self):
        """Charge la configuration de sécurité depuis un fichier"""
        config_file = Path("config/security.json")
        if config_file.exists():
            try:
                with open(config_file, encoding="utf-8") as f:
                    config = json.load(f)
                    self.security_config.update(config)
                    security_logger.info("Configuration de sécurité chargée")
            except Exception as e:
                security_logger.error(f"Erreur chargement config sécurité: {e}")

    def log_security_event(
        self,
        event_type: str,
        details: Dict[str, Any],
        ip_address: str = "unknown",
        severity: str = "info",
    ):
        """Enregistre un événement de sécurité"""
        event = {
            "timestamp": datetime.now().isoformat(),
            "event_type": event_type,
            "ip_address": ip_address,
            "details": details,
            "severity": severity,
        }

        self.security_events.append(event)

        # Log selon la sévérité
        log_message = (
            f"Événement sécurité: {event_type} - IP: {ip_address} - Détails: {details}"
        )

        if severity == "critical":
            security_logger.critical(log_message)
        elif severity == "error":
            security_logger.error(log_message)
        elif severity == "warning":
            security_logger.warning(log_message)
        else:
            security_logger.info(log_message)

        # Garder seulement les 1000 derniers événements
        if len(self.security_events) > 1000:
            self.security_events = self.security_events[-1000:]

    def check_input_security(
        self, input_data: str, ip_address: str = "unknown"
    ) -> Dict[str, Any]:
        """Vérifie la sécurité d'une entrée utilisateur"""
        result = {"is_safe": True, "threats_detected": [], "risk_level": "low"}

        # Vérifier la taille
        if len(input_data) > self.security_config["max_request_size"]:
            result["is_safe"] = False
            result["threats_detected"].append("input_too_large")
            result["risk_level"] = "high"

        # Vérifier les patterns suspects
        input_lower = input_data.lower()
        for pattern in self.security_config["suspicious_patterns"]:
            if pattern in input_lower:
                result["is_safe"] = False
                result["threats_detected"].append(f"pattern_{pattern}")
                result["risk_level"] = "critical"

        # Log si menace détectée
        if not result["is_safe"]:
            self.log_security_event(
                "input_threat_detected",
                {
                    "input_preview": input_data[:100],
                    "threats": result["threats_detected"],
                    "risk_level": result["risk_level"],
                },
                ip_address,
                "warning" if result["risk_level"] != "critical" else "critical",
            )

        return result

    def check_rate_limit_violation(
        self, ip_address: str, current_count: int, limit: int
    ) -> bool:
        """Vérifie si une IP a violé le rate limiting"""
        if current_count > limit:
            self.log_security_event(
                "rate_limit_violation",
                {
                    "current_count": current_count,
                    "limit": limit,
                    "timestamp": datetime.now().isoformat(),
                },
                ip_address,
                "warning",
            )

            # Ajouter à la liste des violations
            self.rate_limit_violations.append(
                {
                    "ip_address": ip_address,
                    "timestamp": datetime.now().isoformat(),
                    "count": current_count,
                    "limit": limit,
                }
            )

            return True
        return False

    def block_ip(self, ip_address: str, reason: str, duration: Optional[int] = None):
        """Bloque une IP pour une durée donnée"""
        if duration is None:
            duration = self.security_config["block_duration"]

        block_info = {
            "ip_address": ip_address,
            "reason": reason,
            "blocked_at": datetime.now().isoformat(),
            "unblock_at": datetime.fromtimestamp(time.time() + duration).isoformat(),
        }

        self.blocked_ips.add(ip_address)

        self.log_security_event("ip_blocked", block_info, ip_address, "warning")

        security_logger.warning(f"IP {ip_address} bloquée: {reason}")

    def is_ip_blocked(self, ip_address: str) -> bool:
        """Vérifie si une IP est bloquée"""
        return ip_address in self.blocked_ips

    def check_origin_security(self, origin: str, ip_address: str = "unknown") -> bool:
        """Vérifie la sécurité de l'origine de la requête"""
        if not origin:
            return True  # Pas d'origine = OK (requête directe)

        # Extraire le domaine de l'origine
        try:
            domain = origin.split("://")[1].split("/")[0].split(":")[0]
        except (IndexError, AttributeError):
            domain = origin

        # Vérifier si l'origine est autorisée
        is_allowed = any(
            allowed in domain for allowed in self.security_config["allowed_origins"]
        )

        if not is_allowed:
            self.log_security_event(
                "unauthorized_origin",
                {
                    "origin": origin,
                    "domain": domain,
                    "allowed_origins": self.security_config["allowed_origins"],
                },
                ip_address,
                "warning",
            )

        return is_allowed

    def get_security_report(self) -> Dict[str, Any]:
        """Génère un rapport de sécurité"""
        now = datetime.now()

        # Statistiques des dernières 24h
        last_24h = now.timestamp() - 86400
        recent_events = [
            event
            for event in self.security_events
            if datetime.fromisoformat(event["timestamp"]).timestamp() > last_24h
        ]

        # Compter par type d'événement
        event_counts = {}
        for event in recent_events:
            event_type = event["event_type"]
            event_counts[event_type] = event_counts.get(event_type, 0) + 1

        return {
            "total_events_24h": len(recent_events),
            "blocked_ips_count": len(self.blocked_ips),
            "suspicious_activities_count": len(self.suspicious_activities),
            "rate_limit_violations_count": len(self.rate_limit_violations),
            "event_counts": event_counts,
            "security_status": "healthy" if len(recent_events) < 100 else "attention",
            "last_update": now.isoformat(),
        }

    def cleanup_old_data(self):
        """Nettoie les anciennes données de sécurité"""
        now = datetime.now()
        cutoff_time = now.timestamp() - 86400 * 7  # 7 jours

        # Nettoyer les événements anciens
        self.security_events = [
            event
            for event in self.security_events
            if datetime.fromisoformat(event["timestamp"]).timestamp() > cutoff_time
        ]

        # Nettoyer les violations de rate limit anciennes
        self.rate_limit_violations = [
            violation
            for violation in self.rate_limit_violations
            if datetime.fromisoformat(violation["timestamp"]).timestamp() > cutoff_time
        ]

        security_logger.info("Nettoyage des anciennes données de sécurité effectué")


# Instance globale du gestionnaire de sécurité
security_manager = SecurityManager()
