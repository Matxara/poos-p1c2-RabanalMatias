from dependencia.reglas import validar_moneda
from persistencia.conexion import ERRORES_BD
from persistencia.indicador_dao import IndicadorDAO
from servicios.cliente_http import ErrorServicio
from servicios.deserializador_indicador import DeserializadorIndicador
from servicios.indicador_api import obtener_datos, url_indicador
from servicios.permisos import exigir_sesion


def _resultado(indicador, origen, mensaje, guardado=False):
    return {"indicador": indicador, "origen": origen, "mensaje": mensaje, "guardado": guardado}


def buscar_respaldo(codigo, motivo):
    try:
        respaldo = IndicadorDAO.ultimo(codigo)
    except ERRORES_BD:
        return _resultado(None, "BD local", f"{motivo} Tampoco fue posible leer el respaldo local.")
    if respaldo is None:
        return _resultado(None, "BD local", f"{motivo} No hay datos de respaldo guardados.")
    return _resultado(respaldo, "BD local", f"{motivo} Se muestra el último dato guardado.")


def consultar_indicador(sesion, codigo="dolar"):
    exigir_sesion(sesion)
    codigo = validar_moneda(codigo)
    try:
        datos = obtener_datos(codigo)
        dato = DeserializadorIndicador.desde_api(datos, codigo)
    except ErrorServicio as error:
        return buscar_respaldo(codigo, error.mensaje)
    except (ValueError, KeyError, TypeError):
        return buscar_respaldo(codigo, "La respuesta del servicio no es válida.")

    origen = f"API ({url_indicador(codigo)})"
    try:
        IndicadorDAO.guardar(dato)
    except ERRORES_BD:
        return _resultado(dato, origen, "El dato no pudo guardarse en la base de datos local.")
    return _resultado(dato, origen, "Dato guardado en la base de datos local.", True)


def obtener_historial(sesion, codigo="dolar"):
    exigir_sesion(sesion)
    return IndicadorDAO.listar(validar_moneda(codigo))
