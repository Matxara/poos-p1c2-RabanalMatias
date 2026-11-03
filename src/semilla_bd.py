from getpass import getpass

from dependencia.empleado import Empleado
from dependencia.usuario import Usuario
from menus.comun import pedir_dato
from persistencia.conexion import ERRORES_BD
from persistencia.crear_bd import crear_tablas
from persistencia.empleado_dao import EmpleadoDAO
from persistencia.usuario_dao import UsuarioDAO
from servicios.autenticacion import crear_cuenta

CUENTAS = (
    ("Administrador", "admin@ecotech.cl", "900000000", "Administrador", "admin", "admin"),
    ("Ana Torres", "ana@ecotech.cl", "911111111", "Analista", "ana_torres", "empleado"),
    ("Bruno Díaz", "bruno@ecotech.cl", "922222222", "Analista", "bruno_diaz", "empleado"),
)


def pedir_clave(usuario):
    while True:
        clave = pedir_dato(f"Contraseña para '{usuario}': ", Usuario.validar_clave, getpass)
        if clave == getpass("Repita la contraseña: "):
            return clave
        print("Las contraseñas no coinciden.")


def sembrar_cuenta(nombre, correo, telefono, cargo, usuario, rol):
    empleado = EmpleadoDAO.buscar_por_correo(correo)
    if empleado is None:
        empleado = EmpleadoDAO.insertar(Empleado(nombre, correo, telefono, cargo))
        print(f"Empleado {nombre} creado con ID {empleado.id}.")
    else:
        print(f"Empleado {nombre} ya existe con ID {empleado.id}.")

    if UsuarioDAO.buscar_por_empleado(empleado.id) is not None:
        print(f"La cuenta de {nombre} ya existe. No se modificó nada.")
        return
    clave = pedir_clave(usuario)
    usuario_id = crear_cuenta(empleado.id, usuario, clave, rol)
    print(f"Cuenta '{usuario}' ({rol}) creada con ID {usuario_id}.")


def sembrar():
    crear_tablas()
    for cuenta in CUENTAS:
        sembrar_cuenta(*cuenta)


if __name__ == "__main__":
    try:
        sembrar()
    except (ValueError, *ERRORES_BD):
        print("No fue posible preparar la base de datos. Revise su archivo .env.")
