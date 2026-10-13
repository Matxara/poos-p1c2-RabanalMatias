from datetime import date

from dependencia.empleado import Empleado
from dependencia.proyecto import Proyecto
from dependencia.registro_trabajo import RegistroTrabajo
from persistencia.conexion import marcador_sql
from persistencia.dao_base import consultar, consultar_uno, ejecutar_escritura

_SELECT = (
    "SELECT r.id, r.fecha, r.horas, r.descripcion, "
    "e.id, e.nombre, e.correo, e.cargo, p.id, p.nombre "
    "FROM registro_trabajo r "
    "JOIN empleado e ON e.id = r.empleado_id "
    "JOIN proyecto p ON p.id = r.proyecto_id "
)


class RegistroTrabajoDAO:
    @staticmethod
    def _fila_a_registro(fila):
        fecha = fila[1] if isinstance(fila[1], date) else date.fromisoformat(fila[1])
        empleado = Empleado(fila[5], fila[6], fila[7], id=fila[4])
        proyecto = Proyecto(fila[9], id=fila[8])
        return RegistroTrabajo(empleado, proyecto, fecha, fila[2], fila[3], id=fila[0])

    @staticmethod
    def insertar(registro):
        if registro.empleado.id is None or registro.proyecto.id is None:
            raise ValueError("El empleado y el proyecto deben estar registrados primero.")
        m = marcador_sql()
        sql = ("INSERT INTO registro_trabajo (empleado_id, proyecto_id, fecha, horas, descripcion) "
               f"VALUES ({m}, {m}, {m}, {m}, {m})")
        nuevo_id, _ = ejecutar_escritura(
            sql, (registro.empleado.id, registro.proyecto.id, registro.fecha.isoformat(),
                  registro.horas, registro.descripcion))
        registro.id = nuevo_id
        return registro

    @staticmethod
    def buscar_por_id(id_registro):
        fila = consultar_uno(_SELECT + f"WHERE r.id = {marcador_sql()}", (id_registro,))
        return None if fila is None else RegistroTrabajoDAO._fila_a_registro(fila)

    @staticmethod
    def listar():
        filas = consultar(_SELECT + "ORDER BY r.fecha, r.id")
        return [RegistroTrabajoDAO._fila_a_registro(f) for f in filas]

    @staticmethod
    def listar_por_empleado(id_empleado):
        filas = consultar(_SELECT + f"WHERE r.empleado_id = {marcador_sql()} ORDER BY r.fecha, r.id",
                          (id_empleado,))
        return [RegistroTrabajoDAO._fila_a_registro(f) for f in filas]

    @staticmethod
    def actualizar(registro):
        """Actualiza fecha, horas y descripción (empleado y proyecto no cambian)."""
        m = marcador_sql()
        sql = (f"UPDATE registro_trabajo SET fecha = {m}, horas = {m}, descripcion = {m} "
               f"WHERE id = {m}")
        _, filas = ejecutar_escritura(
            sql, (registro.fecha.isoformat(), registro.horas, registro.descripcion, registro.id))
        return filas > 0

    @staticmethod
    def eliminar(id_registro):
        _, filas = ejecutar_escritura(
            f"DELETE FROM registro_trabajo WHERE id = {marcador_sql()}", (id_registro,))
        return filas > 0
