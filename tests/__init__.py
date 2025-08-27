"""
🧪 Module de tests Arkalia Quest - Structure organisée et modulaire
Organisation des tests par catégories et priorités
"""

# Structure des tests par catégories
TEST_CATEGORIES = {
    "🔥 CRITIQUE": [
        "core",  # Tests des modules core
        "performance",  # Tests de performance et charge
        "security",  # Tests de sécurité
        "integration",  # Tests d'intégration
    ],
    "⚡ HAUTE PRIORITÉ": [
        "ui",  # Tests d'interface utilisateur
        "accessibility",  # Tests d'accessibilité
        "gamification",  # Tests de gamification
        "luna",  # Tests de l'IA LUNA
    ],
    "📱 PRIORITÉ MOYENNE": [
        "mobile",  # Tests mobile et PWA
        "immersion",  # Tests d'immersion
        "educational",  # Tests éducatifs
        "terminal",  # Tests du terminal
    ],
    "🎯 PRIORITÉ BASSE": [
        "utilities",  # Tests utilitaires
        "scripts",  # Tests des scripts
        "reports",  # Tests des rapports
    ],
}

# Modules critiques à tester en priorité
CRITICAL_MODULES = [
    "core.luna_emotions_engine",
    "core.gamification_engine",
    "core.educational_games_engine",
    "core.tutorial_manager",
    "core.analytics_engine",
    "arkalia_engine",
    "app",
]

# Configuration des tests
TEST_CONFIG = {
    "base_url": "http://localhost:5001",
    "timeout": 30,
    "retry_count": 3,
    "parallel_tests": False,
    "generate_reports": True,
    "coverage_target": 85,
}

__version__ = "3.0.0"
__author__ = "Arkalia Quest Team"
__status__ = "Production Ready"
