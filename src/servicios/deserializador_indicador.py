from dependencia.indicador import Indicador
from dependencia.reglas import MONEDAS
from servicios.indicador_api import extraer_primero


class DeserializadorIndicador:
    @staticmethod
    def desde_api(datos, codigo="dolar"):
        if codigo not in MONEDAS:
            raise ValueError("Moneda no admitida.")
        if isinstance(datos, dict) and datos.get("codigo", codigo) != codigo:
            raise ValueError("La respuesta no corresponde a la moneda pedida.")
        fecha, valor = extraer_primero(datos)
        return Indicador(fecha=fecha, valor=valor, codigo=codigo, unidad=MONEDAS[codigo])
