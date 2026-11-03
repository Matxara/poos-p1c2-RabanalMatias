from persistencia.empleado_dao import EmpleadoDAO
from servicios.permisos import exigir_admin


def listar_todos(sesion):
    exigir_admin(sesion)
    return EmpleadoDAO.listar()


def buscar_por_id(sesion, id_empleado):
    exigir_admin(sesion)
    return EmpleadoDAO.buscar_por_id(id_empleado)


def buscar_por_correo(sesion, correo):
    exigir_admin(sesion)
    return EmpleadoDAO.buscar_por_correo(correo)


def registrar(sesion, empleado):
    exigir_admin(sesion)
    return EmpleadoDAO.insertar(empleado)


def actualizar(sesion, empleado):
    exigir_admin(sesion)
    return EmpleadoDAO.actualizar(empleado)


def eliminar(sesion, id_empleado):
    exigir_admin(sesion)
    return EmpleadoDAO.eliminar(id_empleado)
