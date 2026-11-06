from datetime import date
from getpass import getpass

from dependencia.departamento import Departamento
from dependencia.empleado import Empleado
from dependencia.proyecto import Proyecto
from dependencia.registro_trabajo import RegistroTrabajo
from dependencia.usuario import Usuario
from menus.comun import pedir_correo, pedir_dato, pedir_telefono, pedir_texto
from persistencia.asignacion_dao import AsignacionDAO
from persistencia.conexion import ERRORES_BD
from persistencia.crear_bd import crear_tablas
from persistencia.departamento_dao import DepartamentoDAO
from persistencia.empleado_dao import EmpleadoDAO
from persistencia.proyecto_dao import ProyectoDAO
from persistencia.registro_trabajo_dao import RegistroTrabajoDAO
from persistencia.usuario_dao import UsuarioDAO
from servicios.autenticacion import crear_cuenta

DEPARTAMENTOS = ("Tecnología", "Operaciones")
PROYECTOS = ("Portal EcoTech", "Reciclaje Urbano")
EMPLEADOS_EJEMPLO = (
    ("Ana Torres", "ana@ecotech.cl", "911111111", "Analista"),
    ("Bruno Díaz", "bruno@ecotech.cl", "922222222", "Analista"),
)
DEPARTAMENTO_DE = {"ana@ecotech.cl": "Tecnología", "bruno@ecotech.cl": "Operaciones"}
ASIGNACIONES = (
    ("ana@ecotech.cl", "Portal EcoTech"),
    ("ana@ecotech.cl", "Reciclaje Urbano"),
    ("bruno@ecotech.cl", "Reciclaje Urbano"),
)
HORAS = (
    ("ana@ecotech.cl", "Portal EcoTech", "2026-10-05", 6.5, "Diseño de pantallas"),
    ("ana@ecotech.cl", "Reciclaje Urbano", "2026-10-06", 4, "Análisis de datos"),
    ("bruno@ecotech.cl", "Reciclaje Urbano", "2026-10-05", 8, "Ruta de recolección"),
)


def pedir_clave(usuario):
    while True:
        clave = pedir_dato(f"Contraseña para '{usuario}': ", Usuario.validar_clave, getpass)
        if clave == getpass("Repita la contraseña: "):
            return clave
        print("Las contraseñas no coinciden.")


def crear_primer_administrador():
    if UsuarioDAO.hay_administrador():
        print("Ya existe un administrador. No se creó otro.")
        return
    print("Cree la cuenta del primer administrador.")
    nombre = pedir_texto("Nombre completo: ", maximo=100)
    correo = pedir_correo("Correo: ")
    telefono = pedir_telefono("Teléfono (9 dígitos): ")
    cargo = pedir_texto("Cargo: ", maximo=100)
    usuario = pedir_dato("Nombre de usuario: ", Usuario.normalizar_usuario)
    clave = pedir_clave(usuario)
    empleado = EmpleadoDAO.buscar_por_correo(correo)
    if empleado is None:
        empleado = EmpleadoDAO.insertar(Empleado(nombre, correo, telefono, cargo))
    usuario_id = crear_cuenta(empleado.id, usuario, clave, "admin")
    print(f"Administrador '{usuario}' creado con ID {usuario_id}.")


def preguntar_si(mensaje):
    return input(mensaje).strip().lower() in ("s", "si", "sí")


def sembrar_datos():
    departamentos = {d.nombre: d for d in DepartamentoDAO.listar()}
    for nombre in DEPARTAMENTOS:
        if nombre not in departamentos:
            departamentos[nombre] = DepartamentoDAO.insertar(Departamento(nombre))
    proyectos = {p.nombre: p for p in ProyectoDAO.listar()}
    for nombre in PROYECTOS:
        if nombre not in proyectos:
            proyectos[nombre] = ProyectoDAO.insertar(Proyecto(nombre))

    empleados = {}
    for nombre, correo, telefono, cargo in EMPLEADOS_EJEMPLO:
        if EmpleadoDAO.buscar_por_correo(correo) is None:
            EmpleadoDAO.insertar(Empleado(nombre, correo, telefono, cargo))
    for correo, nombre_dep in DEPARTAMENTO_DE.items():
        empleado = EmpleadoDAO.buscar_por_correo(correo)
        empleados[correo] = empleado
        if empleado.departamento is None:
            empleado.cambiar_departamento(departamentos[nombre_dep])
            EmpleadoDAO.actualizar(empleado)

    for correo, nombre_proyecto in ASIGNACIONES:
        proyecto = proyectos[nombre_proyecto]
        if not AsignacionDAO.esta_asignado(proyecto.id, empleados[correo].id):
            AsignacionDAO.asignar(proyecto.id, empleados[correo].id)

    for correo, nombre_proyecto, fecha, horas, descripcion in HORAS:
        empleado = empleados[correo]
        if not RegistroTrabajoDAO.listar_por_empleado(empleado.id):
            for _, nombre_p, f, h, d in (x for x in HORAS if x[0] == correo):
                RegistroTrabajoDAO.insertar(RegistroTrabajo(empleado, proyectos[nombre_p], date.fromisoformat(f), h, d))
    print("Datos de prueba listos (departamentos, proyectos, asignaciones y horas).")


def sembrar():
    crear_tablas()
    crear_primer_administrador()
    if preguntar_si("¿Cargar datos de ejemplo (empleados, proyectos y horas)? (s/n): "):
        sembrar_datos()


if __name__ == "__main__":
    try:
        sembrar()
    except (ValueError, *ERRORES_BD):
        print("No fue posible preparar la base de datos. Revise su archivo .env.")
