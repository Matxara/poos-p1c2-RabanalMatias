from functools import partial

from dependencia.departamento import Departamento
from menus.comun import mostrar_lista, pedir_entero, pedir_existente, pedir_texto, submenu
from servicios import gestion_departamentos


def registrar(sesion):
    departamento = Departamento(pedir_texto("Nombre del departamento: ", maximo=100))
    gestion_departamentos.registrar(sesion, departamento)
    print(f"Departamento registrado con ID {departamento.id}.")


def listar(sesion):
    mostrar_lista(gestion_departamentos.listar(sesion), "No hay departamentos registrados.")


def buscar(sesion):
    departamento = pedir_existente(partial(gestion_departamentos.buscar_por_id, sesion), "departamento")
    if departamento:
        print(" ", departamento, f"- {departamento.cantidad_empleados()} empleado(s)")
        mostrar_lista(departamento.empleados, "  (sin empleados)")


def actualizar(sesion):
    departamento = pedir_existente(partial(gestion_departamentos.buscar_por_id, sesion), "departamento")
    if departamento is None:
        return
    departamento.nombre = pedir_texto(f"Nuevo nombre [{departamento.nombre}]: ", maximo=100)
    print("Departamento actualizado." if gestion_departamentos.actualizar(sesion, departamento)
          else "Departamento no encontrado.")


def eliminar(sesion):
    id_ = pedir_entero("ID del departamento a eliminar: ")
    print("Departamento eliminado." if gestion_departamentos.eliminar(sesion, id_)
          else "No existe un departamento con ese ID.")


def menu_departamento(sesion):
    opciones = {
        "1": ("Registrar departamento", registrar),
        "2": ("Listar departamentos", listar),
        "3": ("Buscar departamento (con sus empleados)", buscar),
        "4": ("Actualizar departamento", actualizar),
        "5": ("Eliminar departamento", eliminar),
    }
    submenu("Departamentos", {k: (t, partial(f, sesion)) for k, (t, f) in opciones.items()})
