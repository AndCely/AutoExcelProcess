"""
Fachada para el sistema de logging
"""
from typing import Dict
from pathlib import Path
from logging.handlers import RotatingFileHandler
from ..interfaces.logger_interface import ILogger
from .base_logger import BaseLogger
from ..settings import settings

class LoggerFactory:
    """Factory para crear instancias de loggers"""
    
    def __init__(self):
        self._loggers: Dict[str, ILogger] = {}
        self._log_dir = settings.logging.log_dir
        
    def get_logger(self, logger_type: str) -> ILogger:
        """
        Obtiene o crea un logger del tipo especificado.
        
        Args:
            logger_type: Tipo de logger ('app', 'error', 'excel', 'siigo')
            
        Returns:
            ILogger: Instancia del logger solicitado
        """
        if logger_type not in self._loggers:
            log_file = self._log_dir / logger_type / f"{logger_type}.log"
            log_file.parent.mkdir(parents=True, exist_ok=True)
            self._loggers[logger_type] = BaseLogger(logger_type, str(log_file))
        else:
            # Reinicializar el logger si ya existe
            logger = self._loggers[logger_type].logger
            for handler in logger.handlers[:]:
                logger.removeHandler(handler)
            log_file = self._log_dir / logger_type / f"{logger_type}.log"
            max_bytes = BaseLogger("temp", "temp.log")._parse_size(settings.logging.rotation_size)
            logger.addHandler(RotatingFileHandler(
                str(log_file),
                maxBytes=max_bytes,
                backupCount=settings.logging.backup_count
            ))
        return self._loggers[logger_type]

class LoggerFacade:
    """Fachada para acceder a todos los loggers de manera simple"""
    
    def __init__(self):
        self._factory = LoggerFactory()
        self.app = self._factory.get_logger('app')
        self.error = self._factory.get_logger('error')
        self.excel = self._factory.get_logger('excel')
        self.siigo = self._factory.get_logger('siigo')

# Instancia global de la fachada
log = LoggerFacade()
