from openpyxl import Workbook
from openpyxl.worksheet.datavalidation import DataValidation
import os
import logging
from ..excel_config import ExcelConfigProvider

class ExcelTemplateGenerator:
    """
    Clase para generar plantillas de Excel.
    Esta clase utiliza la biblioteca openpyxl para crear un archivo Excel con una hoja de cálculo básica.
    """
    def __init__(self, logger=None):
        """
        Inicializa la clase ExcelTemplateGenerator.
        
        :param logger: Instancia de logger para registrar eventos.
        """
        self.logger = logger
        self.logger.debug("ExcelTemplateGenerator inicializado.")
        self.config = ExcelConfigProvider()
        self.logger.debug("Configuración de Excel cargada.")    



    def create_excel_template(self, output_path):
        """
        Crea la plantilla de Excel y la guarda en la ruta especificada.
        :param output_path: Ruta donde se guardará el archivo Excel.
        """
        try:
            # Crear un nuevo libro de trabajo
            wb = Workbook()

            # Configurar las hojas y validaciones
            self._configure_sheets(wb)

            # Guardar el archivo
            wb.save(output_path)
            self.logger.info(f"Plantilla creada exitosamente en: {output_path}")
        except Exception as e:
            self.logger.error(f"Error al crear la plantilla de Excel: {e}", exc_info=True)
            raise

    def _configure_sheets(self, wb):
        """
        Configura las hojas de cálculo y las validaciones necesarias.
        :param wb: Objeto Workbook de openpyxl.
        """ 
        # Crear la hoja "Transacciones"
        sheet_transacciones = wb.active
        sheet_transacciones.title = "Transacciones"
            
        # Definir los encabezados de la hoja "Transacciones"
        sheet_transacciones.append(self.config.headers_transacciones)
        
        # Aplicar estilos a los encabezados
        for cell in sheet_transacciones[1]:
            cell.font = self.config.fontEncabezado
            cell.alignment = self.config.alignmentEncabezado
            cell.fill = self.config.fillfontEncabezado
            cell.border = self.config.borderEncabezado         

        # Definir el ancho de las columnas
        for col, width in self.config.column_widths_transacciones.items():
            sheet_transacciones.column_dimensions[col].width = width
        
        # Validaciones
        
        column_mapping = {
            "Entró": "E",
            "Salió": "F",
            "Saldo": "G",
            "Fecha": "B",
            "Proveedor/Cliente": "D"
        }
        
        # Definir las validaciones de datos
        for key, configVa in self.config.validations.items():
            validation = configVa["validation"]
            validation.errorTitle = configVa["errorTitle"]
            validation.error = configVa["error"]
            validation.sqref = f"{column_mapping[key]}2:{column_mapping[key]}1048576"
            sheet_transacciones.add_data_validation(validation)


        # Crear la hoja "Instrucciones"
        sheet_instrucciones = wb.create_sheet(title="Instrucciones")

        # Definir los encabezados de la hoja "Instrucciones"
        sheet_instrucciones.append(self.config.headers_instrucciones)

        # Definir el ancho de las columnas
        for col, width in self.config.column_widths_instrucciones.items():
            sheet_instrucciones.column_dimensions[col].width = width

        # Aplicar estilos a los encabezados
        for cell in sheet_instrucciones[1]:
            cell.font = self.config.fontEncabezado
            cell.alignment = self.config.alignmentEncabezado
            cell.fill = self.config.fillfontEncabezado
            cell.border = self.config.borderEncabezado
        
        # Agregar instrucciones
        for row in self.config.instructions:
            sheet_instrucciones.append(row)

        # Aquí puedes agregar la lógica para configurar las hojas de cálculo y las validaciones necesarias.
        self.logger.debug("Hojas de cálculo configuradas y validaciones aplicadas.")

if __name__ == "__main__":
    logger = logging.getLogger("ExcelTemplateGenerator")
    logging.basicConfig(level=logging.INFO)

    output_file = os.path.join(os.path.dirname(__file__), "plantilla_transacciones(3).xlsx")
    generator = ExcelTemplateGenerator(logger=logger)
    generator.create_excel_template(output_file)