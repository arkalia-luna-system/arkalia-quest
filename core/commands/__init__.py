"""
Module de commandes Arkalia Quest
Organisation modulaire des commandes par catégorie
"""

from .basic_commands import BasicCommands
from .game_commands import GameCommands
from .luna_commands import LunaCommands
from .system_commands import SystemCommands
from .easter_egg_commands import EasterEggCommands

__all__ = [
    "BasicCommands",
    "GameCommands",
    "LunaCommands",
    "SystemCommands",
    "EasterEggCommands",
]
