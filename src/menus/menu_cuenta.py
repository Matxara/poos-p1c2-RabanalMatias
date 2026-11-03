from getpass import getpass

from dependencia.usuario import Usuario
from menus.comun import pedir_dato, pedir_entero
from persistencia.conexion import ERRORES_BD, ERRORES_INTEGRIDAD
from servicios.autenticacion import registrar_usuario


def solicitar_registro(sesion):
    try:
        empleado_id = pedir_entero("ID del empleado: ")
        nombre = pedir_dato("Nuevo usuario: ", Usuario.normalizar_usuario)
        clave = pedir_dato("Contraseña: ", Usuario.validar_clave, getpass)
        if clave != getpass("Repita la contraseña: "):
            print("Las contraseñas no coinciden. Vuelva al registro.")
            return None
        usuario_id = registrar_usuario(sesion, empleado_id, nombre, clave)
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
