from persistencia.proyecto_dao import ProyectoDAO
from servicios.permisos import exigir_admin


def listar(sesion):
    exigir_admin(sesion)
    return ProyectoDAO.listar()


def buscar_por_id(sesion, id_proyecto):
    exigir_admin(sesion)
    return ProyectoDAO.buscar_por_id(id_proyecto)


def registrar(sesion, proyecto):
    exigir_admin(sesion)
    return ProyectoDAO.insertar(proyecto)


def actualizar(sesion, proyecto):
    exigir_admin(sesion)
    return ProyectoDAO.actualizar(proyecto)


def eliminar(sesion, id_proyecto):
    exigir_admin(sesion)
    return ProyectoDAO.eliminar(id_proyecto)
