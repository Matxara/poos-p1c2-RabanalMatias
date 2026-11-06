from getpass import getpass

from dependencia.usuario import Usuario
from menus.comun import mostrar_lista, pedir_dato, pedir_entero
from persistencia.conexion import ERRORES_BD, ERRORES_INTEGRIDAD
from servicios.autenticacion import listar_cuentas, registrar_usuario


def pedir_rol():
    while True:
        opcion = input("Rol (1 = empleado, 2 = administrador): ").strip()
        if opcion == "1":
            return "empleado"
        if opcion == "2":
            return "admin"
        print("Opción no válida.")


def solicitar_registro(sesion):
    try:
        empleado_id = pedir_entero("ID del empleado: ")
        nombre = pedir_dato("Nuevo usuario: ", Usuario.normalizar_usuario)
        clave = pedir_dato("Contraseña: ", Usuario.validar_clave, getpass)
        if clave != getpass("Repita la contraseña: "):
            print("Las contraseñas no coinciden. Vuelva al registro.")
            return None
        rol = pedir_rol()
        usuario_id = registrar_usuario(sesion, empleado_id, nombre, clave, rol)
    except (PermissionError, TypeError, ValueError) as error:
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


def ver_cuentas(sesion):
    mostrar_lista([c.mostrar_datos() for c in listar_cuentas(sesion)], "No hay cuentas registradas.")
