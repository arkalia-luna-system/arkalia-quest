#!/usr/bin/env python3
"""
Optimiseur de performances pour Arkalia Quest
"""

import functools
import gzip
import json
import threading
import time
from datetime import datetime, timedelta
from typing import Any, Callable


class PerformanceOptimizer:
    """Optimiseur de performances avec monitoring et cache"""

    def __init__(self):
        """Initialise l'optimiseur de performances"""
        self.metrics = {
            "api_calls": 0,
            "cache_hits": 0,
            "cache_misses": 0,
            "response_times": [],
            "error_count": 0,
            "start_time": time.time(),
            "compression_savings": 0,
            "cache_size": 0,
        }
        self.lock = threading.RLock()
        self.slow_queries = []
        self.error_log = []
        # Cache optimisé avec TTL
        self.cache = {}
        self.cache_ttl = {}
        self.max_cache_size = 1000  # Limite du cache

    def monitor_performance(self, func_name: str = None):
        """
        Décorateur pour monitorer les performances d'une fonction

        Args:
            func_name: Nom de la fonction (optionnel)
        """

        def decorator(func: Callable) -> Callable:
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                start_time = time.time()
                function_name = func_name or func.__name__

                try:
                    result = func(*args, **kwargs)
                    execution_time = time.time() - start_time

                    with self.lock:
                        self.metrics["api_calls"] += 1
                        self.metrics["response_times"].append(execution_time)

                        # Garder seulement les 1000 derniers temps de réponse
                        if len(self.metrics["response_times"]) > 1000:
                            self.metrics["response_times"] = self.metrics["response_times"][-1000:]

                        # Enregistrer les requêtes lentes (> 1 seconde)
                        if execution_time > 1.0:
                            self.slow_queries.append(
                                {
                                    "function": function_name,
                                    "execution_time": execution_time,
                                    "timestamp": datetime.now().isoformat(),
                                    "args": str(args)[:100],  # Limiter la taille
                                    "kwargs": str(kwargs)[:100],
                                }
                            )

                            # Garder seulement les 100 dernières requêtes lentes
                            if len(self.slow_queries) > 100:
                                self.slow_queries = self.slow_queries[-100:]

                    return result

                except Exception as e:
                    execution_time = time.time() - start_time

                    with self.lock:
                        self.metrics["error_count"] += 1
                        self.error_log.append(
                            {
                                "function": function_name,
                                "error": str(e),
                                "execution_time": execution_time,
                                "timestamp": datetime.now().isoformat(),
                            }
                        )

                        # Garder seulement les 100 dernières erreurs
                        if len(self.error_log) > 100:
                            self.error_log = self.error_log[-100:]

                    raise

            return wrapper

        return decorator

    def compress_response(self, data: Any) -> bytes:
        """
        Compresse une réponse JSON

        Args:
            data: Données à compresser

        Returns:
            Données compressées
        """
        if isinstance(data, (dict, list)):
            json_data = json.dumps(data, ensure_ascii=False)
        else:
            json_data = str(data)

        # Compresser avec gzip
        compressed = gzip.compress(json_data.encode("utf-8"))
        return compressed

    def optimize_database_query(self, query: str, params: tuple = None) -> str:
        """
        Optimise une requête de base de données

        Args:
            query: Requête SQL
            params: Paramètres de la requête

        Returns:
            Requête optimisée
        """
        # Ajouter des index suggérés
        optimizations = []

        if "WHERE" in query.upper():
            optimizations.append("-- Vérifiez que les colonnes WHERE sont indexées")

        if "ORDER BY" in query.upper():
            optimizations.append("-- Considérez un index composite pour ORDER BY")

        if "JOIN" in query.upper():
            optimizations.append("-- Vérifiez que les colonnes JOIN sont indexées")

        if optimizations:
            return query + "\n" + "\n".join(optimizations)

        return query

    def batch_process(
        self, items: list[Any], batch_size: int = 100, process_func: Callable = None
    ) -> list[Any]:
        """
        Traite une liste d'éléments par lots pour optimiser les performances

        Args:
            items: Liste d'éléments à traiter
            batch_size: Taille des lots
            process_func: Fonction de traitement (optionnelle)

        Returns:
            Liste des résultats
        """
        results = []

        for i in range(0, len(items), batch_size):
            batch = items[i : i + batch_size]

            if process_func:
                batch_results = process_func(batch)
                results.extend(batch_results)
            else:
                results.extend(batch)

        return results

    def get_performance_stats(self) -> dict[str, Any]:
        """
        Retourne les statistiques de performance

        Returns:
            Dictionnaire avec les statistiques
        """
        with self.lock:
            uptime = time.time() - self.metrics["start_time"]
            response_times = self.metrics["response_times"]

            avg_response_time = 0
            max_response_time = 0
            min_response_time = 0

            if response_times:
                avg_response_time = sum(response_times) / len(response_times)
                max_response_time = max(response_times)
                min_response_time = min(response_times)

            return {
                "uptime_seconds": round(uptime, 2),
                "uptime_hours": round(uptime / 3600, 2),
                "total_api_calls": self.metrics["api_calls"],
                "calls_per_second": (
                    round(self.metrics["api_calls"] / uptime, 2) if uptime > 0 else 0
                ),
                "average_response_time": round(avg_response_time * 1000, 2),  # en ms
                "max_response_time": round(max_response_time * 1000, 2),  # en ms
                "min_response_time": round(min_response_time * 1000, 2),  # en ms
                "error_count": self.metrics["error_count"],
                "error_rate": (
                    round(self.metrics["error_count"] / self.metrics["api_calls"] * 100, 2)
                    if self.metrics["api_calls"] > 0
                    else 0
                ),
                "slow_queries_count": len(self.slow_queries),
                "recent_errors": len(
                    [
                        e
                        for e in self.error_log
                        if datetime.fromisoformat(e["timestamp"])
                        > datetime.now() - timedelta(hours=1)
                    ]
                ),
            }

    def get_slow_queries(self, limit: int = 10) -> list[dict[str, Any]]:
        """
        Retourne les requêtes les plus lentes

        Args:
            limit: Nombre maximum de requêtes à retourner

        Returns:
            Liste des requêtes lentes
        """
        with self.lock:
            return sorted(self.slow_queries, key=lambda x: x["execution_time"], reverse=True)[
                :limit
            ]

    def get_recent_errors(self, limit: int = 10) -> list[dict[str, Any]]:
        """
        Retourne les erreurs récentes

        Args:
            limit: Nombre maximum d'erreurs à retourner

        Returns:
            Liste des erreurs récentes
        """
        with self.lock:
            return sorted(self.error_log, key=lambda x: x["timestamp"], reverse=True)[:limit]

    def clear_metrics(self):
        """Remet à zéro les métriques"""
        with self.lock:
            self.metrics = {
                "api_calls": 0,
                "cache_hits": 0,
                "cache_misses": 0,
                "response_times": [],
                "error_count": 0,
                "start_time": time.time(),
            }
            self.slow_queries.clear()
            self.error_log.clear()

    def suggest_optimizations(self) -> list[str]:
        """
        Suggère des optimisations basées sur les métriques

        Returns:
            Liste des suggestions d'optimisation
        """
        suggestions = []
        stats = self.get_performance_stats()

        # Vérifier le temps de réponse moyen
        if stats["average_response_time"] > 500:  # > 500ms
            suggestions.append("🚨 Temps de réponse élevé - Considérez l'ajout de cache")

        # Vérifier le taux d'erreur
        if stats["error_rate"] > 5:  # > 5%
            suggestions.append("🚨 Taux d'erreur élevé - Vérifiez la gestion d'erreurs")

        # Vérifier les requêtes lentes
        if stats["slow_queries_count"] > 10:
            suggestions.append(
                "⚠️ Nombreuses requêtes lentes - Optimisez les requêtes de base de données"
            )

        # Vérifier l'utilisation du cache
        total_cache_requests = self.metrics["cache_hits"] + self.metrics["cache_misses"]
        if total_cache_requests > 0:
            cache_hit_rate = self.metrics["cache_hits"] / total_cache_requests * 100
            if cache_hit_rate < 70:  # < 70%
                suggestions.append("⚠️ Taux de cache faible - Améliorez la stratégie de cache")

        # Vérifier la charge
        if stats["calls_per_second"] > 50:
            suggestions.append("💡 Charge élevée - Considérez la mise en place d'un load balancer")

        return suggestions

    def get_cached_data(self, key: str, ttl_seconds: int = 300):
        """
        Récupère des données du cache avec TTL

        Args:
            key: Clé du cache
            ttl_seconds: Durée de vie en secondes

        Returns:
            Données mises en cache ou None
        """
        with self.lock:
            if key in self.cache:
                if time.time() - self.cache_ttl.get(key, 0) < ttl_seconds:
                    self.metrics["cache_hits"] += 1
                    return self.cache[key]
                else:
                    # Expiré, supprimer
                    del self.cache[key]
                    del self.cache_ttl[key]

            self.metrics["cache_misses"] += 1
            return None

    def set_cached_data(self, key: str, data: Any, ttl_seconds: int = 300):
        """
        Met des données en cache avec TTL

        Args:
            key: Clé du cache
            data: Données à mettre en cache
            ttl_seconds: Durée de vie en secondes
        """
        with self.lock:
            # Nettoyer le cache si nécessaire
            if len(self.cache) >= self.max_cache_size:
                # Supprimer les entrées les plus anciennes
                oldest_key = min(self.cache_ttl.keys(), key=lambda k: self.cache_ttl[k])
                del self.cache[oldest_key]
                del self.cache_ttl[oldest_key]

            self.cache[key] = data
            self.cache_ttl[key] = time.time()
            self.metrics["cache_size"] = len(self.cache)

    def compress_data(self, data: str) -> bytes:
        """
        Compresse des données avec gzip

        Args:
            data: Données à compresser

        Returns:
            Données compressées
        """
        if isinstance(data, str):
            data = data.encode("utf-8")

        compressed = gzip.compress(data)
        savings = len(data) - len(compressed)
        self.metrics["compression_savings"] += savings

        return compressed

    def clear_cache(self):
        """Vide le cache"""
        with self.lock:
            self.cache.clear()
            self.cache_ttl.clear()
            self.metrics["cache_size"] = 0


# Instance globale de l'optimiseur de performances
performance_optimizer = PerformanceOptimizer()
