
#Creando la clase RegistroTiempo
class RegistroTiempo:
    def __init__(self, id, empleado_id, proyecto_id, fecha, horas, descripcion):
        self.id = id
        self.empleado_id = empleado_id
        self.proyecto_id = proyecto_id
        self.fecha = fecha
        self.horas = horas
        self.descripcion = descripcion

    def mostrar_info(self):
        print(f"ID Registro: {self.id}")
        print(f"Empleado ID: {self.empleado_id}")
        print(f"Proyecto ID: {self.proyecto_id}")
        print(f"Fecha: {self.fecha}")
        print(f"Horas: {self.horas} hrs")
        print(f"Descripción: {self.descripcion}")
