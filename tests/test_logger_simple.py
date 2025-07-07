"""
Tests simplifiés pour le système de logging
Version 2.0.0
"""

import pytest
import tempfile
from pathlib import Path
from unittest.mock import patch

# Test de base pour vérifier que le module peut être importé
def test_logger_import():
    """Test que le module logger peut être importé"""
    try:
        from utils.logger import ArkaliaLogger
        assert ArkaliaLogger is not None
    except ImportError as e:
        pytest.skip(f"Module logger non disponible: {e}")

def test_logger_creation():
    """Test de création d'un logger"""
    try:
        from utils.logger import ArkaliaLogger
        
        with tempfile.TemporaryDirectory() as tmp_dir:
            with patch('utils.logger.LOGS_DIR', Path(tmp_dir) / "logs"):
                logger = ArkaliaLogger("test_logger")
                assert logger.name == "test_logger"
    except ImportError:
        pytest.skip("Module logger non disponible")

def test_game_logger():
    """Test du GameLogger"""
    try:
        from utils.logger import GameLogger
        
        with tempfile.TemporaryDirectory() as tmp_dir:
            with patch('utils.logger.LOGS_DIR', Path(tmp_dir) / "logs"):
                logger = GameLogger()
                assert logger.name == "arkalia_game"
    except ImportError:
        pytest.skip("Module logger non disponible")

def test_security_logger():
    """Test du SecurityLogger"""
    try:
        from utils.logger import SecurityLogger
        
        with tempfile.TemporaryDirectory() as tmp_dir:
            with patch('utils.logger.LOGS_DIR', Path(tmp_dir) / "logs"):
                logger = SecurityLogger()
                assert logger.name == "arkalia_security"
    except ImportError:
        pytest.skip("Module logger non disponible")

def test_performance_logger():
    """Test du PerformanceLogger"""
    try:
        from utils.logger import PerformanceLogger
        
        with tempfile.TemporaryDirectory() as tmp_dir:
            with patch('utils.logger.LOGS_DIR', Path(tmp_dir) / "logs"):
                logger = PerformanceLogger()
                assert logger.name == "arkalia_performance"
    except ImportError:
        pytest.skip("Module logger non disponible") 