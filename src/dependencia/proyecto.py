from dependencia.entidad import Entidad
from dependencia.reglas import validar_texto


class Proyecto(Entidad):
    def __init__(self, nombre, id=None):
        super().__init__(id)
        self._nombre = validar_texto(nombre, "nombre del proyecto")

    @property
    def nombre(self):
        return self._nombre

    @nombre.setter
    def nombre(self, valor):
        self._nombre = validar_texto(valor, "nombre del proyecto")

    def __str__(self):
        return f"[{self.id}] {self._nombre}"
