import math
import re
from datetime import date, datetime, timezone

from dependencia.entidad import Entidad

_PATRON_CIUDAD = re.compile(r"^[A-Za-zÁÉÍÓÚÜÑáéíóúüñ' .-]{2,60}$")
_PATRON_PAIS = re.compile(r"^[A-Za-z]{2}$")


class Clima(Entidad):
    def __init__(self, ciudad, pais, fecha, temperatura, humedad, descripcion,
                 verificado_en=None, id=None):
        super().__init__(id)
        self._ciudad = self.normalizar_ciudad(ciudad)
        self._pais = self.normalizar_pais(pais)
        self.fecha = fecha
        self.temperatura = temperatura
        self.humedad = humedad
        self.descripcion = descripcion
        self.verificado_en = verificado_en

    @property
    def ciudad(self):
        return self._ciudad

    @property
    def pais(self):
        return self._pais

    @classmethod
    def normalizar_ciudad(cls, valor):
        if not isinstance(valor, str):
            raise ValueError("La ciudad debe ser texto.")
        limpio = " ".join(valor.split())
        if not _PATRON_CIUDAD.match(limpio) or not any(c.isalpha() for c in limpio):
            raise ValueError("Ciudad no válida: use 2 a 60 letras, espacios, punto, apóstrofe o guion.")
        return limpio.title()

    @classmethod
    def normalizar_pais(cls, valor):
        if not isinstance(valor, str):
            raise ValueError("El país debe ser texto.")
        limpio = valor.strip()
        if not _PATRON_PAIS.match(limpio):
            raise ValueError("País no válido: use el código de 2 letras (ej: CL, AR, ES).")
        return limpio.upper()

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
            raise ValueError("La fecha del clima no es válida.")
        try:
            self._fecha = date.fromisoformat(valor.strip()[:10]).isoformat()
        except ValueError:
            raise ValueError("La fecha del clima no es válida.") from None

    @property
    def temperatura(self):
        return self._temperatura

    @temperatura.setter
    def temperatura(self, valor):
        if type(valor) not in (int, float) or not math.isfinite(valor) or not -90 <= valor <= 60:
            raise ValueError("La temperatura debe estar entre -90 y 60 °C.")
        self._temperatura = float(valor)

    @property
    def humedad(self):
        return self._humedad

    @humedad.setter
    def humedad(self, valor):
        if type(valor) not in (int, float) or not math.isfinite(valor) or not 0 <= valor <= 100:
            raise ValueError("La humedad debe estar entre 0 y 100 %.")
        self._humedad = int(round(valor))

    @property
    def descripcion(self):
        return self._descripcion

    @descripcion.setter
    def descripcion(self, valor):
        if not isinstance(valor, str) or not valor.strip() or len(valor.strip()) > 100:
            raise ValueError("La descripción del clima no es válida.")
        self._descripcion = valor.strip()

    @property
    def verificado_en(self):
        return self._verificado_en

    @verificado_en.setter
    def verificado_en(self, valor):
        if valor is None:
            valor = datetime.now(timezone.utc).isoformat(timespec="seconds")
        if not isinstance(valor, str):
            raise ValueError("La fecha de verificación no es válida.")
        try:
            datetime.fromisoformat(valor.strip())
        except ValueError:
            raise ValueError("La fecha de verificación no es válida.") from None
        self._verificado_en = valor.strip()

    def mostrar_datos(self):
        return (f"{self._ciudad} ({self._pais}) {self._fecha}: {self._temperatura:.1f} °C, "
                f"humedad {self._humedad} %, {self._descripcion}")
