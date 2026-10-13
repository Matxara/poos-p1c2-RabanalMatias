from dependencia.empleado import Empleado
from dependencia.entidad import Entidad
from dependencia.reglas import validar_texto


class Departamento(Entidad):
    def __init__(self, nombre, id=None):
        super().__init__(id)
        self._nombre = validar_texto(nombre, "nombre del departamento")
        self._empleados = []  # colección interna: no se expone directamente

    @property
    def nombre(self):
        return self._nombre

    @nombre.setter
    def nombre(self, valor):
        self._nombre = validar_texto(valor, "nombre del departamento")

    @property
    def empleados(self):
        return tuple(self._empleados)

    def cantidad_empleados(self):
        return len(self._empleados)

    def agregar_empleado(self, empleado):
        if not isinstance(empleado, Empleado):
            raise TypeError("Solo se pueden agregar objetos Empleado.")
        if empleado in self._empleados:
            return False
        anterior = empleado.departamento
        if anterior is not None and anterior is not self:
            anterior.quitar_empleado(empleado)
        self._empleados.append(empleado)
        empleado._vincular(self)
        return True

    def quitar_empleado(self, empleado):
        if empleado not in self._empleados:
            return False
        self._empleados.remove(empleado)
        empleado._vincular(None)
        return True

    def __str__(self):
        return f"[{self.id}] {self._nombre}"
