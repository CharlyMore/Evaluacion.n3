#Creando la clase administrador de Recursos Humanos que hereda de la clase Usuario
from usuario import Usuario

class AdministradorRH(Usuario):
    def __init__(self, id, nombre, email, username, password, id_usuario=None):
        Usuario.__init__(self, id_usuario, username, password, "AdministradorRH")
        self.id_admin = id
        self.nombre = nombre
        self.email = email

    def mostrar_info(self):
        print(f"ID Admin RH: {self.id_admin}")
        print(f"Nombre: {self.nombre}")
        print(f"Email: {self.email}")
