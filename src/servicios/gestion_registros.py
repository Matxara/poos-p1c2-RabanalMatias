from persistencia.registro_trabajo_dao import RegistroTrabajoDAO
from servicios.permisos import exigir_admin


def listar(sesion):
    exigir_admin(sesion)
    return RegistroTrabajoDAO.listar()


def listar_por_empleado(sesion, id_empleado):
    exigir_admin(sesion)
    return RegistroTrabajoDAO.listar_por_empleado(id_empleado)


def buscar_por_id(sesion, id_registro):
    exigir_admin(sesion)
    return RegistroTrabajoDAO.buscar_por_id(id_registro)


def registrar(sesion, registro):
    exigir_admin(sesion)
    return RegistroTrabajoDAO.insertar(registro)


def actualizar(sesion, registro):
    exigir_admin(sesion)
    return RegistroTrabajoDAO.actualizar(registro)


def eliminar(sesion, id_registro):
    exigir_admin(sesion)
    return RegistroTrabajoDAO.eliminar(id_registro)
