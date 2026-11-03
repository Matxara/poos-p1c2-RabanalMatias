from functools import partial

from dependencia.registro_trabajo import RegistroTrabajo
from menus.comun import (mostrar_lista, pedir_decimal, pedir_entero, pedir_existente,
                         pedir_fecha, pedir_texto, submenu)
from servicios import gestion_empleados, gestion_proyectos, gestion_registros


def registrar(sesion):
    mostrar_lista(gestion_empleados.listar_todos(sesion), "(no hay empleados registrados)")
    empleado = pedir_existente(partial(gestion_empleados.buscar_por_id, sesion), "empleado")
    if empleado is None:
        return
    mostrar_lista(gestion_proyectos.listar(sesion), "(no hay proyectos registrados)")
    proyecto = pedir_existente(partial(gestion_proyectos.buscar_por_id, sesion), "proyecto")
    if proyecto is None:
        return
    fecha = pedir_fecha("Fecha AAAA-MM-DD (Enter = hoy): ")
    horas = pedir_decimal("Horas trabajadas: ")
    descripcion = pedir_texto("Descripción (opcional): ", obligatorio=False, maximo=250)
    registro = RegistroTrabajo(empleado, proyecto, fecha, horas, descripcion)
    gestion_registros.registrar(sesion, registro)
    print(f"Registro de trabajo guardado con ID {registro.id}.")


def listar(sesion):
    mostrar_lista(gestion_registros.listar(sesion), "No hay registros de trabajo.")


def listar_por_empleado(sesion):
    registros = gestion_registros.listar_por_empleado(sesion, pedir_entero("ID del empleado: "))
    mostrar_lista(registros, "Ese empleado no tiene registros de trabajo.")
    if registros:
        print(f"  Total: {sum(r.horas for r in registros):g} horas")


def actualizar(sesion):
    registro = pedir_existente(partial(gestion_registros.buscar_por_id, sesion), "registro")
    if registro is None:
        return
    print("Datos actuales:", registro, "\n(Enter conserva el valor actual)")
    registro.fecha = pedir_fecha(f"Fecha [{registro.fecha.isoformat()}]: ", por_defecto=registro.fecha)
    horas = pedir_decimal(f"Horas [{registro.horas:g}]: ", opcional=True)
    descripcion = pedir_texto("Descripción: ", obligatorio=False, maximo=250)
    if horas is not None:
        registro.horas = horas  # el setter valida
    if descripcion:
        registro.descripcion = descripcion
    print("Registro actualizado." if gestion_registros.actualizar(sesion, registro)
          else "Registro no encontrado.")


def eliminar(sesion):
    id_ = pedir_entero("ID del registro a eliminar: ")
    print("Registro eliminado." if gestion_registros.eliminar(sesion, id_)
          else "No existe un registro con ese ID.")


def menu_registro(sesion):
    opciones = {
        "1": ("Registrar horas de trabajo", registrar),
        "2": ("Listar todos los registros", listar),
        "3": ("Listar registros de un empleado", listar_por_empleado),
        "4": ("Actualizar registro", actualizar),
        "5": ("Eliminar registro", eliminar),
    }
    submenu("Registros de trabajo", {k: (t, partial(f, sesion)) for k, (t, f) in opciones.items()})
