"""Menú de Departamentos."""
from dependencia.departamento import Departamento
from menus.comun import mostrar_lista, pedir_entero, pedir_existente, pedir_texto, submenu
from persistencia.departamento_dao import DepartamentoDAO


def registrar():
    departamento = Departamento(pedir_texto("Nombre del departamento: ", maximo=100))
    DepartamentoDAO.insertar(departamento)
    print(f"Departamento registrado con ID {departamento.id}.")


def listar():
    mostrar_lista(DepartamentoDAO.listar(), "No hay departamentos registrados.")


def buscar():
    departamento = pedir_existente(DepartamentoDAO, "departamento")
    if departamento:
        print(" ", departamento, f"- {departamento.cantidad_empleados()} empleado(s)")
        mostrar_lista(departamento.empleados, "  (sin empleados)")


def actualizar():
    departamento = pedir_existente(DepartamentoDAO, "departamento")
    if departamento is None:
        return
    departamento.nombre = pedir_texto(f"Nuevo nombre [{departamento.nombre}]: ", maximo=100)
    print("Departamento actualizado." if DepartamentoDAO.actualizar(departamento)
          else "Departamento no encontrado.")


def eliminar():
    id_ = pedir_entero("ID del departamento a eliminar: ")
    print("Departamento eliminado." if DepartamentoDAO.eliminar(id_)
          else "No existe un departamento con ese ID.")


def menu_departamento():
    submenu("Departamentos", {
        "1": ("Registrar departamento", registrar),
        "2": ("Listar departamentos", listar),
        "3": ("Buscar departamento (con sus empleados)", buscar),
        "4": ("Actualizar departamento", actualizar),
        "5": ("Eliminar departamento", eliminar),
    })
