from functools import partial

from dependencia.proyecto import Proyecto
from menus.comun import mostrar_lista, pedir_entero, pedir_existente, pedir_texto, submenu
from servicios import gestion_asignaciones, gestion_empleados, gestion_proyectos


def registrar(sesion):
    proyecto = Proyecto(pedir_texto("Nombre del proyecto: ", maximo=100))
    gestion_proyectos.registrar(sesion, proyecto)
    print(f"Proyecto registrado con ID {proyecto.id}.")


def listar(sesion):
    mostrar_lista(gestion_proyectos.listar(sesion), "No hay proyectos registrados.")


def buscar(sesion):
    proyecto = pedir_existente(partial(gestion_proyectos.buscar_por_id, sesion), "proyecto")
    if proyecto:
        print(" ", proyecto)


def actualizar(sesion):
    proyecto = pedir_existente(partial(gestion_proyectos.buscar_por_id, sesion), "proyecto")
    if proyecto is None:
        return
    proyecto.nombre = pedir_texto(f"Nuevo nombre [{proyecto.nombre}]: ", maximo=100)
    print("Proyecto actualizado." if gestion_proyectos.actualizar(sesion, proyecto)
          else "Proyecto no encontrado.")


def eliminar(sesion):
    id_ = pedir_entero("ID del proyecto a eliminar: ")
    print("Proyecto eliminado." if gestion_proyectos.eliminar(sesion, id_)
          else "No existe un proyecto con ese ID.")


def asignar(sesion):
    mostrar_lista(gestion_proyectos.listar(sesion), "(no hay proyectos registrados)")
    proyecto = pedir_existente(partial(gestion_proyectos.buscar_por_id, sesion), "proyecto")
    if proyecto is None:
        return
    mostrar_lista(gestion_empleados.listar_todos(sesion), "(no hay empleados registrados)")
    empleado = pedir_existente(partial(gestion_empleados.buscar_por_id, sesion), "empleado")
    if empleado is None:
        return
    gestion_asignaciones.asignar(sesion, proyecto.id, empleado.id)
    print(f"{empleado.nombre} quedó asignado al proyecto {proyecto.nombre}.")


def desasignar(sesion):
    proyecto_id = pedir_entero("ID del proyecto: ")
    empleado_id = pedir_entero("ID del empleado: ")
    print("Asignación eliminada." if gestion_asignaciones.desasignar(sesion, proyecto_id, empleado_id)
          else "Ese empleado no está asignado a ese proyecto.")


def ver_equipo(sesion):
    proyecto = pedir_existente(partial(gestion_proyectos.buscar_por_id, sesion), "proyecto")
    if proyecto is None:
        return
    print(" ", proyecto)
    mostrar_lista(gestion_asignaciones.empleados_del_proyecto(sesion, proyecto.id), "  (sin empleados asignados)")


def menu_proyecto(sesion):
    opciones = {
        "1": ("Registrar proyecto", registrar),
        "2": ("Listar proyectos", listar),
        "3": ("Buscar proyecto", buscar),
        "4": ("Actualizar proyecto", actualizar),
        "5": ("Eliminar proyecto", eliminar),
        "6": ("Asignar empleado a proyecto", asignar),
        "7": ("Quitar empleado de proyecto", desasignar),
        "8": ("Ver empleados asignados a un proyecto", ver_equipo),
    }
    submenu("Proyectos", {k: (t, partial(f, sesion)) for k, (t, f) in opciones.items()})
