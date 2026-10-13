import math
from datetime import date
from dependencia.reglas import validar_correo
from persistencia.conexion import ERRORES_BD, ERRORES_INTEGRIDAD



def pedir_texto(mensaje, obligatorio=True, maximo=None):
    while True:
        texto = input(mensaje).strip()
        if texto == "" and not obligatorio:
            return texto
        if texto == "":
            print("Este dato es obligatorio.")
        elif maximo is not None and len(texto) > maximo:
            print(f"No puede superar los {maximo} caracteres.")
        else:
            return texto


def pedir_entero(mensaje, minimo=1, opcional=False):
    while True:
        texto = input(mensaje).strip()
        if opcional and texto == "":
            return None
        if not texto.isdigit(): 
            print("Debe ingresar un número entero.")
            continue
        valor = int(texto)
        if valor < minimo:
            print(f"El número debe ser {minimo} o mayor.")
            continue
        return valor


def pedir_correo(mensaje, opcional=False):
    while True:
        texto = input(mensaje).strip()
        if opcional and texto == "":
            return ""
        try:
            return validar_correo(texto)
        except ValueError as error:
            print(error)


def pedir_decimal(mensaje, opcional=False):
    while True:
        texto = input(mensaje).strip().replace(",", ".")
        if opcional and texto == "":
            return None
        try:
            valor = float(texto)
        except ValueError:  
            print("Debe ingresar un número (ej: 7.5).")
            continue
        if not math.isfinite(valor):  
            print("Debe ingresar un número válido.")
            continue
        return valor


def pedir_fecha(mensaje, por_defecto=None):
    while True:
        texto = input(mensaje).strip()
        if texto == "":
            return por_defecto or date.today()
        try:
            return date.fromisoformat(texto)
        except ValueError:
            print("Fecha inválida. Use el formato AAAA-MM-DD (ej: 2026-10-15).")


def mostrar_lista(items, vacio):
    if not items:
        print(vacio)
    for item in items:
        print(" ", item)


def pedir_existente(dao, etiqueta):
    id_ = pedir_entero(f"ID del {etiqueta}: ")
    entidad = dao.buscar_por_id(id_)
    if entidad is None:
        print(f"No existe un {etiqueta} con ID {id_}.")
    return entidad


def ejecutar(accion):
    try:
        accion()
    except ValueError as error:  
        print(f"Dato no válido: {error}")
    except ERRORES_INTEGRIDAD:   
        print("No se pudo completar: el dato ya existe o hay registros relacionados.")
    except ERRORES_BD:          
        print("No fue posible completar la operación en la base de datos.")
    except Exception:          
        print("Ocurrió un error inesperado.")


def submenu(titulo, opciones):
    while True:
        print(f"\n--- {titulo} ---")
        for clave, (texto, _) in opciones.items():
            print(f"{clave}. {texto}")
        print("0. Volver")
        opcion = input("Seleccione una opción: ").strip()
        if opcion == "0":
            return
        if opcion in opciones:
            ejecutar(opciones[opcion][1])
        else:
            print("Opción no válida.")
