from dependencia.registro_trabajo import RegistroTrabajo
from persistencia.asignacion_dao import AsignacionDAO
from persistencia.empleado_dao import EmpleadoDAO
from persistencia.proyecto_dao import ProyectoDAO
from persistencia.registro_trabajo_dao import RegistroTrabajoDAO
from servicios.permisos import exigir_sesion


def mi_ficha(sesion):
    exigir_sesion(sesion)
    return EmpleadoDAO.buscar_por_id(sesion["empleado_id"])


def mis_registros(sesion):
    exigir_sesion(sesion)
    return RegistroTrabajoDAO.listar_por_empleado(sesion["empleado_id"])


def mis_proyectos(sesion):
    exigir_sesion(sesion)
    return AsignacionDAO.proyectos_de_empleado(sesion["empleado_id"])


def registrar_mis_horas(sesion, proyecto_id, fecha, horas, descripcion):
    exigir_sesion(sesion)
    empleado = EmpleadoDAO.buscar_por_id(sesion["empleado_id"])
    if empleado is None:
        raise ValueError("Empleado no encontrado.")
    if not AsignacionDAO.esta_asignado(proyecto_id, empleado.id):
        raise PermissionError("Solo puede registrar horas en proyectos que tiene asignados.")
    proyecto = ProyectoDAO.buscar_por_id(proyecto_id)
    if proyecto is None:
        raise ValueError("No existe un proyecto con ese ID.")
    registro = RegistroTrabajo(empleado, proyecto, fecha, horas, descripcion)
    RegistroTrabajoDAO.insertar(registro)
    return registro


def actualizar_mis_datos(sesion, nombre, correo):
    exigir_sesion(sesion)
    empleado = EmpleadoDAO.buscar_por_id(sesion["empleado_id"])
    if empleado is None:
        raise ValueError("Empleado no encontrado.")
    empleado.nombre = nombre
    empleado.correo = correo
    return EmpleadoDAO.actualizar(empleado)
