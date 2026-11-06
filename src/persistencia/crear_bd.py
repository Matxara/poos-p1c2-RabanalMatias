from persistencia.conexion import abrir_conexion, obtener_motor


def _tipos():
    if obtener_motor() == "sqlite":
        return {"pk": "INTEGER PRIMARY KEY AUTOINCREMENT", "fk": "INTEGER",
                "t9": "TEXT", "t20": "TEXT", "t40": "TEXT", "t100": "TEXT", "t150": "TEXT", "t250": "TEXT", "fecha": "TEXT", "real": "REAL", "int": "INTEGER"}
    return {"pk": "INT PRIMARY KEY AUTO_INCREMENT", "fk": "INT",
            "t9": "VARCHAR(9)", "t20": "VARCHAR(20)", "t40": "VARCHAR(40)", "t100": "VARCHAR(100)", "t150": "VARCHAR(150)", "t250": "VARCHAR(250)",
            "fecha": "DATE", "real": "DOUBLE", "int": "INT"}


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
                telefono {t['t9']} NOT NULL,
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
        f"""CREATE TABLE IF NOT EXISTS proyecto_empleado (
                id {t['pk']},
                proyecto_id {t['fk']} NOT NULL,
                empleado_id {t['fk']} NOT NULL,
                UNIQUE (proyecto_id, empleado_id),
                FOREIGN KEY (proyecto_id) REFERENCES proyecto(id),
                FOREIGN KEY (empleado_id) REFERENCES empleado(id))""",
        f"""CREATE TABLE IF NOT EXISTS usuario (
                id {t['pk']},
                nombre_usuario {t['t40']} NOT NULL UNIQUE,
                password_hash {t['t100']} NOT NULL,
                empleado_id {t['fk']} NOT NULL UNIQUE,
                rol {t['t20']} NOT NULL DEFAULT 'empleado' CHECK (rol IN ('admin', 'empleado')),
                FOREIGN KEY (empleado_id) REFERENCES empleado(id))""",
        f"""CREATE TABLE IF NOT EXISTS indicador_api (
                id {t['pk']},
                fuente {t['t40']} NOT NULL,
                codigo {t['t20']} NOT NULL,
                fecha {t['fecha']} NOT NULL,
                valor {t['real']} NOT NULL,
                unidad {t['t20']} NOT NULL,
                verificado_en {t['t40']} NOT NULL,
                UNIQUE (fuente, codigo, fecha))""",
        f"""CREATE TABLE IF NOT EXISTS clima_api (
                id {t['pk']},
                ciudad {t['t100']} NOT NULL,
                pais {t['t20']} NOT NULL,
                fecha {t['fecha']} NOT NULL,
                temperatura {t['real']} NOT NULL,
                humedad {t['int']} NOT NULL,
                descripcion {t['t100']} NOT NULL,
                verificado_en {t['t40']} NOT NULL,
                UNIQUE (ciudad, pais, fecha))""",
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
