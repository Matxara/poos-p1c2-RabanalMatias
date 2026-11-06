from dependencia.reglas import validar_moneda, validar_monto_clp
from persistencia.empleado_dao import EmpleadoDAO
from persistencia.registro_trabajo_dao import RegistroTrabajoDAO
from servicios.indicadores import consultar_indicador
from servicios.permisos import exigir_admin


def calcular_pago(sesion, empleado_id, valor_hora_clp, moneda):
    exigir_admin(sesion)
    moneda = validar_moneda(moneda)
    valor_hora = validar_monto_clp(valor_hora_clp)
    empleado = EmpleadoDAO.buscar_por_id(empleado_id)
    if empleado is None:
        raise ValueError("No existe un empleado con ese ID.")
    horas = sum(r.horas for r in RegistroTrabajoDAO.listar_por_empleado(empleado_id))
    if horas <= 0:
        raise ValueError("El empleado no tiene horas registradas.")
    resultado = consultar_indicador(sesion, moneda)
    indicador = resultado["indicador"]
    if indicador is None:
        raise ValueError("No hay tipo de cambio disponible para calcular el pago.")
    total_clp = round(horas * valor_hora, 2)
    return {
        "empleado": empleado, "horas": horas, "valor_hora_clp": valor_hora,
        "total_clp": total_clp, "moneda": moneda, "tipo_cambio": indicador.valor,
        "fecha_tipo_cambio": indicador.fecha, "origen": resultado["origen"],
        "monto": round(total_clp / indicador.valor, 2),
    }
