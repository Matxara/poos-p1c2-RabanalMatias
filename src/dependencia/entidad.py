class Entidad:
   
    def __init__(self, id=None):
        self.id = id  # pasa por el setter, que valida

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, valor):
        if valor is not None and (isinstance(valor, bool) or not isinstance(valor, int) or valor <= 0):
            raise ValueError("El id debe ser un entero positivo o None.")
        self._id = valor
