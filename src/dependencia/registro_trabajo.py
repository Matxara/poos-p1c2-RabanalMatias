from datetime import date

from dependencia.empleado import Empleado
from dependencia.entidad import Entidad
from dependencia.proyecto import Proyecto
from dependencia.reglas import validar_fecha, validar_horas


class RegistroTrabajo(Entidad):
    def __init__(self, empleado, proyecto, fecha, horas, descripcion="", id=None):
        super().__init__(id)
        if not isinstance(empleado, Empleado):
            raise ValueError("El registro requiere un Empleado.")
        if not isinstance(proyecto, Proyecto):
            raise ValueError("El registro requiere un Proyecto.")
        self._empleado = empleado
        self._proyecto = proyecto
        self.fecha = fecha
        self.horas = horas
        self.descripcion = descripcion
        
    @property
    def empleado(self):
        return self._empleado

    @property
    def proyecto(self):
        return self._proyecto

    @property
    def fecha(self):
        return self._fecha

    @fecha.setter
    def fecha(self, valor):
        self._fecha = validar_fecha(valor)

    @property
    def horas(self):
        return self._horas

    @horas.setter
    def horas(self, valor):
        self._horas = validar_horas(valor)

    @property
    def descripcion(self):
        return self._descripcion

    @descripcion.setter
    def descripcion(self, valor):
        texto = "" if valor is None else str(valor).strip()
        if len(texto) > 250:
            raise ValueError("La descripción no puede superar los 250 caracteres.")
        self._descripcion = texto

    def __str__(self):
        return (f"[{self.id}] {self._fecha.isoformat()} | {self._empleado.nombre} | "
                f"{self._proyecto.nombre} | {self._horas:g} h | {self._descripcion or '-'}")
