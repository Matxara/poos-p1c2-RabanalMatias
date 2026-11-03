from persistencia.empleado_dao import EmpleadoDAO
from persistencia.registro_trabajo_dao import RegistroTrabajoDAO
from servicios.permisos import exigir_sesion


def mi_ficha(sesion):
    exigir_sesion(sesion)
    return EmpleadoDAO.buscar_por_id(sesion["empleado_id"])


def mis_registros(sesion):
    exigir_sesion(sesion)
    return RegistroTrabajoDAO.listar_por_empleado(sesion["empleado_id"])


def actualizar_mis_datos(sesion, nombre, correo):
    exigir_sesion(sesion)
    empleado = EmpleadoDAO.buscar_por_id(sesion["empleado_id"])
    if empleado is None:
        raise ValueError("Empleado no encontrado.")
    empleado.nombre = nombre
    empleado.correo = correo
    return EmpleadoDAO.actualizar(empleado)
