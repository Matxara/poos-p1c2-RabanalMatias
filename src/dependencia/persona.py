from dependencia.entidad import Entidad
from dependencia.reglas import validar_correo, validar_telefono, validar_texto


class Persona(Entidad):
    def __init__(self, nombre, correo, telefono, id=None):
        super().__init__(id)
        self._nombre = validar_texto(nombre, "nombre")
        self._correo = validar_correo(correo)
        self._telefono = validar_telefono(telefono)

    @property
    def nombre(self):
        return self._nombre

    @nombre.setter
    def nombre(self, valor):
        self._nombre = validar_texto(valor, "nombre")

    @property
    def correo(self):
        return self._correo

    @correo.setter
    def correo(self, valor):
        self._correo = validar_correo(valor)

    @property
    def telefono(self):
        return self._telefono

    @telefono.setter
    def telefono(self, valor):
        self._telefono = validar_telefono(valor)

    def mostrar_datos(self):
        return f"{self._nombre} - {self._correo} - {self._telefono}"

    def __str__(self):
        return self.mostrar_datos()
