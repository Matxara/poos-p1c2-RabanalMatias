from dependencia.proyecto import Proyecto
from persistencia.conexion import marcador_sql
from persistencia.dao_base import consultar, consultar_uno, ejecutar_escritura


class ProyectoDAO:
    @staticmethod
    def insertar(proyecto):
        nuevo_id, _ = ejecutar_escritura(
            f"INSERT INTO proyecto (nombre) VALUES ({marcador_sql()})", (proyecto.nombre,))
        proyecto.id = nuevo_id
        return proyecto

    @staticmethod
    def buscar_por_id(id_proyecto):
        fila = consultar_uno(f"SELECT id, nombre FROM proyecto WHERE id = {marcador_sql()}",
                             (id_proyecto,))
        return None if fila is None else Proyecto(fila[1], id=fila[0])

    @staticmethod
    def listar():
        filas = consultar("SELECT id, nombre FROM proyecto ORDER BY id")
        return [Proyecto(f[1], id=f[0]) for f in filas]

    @staticmethod
    def actualizar(proyecto):
        m = marcador_sql()
        _, filas = ejecutar_escritura(
            f"UPDATE proyecto SET nombre = {m} WHERE id = {m}", (proyecto.nombre, proyecto.id))
        return filas > 0

    @staticmethod
    def eliminar(id_proyecto):
        _, filas = ejecutar_escritura(
            f"DELETE FROM proyecto WHERE id = {marcador_sql()}", (id_proyecto,))
        return filas > 0
