import os
import sqlite3
from pathlib import Path

import pymysql
from dotenv import load_dotenv
from pymysql.constants import CLIENT

load_dotenv()

ERRORES_BD = (sqlite3.Error, pymysql.MySQLError)
ERRORES_INTEGRIDAD = (sqlite3.IntegrityError, pymysql.IntegrityError)

RAIZ_PROYECTO = Path(__file__).resolve().parents[2]


def obtener_motor():
    return os.getenv("DB_ENGINE", "sqlite").strip().lower()


def marcador_sql():
    return "?" if obtener_motor() == "sqlite" else "%s"


def abrir_conexion():
    motor = obtener_motor()
    if motor == "sqlite":
        ruta = Path(os.getenv("DB_NAME", "ecotech.db"))
        if not ruta.is_absolute():
            ruta = RAIZ_PROYECTO / ruta 
        conexion = sqlite3.connect(ruta)
        conexion.execute("PRAGMA foreign_keys = ON") 
        return conexion
    if motor == "mysql":
        return pymysql.connect(
            host=os.getenv("DB_HOST", "localhost"),
            port=int(os.getenv("DB_PORT", "3306")),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME"),
            charset="utf8mb4",
            client_flag=CLIENT.FOUND_ROWS,
        )
    raise ValueError(f"Motor no soportado en DB_ENGINE: '{motor}'.")
