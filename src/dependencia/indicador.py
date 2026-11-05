import math
from datetime import date, datetime, timezone

from dependencia.entidad import Entidad


class Indicador(Entidad):
    def __init__(self, fecha, valor, verificado_en=None, fuente="mindicador.cl",
                 id=None, codigo="dolar", unidad="CLP/USD"):
        super().__init__(id)
        self.fecha = fecha
        self.valor = valor
        self.fuente = fuente
        self.codigo = codigo
        self.unidad = unidad
        self.verificado_en = verificado_en

    @property
    def fecha(self):
        return self._fecha

    @fecha.setter
    def fecha(self, valor):
        if isinstance(valor, datetime):
            valor = valor.date().isoformat()
        elif isinstance(valor, date):
            valor = valor.isoformat()
        if not isinstance(valor, str):
            raise ValueError("La fecha del indicador no es válida.")
        try:
            self._fecha = date.fromisoformat(valor.strip()[:10]).isoformat()
        except ValueError:
            raise ValueError("La fecha del indicador no es válida.") from None

    @property
    def valor(self):
        return self._valor

    @valor.setter
    def valor(self, valor):
        if type(valor) not in (int, float) or not math.isfinite(valor) or valor <= 0:
            raise ValueError("El valor del indicador debe ser un número positivo.")
        self._valor = float(valor)

    @property
    def fuente(self):
        return self._fuente

    @fuente.setter
    def fuente(self, valor):
        self._fuente = self._texto(valor, "fuente", 40)

    @property
    def codigo(self):
        return self._codigo

    @codigo.setter
    def codigo(self, valor):
        self._codigo = self._texto(valor, "código", 20)

    @property
    def unidad(self):
        return self._unidad

    @unidad.setter
    def unidad(self, valor):
        self._unidad = self._texto(valor, "unidad", 20)

    @property
    def verificado_en(self):
        return self._verificado_en

    @verificado_en.setter
    def verificado_en(self, valor):
        if valor is None:
            valor = datetime.now(timezone.utc).isoformat(timespec="seconds")
        if isinstance(valor, datetime):
            valor = valor.isoformat(timespec="seconds")
        if not isinstance(valor, str):
            raise ValueError("La fecha de verificación no es válida.")
        try:
            datetime.fromisoformat(valor.strip())
        except ValueError:
            raise ValueError("La fecha de verificación no es válida.") from None
        self._verificado_en = valor.strip()

    @staticmethod
    def _texto(valor, etiqueta, maximo):
        if not isinstance(valor, str) or not valor.strip() or len(valor.strip()) > maximo:
            raise ValueError(f"El campo {etiqueta} no es válido.")
        return valor.strip()

    def mostrar_datos(self):
        return f"{self._fecha}: {self._valor:.2f} {self._unidad}"
