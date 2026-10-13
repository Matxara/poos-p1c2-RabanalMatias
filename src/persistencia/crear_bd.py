from persistencia.conexion import abrir_conexion, obtener_motor


def _tipos():
    if obtener_motor() == "sqlite":
        return {"pk": "INTEGER PRIMARY KEY AUTOINCREMENT", "fk": "INTEGER",
                "t100": "TEXT", "t150": "TEXT", "t250": "TEXT", "fecha": "TEXT", "real": "REAL"}
    return {"pk": "INT PRIMARY KEY AUTO_INCREMENT", "fk": "INT",
            "t100": "VARCHAR(100)", "t150": "VARCHAR(150)", "t250": "VARCHAR(250)",
            "fecha": "DATE", "real": "DOUBLE"}


def _sentencias():
    t = _tipos()
    return [
        f"""CREATE TABLE IF NOT EXISTS departamento (
                id {t['pk']},
                nombre {t['t100']} NOT NULL UNIQUE)""",
        f"""CREATE TABLE IF NOT EXISTS empleado (
                id {t['pk']},
                nombre {t['t100']} NOT NULL,
                correo {t['t150']} NOT NULL UNIQUE,
                cargo {t['t100']} NOT NULL,
                departamento_id {t['fk']} NULL,
                FOREIGN KEY (departamento_id) REFERENCES departamento(id))""",
        f"""CREATE TABLE IF NOT EXISTS proyecto (
                id {t['pk']},
                nombre {t['t100']} NOT NULL UNIQUE)""",
        f"""CREATE TABLE IF NOT EXISTS registro_trabajo (
                id {t['pk']},
                empleado_id {t['fk']} NOT NULL,
                proyecto_id {t['fk']} NOT NULL,
                fecha {t['fecha']} NOT NULL,
                horas {t['real']} NOT NULL,
                descripcion {t['t250']} NOT NULL,
                FOREIGN KEY (empleado_id) REFERENCES empleado(id),
                FOREIGN KEY (proyecto_id) REFERENCES proyecto(id))""",
    ]


def crear_tablas():
    conexion = None
    try:
        conexion = abrir_conexion()
        cursor = conexion.cursor()
        for sql in _sentencias():
            cursor.execute(sql)
        conexion.commit()
    except Exception:
        if conexion:
            conexion.rollback()
        raise
    finally:
        if conexion:
            conexion.close()
