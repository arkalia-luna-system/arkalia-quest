"""
Configuration des outils de développement d'Arkalia Quest
"""

from typing import Any


class DevToolsConfig:
    """Configuration des outils de développement"""

    # Configuration Black
    BLACK_CONFIG = {
        "line_length": 88,
        "target_version": ["py38"],
        "include": r"\.pyi?$",
        "extend_exclude": r"""
        /(
          # directories
          \.eggs
          | \.git
          | \.hg
          | \.mypy_cache
          | \.tox
          | \.venv
          | build
          | dist
        )/
        """.strip(),
    }

    # Configuration Ruff
    RUFF_CONFIG = {
        "target_version": "py38",
        "line_length": 88,
        "select": [
            "E",  # pycodestyle errors
            "W",  # pycodestyle warnings
            "F",  # pyflakes
            "I",  # isort
            "B",  # flake8-bugbear
            "C4",  # flake8-comprehensions
            "UP",  # pyupgrade
            "ARG",  # flake8-unused-arguments
            "PIE",  # flake8-pie
            "SIM",  # flake8-simplify
            "TCH",  # flake8-type-checking
            "Q",  # flake8-quotes
        ],
        "ignore": [
            "E501",  # line too long, handled by black
            "B008",  # do not perform function calls in argument defaults
            "C901",  # too complex
            "SIM102",  # use a for loop instead of any/all
            "ARG001",  # unused function argument
            "TCH001",  # import typing in TYPE_CHECKING block
        ],
        "per_file_ignores": {
            "__init__.py": ["F401"],
            "tests/**/*.py": ["B011", "S101", "S603", "S607"],
        },
    }

    # Configuration Pytest
    PYTEST_CONFIG = {
        "minversion": "7.0",
        "addopts": [
            "--strict-markers",
            "--strict-config",
            "--cov=core",
            "--cov=engines",
            "--cov=utils",
            "--cov-report=term-missing",
            "--cov-report=html",
            "--cov-report=xml",
            "--cov-fail-under=80",
        ],
        "testpaths": ["tests"],
        "python_files": ["test_*.py", "*_test.py"],
        "python_classes": ["Test*"],
        "python_functions": ["test_*"],
        "markers": [
            "slow: marks tests as slow (deselect with '-m \"not slow\"')",
            "integration: marks tests as integration tests",
            "unit: marks tests as unit tests",
            "performance: marks tests as performance tests",
            "ui: marks tests as UI tests",
        ],
    }

    # Configuration Coverage
    COVERAGE_CONFIG = {
        "run": {
            "source": ["core", "engines", "utils"],
            "omit": [
                "*/tests/*",
                "*/test_*",
                "*/__pycache__/*",
                "*/venv/*",
                "*/migrations/*",
            ],
        },
        "report": {
            "exclude_lines": [
                "pragma: no cover",
                "def __repr__",
                "if self.debug:",
                "if settings.DEBUG",
                "raise AssertionError",
                "raise NotImplementedError",
                "if 0:",
                "if __name__ == .__main__.:",
                "class .*\\bProtocol\\):",
                "@(abc\\.)?abstractmethod",
            ],
        },
    }

    # Configuration Pre-commit
    PRE_COMMIT_CONFIG = {
        "repos": [
            {
                "repo": "https://github.com/pre-commit/pre-commit-hooks",
                "rev": "v4.4.0",
                "hooks": [
                    {"id": "trailing-whitespace"},
                    {"id": "end-of-file-fixer"},
                    {"id": "check-yaml"},
                    {"id": "check-added-large-files"},
                    {"id": "check-merge-conflict"},
                ],
            },
            {
                "repo": "https://github.com/psf/black",
                "rev": "23.7.0",
                "hooks": [{"id": "black", "language_version": "python3"}],
            },
            {
                "repo": "https://github.com/astral-sh/ruff-pre-commit",
                "rev": "v0.1.0",
                "hooks": [{"id": "ruff", "args": ["--fix"]}],
            },
            {
                "repo": "https://github.com/pre-commit/mirrors-mypy",
                "rev": "v1.5.1",
                "hooks": [{"id": "mypy", "additional_dependencies": ["types-all"]}],
            },
        ],
    }

    # Configuration des outils de qualité
    QUALITY_TOOLS = {
        "black": {"enabled": True, "command": "black", "args": ["--check", "."]},
        "ruff": {
            "enabled": True,
            "command": "ruff",
            "args": ["check", ".", "--output-format=github"],
        },
        "mypy": {
            "enabled": False,  # Désactivé par défaut pour éviter les erreurs
            "command": "mypy",
            "args": ["core", "engines", "utils"],
        },
        "pytest": {
            "enabled": True,
            "command": "pytest",
            "args": ["tests/", "--cov=core", "--cov-report=html"],
        },
    }

    @classmethod
    def get_black_config(cls) -> dict[str, Any]:
        """Retourne la configuration Black"""
        return cls.BLACK_CONFIG

    @classmethod
    def get_ruff_config(cls) -> dict[str, Any]:
        """Retourne la configuration Ruff"""
        return cls.RUFF_CONFIG

    @classmethod
    def get_pytest_config(cls) -> dict[str, Any]:
        """Retourne la configuration Pytest"""
        return cls.PYTEST_CONFIG

    @classmethod
    def get_coverage_config(cls) -> dict[str, Any]:
        """Retourne la configuration Coverage"""
        return cls.COVERAGE_CONFIG

    @classmethod
    def get_pre_commit_config(cls) -> dict[str, Any]:
        """Retourne la configuration Pre-commit"""
        return cls.PRE_COMMIT_CONFIG

    @classmethod
    def get_quality_tools(cls) -> dict[str, Any]:
        """Retourne la configuration des outils de qualité"""
        return cls.QUALITY_TOOLS


# Configuration des outils de développement par défaut
dev_tools_config = DevToolsConfig()
