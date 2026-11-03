from functools import partial

from dependencia.empleado import Empleado
from menus.comun import (mostrar_lista, pedir_correo, pedir_entero, pedir_existente,
                         pedir_telefono, pedir_texto, submenu)
from menus.menu_cuenta import solicitar_registro
from servicios import gestion_departamentos, gestion_empleados


def registrar(sesion):
    nombre = pedir_texto("Nombre: ", maximo=100)
    correo = pedir_correo("Correo: ")
    telefono = pedir_telefono("Teléfono (9 dígitos): ")
    cargo = pedir_texto("Cargo: ", maximo=100)
    mostrar_lista(gestion_departamentos.listar(sesion), "(no hay departamentos registrados)")
    id_dep = pedir_entero("ID del departamento (Enter = sin departamento): ", opcional=True)
    departamento = None
    if id_dep is not None:
        departamento = gestion_departamentos.buscar_por_id(sesion, id_dep)
        if departamento is None:
            print("No existe un departamento con ese ID. Registro cancelado.")
            return
    empleado = Empleado(nombre, correo, telefono, cargo, departamento=departamento)
    gestion_empleados.registrar(sesion, empleado)
    print(f"Empleado registrado con ID {empleado.id}.")


def listar(sesion):
    mostrar_lista(gestion_empleados.listar_todos(sesion), "No hay empleados registrados.")


def buscar_por_id(sesion):
    empleado = pedir_existente(partial(gestion_empleados.buscar_por_id, sesion), "empleado")
    if empleado:
        print(" ", empleado)


def buscar_por_correo(sesion):
    empleado = gestion_empleados.buscar_por_correo(sesion, pedir_texto("Correo: "))
    print(" ", empleado if empleado else "No existe un empleado con ese correo.")


def actualizar(sesion):
    empleado = pedir_existente(partial(gestion_empleados.buscar_por_id, sesion), "empleado")
    if empleado is None:
        return
    print("Datos actuales:", empleado, "\n(Enter conserva el valor actual)")
    nombre = pedir_texto(f"Nombre [{empleado.nombre}]: ", obligatorio=False, maximo=100)
    correo = pedir_correo(f"Correo [{empleado.correo}]: ", opcional=True)
    telefono = pedir_telefono(f"Teléfono [{empleado.telefono}]: ", opcional=True)
    cargo = pedir_texto(f"Cargo [{empleado.cargo}]: ", obligatorio=False, maximo=100)
    if nombre:
        empleado.nombre = nombre
    if correo:
        empleado.correo = correo
    if telefono:
        empleado.telefono = telefono
    if cargo:
        empleado.cargo = cargo
    mostrar_lista(gestion_departamentos.listar(sesion), "(no hay departamentos registrados)")
    id_dep = pedir_entero("ID del departamento (Enter = sin cambio, 0 = quitar): ",
                          minimo=0, opcional=True)
    if id_dep == 0:
        empleado.cambiar_departamento(None)
    elif id_dep is not None:
        departamento = gestion_departamentos.buscar_por_id(sesion, id_dep)
        if departamento is None:
            print("No existe un departamento con ese ID. Actualización cancelada.")
            return
        empleado.cambiar_departamento(departamento)
    if gestion_empleados.actualizar(sesion, empleado):
        print("Empleado actualizado correctamente.")
    else:
        print("Empleado no encontrado.")


def eliminar(sesion):
    if gestion_empleados.eliminar(sesion, pedir_entero("ID del empleado a eliminar: ")):
        print("Empleado eliminado.")
    else:
        print("No existe un empleado con ese ID.")


def menu_empleado(sesion):
    opciones = {
        "1": ("Registrar empleado", registrar),
        "2": ("Listar empleados", listar),
        "3": ("Buscar empleado por ID", buscar_por_id),
        "4": ("Buscar empleado por correo", buscar_por_correo),
        "5": ("Actualizar empleado", actualizar),
        "6": ("Eliminar empleado", eliminar),
        "7": ("Registrar cuenta de usuario", solicitar_registro),
    }
    submenu("Empleados", {k: (t, partial(f, sesion)) for k, (t, f) in opciones.items()})
