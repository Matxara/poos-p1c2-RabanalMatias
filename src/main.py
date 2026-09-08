# src/main.py
from dominio.empleado import Empleado
empleado = Empleado(
    nombre="Ana Torres",
    correo="ana.torres@ecotech.cl"

)

print(empleado.mostrar_datos())

from dominio.departamento import Departamento
departamento = Departamento(
    nombre="departamento 1"

)
print(departamento.mostrar_datos())