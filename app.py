# Aplicación de consumo de API de clima
# Las consultas meteorológicas usan Open-Meteo.
# JSONPlaceholder permite demostrar CRUD de un registro de clima de ejemplo.

import hashlib
import hmac
import re
import secrets
import sqlite3
from getpass import getpass

import main as demo_empresa
import requests

GEOCODING_URL = "https://geocoding-api.open-meteo.com/v1/search"
WEATHER_URL = "https://api.open-meteo.com/v1/forecast"
CRUD_URL = "https://jsonplaceholder.typicode.com/posts"
TIMEOUT = 10
DATABASE = "ecotech_usuarios.db"
ITERACIONES_HASH = 310_000


def mostrar_respuesta(respuesta):
    print("Código HTTP:", respuesta.status_code)
    if respuesta.text:
        print("Respuesta JSON:")
        print(respuesta.json())
    else:
        print("La respuesta no tiene datos.")


def conectar_db():
    conexion = sqlite3.connect(DATABASE)
    conexion.execute(
        """CREATE TABLE IF NOT EXISTS usuarios (
               usuario TEXT PRIMARY KEY,
               sal BLOB NOT NULL,
               hash_contrasena BLOB NOT NULL
           )"""
    )
    return conexion


def validar_usuario(usuario):
    return bool(re.fullmatch(r"[A-Za-z0-9_.-]{3,32}", usuario))


def generar_hash(contrasena, sal=None):
    sal = sal or secrets.token_bytes(16)
    hash_contrasena = hashlib.pbkdf2_hmac(
        "sha256", contrasena.encode("utf-8"), sal, ITERACIONES_HASH
    )
    return sal, hash_contrasena


def registrar_usuario(conexion):
    usuario = input("Nuevo usuario (3-32 letras o números): ").strip()
    if not validar_usuario(usuario):
        print("Nombre de usuario inválido.")
        return

    contrasena = getpass("Nueva contraseña (mínimo 6 caracteres): ")
    confirmacion = getpass("Repita la contraseña: ")
    if not 6 <= len(contrasena) <= 128 or contrasena != confirmacion:
        print("Contraseña inválida o las contraseñas no coinciden.")
        return

    sal, hash_contrasena = generar_hash(contrasena)
    try:
        with conexion:
            conexion.execute(
                "INSERT INTO usuarios (usuario, sal, hash_contrasena) VALUES (?, ?, ?)",
                (usuario, sal, hash_contrasena),
            )
    except sqlite3.IntegrityError:
        print("Ese usuario ya existe.")
        return
    print("Usuario registrado.")


def autenticar(conexion):
    usuario = input("Usuario: ").strip()
    contrasena = getpass("Contraseña: ")
    if not validar_usuario(usuario) or not 1 <= len(contrasena) <= 128:
        print("Credenciales inválidas.")
        return False

    fila = conexion.execute(
        "SELECT sal, hash_contrasena FROM usuarios WHERE usuario = ?", (usuario,)
    ).fetchone()
    if fila is None:
        generar_hash(contrasena, b"\0" * 16)
        print("Credenciales inválidas.")
        return False

    sal, hash_guardado = fila
    _, hash_ingresado = generar_hash(contrasena, sal)
    if not hmac.compare_digest(hash_guardado, hash_ingresado):
        print("Credenciales inválidas.")
        return False
    return True


def validar_ciudad(ciudad):
    ciudad = " ".join(ciudad.strip().split())
    if 1 <= len(ciudad) <= 80 and re.fullmatch(r"[^\W\d_][\w .'-]*", ciudad):
        return ciudad
    return None


def consultar_clima(ciudad):
    # GET 1: busca las coordenadas de la ciudad.
    respuesta = requests.get(
        GEOCODING_URL,
        params={"name": ciudad, "count": 1, "language": "es", "format": "json"},
        timeout=TIMEOUT,
    )
    respuesta.raise_for_status()
    resultados = respuesta.json().get("results", [])
    if not resultados:
        print("No se encontró la ciudad.")
        return None

    lugar = resultados[0]

    # GET 2: obtiene el clima actual usando las coordenadas encontradas.
    respuesta = requests.get(
        WEATHER_URL,
        params={
            "latitude": lugar["latitude"],
            "longitude": lugar["longitude"],
            "current": "temperature_2m,relative_humidity_2m,weather_code,wind_speed_10m",
            "timezone": "auto",
        },
        timeout=TIMEOUT,
    )
    respuesta.raise_for_status()
    clima = respuesta.json()["current"]
    print("\nClima actual en", lugar["name"], lugar.get("country", ""))
    print("Temperatura:", clima["temperature_2m"], "°C")
    print("Humedad:", clima["relative_humidity_2m"], "%")
    print("Código meteorológico:", clima["weather_code"])
    print("Viento:", clima["wind_speed_10m"], "km/h")
    return clima


