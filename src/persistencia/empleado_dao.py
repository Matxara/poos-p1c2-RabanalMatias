from dependencia.departamento import Departamento
from dependencia.empleado import Empleado
from persistencia.conexion import marcador_sql
from persistencia.dao_base import consultar, consultar_uno, ejecutar_escritura

_SELECT = (
    "SELECT e.id, e.nombre, e.correo, e.cargo, d.id, d.nombre "
    "FROM empleado e LEFT JOIN departamento d ON d.id = e.departamento_id "
)


class EmpleadoDAO:
    @staticmethod
    def _fila_a_empleado(fila):
        """Transforma una fila en un objeto Empleado (con su Departamento, si tiene)."""
        departamento = Departamento(fila[5], id=fila[4]) if fila[4] is not None else None
        return Empleado(fila[1], fila[2], fila[3], id=fila[0], departamento=departamento)

    @staticmethod
    def _id_departamento(empleado):
        if empleado.departamento is None:
            return None
        if empleado.departamento.id is None:
            raise ValueError("El departamento del empleado debe estar registrado primero.")
        return empleado.departamento.id

    @staticmethod
    def insertar(empleado):
        m = marcador_sql()
        sql = (f"INSERT INTO empleado (nombre, correo, cargo, departamento_id) "
               f"VALUES ({m}, {m}, {m}, {m})")
        nuevo_id, _ = ejecutar_escritura(
            sql, (empleado.nombre, empleado.correo, empleado.cargo,
                  EmpleadoDAO._id_departamento(empleado)))
        empleado.id = nuevo_id
        return empleado

    @staticmethod
    def buscar_por_id(id_empleado):
        fila = consultar_uno(_SELECT + f"WHERE e.id = {marcador_sql()}", (id_empleado,))
        return None if fila is None else EmpleadoDAO._fila_a_empleado(fila)

    @staticmethod
    def buscar_por_correo(correo):
        fila = consultar_uno(_SELECT + f"WHERE e.correo = {marcador_sql()}",
                             (correo.strip().lower(),))
        return None if fila is None else EmpleadoDAO._fila_a_empleado(fila)

    @staticmethod
    def listar():
        filas = consultar(_SELECT + "ORDER BY e.id")
        return [EmpleadoDAO._fila_a_empleado(f) for f in filas]

    @staticmethod
    def actualizar(empleado):
        m = marcador_sql()
        sql = (f"UPDATE empleado SET nombre = {m}, correo = {m}, cargo = {m}, "
               f"departamento_id = {m} WHERE id = {m}")
        _, filas = ejecutar_escritura(
            sql, (empleado.nombre, empleado.correo, empleado.cargo,
                  EmpleadoDAO._id_departamento(empleado), empleado.id))
        return filas > 0  # False si no existía ese id

    @staticmethod
    def eliminar(id_empleado):
        _, filas = ejecutar_escritura(
            f"DELETE FROM empleado WHERE id = {marcador_sql()}", (id_empleado,))
        return filas > 0
