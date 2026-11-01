#Creando la clase Departamento
class Departamento:
    def __init__(self, id, nombre, gerente_id):
        self.id = id
        self.nombre = nombre
        self.gerente_id = gerente_id

    def mostrar_info(self):
        print(f"ID Departamento: {self.id}")
        print(f"Nombre: {self.nombre}")
        print(f"Gerente ID: {self.gerente_id}")
