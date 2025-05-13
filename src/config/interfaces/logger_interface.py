from abc import ABC, abstractmethod
from typing import Any, Optional

class ILogger(ABC):
    """Interface base para todos los loggers"""
    
    @abstractmethod
    def info(self, message: str, **kwargs: Any) -> None:
        """Registra un mensaje de nivel INFO"""
        pass
    
    @abstractmethod
    def error(self, message: str, exc_info: Optional[bool] = None, **kwargs: Any) -> None:
        """Registra un mensaje de nivel ERROR"""
        pass
    
    @abstractmethod
    def debug(self, message: str, **kwargs: Any) -> None:
        """Registra un mensaje de nivel DEBUG"""
        pass
    
    @abstractmethod
    def warning(self, message: str, **kwargs: Any) -> None:
        """Registra un mensaje de nivel WARNING"""
        pass
