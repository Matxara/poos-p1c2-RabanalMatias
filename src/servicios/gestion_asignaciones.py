from persistencia.asignacion_dao import AsignacionDAO
from persistencia.empleado_dao import EmpleadoDAO
from persistencia.proyecto_dao import ProyectoDAO
from servicios.permisos import exigir_admin


def asignar(sesion, proyecto_id, empleado_id):
    exigir_admin(sesion)
    if ProyectoDAO.buscar_por_id(proyecto_id) is None:
        raise ValueError("No existe un proyecto con ese ID.")
    if EmpleadoDAO.buscar_por_id(empleado_id) is None:
        raise ValueError("No existe un empleado con ese ID.")
    if AsignacionDAO.esta_asignado(proyecto_id, empleado_id):
        raise ValueError("El empleado ya está asignado a ese proyecto.")
    AsignacionDAO.asignar(proyecto_id, empleado_id)


def desasignar(sesion, proyecto_id, empleado_id):
    exigir_admin(sesion)
    return AsignacionDAO.desasignar(proyecto_id, empleado_id)


def empleados_del_proyecto(sesion, proyecto_id):
    exigir_admin(sesion)
    return AsignacionDAO.empleados_de_proyecto(proyecto_id)
