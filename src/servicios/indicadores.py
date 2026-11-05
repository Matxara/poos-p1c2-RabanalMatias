import requests

from persistencia.conexion import ERRORES_BD
from persistencia.indicador_dao import IndicadorDAO
from servicios.deserializador_indicador import DeserializadorIndicador
from servicios.indicador_api import URL_DOLAR, obtener_datos
from servicios.permisos import exigir_sesion


def _resultado(indicador, origen, mensaje, guardado=False):
    return {"indicador": indicador, "origen": origen, "mensaje": mensaje, "guardado": guardado}


def buscar_respaldo():
    try:
        respaldo = IndicadorDAO.ultimo()
    except ERRORES_BD:
        return _resultado(None, "BD local",
                          "El servicio no está disponible y no fue posible leer el respaldo local.")
    if respaldo is None:
        return _resultado(None, "BD local",
                          "El servicio no está disponible y no hay datos de respaldo guardados.")
    return _resultado(respaldo, "BD local",
                      "Servicio no disponible o respuesta inválida. Se muestra el último dato guardado.")


def consultar_indicador(sesion):
    exigir_sesion(sesion)
    try:
        datos = obtener_datos()
        dato = DeserializadorIndicador.desde_api(datos)
    except (requests.exceptions.RequestException, ValueError, KeyError, TypeError):
        return buscar_respaldo()

    try:
        IndicadorDAO.guardar(dato)
    except ERRORES_BD:
        return _resultado(dato, f"API ({URL_DOLAR})",
                          "El dato no pudo guardarse en la base de datos local.")
    return _resultado(dato, f"API ({URL_DOLAR})", "Dato guardado en la base de datos local.", True)


def obtener_historial(sesion):
    exigir_sesion(sesion)
    return IndicadorDAO.listar()
