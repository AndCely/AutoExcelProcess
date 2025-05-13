"""
Módulo de configuración para la aplicación de Auto Conciliación de Cartera.
Proporciona configuraciones centralizadas y sistema de logging.
"""

from .loggers.logger_facade import log
from .settings import Settings

__all__ = ['log', 'Settings']