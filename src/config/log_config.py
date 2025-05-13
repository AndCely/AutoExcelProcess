import os
import logging
from datetime import datetime
from pathlib import Path
from pythonjsonlogger import jsonlogger
import coloredlogs

# Definir constantes para los paths de logs
BASE_DIR = Path(__file__).parent.parent.parent
LOGS_DIR = BASE_DIR / 'logs'
APP_LOGS = LOGS_DIR / 'app'
ERROR_LOGS = LOGS_DIR / 'errors'
EXCEL_LOGS = LOGS_DIR / 'excel'
SIIGO_LOGS = LOGS_DIR / 'siigo'

# Asegurar que los directorios de logs existan
for dir_path in [APP_LOGS, ERROR_LOGS, EXCEL_LOGS, SIIGO_LOGS]:
    dir_path.mkdir(parents=True, exist_ok=True)

class CustomJsonFormatter(jsonlogger.JsonFormatter):
    def add_fields(self, log_record, record, message_dict):
        super(CustomJsonFormatter, self).add_fields(log_record, record, message_dict)
        log_record['timestamp'] = datetime.utcnow().isoformat()
        log_record['level'] = record.levelname
        log_record['module'] = record.module

def setup_logger(name, log_file, level=logging.INFO):
    """Configura un logger específico con manejo de archivos y formato JSON"""
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # Manejador de archivo
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(level)
    formatter = CustomJsonFormatter('%(timestamp)s %(level)s %(name)s %(module)s %(message)s')
    file_handler.setFormatter(formatter)
    
    # Manejador de consola con colores
    console_handler = logging.StreamHandler()
    console_handler.setLevel(level)
    coloredlogs.install(level=level, logger=logger)
    
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger

# Configurar loggers específicos
app_logger = setup_logger('app', APP_LOGS / 'app.log')
error_logger = setup_logger('error', ERROR_LOGS / 'error.log', level=logging.ERROR)
excel_logger = setup_logger('excel', EXCEL_LOGS / 'excel.log')
siigo_logger = setup_logger('siigo', SIIGO_LOGS / 'siigo.log')
