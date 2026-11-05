from dependencia.indicador import Indicador
from persistencia.conexion import marcador_sql, obtener_motor
from persistencia.dao_base import consultar, consultar_uno, ejecutar_escritura

_COLUMNAS = "id, fuente, codigo, fecha, valor, unidad, verificado_en"

_SQL_SQLITE = """
INSERT INTO indicador_api (fuente, codigo, fecha, valor, unidad, verificado_en)
VALUES (?, ?, ?, ?, ?, ?)
ON CONFLICT (fuente, codigo, fecha) DO UPDATE SET
    valor = excluded.valor,
    unidad = excluded.unidad,
    verificado_en = excluded.verificado_en
"""

_SQL_MYSQL = """
INSERT INTO indicador_api (fuente, codigo, fecha, valor, unidad, verificado_en)
VALUES (%s, %s, %s, %s, %s, %s)
ON DUPLICATE KEY UPDATE
    valor = VALUES(valor),
    unidad = VALUES(unidad),
    verificado_en = VALUES(verificado_en)
"""


class IndicadorDAO:
    @staticmethod
    def _fila_a_indicador(fila):
        return Indicador(str(fila[3]), fila[4], verificado_en=fila[6], fuente=fila[1],
                         id=fila[0], codigo=fila[2], unidad=fila[5])

    @staticmethod
    def guardar(indicador):
        sql = _SQL_SQLITE if obtener_motor() == "sqlite" else _SQL_MYSQL
        ejecutar_escritura(sql, (indicador.fuente, indicador.codigo, indicador.fecha,
                                 indicador.valor, indicador.unidad, indicador.verificado_en))

    @staticmethod
    def listar(codigo="dolar"):
        filas = consultar(
            f"SELECT {_COLUMNAS} FROM indicador_api WHERE codigo = {marcador_sql()} "
            "ORDER BY fecha DESC, id DESC", (codigo,))
        return [IndicadorDAO._fila_a_indicador(f) for f in filas]

    @staticmethod
    def ultimo(codigo="dolar"):
        fila = consultar_uno(
            f"SELECT {_COLUMNAS} FROM indicador_api WHERE codigo = {marcador_sql()} "
            "ORDER BY fecha DESC, verificado_en DESC LIMIT 1", (codigo,))
        return None if fila is None else IndicadorDAO._fila_a_indicador(fila)
