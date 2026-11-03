from persistencia.departamento_dao import DepartamentoDAO
from servicios.permisos import exigir_admin


def listar(sesion):
    exigir_admin(sesion)
    return DepartamentoDAO.listar()


def buscar_por_id(sesion, id_departamento):
    exigir_admin(sesion)
    return DepartamentoDAO.buscar_por_id(id_departamento)


def registrar(sesion, departamento):
    exigir_admin(sesion)
    return DepartamentoDAO.insertar(departamento)


def actualizar(sesion, departamento):
    exigir_admin(sesion)
    return DepartamentoDAO.actualizar(departamento)


def eliminar(sesion, id_departamento):
    exigir_admin(sesion)
    return DepartamentoDAO.eliminar(id_departamento)
