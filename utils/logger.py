"""
Système de logging professionnel pour Arkalia Quest
Version 2.0.0
"""

from __future__ import annotations

import json
import logging
import logging.config
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

# Configuration de logging simplifiée
LOGS_DIR = Path("logs")
LOGS_DIR.mkdir(exist_ok=True)

LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "detailed": {
            "format": "[%(asctime)s] %(levelname)s [%(name)s] %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
        "simple": {"format": "%(levelname)s [%(name)s] %(message)s"},
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "level": "INFO",
            "formatter": "simple",
            "stream": "ext://sys.stdout",
        },
        "file": {
            "class": "logging.FileHandler",
            "level": "DEBUG",
            "formatter": "detailed",
            "filename": str(LOGS_DIR / "arkalia.log"),
            "mode": "a",
            "encoding": "utf-8",
        },
        "error_file": {
            "class": "logging.FileHandler",
            "level": "ERROR",
            "formatter": "detailed",
            "filename": str(LOGS_DIR / "error.log"),
            "mode": "a",
            "encoding": "utf-8",
        },
    },
    "loggers": {
        "arkalia_quest": {
            "level": "DEBUG",
            "handlers": ["console", "file", "error_file"],
            "propagate": False,
        },
        "arkalia_game": {
            "level": "INFO",
            "handlers": ["console", "file"],
            "propagate": False,
        },
        "arkalia_security": {
            "level": "WARNING",
            "handlers": ["console", "file", "error_file"],
            "propagate": False,
        },
        "arkalia_performance": {
            "level": "INFO",
            "handlers": ["console", "file"],
            "propagate": False,
        },
    },
    "root": {"level": "INFO", "handlers": ["console"]},
}


class ArkaliaLogger:
    """Logger personnalisé pour Arkalia Quest"""

    def __init__(self, name: str = "arkalia_quest"):
        self.name = name
        self.logger = None
        self._setup_logging()

    def _setup_logging(self):
        """Configure le système de logging"""
        # Configuration du logging
        logging.config.dictConfig(LOGGING_CONFIG)
        self.logger = logging.getLogger(self.name)

    def info(self, message: str, extra: dict[str, Any] | None = None):
        """Log un message d'information"""
        self._log("INFO", message, extra)

    def warning(self, message: str, extra: dict[str, Any] | None = None):
        """Log un avertissement"""
        self._log("WARNING", message, extra)

    def error(
        self,
        message: str,
        extra: dict[str, Any] | None = None,
        *,
        exc_info: bool = False,
    ):
        """Log une erreur"""
        self._log("ERROR", message, extra, exc_info=exc_info)

    def debug(self, message: str, extra: dict[str, Any] | None = None):
        """Log un message de debug"""
        self._log("DEBUG", message, extra)

    def _log(
        self,
        level: str,
        message: str,
        extra: dict[str, Any] | None = None,
        *,
        exc_info: bool = False,
    ):
        """Méthode interne de logging"""
        if extra is None:
            extra = {}

        # Ajout d'informations contextuelles
        extra.update(
            {
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "module_name": self.name,
            }
        )

        if self.logger is not None:
            if level == "INFO":
                self.logger.info(message, extra=extra)
            elif level == "WARNING":
                self.logger.warning(message, extra=extra)
            elif level == "ERROR":
                self.logger.error(message, extra=extra, exc_info=exc_info)
            elif level == "DEBUG":
                self.logger.debug(message, extra=extra)


class GameLogger(ArkaliaLogger):
    """Logger spécialisé pour les événements de jeu"""

    def __init__(self):
        super().__init__("arkalia_game")

    def player_action(self, action: str, player_id: str = "default", **kwargs):
        """Log une action du joueur"""
        extra = {
            "event_type": "player_action",
            "action": action,
            "player_id": player_id,
            **kwargs,
        }
        self.info(f"Action joueur: {action}", extra)

    def mission_completed(self, mission_id: str, player_id: str = "default", score: int = 0):
        """Log la completion d'une mission"""
        extra = {
            "event_type": "mission_completed",
            "mission_id": mission_id,
            "player_id": player_id,
            "score": score,
        }
        self.info(f"Mission complétée: {mission_id}", extra)

    def personality_detected(self, personality_type: str, player_id: str = "default"):
        """Log la détection de personnalité"""
        extra = {
            "event_type": "personality_detected",
            "personality_type": personality_type,
            "player_id": player_id,
        }
        self.info(f"Personnalité détectée: {personality_type}", extra)

    def badge_earned(self, badge_name: str, player_id: str = "default"):
        """Log l'obtention d'un badge"""
        extra = {
            "event_type": "badge_earned",
            "badge_name": badge_name,
            "player_id": player_id,
        }
        self.info(f"Badge obtenu: {badge_name}", extra)

    def command_executed(self, command: str, *, success: bool, player_id: str = "default"):
        """Log l'exécution d'une commande"""
        extra = {
            "event_type": "command_executed",
            "command": command,
            "success": success,
            "player_id": player_id,
        }
        level = "INFO" if success else "WARNING"
        message = f"Commande exécutée: {command} ({'succès' if success else 'échec'})"
        self._log(level, message, extra)


