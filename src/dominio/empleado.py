# src/dominio/empleado.py
class Empleado:
    def __init__(self, nombre, correo, id=None):
        self.id = id
        self.nombre = nombre
        self.correo = correo
    def mostrar_datos(self) -> str:
        return f"{self.nombre} - {self.correo}"