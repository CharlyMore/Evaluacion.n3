
#Creando la clase Usuario
class Usuario:
    def __init__(self, id, username, password, rol):
        self.id = id
        self.username = username
        self.password = password
        self.rol = rol
    #mostrando la informacion
    def mostrar_info(self):
        print(f"ID Usuario: {self.id}")
        print(f"Username: {self.username}")
        print(f"Rol: {self.rol}")

    
