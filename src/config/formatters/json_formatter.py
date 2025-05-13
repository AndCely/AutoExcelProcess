"""
Formateador personalizado para logs en formato JSON
"""
from datetime import datetime
from pythonjsonlogger.json import JsonFormatter
from typing import Any, Dict
from ..settings import settings

class JsonLogFormatter(JsonFormatter):
    """Formateador personalizado para logs en formato JSON"""
    
    def add_fields(self, log_record: Dict[str, Any], record: Any, message_dict: Dict[str, Any]) -> None:
        """
        Agrega campos personalizados al registro de log.
        
        Args:
            log_record: Registro de log a modificar
            record: Registro original
            message_dict: Diccionario de mensaje
        """
        super().add_fields(log_record, record, message_dict)
        
        # Campos estándar
        log_record.update({
            'timestamp': datetime.utcnow().isoformat(),
            'level': record.levelname,
            'module': record.module,
            'logger': record.name
        })
        
        # Campos adicionales si existen
        if hasattr(record, 'props'):
            log_record.update(record.props)
