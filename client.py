import os
import signal
import sys
import json
import time
import platform
import subprocess
import api_client

SEPARATOR = "="*50

# Controlador Ctrl+C
def ctrl_c(signal, frame):
    print("\n\n[!] Cancelando programa...")
    sys.exit(0)

signal.signal(signal.SIGINT, ctrl_c)

# Detectar Sistema Operativo
def os_detect():
    system = platform.system()
    if system == "Windows":
        os.system("cls")
    elif system == "Linux":
        os.system("clear")
    else:
        print(system)

# Detectar conexión con el servidor
def connect_server(response):
    if response is None:
        print("[!] No se pudo conectar al servidor.")
        print(SEPARATOR)
        return

    print(SEPARATOR)
    print(f"Status: {response.status_code}")
    responses(response)

# Orquestador de las respuestas
def responses(response):
    if response.status_code == 200:
        data = response.json()
        print(SEPARATOR)
        print(json.dumps(data, indent=2))
        print(SEPARATOR)

    elif response.status_code == 201:
        print(SEPARATOR)
        data = response.json()
        print(json.dumps(data, indent=2))
        print(SEPARATOR)

    elif response.status_code == 204:
        print(SEPARATOR)
        print("[+] Usuario/s eliminado exitosamente")
        print(SEPARATOR)

    elif response.status_code == 404:
        print(SEPARATOR)
        print("[!] Recurso no encontrado")
        print(SEPARATOR)

    else:
        print(SEPARATOR)
        print(f"[!] Error no esperado: {response.status_code}")
        print(SEPARATOR)


# Menú/Algoritmo principal
if __name__ == "__main__":
    os_detect()
    while True:
        print("\n\n==== CLIENTE - API/REST ===\n")
        print("[0] Limpiar la pantalla")
        print("[1] Consultar todos los usuarios.")
        print("[2] Consultar un usuario especifico.")
        print("[3] Crear un nuevo usuario.")
        print("[4] Crear varios usuarios")
        print("[5] Eliminar un usuario existente")
        print("[6] Eliminar todos los usuarios")
        print("[7] Actualizar datos de un usuario")
        print("[8] Abrir interfaz gráfica (GUI)")
        print("[9] Salir")

        try:
            opcion = int(input("\n[-] Ingresa tu opción: "))
        except (ValueError, IndexError):
            print("\n[!] Opción no válida. Ingresa uno de los números en el menú.")
            print(SEPARATOR)
            continue

        match opcion:
            case 0:
                os_detect()

            case 1:
                print()
                response = api_client.all_users()
                connect_server(response)

            case 2:
                try:
                    id_user = int(input("[-] Ingresa el id del usuario a consultar: "))
                    print()
                    response = api_client.user(id_user)
                    connect_server(response)
                except ValueError:
                    print("\n[!] Formato no válido. Ingresa un número entero.")
                    print(SEPARATOR)

            case 3:
                try:
                    new_name = input("[-] Ingresa el nombre del nuevo usuario: ")
                    new_age = int(input("[-] Ingresa la edad del nuevo usuario: "))
                    new_phone = input("[-] Ingresa el teléfono del nuevo usuario: ")
                    print()
                    response = api_client.upload_users(new_name, new_age, new_phone)
                    connect_server(response)
                except ValueError:
                    print("\n[!] Formato no válido. Alguno de los datos no cumple con el formato esperado.")
                    print(SEPARATOR)
            case 4:
                try:
                    count = int(input("[-] Ingresa la cantidad de usuarios que vas a registrar: "))
                    for i in range(1, count+1):
                        new_name = input(f"[-] Ingresa el nombre del usuario {i}: ")
                        new_age = int(input(f"[-] Ingresa la edad del usuario {i}: "))
                        new_phone = input(f"[-] Ingresa el teléfono del usuario {i}: ")
                        print()
                        response = api_client.upload_users(new_name, new_age, new_phone)
                        connect_server(response)
                except ValueError:
                    print("\n[!] Formato no válido. Alguno de los datos no cumple con el formato esperado.")
                    print(SEPARATOR)

            case 5:
                try:
                    delete_user = int(input("[-] Ingresa el id del usuario a eliminar: "))
                    print()
                    response = api_client.delete_users(delete_user)
                    connect_server(response)
                except ValueError:
                    print("\n[!] Formato no válido. Ingresa un número entero.")
                    print(SEPARATOR)

            case 6:
                response = api_client.delete_all_users()
                connect_server(response)

            case 7:
                try:
                    user_id = int(input("[-] Ingresa el 'id' del usuario a actualizar: "))
                except ValueError:
                    print("\n[!] Formato no válido. Ingresa un número entero.")
                    print(SEPARATOR)
                    continue

                while True:
                    print("\n=== Submenú - Actualizar datos ===\n")
                    print("[0] Limpiar la pantalla")
                    print("[1] Actualizar un campo único")
                    print("[2] Actualizar todos los campos")
                    print("[9] Volver al menú principal")

                    try:
                        sub_opcion = int(input("[-] Ingresa tu opción: "))
                    except ValueError:
                        print("\n[!] Opción no válida.")
                        continue

                    match sub_opcion:
                        case 0:
                            os_detect()

                        case 1:
                            print("\n=== Campos válidos: name, age, phone")
                            field = input("[-] Ingresa el campo a actualizar: ").strip()

                            if field not in ("name", "age", "phone"):
                                print("\n[!] Campo no válido")
                                break

                            value = input(f"[-] Ingresa el nuevo valor de '{field}': ")
                            response = api_client.update_user_field(user_id, field, value)
                            connect_server(response)
                            break

            case 8:
                print("\n[+] Abriendo interfaz gráfica...")
                subprocess.run(["python", "client_gui.py"])
                os_detect()

            case 9:
                print("\n[+] Saliendo...")
                time.sleep(0.5)
                sys.exit(0)

            case _:
                print("\n[!] Ingresa uno de los números en el menú.")
                print(SEPARATOR)
                time.sleep(1)
                os_detect()
                continue
