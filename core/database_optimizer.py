#!/usr/bin/env python3
"""
Optimiseur de base de données pour Arkalia Quest
"""

import logging
import sqlite3
import threading
import time
from contextlib import contextmanager
from typing import Optional


class DatabaseOptimizer:
    """Optimiseur de base de données avec pool de connexions et cache"""

    def __init__(self, db_path: str = "data/arkalia_quest.db"):
        """
        Initialise l'optimiseur de base de données

        Args:
            db_path: Chemin vers la base de données SQLite
        """
        self.db_path = db_path
        self.connection_pool = []
        self.pool_size = 10
        self.pool_lock = threading.Lock()
        self.query_cache = {}
        self.cache_ttl = 300  # 5 minutes
        self.stats = {
            "queries_executed": 0,
            "cache_hits": 0,
            "cache_misses": 0,
            "connection_creates": 0,
            "connection_reuses": 0,
            "slow_queries": 0,
            "prepared_queries": 0,
            "batch_operations": 0,
        }

        # Initialiser le pool de connexions
        self._initialize_connection_pool()

        # Optimiser la base de données
        self._optimize_database()

    def _initialize_connection_pool(self):
        """Initialise le pool de connexions"""
        with self.pool_lock:
            for _ in range(self.pool_size):
                conn = self._create_connection()
                self.connection_pool.append(conn)
                self.stats["connection_creates"] += 1

    def _create_connection(self) -> sqlite3.Connection:
        """Crée une nouvelle connexion optimisée"""
        conn = sqlite3.connect(self.db_path, check_same_thread=False, timeout=30.0)

        # Optimisations SQLite
        conn.execute("PRAGMA journal_mode=WAL")
        conn.execute("PRAGMA synchronous=NORMAL")
        conn.execute("PRAGMA cache_size=10000")
        conn.execute("PRAGMA temp_store=MEMORY")
        conn.execute("PRAGMA mmap_size=268435456")  # 256MB
        conn.execute("PRAGMA optimize")

        # Activer les clés étrangères
        conn.execute("PRAGMA foreign_keys=ON")

        return conn

    @contextmanager
    def get_connection(self):
        """Context manager pour obtenir une connexion du pool"""
        conn = None
        try:
            with self.pool_lock:
                if self.connection_pool:
                    conn = self.connection_pool.pop()
                    self.stats["connection_reuses"] += 1
                else:
                    conn = self._create_connection()
                    self.stats["connection_creates"] += 1

            yield conn

        finally:
            if conn:
                with self.pool_lock:
                    if len(self.connection_pool) < self.pool_size:
                        self.connection_pool.append(conn)
                    else:
                        conn.close()

    def _optimize_database(self):
        """Optimise la base de données avec des index et des vues"""
        with self.get_connection() as conn:
            # Créer les index pour optimiser les requêtes
            indexes = [
                "CREATE INDEX IF NOT EXISTS idx_users_username ON users(username)",
                "CREATE INDEX IF NOT EXISTS idx_users_email ON users(email)",
                "CREATE INDEX IF NOT EXISTS idx_users_score ON users(score)",
                "CREATE INDEX IF NOT EXISTS idx_users_level ON users(level)",
                "CREATE INDEX IF NOT EXISTS idx_users_created_at ON users(created_at)",
                "CREATE INDEX IF NOT EXISTS idx_games_user_id ON games(user_id)",
                "CREATE INDEX IF NOT EXISTS idx_games_type ON games(type)",
                "CREATE INDEX IF NOT EXISTS idx_games_score ON games(score)",
                "CREATE INDEX IF NOT EXISTS idx_games_created_at ON games(created_at)",
                "CREATE INDEX IF NOT EXISTS idx_badges_user_id ON badges(user_id)",
                "CREATE INDEX IF NOT EXISTS idx_badges_type ON badges(type)",
                "CREATE INDEX IF NOT EXISTS idx_badges_earned_at ON badges(earned_at)",
                "CREATE INDEX IF NOT EXISTS idx_missions_user_id ON missions(user_id)",
                "CREATE INDEX IF NOT EXISTS idx_missions_status ON missions(status)",
                "CREATE INDEX IF NOT EXISTS idx_missions_created_at ON missions(created_at)",
                "CREATE INDEX IF NOT EXISTS idx_leaderboard_score ON leaderboard(score)",
                "CREATE INDEX IF NOT EXISTS idx_leaderboard_updated_at ON leaderboard(updated_at)",
            ]

            for index_sql in indexes:
                try:
                    conn.execute(index_sql)
                except sqlite3.Error as e:
                    logging.warning(f"Erreur création index: {e}")

            conn.commit()

    def execute_query(
        self, query: str, params: tuple = None, cache_key: str = None
    ) -> list[dict]:
        """
        Exécute une requête avec cache et monitoring

        Args:
            query: Requête SQL
            params: Paramètres de la requête
            cache_key: Clé de cache (optionnelle)

        Returns:
            Résultats de la requête
        """
        start_time = time.time()

        # Vérifier le cache
        if cache_key and cache_key in self.query_cache:
            cache_entry = self.query_cache[cache_key]
            if time.time() - cache_entry["timestamp"] < self.cache_ttl:
                self.stats["cache_hits"] += 1
                return cache_entry["data"]
            else:
                del self.query_cache[cache_key]

        self.stats["cache_misses"] += 1

        # Exécuter la requête
        with self.get_connection() as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()

            try:
                if params:
                    cursor.execute(query, params)
                else:
                    cursor.execute(query)

                results = [dict(row) for row in cursor.fetchall()]

                # Mettre en cache si demandé
                if cache_key:
                    self.query_cache[cache_key] = {
                        "data": results,
                        "timestamp": time.time(),
                    }

                self.stats["queries_executed"] += 1

                # Vérifier si la requête est lente
                execution_time = time.time() - start_time
                if execution_time > 1.0:  # > 1 seconde
                    self.stats["slow_queries"] += 1
                    logging.warning(
                        f"Requête lente détectée: {execution_time:.2f}s - {query[:100]}"
                    )

                return results

            except sqlite3.Error as e:
                logging.error(f"Erreur requête SQL: {e}")
                raise

    def execute_update(self, query: str, params: tuple = None) -> int:
        """
        Exécute une requête de mise à jour

        Args:
            query: Requête SQL
            params: Paramètres de la requête

        Returns:
            Nombre de lignes affectées
        """
        start_time = time.time()

        with self.get_connection() as conn:
            cursor = conn.cursor()

            try:
                if params:
                    cursor.execute(query, params)
                else:
                    cursor.execute(query)

                conn.commit()

                # Invalider le cache pour les requêtes de mise à jour
                self._invalidate_cache()

                self.stats["queries_executed"] += 1

                # Vérifier si la requête est lente
                execution_time = time.time() - start_time
                if execution_time > 1.0:
                    self.stats["slow_queries"] += 1
                    logging.warning(
                        f"Requête lente détectée: {execution_time:.2f}s - {query[:100]}"
                    )

                return cursor.rowcount

            except sqlite3.Error as e:
                conn.rollback()
                logging.error(f"Erreur requête SQL: {e}")
                raise

    def _invalidate_cache(self):
        """Invalide le cache des requêtes"""
        self.query_cache.clear()

    def get_user_profile(self, user_id: str) -> Optional[dict]:
        """Récupère le profil utilisateur avec cache"""
        cache_key = f"user_profile:{user_id}"

        query = """
            SELECT u.*,
                   COUNT(DISTINCT g.id) as games_played,
                   COUNT(DISTINCT b.id) as badges_earned,
                   COUNT(DISTINCT m.id) as missions_completed
            FROM users u
            LEFT JOIN games g ON u.id = g.user_id
            LEFT JOIN badges b ON u.id = b.user_id
            LEFT JOIN missions m ON u.id = m.user_id
            WHERE u.id = ?
            GROUP BY u.id
        """

        results = self.execute_query(query, (user_id,), cache_key)
        return results[0] if results else None

    def get_leaderboard(self, limit: int = 10) -> list[dict]:
        """Récupère le classement avec cache"""
        cache_key = f"leaderboard:{limit}"

        query = """
            SELECT u.username, u.score, u.level, u.avatar,
                   COUNT(DISTINCT b.id) as badges_count,
                   COUNT(DISTINCT g.id) as games_played
            FROM users u
            LEFT JOIN badges b ON u.id = b.user_id
            LEFT JOIN games g ON u.id = g.user_id
            GROUP BY u.id
            ORDER BY u.score DESC, u.level DESC
            LIMIT ?
        """

        return self.execute_query(query, (limit,), cache_key)

    def get_game_stats(self, user_id: str = None) -> dict:
        """Récupère les statistiques des jeux"""
        cache_key = f"game_stats:{user_id or 'global'}"

        if user_id:
            query = """
                SELECT
                    type,
                    COUNT(*) as count,
                    AVG(score) as avg_score,
                    MAX(score) as max_score,
                    MIN(score) as min_score
                FROM games
                WHERE user_id = ?
                GROUP BY type
            """
            params = (user_id,)
        else:
            query = """
                SELECT
                    type,
                    COUNT(*) as count,
                    AVG(score) as avg_score,
                    MAX(score) as max_score,
                    MIN(score) as min_score
                FROM games
                GROUP BY type
            """
            params = None

        results = self.execute_query(query, params, cache_key)

        stats = {}
        for row in results:
            stats[row["type"]] = {
                "count": row["count"],
                "avg_score": round(row["avg_score"] or 0, 2),
                "max_score": row["max_score"] or 0,
                "min_score": row["min_score"] or 0,
            }

        return stats

    def get_performance_stats(self) -> dict:
        """Retourne les statistiques de performance de la base de données"""
        with self.get_connection() as conn:
            # Statistiques SQLite
            pragma_stats = {}
            pragmas = [
                "cache_size",
                "page_count",
                "page_size",
                "freelist_count",
                "synchronous",
                "journal_mode",
                "temp_store",
            ]

            for pragma in pragmas:
                try:
                    cursor = conn.execute(f"PRAGMA {pragma}")
                    result = cursor.fetchone()
                    pragma_stats[pragma] = result[0] if result else None
                except sqlite3.Error:
                    pragma_stats[pragma] = None

            # Statistiques des tables
            table_stats = {}
            tables = ["users", "games", "badges", "missions", "leaderboard"]

            for table in tables:
                try:
                    cursor = conn.execute("SELECT COUNT(*) FROM ?", (table,))
                    count = cursor.fetchone()[0]
                    table_stats[table] = count
                except sqlite3.Error:
                    table_stats[table] = 0

            return {
                "connection_pool_size": len(self.connection_pool),
                "cache_size": len(self.query_cache),
                "stats": self.stats,
                "pragma_stats": pragma_stats,
                "table_stats": table_stats,
            }

    def optimize_database(self):
        """Optimise la base de données"""
        with self.get_connection() as conn:
            # Analyser les tables
            conn.execute("ANALYZE")

            # Optimiser
            conn.execute("PRAGMA optimize")

            # Vérifier l'intégrité
            cursor = conn.execute("PRAGMA integrity_check")
            integrity_result = cursor.fetchone()[0]

            if integrity_result != "ok":
                logging.warning(f"Problème d'intégrité détecté: {integrity_result}")

            conn.commit()

    def execute_prepared_query(
        self, query: str, params: tuple = (), cache_key: str = None
    ):
        """
        Exécute une requête préparée avec cache

        Args:
            query: Requête SQL préparée
            params: Paramètres de la requête
            cache_key: Clé de cache (optionnel)

        Returns:
            Résultats de la requête
        """
        # Vérifier le cache
        if cache_key and cache_key in self.query_cache:
            if time.time() - self.query_cache[cache_key]["timestamp"] < self.cache_ttl:
                self.stats["cache_hits"] += 1
                return self.query_cache[cache_key]["data"]
            else:
                del self.query_cache[cache_key]

        self.stats["cache_misses"] += 1

        # Exécuter la requête
        with self.get_connection() as conn:
            start_time = time.time()
            cursor = conn.cursor()
            cursor.execute(query, params)
            results = cursor.fetchall()
            execution_time = time.time() - start_time

            # Mettre en cache si nécessaire
            if cache_key and execution_time < 1.0:  # Seulement les requêtes rapides
                self.query_cache[cache_key] = {
                    "data": results,
                    "timestamp": time.time(),
                }

            self.stats["queries_executed"] += 1
            self.stats["prepared_queries"] += 1

            if execution_time > 0.1:  # Requête lente
                self.stats["slow_queries"] += 1
                logging.warning(
                    f"Requête lente détectée: {execution_time:.3f}s - {query[:50]}..."
                )

            return results

    def execute_batch_operations(self, operations: list):
        """
        Exécute plusieurs opérations en lot pour optimiser les performances

        Args:
            operations: Liste de tuples (query, params)
        """
        with self.get_connection() as conn:
            start_time = time.time()
            cursor = conn.cursor()

            try:
                for query, params in operations:
                    cursor.execute(query, params)

                conn.commit()
                self.stats["batch_operations"] += 1
                self.stats["queries_executed"] += len(operations)

                execution_time = time.time() - start_time
                logging.info(
                    f"Batch de {len(operations)} opérations exécuté en {execution_time:.3f}s"
                )

            except sqlite3.Error as e:
                conn.rollback()
                logging.error(f"Erreur lors de l'exécution du batch: {e}")
                raise

    def close_all_connections(self):
        """Ferme toutes les connexions"""
        with self.pool_lock:
            for conn in self.connection_pool:
                try:
                    conn.close()
                except sqlite3.Error:
                    pass
            self.connection_pool.clear()


# Instance globale de l'optimiseur de base de données
database_optimizer = DatabaseOptimizer()
