from dependencia.persona import Persona
from dependencia.reglas import validar_texto


class Empleado(Persona):
    def __init__(self, nombre, correo, telefono, cargo, id=None, departamento=None):
        super().__init__(nombre, correo, telefono, id)  
        self._cargo = validar_texto(cargo, "cargo")
        self._departamento = departamento  

    @property
    def cargo(self):
        return self._cargo

    @cargo.setter
    def cargo(self, valor):
        self._cargo = validar_texto(valor, "cargo")

    @property
    def departamento(self):
        return self._departamento

    def cambiar_departamento(self, departamento):
        if departamento is None:
            if self._departamento is not None:
                self._departamento.quitar_empleado(self)
            self._departamento = None
        else:
            departamento.agregar_empleado(self)

    def _vincular(self, departamento):
        self._departamento = departamento

    def mostrar_datos(self):
        return f"{super().mostrar_datos()} - {self._cargo}"

    def __str__(self):
        depto = self._departamento.nombre if self._departamento else "sin departamento"
        return f"[{self.id}] {self.mostrar_datos()} ({depto})"
