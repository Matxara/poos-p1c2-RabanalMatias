from dependencia.clima import Clima
from persistencia.conexion import marcador_sql, obtener_motor
from persistencia.dao_base import consultar, consultar_uno, ejecutar_escritura

_COLUMNAS = "id, ciudad, pais, fecha, temperatura, humedad, descripcion, verificado_en"

_SQL_SQLITE = """
INSERT INTO clima_api (ciudad, pais, fecha, temperatura, humedad, descripcion, verificado_en)
VALUES (?, ?, ?, ?, ?, ?, ?)
ON CONFLICT (ciudad, pais, fecha) DO UPDATE SET
    temperatura = excluded.temperatura,
    humedad = excluded.humedad,
    descripcion = excluded.descripcion,
    verificado_en = excluded.verificado_en
"""

_SQL_MYSQL = """
INSERT INTO clima_api (ciudad, pais, fecha, temperatura, humedad, descripcion, verificado_en)
VALUES (%s, %s, %s, %s, %s, %s, %s)
ON DUPLICATE KEY UPDATE
    temperatura = VALUES(temperatura),
    humedad = VALUES(humedad),
    descripcion = VALUES(descripcion),
    verificado_en = VALUES(verificado_en)
"""


class ClimaDAO:
    @staticmethod
    def _fila_a_clima(fila):
        return Clima(fila[1], fila[2], str(fila[3]), fila[4], fila[5], fila[6],
                     verificado_en=fila[7], id=fila[0])

    @staticmethod
    def guardar(clima):
        sql = _SQL_SQLITE if obtener_motor() == "sqlite" else _SQL_MYSQL
        ejecutar_escritura(sql, (clima.ciudad, clima.pais, clima.fecha, clima.temperatura,
                                 clima.humedad, clima.descripcion, clima.verificado_en))

    @staticmethod
    def listar(limite=20):
        filas = consultar(f"SELECT {_COLUMNAS} FROM clima_api ORDER BY fecha DESC, id DESC LIMIT {int(limite)}")
        return [ClimaDAO._fila_a_clima(f) for f in filas]

    @staticmethod
    def ultimo(ciudad, pais):
        m = marcador_sql()
        fila = consultar_uno(
            f"SELECT {_COLUMNAS} FROM clima_api WHERE ciudad = {m} AND pais = {m} "
            "ORDER BY fecha DESC, verificado_en DESC LIMIT 1", (ciudad, pais))
        return None if fila is None else ClimaDAO._fila_a_clima(fila)
