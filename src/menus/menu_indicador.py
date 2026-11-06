from functools import partial

from dependencia.reglas import MONEDAS, validar_moneda
from menus.comun import pedir_dato, submenu
from servicios.indicadores import consultar_indicador, obtener_historial


def _pedir_moneda():
    return pedir_dato("Moneda (dolar/euro): ", validar_moneda)


def consultar(sesion):
    resultado = consultar_indicador(sesion, _pedir_moneda())
    dato = resultado["indicador"]
    if dato is None:
        print(resultado["mensaje"])
        return
    print(f"{dato.codigo.capitalize()}: {dato.valor:.2f} {dato.unidad}")
    print(f"Fecha del dato: {dato.fecha}")
    print(f"Última verificación: {dato.verificado_en}")
    print(f"Origen: {resultado['origen']}")
    print(resultado["mensaje"])


def ver_historial(sesion):
    historial = obtener_historial(sesion, _pedir_moneda())
    if not historial:
        print("Aún no existe historial guardado.")
        return
    print("Origen: BD local")
    for dato in historial:
        print(f"  {dato.fecha}: {dato.valor:.2f} {dato.unidad} (verificado: {dato.verificado_en})")


def menu_indicador(sesion):
    opciones = {
        "1": ("Consultar tipo de cambio actualizado", consultar),
        "2": ("Ver historial guardado", ver_historial),
    }
    submenu("Tipo de cambio", {k: (t, partial(f, sesion)) for k, (t, f) in opciones.items()})
