import math

from dependencia.reglas import MONEDAS
from servicios.cliente_http import solicitar_json

URL_BASE = "https://mindicador.cl/api/"


def url_indicador(codigo):
    if codigo not in MONEDAS:
        raise ValueError("Moneda no admitida.")
    return URL_BASE + codigo


def obtener_datos(codigo="dolar"):
    return solicitar_json(url_indicador(codigo))


def extraer_primero(datos):
    if not isinstance(datos, dict):
        raise ValueError("Respuesta inesperada.")

    serie = datos.get("serie")

    if not isinstance(serie, list) or not serie:
        raise ValueError("No hay valores disponibles.")

    registro = serie[0]
    valor = registro["valor"]

    if type(valor) not in (int, float) or not math.isfinite(valor) or valor <= 0:
        raise ValueError("Valor del indicador inválido.")

    return registro["fecha"], valor
