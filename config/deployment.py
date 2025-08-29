"""
Configuration de déploiement d'Arkalia Quest
"""

import os
from typing import Any, Dict


class DeploymentConfig:
    """Configuration pour le déploiement"""

    # Configuration Docker
    DOCKER_IMAGE_NAME = "arkalia-quest"
    DOCKER_IMAGE_TAG = "latest"
    DOCKER_PORT = 5001

    # Configuration Kubernetes
    K8S_NAMESPACE = "arkalia"
    K8S_REPLICAS = 3
    K8S_RESOURCES = {
        "requests": {"cpu": "100m", "memory": "128Mi"},
        "limits": {"cpu": "500m", "memory": "512Mi"},
    }

    # Configuration des environnements
    ENVIRONMENTS = {
        "development": {
            "host": "localhost",
            "port": 5001,
            "debug": True,
            "database": "sqlite:///data/database/dev_arkalia.db",
        },
        "staging": {
            "host": "0.0.0.0",
            "port": 5001,
            "debug": False,
            "database": "sqlite:///data/database/staging_arkalia.db",
        },
        "production": {
            "host": "0.0.0.0",
            "port": 5001,
            "debug": False,
            "database": "sqlite:///data/database/production_arkalia.db",
        },
    }

    # Configuration des services externes
    EXTERNAL_SERVICES = {
        "redis": {
            "url": os.getenv("REDIS_URL", "redis://localhost:6379"),
            "enabled": os.getenv("REDIS_ENABLED", "False").lower() == "true",
        },
        "sentry": {
            "dsn": os.getenv("SENTRY_DSN", ""),
            "enabled": bool(os.getenv("SENTRY_DSN")),
        },
        "monitoring": {
            "enabled": os.getenv("ENABLE_MONITORING", "False").lower() == "true",
            "port": int(os.getenv("MONITORING_PORT", "9090")),
        },
    }

    # Configuration de la sécurité
    SECURITY_CONFIG = {
        "cors_origins": os.getenv("CORS_ORIGINS", "*").split(","),
        "rate_limit": {
            "enabled": os.getenv("RATE_LIMIT_ENABLED", "True").lower() == "true",
            "requests_per_minute": int(os.getenv("RATE_LIMIT_REQUESTS", "100")),
        },
        "ssl": {
            "enabled": os.getenv("SSL_ENABLED", "False").lower() == "true",
            "cert_file": os.getenv("SSL_CERT_FILE", ""),
            "key_file": os.getenv("SSL_KEY_FILE", ""),
        },
    }

    @classmethod
    def get_environment_config(cls, env: str) -> Dict[str, Any]:
        """Retourne la configuration pour un environnement spécifique"""
        return cls.ENVIRONMENTS.get(env, cls.ENVIRONMENTS["development"])

    @classmethod
    def get_docker_config(cls) -> Dict[str, Any]:
        """Retourne la configuration Docker"""
        return {
            "image_name": cls.DOCKER_IMAGE_NAME,
            "image_tag": cls.DOCKER_IMAGE_TAG,
            "port": cls.DOCKER_PORT,
        }

    @classmethod
    def get_k8s_config(cls) -> Dict[str, Any]:
        """Retourne la configuration Kubernetes"""
        return {
            "namespace": cls.K8S_NAMESPACE,
            "replicas": cls.K8S_REPLICAS,
            "resources": cls.K8S_RESOURCES,
        }


# Configuration de déploiement par défaut
deployment_config = DeploymentConfig()
