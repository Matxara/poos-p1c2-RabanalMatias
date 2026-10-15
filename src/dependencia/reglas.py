import re
from datetime import date 
FECHA_MINIMA = date(2020, 1, 1)
FECHA_MAXIMA = date(2027, 1, 1)

_PATRON_CORREO = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def validar_texto(valor, campo, maximo=100):
    if not isinstance(valor, str) or not valor.strip():
        raise ValueError(f"El {campo} no puede estar vacío.")
    limpio = valor.strip()
    if len(limpio) > maximo:
        raise ValueError(f"El {campo} no puede superar los {maximo} caracteres.")
    return limpio


def validar_correo(valor):
    texto = validar_texto(valor, "correo", 150)
    if not _PATRON_CORREO.match(texto):
        raise ValueError("El correo no tiene un formato válido (ej: ana@ecotech.cl).")
    return texto.lower()


def validar_horas(valor):
    if isinstance(valor, bool) or not isinstance(valor, (int, float)):
        raise ValueError("Las horas deben ser un número.")
    if not 0 < valor <= 24:
        raise ValueError("Las horas deben ser mayores que 0 y no superar 24.")
    return float(valor)


def validar_fecha(valor):
    if not isinstance(valor, date):
        raise ValueError("La fecha debe ser un objeto date.")
    if not FECHA_MINIMA <= valor <= FECHA_MAXIMA:
        raise ValueError("La fecha debe estar entre 2020 y 2026.")
    return valor

