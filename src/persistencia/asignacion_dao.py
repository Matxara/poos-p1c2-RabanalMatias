from dependencia.empleado import Empleado
from dependencia.proyecto import Proyecto
from persistencia.conexion import marcador_sql
from persistencia.dao_base import consultar, consultar_uno, ejecutar_escritura


class AsignacionDAO:
    @staticmethod
    def asignar(proyecto_id, empleado_id):
        m = marcador_sql()
        ejecutar_escritura(
            f"INSERT INTO proyecto_empleado (proyecto_id, empleado_id) VALUES ({m}, {m})",
            (proyecto_id, empleado_id))

    @staticmethod
    def desasignar(proyecto_id, empleado_id):
        m = marcador_sql()
        _, filas = ejecutar_escritura(
            f"DELETE FROM proyecto_empleado WHERE proyecto_id = {m} AND empleado_id = {m}",
            (proyecto_id, empleado_id))
        return filas > 0

    @staticmethod
    def esta_asignado(proyecto_id, empleado_id):
        m = marcador_sql()
        fila = consultar_uno(
            f"SELECT 1 FROM proyecto_empleado WHERE proyecto_id = {m} AND empleado_id = {m}",
            (proyecto_id, empleado_id))
        return fila is not None

    @staticmethod
    def proyectos_de_empleado(empleado_id):
        filas = consultar(
            "SELECT p.id, p.nombre FROM proyecto p "
            "JOIN proyecto_empleado pe ON pe.proyecto_id = p.id "
            f"WHERE pe.empleado_id = {marcador_sql()} ORDER BY p.id", (empleado_id,))
        return [Proyecto(f[1], id=f[0]) for f in filas]

    @staticmethod
    def empleados_de_proyecto(proyecto_id):
        filas = consultar(
            "SELECT e.id, e.nombre, e.correo, e.telefono, e.cargo FROM empleado e "
            "JOIN proyecto_empleado pe ON pe.empleado_id = e.id "
            f"WHERE pe.proyecto_id = {marcador_sql()} ORDER BY e.id", (proyecto_id,))
        return [Empleado(f[1], f[2], f[3], f[4], id=f[0]) for f in filas]
