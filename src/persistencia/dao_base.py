from persistencia.conexion import abrir_conexion


def ejecutar_escritura(sql, parametros=()):
    conexion = None
    try:
        conexion = abrir_conexion()
        cursor = conexion.cursor()
        cursor.execute(sql, parametros)
        conexion.commit()
        return cursor.lastrowid, cursor.rowcount
    except Exception:
        if conexion:
            conexion.rollback()  
        raise
    finally:
        if conexion:
            conexion.close()  


def consultar(sql, parametros=()):
    conexion = None
    try:
        conexion = abrir_conexion()
        cursor = conexion.cursor()
        cursor.execute(sql, parametros)
        return cursor.fetchall()
    finally:
        if conexion:
            conexion.close()


def consultar_uno(sql, parametros=()):
    conexion = None
    try:
        conexion = abrir_conexion()
        cursor = conexion.cursor()
        cursor.execute(sql, parametros)
        return cursor.fetchone()
    finally:
        if conexion:
            conexion.close()
