from dependencia.registro_trabajo import RegistroTrabajo
from menus.comun import (mostrar_lista, pedir_decimal, pedir_entero, pedir_existente,
                         pedir_fecha, pedir_texto, submenu)
from persistencia.empleado_dao import EmpleadoDAO
from persistencia.proyecto_dao import ProyectoDAO
from persistencia.registro_trabajo_dao import RegistroTrabajoDAO


def registrar():
    mostrar_lista(EmpleadoDAO.listar(), "(no hay empleados registrados)")
    empleado = pedir_existente(EmpleadoDAO, "empleado")
    if empleado is None:
        return
    mostrar_lista(ProyectoDAO.listar(), "(no hay proyectos registrados)")
    proyecto = pedir_existente(ProyectoDAO, "proyecto")
    if proyecto is None:
        return
    fecha = pedir_fecha("Fecha AAAA-MM-DD (Enter = hoy): ")
    horas = pedir_decimal("Horas trabajadas: ")
    descripcion = pedir_texto("Descripción (opcional): ", obligatorio=False, maximo=250)
    registro = RegistroTrabajo(empleado, proyecto, fecha, horas, descripcion)
    RegistroTrabajoDAO.insertar(registro)
    print(f"Registro de trabajo guardado con ID {registro.id}.")


def listar():
    mostrar_lista(RegistroTrabajoDAO.listar(), "No hay registros de trabajo.")


def listar_por_empleado():
    registros = RegistroTrabajoDAO.listar_por_empleado(pedir_entero("ID del empleado: "))
    mostrar_lista(registros, "Ese empleado no tiene registros de trabajo.")
    if registros:
        print(f"  Total: {sum(r.horas for r in registros):g} horas")


def actualizar():
    registro = pedir_existente(RegistroTrabajoDAO, "registro")
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
    print("Registro actualizado." if RegistroTrabajoDAO.actualizar(registro)
          else "Registro no encontrado.")


def eliminar():
    id_ = pedir_entero("ID del registro a eliminar: ")
    print("Registro eliminado." if RegistroTrabajoDAO.eliminar(id_)
          else "No existe un registro con ese ID.")


def menu_registro():
    submenu("Registros de trabajo", {
        "1": ("Registrar horas de trabajo", registrar),
        "2": ("Listar todos los registros", listar),
        "3": ("Listar registros de un empleado", listar_por_empleado),
        "4": ("Actualizar registro", actualizar),
        "5": ("Eliminar registro", eliminar),
    })
