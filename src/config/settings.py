"""
Configuración general de la aplicación
"""
import os
from pathlib import Path
from dataclasses import dataclass
from typing import Optional
import configparser

@dataclass
class SiigoConfig:
    """Configuración para la API de SIIGO"""
    api_url: str
    api_key: str
    tenant_id: str

@dataclass
class LoggingConfig:
    """Configuración para el sistema de logging"""
    level: str = "INFO"
    rotation_size: str = "1 MB"
    backup_count: int = 5
    log_dir: Optional[Path] = None

class Settings:
    """Clase principal de configuración de la aplicación"""
    
    def __init__(self):
        self.base_dir = Path(__file__).parent.parent.parent
        self.config = configparser.ConfigParser()
        self.config_file = self.base_dir / "configuracion.ini"
        self._load_config()
        self._initialize_configs()
    
    def _initialize_configs(self):
        """Inicializa las configuraciones con valores por defecto si no existen"""
        # Configuración de logging
        self.logging = LoggingConfig(
            level=self.config.get("logging", "level", fallback="INFO"),
            rotation_size=self.config.get("logging", "rotation_size", fallback="1 MB"),
            backup_count=self.config.getint("logging", "backup_count", fallback=5),
            log_dir=self.base_dir / "logs"
        )
        
        # Configuración de SIIGO con valores por defecto
        self.siigo = SiigoConfig(
            api_url=self.config.get("siigo", "api_url", fallback="https://api.siigo.com/v1"),
            api_key=self.config.get("siigo", "api_key", fallback=""),
            tenant_id=self.config.get("siigo", "tenant_id", fallback="")
        )
    
    def _load_config(self) -> None:
        """Carga la configuración desde el archivo .ini o crea uno por defecto"""
        if self.config_file.exists():
            self.config.read(self.config_file)
        else:
            self._create_default_config()
    
    def _create_default_config(self) -> None:
        """Crea un archivo de configuración por defecto"""
        self.config["logging"] = {
            "level": "INFO",
            "rotation_size": "1 MB",
            "backup_count": "5"
        }
        
        self.config["siigo"] = {
            "api_url": "https://api.siigo.com/v1",
            "api_key": "",
            "tenant_id": ""
        }
        
        with open(self.config_file, "w") as f:
            self.config.write(f)

    def get_config(self) -> configparser.ConfigParser:
        """Devuelve la configuración cargada."""
        return self.config

# Instancia global de configuración
settings = Settings()