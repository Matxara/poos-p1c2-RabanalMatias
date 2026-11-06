from functools import partial

from dependencia.reglas import validar_moneda, validar_monto_clp
from menus.comun import mostrar_lista, pedir_dato, pedir_existente
from servicios import gestion_empleados
from servicios.pagos import calcular_pago


def calcular(sesion):
    mostrar_lista(gestion_empleados.listar_todos(sesion), "(no hay empleados registrados)")
    empleado = pedir_existente(partial(gestion_empleados.buscar_por_id, sesion), "empleado")
    if empleado is None:
        return
    valor_hora = pedir_dato("Valor por hora en CLP: ", validar_monto_clp)
    moneda = pedir_dato("Moneda de pago (dolar/euro): ", validar_moneda)
    pago = calcular_pago(sesion, empleado.id, valor_hora, moneda)
    print(f"Empleado: {pago['empleado'].nombre}")
    print(f"Horas registradas: {pago['horas']:g}")
    print(f"Total en CLP: {pago['total_clp']:,.2f}")
    print(f"Tipo de cambio: {pago['tipo_cambio']:.2f} (fecha {pago['fecha_tipo_cambio']}, {pago['origen']})")
    print(f"Pago en {pago['moneda']}: {pago['monto']:,.2f}")
