import re
<<<<<<< HEAD
from datetime import date
=======
from datetime import date 
FECHA_MINIMA = date(2020, 1, 1)
FECHA_MAXIMA = date(2027, 1, 1)
>>>>>>> 7241be47e2963bf991dc9145db90b3713bc4d672

_PATRON_CORREO = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
_PATRON_TELEFONO = re.compile(r"^[0-9]{9}$")


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


def validar_telefono(valor):
    texto = validar_texto(valor, "teléfono", 9)
    if not _PATRON_TELEFONO.match(texto):
        raise ValueError("El teléfono debe tener exactamente 9 dígitos (solo números, ej: 912345678).")
    return texto


def validar_horas(valor):
    if isinstance(valor, bool) or not isinstance(valor, (int, float)):
        raise ValueError("Las horas deben ser un número.")
    if not 0 < valor <= 24:
        raise ValueError("Las horas deben ser mayores que 0 y no superar 24.")
    return float(valor)


def validar_fecha(valor):
    if not isinstance(valor, date):
        raise ValueError("La fecha debe ser un objeto date.")
<<<<<<< HEAD
    if not 2020 <= valor.year <= 2027:
        raise ValueError("El año de la fecha debe estar entre 2020 y 2027.")
    return valor
=======
    if not FECHA_MINIMA <= valor <= FECHA_MAXIMA:
        raise ValueError("La fecha debe estar entre 2020 y 2026.")
    return valor

>>>>>>> 7241be47e2963bf991dc9145db90b3713bc4d672
