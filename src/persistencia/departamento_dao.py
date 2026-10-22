from dependencia.departamento import Departamento
from dependencia.empleado import Empleado
from persistencia.conexion import marcador_sql
from persistencia.dao_base import consultar, consultar_uno, ejecutar_escritura


class DepartamentoDAO:
    @staticmethod
    def insertar(departamento):
        nuevo_id, _ = ejecutar_escritura(
            f"INSERT INTO departamento (nombre) VALUES ({marcador_sql()})",
            (departamento.nombre,))
        departamento.id = nuevo_id
        return departamento

    @staticmethod
    def buscar_por_id(id_departamento):
        """Retorna el Departamento con sus empleados cargados, o None si no existe."""
        m = marcador_sql()
        fila = consultar_uno(f"SELECT id, nombre FROM departamento WHERE id = {m}",
                             (id_departamento,))
        if fila is None:
            return None
        departamento = Departamento(fila[1], id=fila[0])
        filas_emp = consultar(
            f"SELECT id, nombre, correo, telefono, cargo FROM empleado WHERE departamento_id = {m} ORDER BY id",
            (departamento.id,))
        for f in filas_emp:
            departamento.agregar_empleado(Empleado(f[1], f[2], f[3], f[4], id=f[0]))
        return departamento

    @staticmethod
    def listar():
        filas = consultar("SELECT id, nombre FROM departamento ORDER BY id")
        return [Departamento(f[1], id=f[0]) for f in filas]

    @staticmethod
    def actualizar(departamento):
        m = marcador_sql()
        _, filas = ejecutar_escritura(
            f"UPDATE departamento SET nombre = {m} WHERE id = {m}",
            (departamento.nombre, departamento.id))
        return filas > 0

    @staticmethod
    def eliminar(id_departamento):
        _, filas = ejecutar_escritura(
            f"DELETE FROM departamento WHERE id = {marcador_sql()}", (id_departamento,))
        return filas > 0
