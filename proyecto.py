#Creando la clase Proyecto
class Proyecto:
    def __init__(self, id, nombre, descripcion, fecha_inicio):
        self.id = id
        self.nombre = nombre
        self.descripcion = descripcion
        self.fecha_inicio = fecha_inicio

    def mostrar_info(self):
        print(f"ID Proyecto: {self.id}")
        print(f"Proyecto: {self.nombre}")
        print(f"Descripción: {self.descripcion}")
        print(f"Fecha Inicio: {self.fecha_inicio}")
