from openpyxl.styles import Font, Alignment, PatternFill, Border, Side
from openpyxl.worksheet.datavalidation import DataValidation

class ExcelConfigProvider:
    """
    Configuration class for Excel file handling.
    """

    def __init__(self):

        # Definición de los encabezados de la hoja "Transacciones"
        self.headers_transacciones = [
            "ID", 
            "Fecha",
            "Detalle", 
            "Proveedor/Cliente", 
            "Entró", 
            "Salió", 
            "Saldo", 
            "Categoría", 
            "Conciliado en SIIGO"
        ]

        # Definición del ancho de las columnas en la hoja "Transacciones"
        self.column_widths_transacciones = {
            "A": 10,  # ID
            "B": 15,  # Fecha
            "C": 30,  # Detalle
            "D": 20,  # Proveedor/Cliente
            "E": 15,  # Entró
            "F": 15,  # Salió
            "G": 15,  # Saldo
            "H": 20,  # Categoría
            "I": 25   # Conciliado en SIIGO
        }

        # Definición de los encabezados de la hoja "Instrucciones"
        self.headers_instrucciones = [
            "Nombre de la columna", 
            "Descripción", 
            "Formato esperado", 
            "Ejemplo"
        ]

        # Definición del ancho de las columnas en la hoja "Instrucciones"
        self.column_widths_instrucciones = {
            "A": 20,  # Nombre de la columna
            "B": 60,  # Descripción
            "C": 50,  # Formato esperado
            "D": 20   # Ejemplo
        }

        # Definición de las instrucciones
        self.instructions = [
            ["ID", "Identificador único de la transacción", "Texto o número único", "T0001"],
            ["Fecha", "Fecha de la transacción", "Formato de fecha (DD/MM/AAAA)", "01/01/2023"],
            ["Detalle", "Descripción de la transacción", "Texto", "Compra de suministros"],
            ["Proveedor/Cliente", "Nombre del proveedor o cliente que se encuentre incluido en la lista", "Texto", "Proveedor XYZ"],
            ["Entró", "Monto que entró en la transacción", "Número decimal positivo", "100.00"],
            ["Salió", "Monto que salió en la transacción", "Número decimal negativo", "-50.00"],
            ["Saldo", "Saldo después de la transacción", "Número decimal derivado de la suma entre entro y salio", "50.00"],
            ["Categoría", "Categoría de la transacción", "Texto", "Gastos generales"],
            ["Conciliado en SIIGO", "Estado de conciliación en SIIGO (Sí/No)", "Texto (Sí/No)", "Sí"]
        ]
        
        # Encabezado
        self.fontEncabezado = Font(bold=True)
        self.alignmentEncabezado = Alignment(horizontal="center")
        self.fillfontEncabezado = PatternFill(start_color="FFFF00", end_color="FFFF00", fill_type="solid")
        sideEncabezado = Side(style="thin", color="000000")
        self.borderEncabezado = Border(
            left=sideEncabezado,
            right=sideEncabezado,
            top=sideEncabezado,
            bottom=sideEncabezado
            )
        
        # Validaciones de datos
        self.validations = {
    "Entró": {
        "validation": DataValidation(type="decimal", operator="greaterThanOrEqual", formula1="0", allow_blank=True, showErrorMessage = True),
        "errorTitle": "Valor inválido",
        "error": "El valor debe ser un número positivo."
    },
    "Salió": {
        "validation": DataValidation(type="decimal", operator="lessThanOrEqual", formula1="0", allow_blank=True, showErrorMessage = True),
        "errorTitle": "Valor inválido",
        "error": "El valor debe ser un número negativo."
    },
    "Saldo": {
        "validation": DataValidation(type="decimal", allow_blank=True, showErrorMessage = True),
        "errorTitle": "Valor inválido",
        "error": "El valor debe ser un número decimal."
    },
    "Fecha": {
        "validation": DataValidation(type="date", allow_blank=True, showErrorMessage = True),
        "errorTitle": "Fecha inválida",
        "error": "Debe ingresar una fecha válida."
    },
    "Proveedor/Cliente": {
        "validation": DataValidation(type="list", formula1='"Proveedor1,Proveedor2,Proveedor3"', allow_blank=True, showErrorMessage = True),
        "errorTitle": "Valor inválido",
        "error": "Debe seleccionar un valor de la lista."
    }
}
    