"""
Implementación base del logger
"""
import logging
from logging.handlers import RotatingFileHandler
from typing import Any, Optional
import coloredlogs
from ..interfaces.logger_interface import ILogger
from ..formatters.json_formatter import JsonLogFormatter
from ..settings import settings

class BaseLogger(ILogger):
    """Implementación base del logger que cumple con la interfaz ILogger"""
    
    def __init__(self, name: str, log_file: str):
        """
        Inicializa un nuevo logger.
        
        Args:
            name: Nombre del logger
            log_file: Ruta al archivo de log
        """
        self.name = name
        self.log_file = log_file
        self.logger = self._setup_logger()
    
    def _setup_logger(self) -> logging.Logger:
        """Configura y retorna un logger con rotación de archivos"""
        logger = logging.getLogger(self.name)

        # Configurar nivel DEBUG para el logger principal
        level = logging.DEBUG
        logger.setLevel(level)

        # Eliminar handlers existentes
        for handler in logger.handlers[:]:
            logger.removeHandler(handler)

        # Handler de archivo con rotación
        file_handler = RotatingFileHandler(
            self.log_file,
            maxBytes=self._parse_size(settings.logging.rotation_size),
            backupCount=settings.logging.backup_count
        )
        file_handler.setLevel(level)
        file_handler.setFormatter(JsonLogFormatter())
        logger.addHandler(file_handler)

        # Handler de consola con colores
        console_handler = logging.StreamHandler()
        console_handler.setLevel(level)
        coloredlogs.install(level=level, logger=logger)
        logger.addHandler(console_handler)

        return logger
    
    def _parse_size(self, size_str: str) -> int:
        """
        Convierte una cadena de tamaño (ej: '1 MB') a bytes.
        
        Args:
            size_str: Cadena que representa el tamaño (ej: '1 MB', '500 KB')
            
        Returns:
            int: Tamaño en bytes
        """
        size = int(size_str.split()[0])
        unit = size_str.split()[1].upper()
        
        units = {
            'B': 1,
            'KB': 1024,
            'MB': 1024 * 1024,
            'GB': 1024 * 1024 * 1024
        }
        
        return size * units.get(unit, 1)
    
    def info(self, message: str, **kwargs: Any) -> None:
        self.logger.info(message, extra={'props': kwargs})
    
    def error(self, message: str, exc_info: Optional[bool] = None, **kwargs: Any) -> None:
        self.logger.error(message, exc_info=exc_info, extra={'props': kwargs})
    
    def debug(self, message: str, **kwargs: Any) -> None:
        self.logger.debug(message, extra={'props': kwargs})
    
    def warning(self, message: str, **kwargs: Any) -> None:
        self.logger.warning(message, extra={'props': kwargs})