def ejecutar_consultas():
    ciudad = validar_ciudad(input("Ingrese una ciudad: "))
    if not ciudad:
        print("Nombre de ciudad inválido.")
        return

    print("\nGET --- Consultar clima")
    clima = consultar_clima(ciudad)
    if clima is None:
        return

    # JSONPlaceholder simula CRUD; no conserva los cambios permanentemente.
    registro_clima = {
        "title": f"Clima en {ciudad}",
        "body": f"Temperatura: {clima['temperature_2m']} °C",
        "userId": 1,
    }

    print("\nPOST --- Crear registro de clima de prueba")
    respuesta = requests.post(CRUD_URL, json=registro_clima, timeout=TIMEOUT)
    respuesta.raise_for_status()
    mostrar_respuesta(respuesta)

    print("\nPUT --- Reemplazar registro de clima de prueba")
    registro_actualizado = {
        "title": f"Reporte del clima en {ciudad}",
        "body": (
            f"Temperatura: {clima['temperature_2m']} °C; "
            f"humedad: {clima['relative_humidity_2m']} %; "
            f"viento: {clima['wind_speed_10m']} km/h"
        ),
        "userId": 1,
    }
    respuesta = requests.put(
        f"{CRUD_URL}/1", json=registro_actualizado, timeout=TIMEOUT
    )
    respuesta.raise_for_status()
    mostrar_respuesta(respuesta)

    print("\nPATCH --- Modificar parcialmente el registro de clima")
    respuesta = requests.patch(
        f"{CRUD_URL}/1",
        json={"body": f"Temperatura actual: {clima['temperature_2m']} °C"},
        timeout=TIMEOUT,
    )
    respuesta.raise_for_status()
    mostrar_respuesta(respuesta)

    print("\nDELETE --- Eliminar registro de clima de prueba")
    respuesta = requests.delete(f"{CRUD_URL}/1", timeout=TIMEOUT)
    respuesta.raise_for_status()
    mostrar_respuesta(respuesta)


def menu_sesion():
    while True:
        print("\n=== Funciones disponibles ===")
        print("1. Consultar clima y probar API")
        print("2. Ejecutar demo CRUD de la empresa")
        print("3. Cerrar sesión")
        opcion = input("Opción: ").strip()
        if opcion == "1":
            ejecutar_consultas()
        elif opcion == "2":
            demo_empresa.main()
        elif opcion == "3":
            print("Sesión cerrada.")
            return
        else:
            print("Opción inválida.")


def main():
    try:
        with conectar_db() as conexion:
            while True:
                print("\n=== EcoTech | Acceso seguro ===")
                print("1. Iniciar sesión")
                print("2. Registrar usuario")
                print("3. Salir")
                opcion = input("Opción: ").strip()
                if opcion == "1":
                    if autenticar(conexion):
                        print("Acceso autorizado.")
                        menu_sesion()
                elif opcion == "2":
                    registrar_usuario(conexion)
                elif opcion == "3":
                    print("Programa finalizado.")
                    break
                else:
                    print("Opción inválida.")
    except requests.exceptions.Timeout:
        print("Error: se agotó el tiempo de espera.")
    except requests.exceptions.HTTPError as error:
        estado = error.response.status_code if error.response is not None else "desconocido"
        print("Error HTTP:", estado)
    except requests.exceptions.ConnectionError:
        print("Error: no fue posible conectar con la API.")
    except requests.exceptions.RequestException:
        print("Error en la solicitud a la API.")
    except (ValueError, KeyError, TypeError):
        print("Error al procesar la respuesta de la API.")
    except sqlite3.Error:
        print("No fue posible acceder a la base local de usuarios.")


if __name__ == "__main__":
    main()
