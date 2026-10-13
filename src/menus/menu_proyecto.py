"""Menú de Proyectos."""
from dependencia.proyecto import Proyecto
from menus.comun import mostrar_lista, pedir_entero, pedir_existente, pedir_texto, submenu
from persistencia.proyecto_dao import ProyectoDAO


def registrar():
    proyecto = Proyecto(pedir_texto("Nombre del proyecto: ", maximo=100))
    ProyectoDAO.insertar(proyecto)
    print(f"Proyecto registrado con ID {proyecto.id}.")


def listar():
    mostrar_lista(ProyectoDAO.listar(), "No hay proyectos registrados.")


def buscar():
    proyecto = pedir_existente(ProyectoDAO, "proyecto")
    if proyecto:
        print(" ", proyecto)


def actualizar():
    proyecto = pedir_existente(ProyectoDAO, "proyecto")
    if proyecto is None:
        return
    proyecto.nombre = pedir_texto(f"Nuevo nombre [{proyecto.nombre}]: ", maximo=100)
    print("Proyecto actualizado." if ProyectoDAO.actualizar(proyecto)
          else "Proyecto no encontrado.")


def eliminar():
    id_ = pedir_entero("ID del proyecto a eliminar: ")
    print("Proyecto eliminado." if ProyectoDAO.eliminar(id_)
          else "No existe un proyecto con ese ID.")


def menu_proyecto():
    submenu("Proyectos", {
        "1": ("Registrar proyecto", registrar),
        "2": ("Listar proyectos", listar),
        "3": ("Buscar proyecto", buscar),
        "4": ("Actualizar proyecto", actualizar),
        "5": ("Eliminar proyecto", eliminar),
    })
