import requests

from servicios.indicador_api import URL_DOLAR, extraer_primero, obtener_datos


def consultar_dolar():
    try:
        datos = obtener_datos()
        fecha, valor = extraer_primero(datos)
        print(f"Dólar observado: {valor:.2f} CLP por USD")
        print(f"Fecha del registro: {fecha}")
        print(f"Origen: {URL_DOLAR}")
    except requests.exceptions.RequestException:
        print("No pudimos consultar el servicio. Reintente.")
    except (ValueError, KeyError, TypeError):
        print("La respuesta no contiene un indicador válido.")
