from config.logging_config import app_logger, excel_logger, siigo_logger, error_logger

def main():
    try:
        app_logger.info("Iniciando la aplicación AutoExcelProcess")
        
        # Ejemplo de uso de los diferentes loggers
        excel_logger.info("Preparando para procesar archivo Excel")
        excel_logger.debug("Configurando parámetros de lectura")
        
        siigo_logger.info("Iniciando conexión con SIIGO")
        
        # Simulación de un error
        try:
            # Código que podría generar un error
            raise ValueError("Ejemplo de error controlado")
        except Exception as e:
            error_logger.error(f"Error en el procesamiento: {str(e)}", exc_info=True)
        
        app_logger.info("Aplicación inicializada correctamente")
        
    except Exception as e:
        error_logger.critical(f"Error crítico en la aplicación: {str(e)}", exc_info=True)
        raise

if __name__ == "__main__":
    main()