from dependencia.usuario import Usuario
from persistencia.conexion import marcador_sql
from persistencia.dao_base import consultar_uno, ejecutar_escritura

_SELECT = "SELECT id, nombre_usuario, password_hash, empleado_id FROM usuario "


class UsuarioDAO:
    @staticmethod
    def _fila_a_usuario(fila):
        return Usuario(fila[1], fila[2], fila[3], id=fila[0])

    @staticmethod
    def insertar(usuario):
        m = marcador_sql()
        sql = f"INSERT INTO usuario (nombre_usuario, password_hash, empleado_id) VALUES ({m}, {m}, {m})"
        nuevo_id, _ = ejecutar_escritura(
            sql, (usuario.nombre_usuario, usuario.password_hash, usuario.empleado_id))
        usuario.id = nuevo_id
        return nuevo_id

    @staticmethod
    def buscar_por_nombre(nombre):
        fila = consultar_uno(_SELECT + f"WHERE nombre_usuario = {marcador_sql()}", (nombre,))
        return None if fila is None else UsuarioDAO._fila_a_usuario(fila)

    @staticmethod
    def buscar_por_empleado(empleado_id):
        fila = consultar_uno(_SELECT + f"WHERE empleado_id = {marcador_sql()}", (empleado_id,))
        return None if fila is None else UsuarioDAO._fila_a_usuario(fila)
