from functools import partial

from dependencia.clima import Clima
from menus.comun import pedir_dato, submenu
from servicios.climas import consultar_clima, obtener_historial


def consultar(sesion):
    ciudad = pedir_dato("Ciudad: ", Clima.normalizar_ciudad)
    pais = pedir_dato("País (código de 2 letras, ej: CL): ", Clima.normalizar_pais)
    resultado = consultar_clima(sesion, ciudad, pais)
    dato = resultado["clima"]
    if dato is None:
        print(resultado["mensaje"])
        return
    print(f"Clima en {dato.ciudad} ({dato.pais})")
    print(f"Temperatura: {dato.temperatura:.1f} °C")
    print(f"Estado del tiempo: {dato.descripcion}")
    print(f"Humedad: {dato.humedad} %")
    print(f"Fecha del dato: {dato.fecha}")
    print(f"Última verificación: {dato.verificado_en}")
    print(f"Origen: {resultado['origen']}")
    print(resultado["mensaje"])


def ver_historial(sesion):
    historial = obtener_historial(sesion)
    if not historial:
        print("Aún no existe historial de clima guardado.")
        return
    print("Origen: BD local")
    for dato in historial:
        print(" ", dato.mostrar_datos())


def menu_clima(sesion):
    opciones = {
        "1": ("Consultar clima de una ciudad", consultar),
        "2": ("Ver historial guardado", ver_historial),
    }
    submenu("Clima", {k: (t, partial(f, sesion)) for k, (t, f) in opciones.items()})
