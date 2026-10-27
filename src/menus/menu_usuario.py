from getpass import getpass

from dependencia.usuario import Usuario
from menus.comun import ejecutar, pedir_dato, pedir_entero
from menus.menu_departamento import menu_departamento
from menus.menu_empleado import menu_empleado
from menus.menu_indicador import consultar_dolar
from menus.menu_proyecto import menu_proyecto
from menus.menu_registro import menu_registro
from persistencia.conexion import ERRORES_BD, ERRORES_INTEGRIDAD
from servicios.autenticacion import autenticar, registrar_usuario


def solicitar_registro():
    try:
        empleado_id = pedir_entero("ID del empleado: ")
        nombre = pedir_dato("Nuevo usuario: ", Usuario.normalizar_usuario)
        clave = pedir_dato("Contraseña: ", Usuario.validar_clave, getpass)
        if clave != getpass("Repita la contraseña: "):
            print("Las contraseñas no coinciden. Vuelva al registro.")
            return None
        usuario_id = registrar_usuario(empleado_id, nombre, clave)
    except (TypeError, ValueError) as error:
        print(error)
        return None
    except ERRORES_INTEGRIDAD:
        print("No se pudo crear esa cuenta.")
        return None
    except ERRORES_BD:
        print("No fue posible completar la operación en la base de datos.")
        return None
    print(f"Cuenta creada correctamente. ID: {usuario_id}")
    return usuario_id


def solicitar_login():
    nombre = input("Usuario: ")
    clave = getpass("Contraseña: ")
    try:
        usuario = autenticar(nombre, clave)
    except (TypeError, ValueError):
        print("No se pudo validar el acceso.")
        return None
    except ERRORES_BD:
        print("No fue posible completar la operación en la base de datos.")
        return None
    if usuario is None:
        print("Usuario o contraseña incorrectos.")
    else:
        print("Sesión iniciada correctamente.")
    return usuario


def mostrar_perfil(usuario_actual):
    if usuario_actual is None:
        print("Inicie sesión para ver el perfil.")
        return
    print(f"Usuario: {usuario_actual['nombre_usuario']}")
    print(f"Empleado: {usuario_actual['empleado_id']}")


def consultar_indicador(usuario_actual):
    if usuario_actual is None:
        print("Inicie sesión para consultar indicadores.")
        return
    consultar_dolar()


def mostrar_menu():
    print("\n---MENU ECOTECH---")
    print("1. Empleados")
    print("2. Departamentos")
    print("3. Proyectos")
    print("4. Registros de trabajo")
    print("5. Consultar dólar observado")
    print("6. Registrar usuario")
    print("7. Perfil")
    print("9. Cerrar sesión")
    print("0. Salir")


def menu_privado(usuario_actual):
    if usuario_actual is None:
        print("Debe iniciar sesión.")
        return "9"
    while True:
        mostrar_menu()
        opcion = input("Seleccione una opción: ").strip()
        if opcion in ("0", "9"):
            return opcion
        if opcion == "1":
            menu_empleado()
        elif opcion == "2":
            menu_departamento()
        elif opcion == "3":
            menu_proyecto()
        elif opcion == "4":
            menu_registro()
        elif opcion == "5":
            consultar_indicador(usuario_actual)
        elif opcion == "6":
            ejecutar(solicitar_registro)
        elif opcion == "7":
            mostrar_perfil(usuario_actual)
        else:
            print("Opción no válida.")
