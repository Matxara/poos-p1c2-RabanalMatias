# src/main.py
from dominio.departamento import Departamento
from dominio.empleado import Empleado
from dominio.registrotiempo import Registrot


empleado_ana = Empleado(
    nombre="Ana Torres",
    correo="ana.torres@ecotech.cl"

)

empleado_junito = Empleado(
    nombre="junito Torres",
    correo="junito.torres@ecotech.cl"
)

dpt_desarrollo=Departamento("dpt desarrollo")

dpt_desarrollo.agregar_empleado(empleado_ana)
dpt_desarrollo.agregar_empleado(empleado_junito)


print(empleado_junito.mostrar_datos())

departamento = Departamento(
    nombre="departamento 1"
)

departamento.agregar_empleado(empleado_junito)
print(departamento.cantidad_empleados())

for empleado in dpt_desarrollo.empleados:
    print(empleado.mostrar_datos())

