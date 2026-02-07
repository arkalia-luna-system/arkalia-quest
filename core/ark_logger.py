"""
Module de compatibilité pour les imports core.ark_logger.
Délègue vers utils.logger pour éviter les erreurs d'import.
"""

from utils.logger import (
    game_logger,
    performance_logger,
    security_logger,
)

__all__ = ["game_logger", "security_logger", "performance_logger"]
