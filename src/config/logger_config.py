from dataclasses import dataclass
from pathlib import Path
from typing import Optional
import logging

@dataclass
class LogConfig:
    """Configuración para un logger específico"""
    name: str
    log_file: Path
    level: int = logging.INFO
    format_string: str = '%(timestamp)s %(level)s %(name)s %(module)s %(message)s'

class LoggerConfig:
    """Clase de configuración para todos los loggers"""
    def __init__(self, base_dir: Optional[Path] = None):
        self.base_dir = base_dir or Path(__file__).parent.parent.parent.parent
        self.logs_dir = self.base_dir / 'logs'
        self._ensure_log_directories()
        
        # Configuraciones específicas para cada tipo de logger
        self.app_config = LogConfig('app', self.logs_dir / 'app' / 'app.log')
        self.error_config = LogConfig('error', self.logs_dir / 'errors' / 'error.log', logging.ERROR)
        self.excel_config = LogConfig('excel', self.logs_dir / 'excel' / 'excel.log')
        self.siigo_config = LogConfig('siigo', self.logs_dir / 'siigo' / 'siigo.log')
    
    def _ensure_log_directories(self) -> None:
        """Asegura que existan los directorios necesarios para los logs"""
        for dir_name in ['app', 'errors', 'excel', 'siigo']:
            (self.logs_dir / dir_name).mkdir(parents=True, exist_ok=True)
