class Registrot:
    def __init__(self, fecha: int, horas: float):
        self.fecha = fecha
        self.horas = horas
    def mostrar_datos(self) -> str:
        return f"{self.fecha} - {self.horas}"