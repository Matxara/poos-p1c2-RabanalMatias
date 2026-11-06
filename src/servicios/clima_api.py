import os
import re
from datetime import datetime, timezone

from dotenv import load_dotenv

from dependencia.clima import Clima
from servicios.cliente_http import ErrorServicio, solicitar_json

URL_CLIMA = "https://api.openweathermap.org/data/2.5/weather"
_PATRON_LLAVE = re.compile(r"^[A-Za-z0-9]{16,64}$")

load_dotenv()


def _llave():
    llave = os.getenv("OPENWEATHER_API_KEY", "").strip()
    if not _PATRON_LLAVE.match(llave):
        raise ErrorServicio("La llave del servicio de clima no está configurada correctamente.")
    return llave


def obtener_clima(ciudad, pais):
    parametros = {"q": f"{ciudad},{pais}", "appid": _llave(), "units": "metric", "lang": "es"}
    return solicitar_json(URL_CLIMA, parametros)


class DeserializadorClima:
    @staticmethod
    def desde_api(datos, ciudad, pais):
        if not isinstance(datos, dict):
            raise ValueError("Respuesta inesperada.")
        principal = datos["main"]
        descripcion = datos["weather"][0]["description"]
        instante = datos["dt"]
        if type(instante) is not int:
            raise ValueError("Fecha inválida.")
        fecha = datetime.fromtimestamp(instante, tz=timezone.utc).date()
        return Clima(ciudad, pais, fecha, principal["temp"], principal["humidity"], descripcion)
