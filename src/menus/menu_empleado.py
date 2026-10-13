"""Menú de Empleados (coordina: pide datos, crea objetos, llama al EmpleadoDAO)."""
from dependencia.empleado import Empleado
from menus.comun import (mostrar_lista, pedir_correo, pedir_entero, pedir_existente,
                         pedir_texto, submenu)
from persistencia.departamento_dao import DepartamentoDAO
from persistencia.empleado_dao import EmpleadoDAO


def registrar():
    nombre = pedir_texto("Nombre: ", maximo=100)
    correo = pedir_correo("Correo: ")
    cargo = pedir_texto("Cargo: ", maximo=100)
    mostrar_lista(DepartamentoDAO.listar(), "(no hay departamentos registrados)")
    id_dep = pedir_entero("ID del departamento (Enter = sin departamento): ", opcional=True)
    departamento = None
    if id_dep is not None:
        departamento = DepartamentoDAO.buscar_por_id(id_dep)
        if departamento is None:
            print("No existe un departamento con ese ID. Registro cancelado.")
            return
    empleado = Empleado(nombre, correo, cargo, departamento=departamento)  # id=None
    EmpleadoDAO.insertar(empleado)  # la BD genera el id y el DAO lo asigna
    print(f"Empleado registrado con ID {empleado.id}.")


def listar():
    mostrar_lista(EmpleadoDAO.listar(), "No hay empleados registrados.")


def buscar_por_id():
    empleado = pedir_existente(EmpleadoDAO, "empleado")
    if empleado:
        print(" ", empleado)


def buscar_por_correo():
    empleado = EmpleadoDAO.buscar_por_correo(pedir_texto("Correo: "))
    print(" ", empleado if empleado else "No existe un empleado con ese correo.")


def actualizar():
    empleado = pedir_existente(EmpleadoDAO, "empleado")
    if empleado is None:
        return
    print("Datos actuales:", empleado, "\n(Enter conserva el valor actual)")
    nombre = pedir_texto(f"Nombre [{empleado.nombre}]: ", obligatorio=False, maximo=100)
    correo = pedir_correo(f"Correo [{empleado.correo}]: ", opcional=True)
    cargo = pedir_texto(f"Cargo [{empleado.cargo}]: ", obligatorio=False, maximo=100)
    if nombre:
        empleado.nombre = nombre  # el setter valida
    if correo:
        empleado.correo = correo
    if cargo:
        empleado.cargo = cargo
    mostrar_lista(DepartamentoDAO.listar(), "(no hay departamentos registrados)")
    id_dep = pedir_entero("ID del departamento (Enter = sin cambio, 0 = quitar): ",
                          minimo=0, opcional=True)
    if id_dep == 0:
        empleado.cambiar_departamento(None)
    elif id_dep is not None:
        departamento = DepartamentoDAO.buscar_por_id(id_dep)
        if departamento is None:
            print("No existe un departamento con ese ID. Actualización cancelada.")
            return
        empleado.cambiar_departamento(departamento)
    if EmpleadoDAO.actualizar(empleado):
        print("Empleado actualizado correctamente.")
    else:
        print("Empleado no encontrado.")


def eliminar():
    if EmpleadoDAO.eliminar(pedir_entero("ID del empleado a eliminar: ")):
        print("Empleado eliminado.")
    else:
        print("No existe un empleado con ese ID.")


def menu_empleado():
    submenu("Empleados", {
        "1": ("Registrar empleado", registrar),
        "2": ("Listar empleados", listar),
        "3": ("Buscar empleado por ID", buscar_por_id),
        "4": ("Buscar empleado por correo", buscar_por_correo),
        "5": ("Actualizar empleado", actualizar),
        "6": ("Eliminar empleado", eliminar),
    })
