from dependencia.clima import Clima
from persistencia.clima_dao import ClimaDAO
from persistencia.conexion import ERRORES_BD
from servicios.clima_api import DeserializadorClima, obtener_clima
from servicios.cliente_http import ErrorServicio
from servicios.permisos import exigir_sesion


def _resultado(clima, origen, mensaje, guardado=False):
    return {"clima": clima, "origen": origen, "mensaje": mensaje, "guardado": guardado}


def buscar_respaldo(ciudad, pais, motivo):
    try:
        respaldo = ClimaDAO.ultimo(ciudad, pais)
    except ERRORES_BD:
        return _resultado(None, "BD local", f"{motivo} Tampoco fue posible leer el respaldo local.")
    if respaldo is None:
        return _resultado(None, "BD local", f"{motivo} No hay datos de respaldo guardados.")
    return _resultado(respaldo, "BD local", f"{motivo} Se muestra el último dato guardado.")


def consultar_clima(sesion, ciudad, pais):
    exigir_sesion(sesion)
    ciudad = Clima.normalizar_ciudad(ciudad)
    pais = Clima.normalizar_pais(pais)
    try:
        datos = obtener_clima(ciudad, pais)
        dato = DeserializadorClima.desde_api(datos, ciudad, pais)
    except ErrorServicio as error:
        if error.codigo == 404:
            return _resultado(None, "API", "El servicio no encontró esa ciudad. Revise el nombre y el país.")
        return buscar_respaldo(ciudad, pais, error.mensaje)
    except (ValueError, KeyError, TypeError, IndexError):
        return buscar_respaldo(ciudad, pais, "La respuesta del servicio no es válida.")

    try:
        ClimaDAO.guardar(dato)
    except ERRORES_BD:
        return _resultado(dato, "API (OpenWeatherMap)", "El dato no pudo guardarse en la base de datos local.")
    return _resultado(dato, "API (OpenWeatherMap)", "Dato guardado en la base de datos local.", True)


def obtener_historial(sesion):
    exigir_sesion(sesion)
    return ClimaDAO.listar()
