from .log_config import app_logger, error_logger, excel_logger, siigo_logger

class Logger:
    @staticmethod
    def app(message, level='info'):
        """Log mensajes generales de la aplicación"""
        getattr(app_logger, level.lower())(message)

    @staticmethod
    def error(message, exc_info=None):
        """Log errores críticos"""
        error_logger.error(message, exc_info=exc_info)

    @staticmethod
    def excel(message, level='info'):
        """Log operaciones relacionadas con Excel"""
        getattr(excel_logger, level.lower())(message)

    @staticmethod
    def siigo(message, level='info'):
        """Log operaciones relacionadas con SIIGO"""
        getattr(siigo_logger, level.lower())(message)

# Crear una instancia global para uso fácil
log = Logger()
