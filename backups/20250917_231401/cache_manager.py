#!/usr/bin/env python3
"""
Gestionnaire de cache pour optimiser les performances d'Arkalia Quest
"""

import threading
import time
from typing import Any, Optional


class CacheManager:
    """Gestionnaire de cache en mémoire pour optimiser les performances"""

    def __init__(self, default_ttl: int = 300):
        """
        Initialise le gestionnaire de cache

        Args:
            default_ttl: Durée de vie par défaut en secondes (5 minutes)
        """
        self.cache: dict[str, dict[str, Any]] = {}
        self.default_ttl = default_ttl
        self.lock = threading.RLock()
        self.stats = {"hits": 0, "misses": 0, "sets": 0, "deletes": 0, "expired": 0}

    def _is_expired(self, cache_entry: dict[str, Any]) -> bool:
        """Vérifie si une entrée de cache est expirée"""
        return time.time() > cache_entry.get("expires_at", 0)

    def _cleanup_expired(self):
        """Nettoie les entrées expirées"""
        current_time = time.time()
        expired_keys = []

        for key, entry in self.cache.items():
            if current_time > entry.get("expires_at", 0):
                expired_keys.append(key)

        for key in expired_keys:
            del self.cache[key]
            self.stats["expired"] += 1

    def get(self, key: str) -> Optional[Any]:
        """
        Récupère une valeur du cache

        Args:
            key: Clé de la valeur à récupérer

        Returns:
            La valeur mise en cache ou None si non trouvée/expirée
        """
        with self.lock:
            if key not in self.cache:
                self.stats["misses"] += 1
                return None

            entry = self.cache[key]
            if self._is_expired(entry):
                del self.cache[key]
                self.stats["misses"] += 1
                self.stats["expired"] += 1
                return None

            self.stats["hits"] += 1
            return entry["value"]

    def set(self, key: str, value: Any, ttl: Optional[int] = None) -> None:
        """
        Stocke une valeur dans le cache

        Args:
            key: Clé de la valeur
            value: Valeur à stocker
            ttl: Durée de vie en secondes (utilise default_ttl si None)
        """
        with self.lock:
            if ttl is None:
                ttl = self.default_ttl

            self.cache[key] = {
                "value": value,
                "expires_at": time.time() + ttl,
                "created_at": time.time(),
            }
            self.stats["sets"] += 1

    def delete(self, key: str) -> bool:
        """
        Supprime une valeur du cache

        Args:
            key: Clé de la valeur à supprimer

        Returns:
            True si la clé existait, False sinon
        """
        with self.lock:
            if key in self.cache:
                del self.cache[key]
                self.stats["deletes"] += 1
                return True
            return False

    def clear(self) -> None:
        """Vide complètement le cache"""
        with self.lock:
            self.cache.clear()
            self.stats["deletes"] += len(self.cache)

    def get_stats(self) -> dict[str, Any]:
        """
        Retourne les statistiques du cache

        Returns:
            Dictionnaire avec les statistiques
        """
        with self.lock:
            total_requests = self.stats["hits"] + self.stats["misses"]
            hit_rate = (self.stats["hits"] / total_requests * 100) if total_requests > 0 else 0

            return {
                "cache_size": len(self.cache),
                "hit_rate": round(hit_rate, 2),
                "total_requests": total_requests,
                "hits": self.stats["hits"],
                "misses": self.stats["misses"],
                "sets": self.stats["sets"],
                "deletes": self.stats["deletes"],
                "expired": self.stats["expired"],
            }

    def get_user_profile(self, user_id: str) -> Optional[dict[str, Any]]:
        """
        Récupère le profil utilisateur depuis le cache

        Args:
            user_id: ID de l'utilisateur

        Returns:
            Profil utilisateur ou None
        """
        return self.get(f"user_profile:{user_id}")

    def set_user_profile(self, user_id: str, profile: dict[str, Any], ttl: int = 600) -> None:
        """
        Met en cache le profil utilisateur

        Args:
            user_id: ID de l'utilisateur
            profile: Profil utilisateur
            ttl: Durée de vie en secondes (10 minutes par défaut)
        """
        self.set(f"user_profile:{user_id}", profile, ttl)

    def get_game_data(self, game_id: str) -> Optional[dict[str, Any]]:
        """
        Récupère les données d'un jeu depuis le cache

        Args:
            game_id: ID du jeu

        Returns:
            Données du jeu ou None
        """
        return self.get(f"game_data:{game_id}")

    def set_game_data(self, game_id: str, game_data: dict[str, Any], ttl: int = 1800) -> None:
        """
        Met en cache les données d'un jeu

        Args:
            game_id: ID du jeu
            game_data: Données du jeu
            ttl: Durée de vie en secondes (30 minutes par défaut)
        """
        self.set(f"game_data:{game_id}", game_data, ttl)

    def get_leaderboard(self, leaderboard_type: str = "global") -> Optional[dict[str, Any]]:
        """
        Récupère le classement depuis le cache

        Args:
            leaderboard_type: Type de classement

        Returns:
            Données du classement ou None
        """
        return self.get(f"leaderboard:{leaderboard_type}")

    def set_leaderboard(self, leaderboard_type: str, data: dict[str, Any], ttl: int = 300) -> None:
        """
        Met en cache le classement

        Args:
            leaderboard_type: Type de classement
            data: Données du classement
            ttl: Durée de vie en secondes (5 minutes par défaut)
        """
        self.set(f"leaderboard:{leaderboard_type}", data, ttl)

    def invalidate_user_cache(self, user_id: str) -> None:
        """
        Invalide le cache d'un utilisateur spécifique

        Args:
            user_id: ID de l'utilisateur
        """
        self.delete(f"user_profile:{user_id}")
        # Invalider aussi les classements car ils peuvent changer
        self.delete("leaderboard:global")
        self.delete("leaderboard:weekly")
        self.delete("leaderboard:monthly")


# Instance globale du gestionnaire de cache
cache_manager = CacheManager(default_ttl=300)
