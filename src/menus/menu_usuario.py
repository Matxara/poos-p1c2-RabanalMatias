from getpass import getpass

from menus.comun import (ejecutar, mostrar_lista, pedir_correo, pedir_decimal, pedir_entero,
                         pedir_fecha, pedir_texto, submenu)
from menus.menu_departamento import menu_departamento
from menus.menu_clima import menu_clima
from menus.menu_empleado import menu_empleado
from menus.menu_indicador import menu_indicador
from menus.menu_pago import calcular
from menus.menu_proyecto import menu_proyecto
from menus.menu_registro import menu_registro
from persistencia.conexion import ERRORES_BD
from servicios.autenticacion import autenticar
from servicios.mi_cuenta import (actualizar_mis_datos, mi_ficha, mis_proyectos, mis_registros,
                                 registrar_mis_horas)
from servicios.permisos import exigir_admin, exigir_sesion


def solicitar_login():
    nombre = input("Usuario: ")
    clave = getpass("Contraseña: ")
    try:
        usuario = autenticar(nombre, clave)
    except (TypeError, ValueError):
        print("No se pudo validar el acceso.")
        return None
    except ERRORES_BD:
        print("No fue posible completar la operación en la base de datos.")
        return None
    if usuario is None:
        print("Usuario o contraseña incorrectos.")
    else:
        print("Sesión iniciada correctamente.")
    return usuario


def mostrar_mi_ficha(usuario_actual):
    empleado = mi_ficha(usuario_actual)
    print(f"Usuario: {usuario_actual['nombre_usuario']}")
    print(f"Rol: {usuario_actual['rol']}")
    print(" ", empleado if empleado else "No se encontró su ficha de empleado.")


def mostrar_mis_registros(usuario_actual):
    registros = mis_registros(usuario_actual)
    if not registros:
        print("No tiene registros de trabajo.")
    for registro in registros:
        print(" ", registro)
    if registros:
        print(f"  Total: {sum(r.horas for r in registros):g} horas")


def mostrar_mis_proyectos(usuario_actual):
    mostrar_lista(mis_proyectos(usuario_actual), "No tiene proyectos asignados.")


def registrar_horas(usuario_actual):
    proyectos = mis_proyectos(usuario_actual)
    if not proyectos:
        print("No tiene proyectos asignados. Pida a un administrador que lo asigne.")
        return
    mostrar_lista(proyectos, "")
    proyecto_id = pedir_entero("ID del proyecto: ")
    fecha = pedir_fecha("Fecha AAAA-MM-DD (Enter = hoy): ")
    horas = pedir_decimal("Horas trabajadas: ")
    descripcion = pedir_texto("Descripción (opcional): ", obligatorio=False, maximo=250)
    registro = registrar_mis_horas(usuario_actual, proyecto_id, fecha, horas, descripcion)
    print(f"Registro de trabajo guardado con ID {registro.id}.")


def modificar_mis_datos(usuario_actual):
    empleado = mi_ficha(usuario_actual)
    if empleado is None:
        print("No se encontró su ficha de empleado.")
        return
    print("Datos actuales:", empleado, "\n(Enter conserva el valor actual)")
    nombre = pedir_texto(f"Nombre [{empleado.nombre}]: ", obligatorio=False, maximo=100)
    correo = pedir_correo(f"Correo [{empleado.correo}]: ", opcional=True)
    actualizar_mis_datos(usuario_actual, nombre or empleado.nombre, correo or empleado.correo)
    print("Sus datos fueron actualizados.")


def menu_servicios_externos(usuario_actual):
    exigir_sesion(usuario_actual)
    submenu("Servicios externos", {
        "1": ("Tipo de cambio (dólar / euro)", lambda: menu_indicador(usuario_actual)),
        "2": ("Clima de una ciudad", lambda: menu_clima(usuario_actual)),
    })


def menu_administracion(usuario_actual):
    exigir_admin(usuario_actual)
    submenu("Administración", {
        "1": ("Empleados", lambda: menu_empleado(usuario_actual)),
        "2": ("Departamentos", lambda: menu_departamento(usuario_actual)),
        "3": ("Proyectos y asignaciones", lambda: menu_proyecto(usuario_actual)),
        "4": ("Registros de trabajo (todos)", lambda: menu_registro(usuario_actual)),
        "5": ("Calcular pago en moneda extranjera", lambda: calcular(usuario_actual)),
    })


def mostrar_menu(usuario_actual):
    print("\n---MENU ECOTECH---")
    print("1. Mi ficha")
    print("2. Mis proyectos")
    print("3. Mis registros")
    print("4. Registrar mis horas")
    print("5. Modificar mis datos")
    print("6. Servicios externos (tipo de cambio y clima)")
    if usuario_actual["rol"] == "admin":
        print("7. Administración")
    print("9. Cerrar sesión")
    print("0. Salir")


def menu_privado(usuario_actual):
    try:
        exigir_sesion(usuario_actual)
    except PermissionError as error:
        print(error)
        return "9"
    acciones = {
        "1": mostrar_mi_ficha,
        "2": mostrar_mis_proyectos,
        "3": mostrar_mis_registros,
        "4": registrar_horas,
        "5": modificar_mis_datos,
        "6": menu_servicios_externos,
        "7": menu_administracion,
    }
    while True:
        mostrar_menu(usuario_actual)
        opcion = input("Seleccione una opción: ").strip()
        if opcion in ("0", "9"):
            return opcion
        if opcion in acciones:
            ejecutar(lambda: acciones[opcion](usuario_actual))
        else:
            print("Opción no válida.")
