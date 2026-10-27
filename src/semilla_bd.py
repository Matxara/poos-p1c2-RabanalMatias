from getpass import getpass

from dependencia.empleado import Empleado
from dependencia.usuario import Usuario
from menus.comun import pedir_dato
from persistencia.conexion import ERRORES_BD
from persistencia.crear_bd import crear_tablas
from persistencia.empleado_dao import EmpleadoDAO
from persistencia.usuario_dao import UsuarioDAO
from servicios.autenticacion import registrar_usuario

CORREO_ADMIN = "admin@ecotech.cl"
USUARIO_ADMIN = "admin"


def sembrar():
    crear_tablas()
    empleado = EmpleadoDAO.buscar_por_correo(CORREO_ADMIN)
    if empleado is None:
        empleado = EmpleadoDAO.insertar(
            Empleado("Administrador", CORREO_ADMIN, "900000000", "Administrador"))
        print(f"Empleado administrador creado con ID {empleado.id}.")
    else:
        print(f"Empleado administrador ya existe con ID {empleado.id}.")

    if UsuarioDAO.buscar_por_empleado(empleado.id) is not None:
        print("La cuenta admin ya existe. No se modificó nada.")
        return

    while True:
        clave = pedir_dato(f"Contraseña para '{USUARIO_ADMIN}': ", Usuario.validar_clave, getpass)
        if clave == getpass("Repita la contraseña: "):
            break
        print("Las contraseñas no coinciden.")
    usuario_id = registrar_usuario(empleado.id, USUARIO_ADMIN, clave)
    print(f"Cuenta admin creada con ID {usuario_id}.")


if __name__ == "__main__":
    try:
        sembrar()
    except (ValueError, *ERRORES_BD):
        print("No fue posible preparar la base de datos. Revise su archivo .env.")
