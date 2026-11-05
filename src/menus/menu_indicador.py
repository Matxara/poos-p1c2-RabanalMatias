from functools import partial

from menus.comun import submenu
from servicios.indicadores import consultar_indicador, obtener_historial


def consultar(sesion):
    resultado = consultar_indicador(sesion)
    dato = resultado["indicador"]
    if dato is None:
        print(resultado["mensaje"])
        return
    print(f"Dólar: {dato.valor:.2f} CLP por USD")
    print(f"Fecha del dato: {dato.fecha}")
    print(f"Última verificación: {dato.verificado_en}")
    print(f"Origen: {resultado['origen']}")
    print(resultado["mensaje"])


def ver_historial(sesion):
    historial = obtener_historial(sesion)
    if not historial:
        print("Aún no existe historial guardado.")
        return
    print("Origen: BD local")
    for dato in historial:
        print(f"  {dato.fecha}: {dato.valor:.2f} {dato.unidad} (verificado: {dato.verificado_en})")


def menu_indicador(sesion):
    opciones = {
        "1": ("Consultar valor actualizado (dólar)", consultar),
        "2": ("Ver historial guardado", ver_historial),
    }
    submenu("Indicadores", {k: (t, partial(f, sesion)) for k, (t, f) in opciones.items()})