class SecurityLogger(ArkaliaLogger):
    """Logger spécialisé pour la sécurité"""

    def __init__(self):
        super().__init__("arkalia_security")

    def unauthorized_command(self, command: str, ip_address: str = "unknown"):
        """Log une tentative de commande non autorisée"""
        extra = {
            "event_type": "unauthorized_command",
            "command": command,
            "ip_address": ip_address,
            "security_level": "warning",
        }
        self.warning(f"Commande non autorisée tentée: {command}", extra)

    def rate_limit_exceeded(self, ip_address: str = "unknown", limit_type: str = "commands"):
        """Log un dépassement de limite de taux"""
        extra = {
            "event_type": "rate_limit_exceeded",
            "ip_address": ip_address,
            "limit_type": limit_type,
            "security_level": "warning",
        }
        self.warning(f"Limite de taux dépassée: {limit_type}", extra)

    def suspicious_activity(self, activity_type: str, details: str, ip_address: str = "unknown"):
        """Log une activité suspecte"""
        extra = {
            "event_type": "suspicious_activity",
            "activity_type": activity_type,
            "details": details,
            "ip_address": ip_address,
            "security_level": "high",
        }
        self.error(f"Activité suspecte détectée: {activity_type}", extra)


class PerformanceLogger(ArkaliaLogger):
    """Logger spécialisé pour les performances"""

    def __init__(self):
        super().__init__("arkalia_performance")

    def response_time(self, endpoint: str, response_time: float, status_code: int = 200):
        """Log le temps de réponse d'un endpoint"""
        extra = {
            "event_type": "response_time",
            "endpoint": endpoint,
            "response_time": response_time,
            "status_code": status_code,
        }
        self.info(f"Temps de réponse {endpoint}: {response_time:.3f}s", extra)

    def memory_usage(self, memory_mb: float):
        """Log l'utilisation mémoire"""
        extra = {"event_type": "memory_usage", "memory_mb": memory_mb}
        self.info(f"Utilisation mémoire: {memory_mb:.2f}MB", extra)

    def database_query(self, query_type: str, execution_time: float, *, success: bool = True):
        """Log une requête base de données"""
        extra = {
            "event_type": "database_query",
            "query_type": query_type,
            "execution_time": execution_time,
            "success": success,
        }
        level = "INFO" if success else "ERROR"
        message = f"Requête DB {query_type}: {execution_time:.3f}s"
        self._log(level, message, extra)


# Instances globales
game_logger = GameLogger()
security_logger = SecurityLogger()
performance_logger = PerformanceLogger()


def log_exception(func):
    """Décorateur pour logger les exceptions"""

    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            game_logger.exception(f"Exception dans {func.__name__}: {e!s}")
            raise

    return wrapper


def log_function_call(func):
    """Décorateur pour logger les appels de fonction"""

    def wrapper(*args, **kwargs):
        game_logger.debug(f"Appel de fonction: {func.__name__}")
        try:
            result = func(*args, **kwargs)
            game_logger.debug(f"Fonction {func.__name__} terminée avec succès")
        except Exception as e:
            game_logger.exception(f"Erreur dans {func.__name__}: {e!s}")
            raise
        else:
            return result

    return wrapper


def export_logs_to_json(output_file: str | None = None):
    """Exporte les logs en JSON"""
    if output_file is None:
        output_file = str(
            LOGS_DIR / f"logs_export_{datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S')}.json"
        )

    logs_data = []

    # Lire le fichier de log principal
    log_file = LOGS_DIR / "arkalia.log"
    if log_file.exists():
        with log_file.open(encoding="utf-8", mode="a") as f:
            for line in f:
                if line.strip():
                    logs_data.append(
                        {
                            "timestamp": datetime.now(timezone.utc).isoformat(),
                            "log_entry": line.strip(),
                        },
                    )

    # Sauvegarder en JSON
    with Path(output_file).open("w", encoding="utf-8") as f:
        json.dump(logs_data, f, indent=2, ensure_ascii=False)

    return output_file


def cleanup_old_logs(days_to_keep: int = 30):
    """Nettoie les anciens logs"""
    cutoff_date = datetime.now(timezone.utc).timestamp() - (days_to_keep * 24 * 60 * 60)

    for log_file in LOGS_DIR.glob("*.log"):
        if log_file.stat().st_mtime < cutoff_date:
            log_file.unlink()
            game_logger.info(f"Ancien log supprimé: {log_file.name}")
