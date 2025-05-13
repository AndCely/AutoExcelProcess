"""
Tests para el sistema de logging
"""
import json
import logging
import os
from pathlib import Path
import pytest
import configparser
from src.config.settings import settings
from src.config.formatters.json_formatter import JsonLogFormatter
from src.config.loggers.base_logger import BaseLogger
from src.config.loggers.logger_facade import LoggerFactory, LoggerFacade, log

from src.config.loggers.logger_facade import LoggerFacade

@pytest.fixture(scope="session", autouse=True)
def test_config():
    """Fixture que configura el entorno de prueba"""
    # Guardar la configuración original
    original_config = settings.get_config()
    original_config_file = settings.config_file
    
    # Configurar el archivo de prueba
    test_config = configparser.ConfigParser()
    test_config.read(Path(__file__).parent / "test_config.ini")
    test_config.set("logging", "level", "DEBUG")  # Establecer nivel DEBUG
    settings.config = test_config
    settings.config_file = Path(__file__).parent / "test_config.ini"
    
    # Reinicializar `log` con la nueva configuración
    global log
    log = LoggerFacade()
    
    yield
    
    # Restaurar la configuración original
    settings.config = original_config
    settings.config_file = original_config_file
    log = LoggerFacade()

@pytest.fixture
def temp_log_dir(tmp_path):
    """Fixture que proporciona un directorio temporal para logs"""
    # Guardar la configuración original
    original_log_dir = settings.logging.log_dir
    
    # Configurar directorio temporal
    settings.logging.log_dir = tmp_path
    for dir_name in ["app", "error", "excel", "siigo"]:
        (tmp_path / dir_name).mkdir(parents=True, exist_ok=True)
    
    # Crear archivos de log vacíos
    for dir_name in ["app", "error", "excel", "siigo"]:
        log_file = tmp_path / dir_name / f"{dir_name}.log"
        log_file.touch()
    
    # Reinicializar los loggers
    global log
    log = LoggerFacade()
    
    yield tmp_path
    
    # Restaurar la configuración original
    settings.logging.log_dir = original_log_dir
    log = LoggerFacade()

@pytest.fixture
def test_logger(temp_log_dir):
    """Fixture que proporciona un logger de prueba"""
    log_file = temp_log_dir / "test.log"
    return BaseLogger("test", str(log_file))

class TestJsonFormatter:
    """Pruebas para el formateador JSON"""
    
    def test_formatter_adds_required_fields(self):
        """Verifica que el formateador agregue todos los campos requeridos"""
        formatter = JsonLogFormatter()
        record = logging.LogRecord(
            name="test_logger",
            level=logging.INFO,
            pathname="test_module.py",
            lineno=42,
            msg="Test message",
            args=(),
            exc_info=None
        )
        
        log_entry = json.loads(formatter.format(record))
        
        assert "timestamp" in log_entry
        assert "level" in log_entry
        assert "module" in log_entry
        assert "logger" in log_entry
        assert log_entry["message"] == "Test message"
        assert log_entry["level"] == "INFO"

class TestBaseLogger:
    """Pruebas para el logger base"""
    
    def test_info_logging(self, test_logger, temp_log_dir):
        """Verifica el logging de nivel INFO"""
        message = "Test info message"
        extra_data = {"key": "value"}
        
        test_logger.info(message, **extra_data)
        
        log_file = temp_log_dir / "test.log"
        with open(log_file) as f:
            log_entry = json.loads(f.readline())
            assert log_entry["message"] == message
            assert log_entry["level"] == "INFO"
            assert log_entry["props"]["key"] == "value"
    
    def test_error_logging_with_exc_info(self, test_logger, temp_log_dir):
        """Verifica el logging de errores con información de excepción"""
        message = "Test error message"
        try:
            raise ValueError("Test exception")
        except ValueError:
            test_logger.error(message, exc_info=True)
        
        log_file = temp_log_dir / "test.log"
        with open(log_file) as f:
            log_entry = json.loads(f.readline())
            assert log_entry["message"] == message
            assert log_entry["level"] == "ERROR"
            assert "exc_info" in log_entry

class TestLoggerFactory:
    """Pruebas para el factory de loggers"""
    
    def test_logger_singleton(self, temp_log_dir):
        """Verifica que el factory mantenga una única instancia por tipo"""
        factory = LoggerFactory()
        
        logger1 = factory.get_logger("test")
        logger2 = factory.get_logger("test")
        
        assert logger1 is logger2
    
    def test_different_logger_types(self, temp_log_dir):
        """Verifica que se creen diferentes tipos de loggers"""
        factory = LoggerFactory()
        
        app_logger = factory.get_logger("app")
        error_logger = factory.get_logger("error")
        
        assert app_logger is not error_logger

class TestLoggerFacade:
    """Pruebas para la fachada del logger"""
    
    def test_facade_provides_all_loggers(self):
        """Verifica que la fachada proporcione todos los tipos de logger"""
        facade = LoggerFacade()
        
        assert hasattr(facade, "app")
        assert hasattr(facade, "error")
        assert hasattr(facade, "excel")
        assert hasattr(facade, "siigo")
    
    def test_log_directory_creation(self, temp_log_dir):
        """Verifica que se creen los directorios de log necesarios"""
        facade = LoggerFacade()
        
        expected_dirs = ["app", "error", "excel", "siigo"]
        for dir_name in expected_dirs:
            assert (temp_log_dir / dir_name).exists()

class TestConfiguration:
    """Pruebas para la configuración del sistema"""
    
    def test_config_loaded(self):
        """Verifica que la configuración se cargue correctamente"""
        assert settings.config.has_section("logging")
        assert settings.config.has_section("siigo")
        assert settings.config.get("siigo", "api_url") == "http://test.siigo.api"
    
    def test_logging_config(self):
        """Verifica la configuración de logging"""
        assert settings.logging.level == "INFO"
        assert settings.logging.rotation_size == "1 MB"
        assert settings.logging.backup_count == 5

def test_integration_all_log_levels(temp_log_dir):
    """Prueba de integración para todos los niveles de log"""
    test_messages = {
        "info": "Test info message",
        "error": "Test error message",
        "debug": "Test debug message",
        "warning": "Test warning message"
    }
    
    # Usar la fachada global
    for level, message in test_messages.items():
        getattr(log.app, level)(message, test_key=level)
    
    log_file = temp_log_dir / "app" / "app.log"
    with open(log_file) as f:
        logs = [json.loads(line) for line in f]
    
    assert len(logs) == len(test_messages)
    for log_entry, (level, message) in zip(logs, test_messages.items()):
        assert log_entry["message"] == message
        assert log_entry["props"]["test_key"] == level