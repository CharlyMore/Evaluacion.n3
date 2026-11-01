### ==========================================================
### IMPORTAR MÓDULOS Y CLASES
### ==========================================================
# Se importa sqlite3 para conectar el programa con la base de datos.
import sqlite3

# Importación de las clases desde sus respectivos módulos.


from administrador_rh import AdministradorRH
from departamento import Departamento
from empleado import Empleado
from informe import Informe
from proyecto import Proyecto
from registro_tiempo import RegistroTiempo
from usuario import Usuario


### ==========================================================
### FUNCIONES PARA TRABAJAR CON LA BASE DE DATOS
### ==========================================================

# Crea las tablas del sistema si todavía no existen.
def crear_tablas(cursor):
    # Tabla 1: guarda el nombre de usuario, la contraseña y el rol.
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuario (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            rol TEXT NOT NULL
        )
    """)
    # Tabla 2: guarda los datos del empleado y su usuario asociado.
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS empleado (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            direccion TEXT NOT NULL,
            telefono TEXT NOT NULL,
            email TEXT NOT NULL,
            fecha_inicio TEXT NOT NULL,
            salario REAL NOT NULL,
            usuario_id INTEGER NOT NULL,
            FOREIGN KEY (usuario_id) REFERENCES usuario(id)
        )
    """)
    # Tabla 3: guarda los datos del administrador de Recursos Humanos.
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS administrador_rh (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            email TEXT NOT NULL,
            usuario_id INTEGER NOT NULL,
            FOREIGN KEY (usuario_id) REFERENCES usuario(id)
        )
    """)
    # Tabla 4: guarda los departamentos y el empleado que los dirige.
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS departamento (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            gerente_id INTEGER,
            FOREIGN KEY (gerente_id) REFERENCES empleado(id)
        )
    """)
    
    # Tabla 5: guarda los proyectos de la empresa.
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS proyecto (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            descripcion TEXT NOT NULL,
            fecha_inicio TEXT NOT NULL
        )
    """)
    # Tabla 6: registra las horas trabajadas en cada proyecto.
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS registro_tiempo (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            empleado_id INTEGER NOT NULL,
            proyecto_id INTEGER NOT NULL,
            fecha TEXT NOT NULL,
            horas REAL NOT NULL,
            descripcion TEXT NOT NULL,
            FOREIGN KEY (empleado_id) REFERENCES empleado(id),
            FOREIGN KEY (proyecto_id) REFERENCES proyecto(id)
        )
    """)
    # Tabla 7: guarda los informes definidos en el modelo.
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS informe (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tipo_reporte TEXT NOT NULL,
            fecha_generacion TEXT NOT NULL
        )
    """)


# Busca un registro existente o lo inserta si todavía no está guardado.
def obtener_o_crear_id(
    cursor,
    consulta_busqueda,
    valores_busqueda,
    consulta_insercion,
    valores_insercion,
):
    # Busca primero para evitar duplicados al ejecutar nuevamente el programa.
    cursor.execute(consulta_busqueda, valores_busqueda)
    resultado = cursor.fetchone()
    if resultado:
        return resultado[0]

    # Inserta el registro y obtiene el ID asignado por SQLite.
    cursor.execute(consulta_insercion, valores_insercion)
    return cursor.lastrowid


# Ejecuta una consulta y muestra los datos obtenidos.
def mostrar_datos(cursor, titulo, consulta, valores=()):
    cursor.execute(consulta, valores)
    print(titulo)
    for fila in cursor.fetchall():
        print(fila)


### ==========================================================
### INICIAR EL PROGRAMA Y CONECTAR CON LA BASE DE DATOS
### ==========================================================
def main():
    conexion = None

    try:
        # 1. Conectar con la base de datos y crear el cursor.
        conexion = sqlite3.connect("ecotech.db")
        conexion.execute("PRAGMA foreign_keys = ON")
        cursor = conexion.cursor()
        crear_tablas(cursor)
        print("Conexión realizada y tablas verificadas.")

        ### ==========================================================
        ### INSTANCIAR LOS OBJETOS DEL SISTEMA
        ### ==========================================================
        # Creación de usuarios para asociarlos a empleados y administradores.
        usuario_demo = Usuario(None, "usuario_empleado", "pass123", "Empleado")
        usuario_admin_demo = Usuario(
            None, "usuario_admin", "pass456", "Administrador RH"
        )
        usuario_uno = Usuario(
            None, "usuario_empleado_uno", "pass789", "Empleado"
        )
        usuario_admin_uno = Usuario(
            None, "usuario_admin_uno", "pass012", "Administrador RH"
        )

        ### ==========================================================
        ### OPERACIONES INSERT EN LA TABLA USUARIO (CREATE)
        ### ==========================================================
        print("### ==========================================================")
        print("\n--- CREATE: tabla usuario ---")
        usuario_demo.id = obtener_o_crear_id(
            cursor,
            "SELECT id FROM usuario WHERE username = ?",
            (usuario_demo.username,),
            "INSERT INTO usuario (username, password, rol) VALUES (?, ?, ?)",
            (usuario_demo.username, usuario_demo.password, usuario_demo.rol),
        )
        usuario_admin_demo.id = obtener_o_crear_id(
            cursor,
            "SELECT id FROM usuario WHERE username = ?",
            (usuario_admin_demo.username,),
            "INSERT INTO usuario (username, password, rol) VALUES (?, ?, ?)",
            (
                usuario_admin_demo.username,
                usuario_admin_demo.password,
                usuario_admin_demo.rol,
            ),
        )
        usuario_uno.id = obtener_o_crear_id(
            cursor,
            "SELECT id FROM usuario WHERE username = ?",
            (usuario_uno.username,),
            "INSERT INTO usuario (username, password, rol) VALUES (?, ?, ?)",
            (usuario_uno.username, usuario_uno.password, usuario_uno.rol),
        )
        usuario_admin_uno.id = obtener_o_crear_id(
            cursor,
            "SELECT id FROM usuario WHERE username = ?",
            (usuario_admin_uno.username,),
            "INSERT INTO usuario (username, password, rol) VALUES (?, ?, ?)",
            (
                usuario_admin_uno.username,
                usuario_admin_uno.password,
                usuario_admin_uno.rol,
            ),
        )
        mostrar_datos(
            cursor,
            "Datos creados en usuario:",
            "SELECT id, username, rol FROM usuario WHERE id = ?",
            (usuario_demo.id,),
        )
        mostrar_datos(
            cursor,
            "Datos creados en usuario:",
            "SELECT id, username, rol FROM usuario WHERE id = ?",
            (usuario_admin_demo.id,),
        )
        mostrar_datos(
            cursor,
            "Datos creados en usuario:",
            "SELECT id, username, rol FROM usuario WHERE id = ?",
            (usuario_uno.id,),
        )
        mostrar_datos(
            cursor,
            "Datos creados en usuario:",
            "SELECT id, username, rol FROM usuario WHERE id = ?",
            (usuario_admin_uno.id,),
        )

        ### ==========================================================
        ### OPERACIONES INSERT EN LA TABLA EMPLEADO (CREATE)
        ### ==========================================================
        print("\n--- CREATE: tabla empleado ---")
        empleado_demo = Empleado(
            None,
            "Juan Pérez",
            "Calle Falsa 123",
            "+56912345678",
            "juan@ecotech.cl",
            "2025-03-01",
            1800000.0,
            usuario_demo.username,
            usuario_demo.password,
            usuario_demo.id,
        )
        empleado_uno = Empleado(
            None,
            "Ana Martínez",
            "Av. Providencia 1234",
            "+56987654321",
            "ana@ecotech.cl",
            "2025-03-01",
            1800000.0,
            usuario_uno.username,
            usuario_uno.password,
            usuario_uno.id,
        )
        empleado_demo.id_empleado = obtener_o_crear_id(
            cursor,
            "SELECT id FROM empleado WHERE email = ?",
            (empleado_demo.email,),
            """
                INSERT INTO empleado
                (nombre, direccion, telefono, email, fecha_inicio, salario, usuario_id)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                empleado_demo.nombre,
                empleado_demo.direccion,
                empleado_demo.telefono,
                empleado_demo.email,
                empleado_demo.fecha_inicio,
                empleado_demo.salario,
                usuario_demo.id,
            ),
        )
        empleado_uno.id_empleado = obtener_o_crear_id(
            cursor,
            "SELECT id FROM empleado WHERE email = ?",
            (empleado_uno.email,),
            """
                INSERT INTO empleado
                (nombre, direccion, telefono, email, fecha_inicio, salario, usuario_id)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                empleado_uno.nombre,
                empleado_uno.direccion,
                empleado_uno.telefono,
                empleado_uno.email,
                empleado_uno.fecha_inicio,
                empleado_uno.salario,
                usuario_uno.id,
            ),
        )
        mostrar_datos(
            cursor,
            "Datos creados en empleado:",
            "SELECT * FROM empleado WHERE id = ?",
            (empleado_demo.id_empleado,),
        )
        mostrar_datos(
            cursor,
            "Datos creados en empleado:",
            "SELECT * FROM empleado WHERE id = ?",
            (empleado_uno.id_empleado,),
        )

        ### ==========================================================
        ### OPERACIONES INSERT EN LA TABLA ADMINISTRADOR_RH (CREATE)
        ### ==========================================================
        print("\n--- CREATE: tabla administrador_rh ---")
        admin_demo = AdministradorRH(
            None,
            "Roberto Silva",
            "roberto@ecotech.cl",
            usuario_admin_demo.username,
            usuario_admin_demo.password,
            usuario_admin_demo.id,
        )
        admin_uno = AdministradorRH(
            None,
            "Laura Fernández",
            "laura@ecotech.cl",
            usuario_admin_uno.username,
            usuario_admin_uno.password,
            usuario_admin_uno.id,
        )
        admin_demo.id_admin = obtener_o_crear_id(
            cursor,
            "SELECT id FROM administrador_rh WHERE email = ?",
            (admin_demo.email,),
            """
                INSERT INTO administrador_rh (nombre, email, usuario_id)
                VALUES (?, ?, ?)
            """,
            (admin_demo.nombre, admin_demo.email, usuario_admin_demo.id),
        )
        admin_uno.id_admin = obtener_o_crear_id(
            cursor,
            "SELECT id FROM administrador_rh WHERE email = ?",
            (admin_uno.email,),
            """
                INSERT INTO administrador_rh (nombre, email, usuario_id)
                VALUES (?, ?, ?)
            """,
            (admin_uno.nombre, admin_uno.email, usuario_admin_uno.id),
        )
        cursor.execute(
            "UPDATE administrador_rh SET usuario_id = ? WHERE id = ?",
            (usuario_admin_demo.id, admin_demo.id_admin),
        )
        cursor.execute(
            "UPDATE administrador_rh SET usuario_id = ? WHERE id = ?",
            (usuario_admin_uno.id, admin_uno.id_admin),
        )
        mostrar_datos(
            cursor,
            "Datos creados en administrador_rh:",
            "SELECT * FROM administrador_rh WHERE id = ?",
            (admin_demo.id_admin,),
        )
        mostrar_datos(
            cursor,
            "Datos creados en administrador_rh:",
            "SELECT * FROM administrador_rh WHERE id = ?",
            (admin_uno.id_admin,),
        )

        ### ==========================================================
        ### OPERACIONES INSERT EN LA TABLA DEPARTAMENTO (CREATE)
        ### ==========================================================
        print("\n--- CREATE: tabla departamento ---")
        depto_demo = Departamento(None, "Innovación Tecnológica", empleado_demo.id_empleado)
        depto_uno = Departamento(None, "Desarrollo Sostenible", empleado_uno.id_empleado)
        depto_demo.id = obtener_o_crear_id(
            cursor,
            "SELECT id FROM departamento WHERE nombre IN (?, ?)",
            (
                depto_demo.nombre,
                "Innovación Tecnológica - Actualizado",
            ),
            "INSERT INTO departamento (nombre, gerente_id) VALUES (?, ?)",
            (depto_demo.nombre, empleado_demo.id_empleado),
        )
        depto_uno.id = obtener_o_crear_id(
            cursor,
            "SELECT id FROM departamento WHERE nombre = ?",
            (depto_uno.nombre,),
            "INSERT INTO departamento (nombre, gerente_id) VALUES (?, ?)",
            (depto_uno.nombre, empleado_uno.id_empleado),
        )
        mostrar_datos(
            cursor,
            "Datos creados en departamento:",
            "SELECT * FROM departamento WHERE id = ?",
            (depto_demo.id,),
        )
        mostrar_datos(
            cursor,
            "Datos creados en departamento:",
            "SELECT * FROM departamento WHERE id = ?",
            (depto_uno.id,),
        )

        ### ==========================================================
        ### OPERACIONES INSERT EN LA TABLA PROYECTO (CREATE)
        ### ==========================================================
        print("\n--- CREATE: tabla proyecto ---")
        proyecto_demo = Proyecto(
            None,
            "Proyecto Solar",
            "Instalación de paneles solares en la sede central",
            "2025-06-01",
        )
        proyecto_uno = Proyecto(
            None,
            "Proyecto Eólico",
            "Desarrollo de parque eólico en la región norte",
            "2025-07-15",
        )
        proyecto_demo.id = obtener_o_crear_id(
            cursor,
            "SELECT id FROM proyecto WHERE nombre = ?",
            (proyecto_demo.nombre,),
            """
                INSERT INTO proyecto (nombre, descripcion, fecha_inicio)
                VALUES (?, ?, ?)
            """,
            (
                proyecto_demo.nombre,
                proyecto_demo.descripcion,
                proyecto_demo.fecha_inicio,
            ),
        )
        proyecto_uno.id = obtener_o_crear_id(
            cursor,
            "SELECT id FROM proyecto WHERE nombre = ?",
            (proyecto_uno.nombre,),
            """
                INSERT INTO proyecto (nombre, descripcion, fecha_inicio)
                VALUES (?, ?, ?)
            """,
            (
                proyecto_uno.nombre,
                proyecto_uno.descripcion,
                proyecto_uno.fecha_inicio,
            ),
        )
        mostrar_datos(
            cursor,
            "Datos creados en proyecto:",
            "SELECT * FROM proyecto WHERE id = ?",
            (proyecto_demo.id,),
        )
        mostrar_datos(
            cursor,
            "Datos creados en proyecto:",
            "SELECT * FROM proyecto WHERE id = ?",
            (proyecto_uno.id,),
        )

        ### ==========================================================
        ### OPERACIONES INSERT EN LA TABLA REGISTRO_TIEMPO (CREATE)
        ### ==========================================================
        print("### ==========================================================")
        print("\n--- CREATE: tabla registro_tiempo ---")
        registro_demo = RegistroTiempo(
            None,
            empleado_demo.id_empleado,
            proyecto_demo.id,
            "2025-09-01",
            8.0,
            "Desarrollo de módulo de autenticación",
        )
        registro_uno = RegistroTiempo(
            None,
            empleado_uno.id_empleado,
            proyecto_uno.id,
            "2025-09-02",
            7.5,
            "Implementación de interfaz de usuario",
        )
        registro_demo.id = obtener_o_crear_id(
            cursor,
            """
                SELECT id FROM registro_tiempo
                WHERE empleado_id = ? AND proyecto_id = ? AND fecha = ?
            """,
            (
                registro_demo.empleado_id,
                registro_demo.proyecto_id,
                registro_demo.fecha,
            ),
            """
                INSERT INTO registro_tiempo
                (empleado_id, proyecto_id, fecha, horas, descripcion)
                VALUES (?, ?, ?, ?, ?)
            """,
            (
                registro_demo.empleado_id,
                registro_demo.proyecto_id,
                registro_demo.fecha,
                registro_demo.horas,
                registro_demo.descripcion,
            ),
        )
        registro_uno.id = obtener_o_crear_id(
            cursor,
            """
                SELECT id FROM registro_tiempo
                WHERE empleado_id = ? AND proyecto_id = ? AND fecha = ?
            """,
            (
                registro_uno.empleado_id,
                registro_uno.proyecto_id,
                registro_uno.fecha,
            ),
            """
                INSERT INTO registro_tiempo
                (empleado_id, proyecto_id, fecha, horas, descripcion)
                VALUES (?, ?, ?, ?, ?)
            """,
            (
                registro_uno.empleado_id,
                registro_uno.proyecto_id,
                registro_uno.fecha,
                registro_uno.horas,
                registro_uno.descripcion,
            ),
        )
        mostrar_datos(
            cursor,
            "Datos creados en registro_tiempo:",
            "SELECT * FROM registro_tiempo WHERE id = ?",
            (registro_demo.id,),
        )
        mostrar_datos(
            cursor,
            "Datos creados en registro_tiempo:",
            "SELECT * FROM registro_tiempo WHERE id = ?",
            (registro_uno.id,),
        )

        # Creación de un objeto Informe, clase incluida en el modelo UML.
        informe_demo = Informe(
            "INF-001", "Resumen de actividades del Proyecto Solar"
        )

        ### ==========================================================
        ### MOSTRAR INFORMACIÓN DE LOS OBJETOS INSTANCIADOS
        ### ==========================================================
        print("\n--- Objetos del modelo ---")
        for objeto in (
            usuario_demo,
            empleado_demo,
            admin_demo,
            depto_demo,
            proyecto_demo,
            registro_demo,
            informe_demo,
        ):
            objeto.mostrar_info()
            print()

        ### ==========================================================
        ### CONSULTA DE REGISTROS (READ)
        ### ==========================================================
        print("### ==========================================================")
        print("--- READ: consulta de cada una de las seis tablas ---")
        consultas = [
            # 1. Consultar usuarios.
            ("Tabla usuario", "SELECT id, username, rol FROM usuario"),
            (
                # 2. Consultar empleados.
                "Tabla empleado",
                "SELECT id, nombre, email, salario, usuario_id FROM empleado",
            ),
            (
                # 3. Consultar administradores de Recursos Humanos.
                "Tabla administrador_rh",
                "SELECT id, nombre, email, usuario_id FROM administrador_rh",
            ),
            # 4. Consultar departamentos.
            ("Tabla departamento", "SELECT id, nombre, gerente_id FROM departamento"),
            (
                # 5. Consultar proyectos.
                "Tabla proyecto",
                "SELECT id, nombre, descripcion, fecha_inicio FROM proyecto",
            ),
            (
                # 6. Consultar registros de tiempo.
                "Tabla registro_tiempo",
                """
                    SELECT id, empleado_id, proyecto_id, fecha, horas, descripcion
                    FROM registro_tiempo
                """,
            ),
        ]
        # Ejecutar las consultas y mostrar todos los registros encontrados.
        for nombre, consulta in consultas:
            mostrar_datos(cursor, nombre, consulta)

        ### ==========================================================
        ### ACTUALIZACIÓN DE REGISTROS (UPDATE)
        ### ==========================================================
        print("### ==========================================================")
        print("\n--- UPDATE: actualizar un registro en cada tabla ---")
        actualizaciones = [
            # 1. Actualizar el rol de un usuario.
            (
                "usuario",
                "UPDATE usuario SET rol = ? WHERE id = ?",
                ("Administrador de Recursos Humanos", usuario_admin_demo.id),
                "SELECT id, username, rol FROM usuario WHERE id = ?",
                usuario_admin_demo.id,
            ),
            # 2. Actualizar el salario de un empleado.
            (
                "empleado",
                "UPDATE empleado SET salario = ? WHERE id = ?",
                (2100000.0, empleado_demo.id_empleado),
                "SELECT * FROM empleado WHERE id = ?",
                empleado_demo.id_empleado,
            ),
            # 3. Actualizar el nombre del administrador.
            (
                "administrador_rh",
                "UPDATE administrador_rh SET nombre = ? WHERE id = ?",
                ("Roberto Silva - RR. HH.", admin_demo.id_admin),
                "SELECT * FROM administrador_rh WHERE id = ?",
                admin_demo.id_admin,
            ),
            # 4. Actualizar el nombre del departamento.
            (
                "departamento",
                "UPDATE departamento SET nombre = ? WHERE id = ?",
                ("Innovación Tecnológica - Actualizado", depto_demo.id),
                "SELECT * FROM departamento WHERE id = ?",
                depto_demo.id,
            ),
            # 5. Actualizar la descripción del proyecto.
            (
                "proyecto",
                "UPDATE proyecto SET descripcion = ? WHERE id = ?",
                (
                    "Instalación de paneles solares en la sede central (en curso)",
                    proyecto_demo.id,
                ),
                "SELECT * FROM proyecto WHERE id = ?",
                proyecto_demo.id,
            ),
            # 6. Actualizar las horas y descripción del registro de tiempo.
            (
                "registro_tiempo",
                "UPDATE registro_tiempo SET horas = ?, descripcion = ? WHERE id = ?",
                (9.5, "Desarrollo extendido y pruebas", registro_demo.id),
                "SELECT * FROM registro_tiempo WHERE id = ?",
                registro_demo.id,
            ),
        ]
        # Actualizar cada registro y consultar sus datos nuevamente.
        for tabla, consulta, valores, consulta_lectura, id_registro in actualizaciones:
            cursor.execute(consulta, valores)
            mostrar_datos(
                cursor,
                f"Datos actualizados en {tabla}:",
                consulta_lectura,
                (id_registro,),
            )
        conexion.commit()

        ### ==========================================================
        ### ELIMINACIÓN DE REGISTROS (DELETE)
        ### ==========================================================
        print("### ==========================================================")
        print("\n--- DELETE: eliminar datos de prueba en las seis tablas ---")
        # Se muestran los datos antes de eliminarlos.
        mostrar_datos(
            cursor,
            "Datos eliminados de registro_tiempo:",
            "SELECT * FROM registro_tiempo WHERE empleado_id = ? AND proyecto_id = ? AND fecha = ?",
            (
                registro_uno.empleado_id,
                registro_uno.proyecto_id,
                registro_uno.fecha,
            ),
        )
        cursor.execute(
            """
                DELETE FROM registro_tiempo
                WHERE empleado_id = ? AND proyecto_id = ? AND fecha = ?
            """,
            (
                registro_uno.empleado_id,
                registro_uno.proyecto_id,
                registro_uno.fecha,
            ),
        )
        mostrar_datos(
            cursor,
            "Datos eliminados de departamento:",
            "SELECT * FROM departamento WHERE id = ?",
            (depto_uno.id,),
        )
        cursor.execute("DELETE FROM departamento WHERE id = ?", (depto_uno.id,))
        mostrar_datos(
            cursor,
            "Datos eliminados de administrador_rh:",
            "SELECT * FROM administrador_rh WHERE id = ?",
            (admin_uno.id_admin,),
        )
        cursor.execute(
            "DELETE FROM administrador_rh WHERE id = ?", (admin_uno.id_admin,)
        )
        mostrar_datos(
            cursor,
            "Datos eliminados de empleado:",
            "SELECT * FROM empleado WHERE id = ?",
            (empleado_uno.id_empleado,),
        )
        cursor.execute(
            "DELETE FROM empleado WHERE id = ?", (empleado_uno.id_empleado,)
        )
        mostrar_datos(
            cursor,
            "Datos eliminados de proyecto:",
            "SELECT * FROM proyecto WHERE id = ?",
            (proyecto_uno.id,),
        )
        cursor.execute("DELETE FROM proyecto WHERE id = ?", (proyecto_uno.id,))
        mostrar_datos(
            cursor,
            "Datos eliminados de usuario:",
            "SELECT id, username, rol FROM usuario WHERE id = ?",
            (usuario_admin_uno.id,),
        )
        cursor.execute("DELETE FROM usuario WHERE id = ?", (usuario_admin_uno.id,))
        mostrar_datos(
            cursor,
            "Datos eliminados de usuario:",
            "SELECT id, username, rol FROM usuario WHERE id = ?",
            (usuario_uno.id,),
        )
        cursor.execute("DELETE FROM usuario WHERE id = ?", (usuario_uno.id,))
        # Guarda los cambios de las operaciones realizadas en la base de datos.
        conexion.commit()

        print("\nLa ejecución finalizó correctamente.")

    except sqlite3.Error as error:
        # Revierte los cambios pendientes y muestra el error de SQLite.
        if conexion is not None:
            conexion.rollback()
        print(f"Error en la base de datos: {error}")
    ### ==========================================================
    ### CIERRE DE LA CONEXIÓN
    ### ==========================================================
        print("### ==========================================================")
    # Cierra la conexión aunque ocurra un error o termine la ejecución.
    finally:
        if conexion is not None:
            conexion.close()
            print("Conexión a la base de datos cerrada.")
    print("### ==========================================================")


# Ejecuta el programa cuando este archivo se inicia directamente.
if __name__ == "__main__":
    main()
