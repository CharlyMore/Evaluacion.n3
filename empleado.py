#Creando la clase Empleado que hereda de la clase Usuario

from usuario import Usuario

class Empleado(Usuario):
    def __init__(self, id, nombre, direccion, telefono, email, fecha_inicio, salario, username, password, id_usuario=None):
        Usuario.__init__(self, id_usuario, username, password, "Empleado")
        self.id_empleado = id
        self.nombre = nombre
        self.direccion = direccion
        self.telefono = telefono
        self.email = email
        self.fecha_inicio = fecha_inicio
        self.salario = salario

    def mostrar_info(self):
        print(f"ID Empleado: {self.id_empleado}")
        print(f"Nombre: {self.nombre}")
        print(f"Email: {self.email}")
        print(f"Teléfono: {self.telefono}")
        print(f"Salario: ${self.salario:,.2f}")
        print(f"Fecha Inicio: {self.fecha_inicio}")
