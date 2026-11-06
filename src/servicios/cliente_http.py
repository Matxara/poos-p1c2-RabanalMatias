import requests

TIMEOUT = (3, 5)

_MENSAJES = {
    400: "La consulta no es válida.",
    401: "El servicio rechazó las credenciales configuradas.",
    403: "El servicio no autorizó la consulta.",
    404: "No se encontró el recurso solicitado.",
    429: "Se superó el límite de consultas del servicio. Intente más tarde.",
}


class ErrorServicio(Exception):
    def __init__(self, mensaje, codigo=None):
        super().__init__(mensaje)
        self.mensaje = mensaje
        self.codigo = codigo


def solicitar_json(url, params=None):
    try:
        respuesta = requests.get(url, params=params, timeout=TIMEOUT)
    except requests.exceptions.Timeout:
        raise ErrorServicio("El servicio tardó demasiado en responder.") from None
    except requests.exceptions.ConnectionError:
        raise ErrorServicio("No hay conexión con el servicio externo.") from None
    except requests.exceptions.RequestException:
        raise ErrorServicio("No fue posible consultar el servicio externo.") from None

    codigo = respuesta.status_code
    if codigo == 200:
        try:
            return respuesta.json()
        except ValueError:
            raise ErrorServicio("El servicio entregó una respuesta ilegible.", 200) from None
    if codigo in _MENSAJES:
        raise ErrorServicio(_MENSAJES[codigo], codigo)
    if 500 <= codigo <= 599:
        raise ErrorServicio("El servicio externo no está disponible por el momento.", codigo)
    raise ErrorServicio("El servicio entregó una respuesta inesperada.", codigo)
