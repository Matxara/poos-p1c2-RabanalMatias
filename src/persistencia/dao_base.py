"""Funciones que comparten todos los DAO.

Con 4 DAO, repetir el bloque abrir -> ejecutar -> commit/rollback -> cerrar en cada
método sería duplicar código. Aquí se escribe una sola vez. El SQL sigue
escribiéndose en cada DAO; aquí solo se ejecuta, siempre con parámetros.
Los errores se propagan (raise) hacia los menús, que deciden qué mostrar.
"""
from persistencia.conexion import abrir_conexion


def ejecutar_escritura(sql, parametros=()):
    """INSERT / UPDATE / DELETE. Retorna (ultimo_id, filas_afectadas)."""
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
    """SELECT que retorna todas las filas (fetchall)."""
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
    """SELECT que retorna una fila o None (fetchone)."""
    conexion = None
    try:
        conexion = abrir_conexion()
        cursor = conexion.cursor()
        cursor.execute(sql, parametros)
        return cursor.fetchone()
    finally:
        if conexion:
            conexion.close()
