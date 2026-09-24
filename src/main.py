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
departamento_1 = Departamento(
    nombre="departamento 1"
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

# main.py
from persistencia.crear_bd import crear_tablas
from dominio.empleado import Empleado
from persistencia.empleado_dao import EmpleadoDAO

crear_tablas()
#empleado = Empleado(nombre="Ana Pérez", correo="ana@ecotech.cl")
empleado2 = Empleado(nombre="Rodrigo lopez", correo="rodrigo@ecotech.cl")

print("Antes:", empleado.id)
# None

EmpleadoDAO.insertar(empleado)
EmpleadoDAO.insertar(empleado2)

print("Después:", empleado.id)
# id generado por la BD

encontrado = EmpleadoDAO.buscar_por_id(empleado.id)
print("Encontrado:", encontrado)

print("Listado:")
for item in EmpleadoDAO.listar():
    print(item)