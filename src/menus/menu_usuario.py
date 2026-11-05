from getpass import getpass

from menus.comun import ejecutar, pedir_correo, pedir_texto
from menus.menu_departamento import menu_departamento
from menus.menu_empleado import menu_empleado
from menus.menu_indicador import menu_indicador
from menus.menu_proyecto import menu_proyecto
from menus.menu_registro import menu_registro
from persistencia.conexion import ERRORES_BD
from servicios.autenticacion import autenticar
from servicios.mi_cuenta import actualizar_mis_datos, mi_ficha, mis_registros
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


def abrir_admin(menu, usuario_actual):
    exigir_admin(usuario_actual)
    menu(usuario_actual)


def mostrar_menu(usuario_actual):
    print("\n---MENU ECOTECH---")
    print("1. Mi ficha")
    print("2. Mis registros")
    print("3. Indicadores (dólar)")
    print("4. Modificar mis datos")
    if usuario_actual["rol"] == "admin":
        print("5. Administrar empleados")
        print("6. Departamentos")
        print("7. Proyectos")
        print("8. Registros de trabajo (todos)")
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
        "2": mostrar_mis_registros,
        "3": menu_indicador,
        "4": modificar_mis_datos,
    }
    acciones_admin = {
        "5": menu_empleado,
        "6": menu_departamento,
        "7": menu_proyecto,
        "8": menu_registro,
    }
    while True:
        mostrar_menu(usuario_actual)
        opcion = input("Seleccione una opción: ").strip()
        if opcion in ("0", "9"):
            return opcion
        if opcion in acciones:
            ejecutar(lambda: acciones[opcion](usuario_actual))
        elif opcion in acciones_admin:
            ejecutar(lambda: abrir_admin(acciones_admin[opcion], usuario_actual))
        else:
            print("Opción no válida.")
