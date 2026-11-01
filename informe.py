#Creando la clase Informe
class Informe:
    def __init__(self, id, tipo_reporte, fecha_generacion="2026-10-01"):
        self.id = id
        self.tipo_reporte = tipo_reporte
        self.fecha_generacion = fecha_generacion

    def mostrar_info(self):
        print(f"ID Informe: {self.id}")
        print(f"Tipo Reporte: {self.tipo_reporte}")
        print(f"Fecha Generación: {self.fecha_generacion}")
