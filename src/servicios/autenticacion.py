import bcrypt
<<<<<<< HEAD

from dependencia.usuario import Usuario
from persistencia.empleado_dao import EmpleadoDAO
from persistencia.usuario_dao import UsuarioDAO

MAX_BYTES_BCRYPT = 72


=======
from dependencia.usuario import Usuario

MAX_BYTES_BCRYPT = 72

>>>>>>> 277b38f307d3e1889325766d2f7c91ccbec2d936
def crear_hash(clave):
    clave = Usuario.validar_clave(clave)
    clave_bytes = clave.encode("utf-8")
    if len(clave_bytes) > MAX_BYTES_BCRYPT:
        raise ValueError("Máximo 72 bytes UTF-8 para bcrypt.")
<<<<<<< HEAD
    return bcrypt.hashpw(clave_bytes, bcrypt.gensalt()).decode("utf-8")


def registrar_usuario(empleado_id, nombre, clave):
    nombre = Usuario.normalizar_usuario(nombre)
    hash_guardado = crear_hash(clave)
    if (EmpleadoDAO.buscar_por_id(empleado_id) is None
            or UsuarioDAO.buscar_por_empleado(empleado_id) is not None
            or UsuarioDAO.buscar_por_nombre(nombre) is not None):
        raise ValueError("No se pudo crear esa cuenta.")
    usuario = Usuario(nombre, hash_guardado, empleado_id)
    return UsuarioDAO.insertar(usuario)

=======
    return bcrypt.hashpw(
        clave_bytes, bcrypt.gensalt()
    ).decode("utf-8")

def registrar_usuario(empleado_id, nombre, clave):
    nombre = Usuario.normalizar_usuario(nombre)
    if UsuarioDAO.buscar_por_nombre(nombre) is not None:
        raise ValueError("No se pudo crear esa cuenta.")
    
    hash_guardado = crear_hash(clave)
    usuario = Usuario(nombre, hash_guardado, empleado_id)

    return UsuarioDAO.insertar(usuario)
>>>>>>> 277b38f307d3e1889325766d2f7c91ccbec2d936

def autenticar(nombre, clave):
    nombre = Usuario.normalizar_usuario(nombre)
    if not isinstance(clave, str):
        return None
    datos = clave.encode("utf-8")
    if not 0 < len(datos) <= MAX_BYTES_BCRYPT:
        return None
    cuenta = UsuarioDAO.buscar_por_nombre(nombre)
<<<<<<< HEAD
    if cuenta is None:
=======

    if cuenta is None:
        print(f"No se encontró la cuenta para el usuario: {nombre}")
>>>>>>> 277b38f307d3e1889325766d2f7c91ccbec2d936
        return None
    if not bcrypt.checkpw(datos, cuenta.password_hash.encode("utf-8")):
        return None
    return {"id": cuenta.id, "empleado_id": cuenta.empleado_id,
<<<<<<< HEAD
            "nombre_usuario": cuenta.nombre_usuario}
=======
        "nombre_usuario": cuenta.nombre_usuario}
>>>>>>> 277b38f307d3e1889325766d2f7c91ccbec2d936
