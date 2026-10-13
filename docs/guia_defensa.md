# Guía de defensa

## Dónde está cada cosa (Checkpoint Clase 7)
| Piden | Dónde |
|---|---|
| Ejecutar y registrar/listar | `python src/main.py` → Empleados → 1 y 2 |
| Dónde está el SQL | `persistencia/*_dao.py` (CREATE TABLE en `crear_bd.py`) |
| Dónde se configura la conexión | `persistencia/conexion.py` + `.env` |
| `dependencia/` | Clases del problema: atributos, reglas, relaciones. No sabe de SQL |
| `persistencia/` | Conexión, SQL, CRUD, convertir filas ↔ objetos |
| `menus/` y `main.py` | Pedir datos, crear objetos, llamar al DAO, mostrar resultados. Sin SQL |
| Una validación | `menus/comun.py` → `pedir_entero` (rechaza "abc") |
| Un try-except | `menus/comun.py` → `ejecutar()`; `persistencia/dao_base.py` → `ejecutar_escritura()` |

## Criterios
**2.1.1 UML → código.** Clase → `class`; atributo → `self._atributo` + `@property`; multiplicidad "0..1/1" →
referencia (`Empleado._departamento`); "muchos" → colección privada (`Departamento._empleados`, expuesta como tupla).
`id=None` en el constructor: el objeto aún no está guardado; la BD genera el id y el DAO lo asigna (`lastrowid`).

**2.1.2 POO.** Encapsulamiento: setters que validan; colección protegida (`agregar_empleado` evita duplicados y
mantiene "un empleado, un departamento"). Herencia: `Persona → Empleado` (`super().__init__`), y `Entidad` (id) es
base de todas las clases. Polimorfismo: `Empleado.mostrar_datos()` redefine el de `Persona`. Reutilización:
`reglas.py` (validaciones), `entidad.py` (id), `dao_base.py` (patrón conexión/commit/rollback/cierre).
Descartado: subclase `EmpleadoJefe` (ser jefe es un rol, no un tipo).

**2.1.3 Base de datos.** `DB_ENGINE` elige `sqlite3` (módulo oficial) o **PyMySQL**. Parámetros MySQL: host, port,
user, password, database, charset `utf8mb4`, desde `.env` (no en el código). Consultas **parametrizadas** (`?` / `%s`
según `marcador_sql()`); en el f-string solo va el marcador, nunca un dato. CRUD: `insertar` (INSERT + `lastrowid`),
`buscar_*`/`listar` (`fetchone`/`fetchall` → objetos), `actualizar`/`eliminar` (`rowcount > 0`).
Claves foráneas: SQLite requiere `PRAGMA foreign_keys = ON`; MySQL usa `FOUND_ROWS` para que `rowcount` cuente
coincidencias.

**2.1.4 Errores.** Validar (antes, previsible): `pedir_*` en `comun.py`. Excepciones (durante, imprevisto): `dao_base`
hace `rollback()`, re-lanza y `finally` cierra la conexión; `ejecutar()` traduce `ValueError` (regla del dominio),
`ERRORES_INTEGRIDAD` (duplicado/relacionados), `ERRORES_BD` (conexión/tabla) y `Exception` (red final) a mensajes
seguros. Buscar un id inexistente devuelve `None`: es un resultado normal, no una excepción.
Demostración: borrar un departamento con empleados; correo repetido; `DB_ENGINE=oracle`.

**2.1.5 IA.** Tengan 2–3 casos reales verificados por ustedes (ver `registro_ia.md`).

## Preguntas típicas
- *¿Por qué `dao_base.py`?* Con 4 DAO, repetir el bloque try/except/finally en cada método duplicaría código.
- *¿Dónde va la FK y por qué?* En `empleado` (lado "muchos"): cada empleado apunta a su único departamento.
- *¿Por qué el orden de CREATE TABLE?* Una tabla solo puede referenciar a otra que ya existe.
- *¿Qué cambia entre SQLite y MariaDB?* Solo el `.env`; dominio, DAO y menús no cambian.

## Limitaciones conocidas
Lo leído desde la BD son copias (no hay *identity map*); `Departamento.empleados` se carga solo al buscar un
departamento; un registro de trabajo no permite cambiar empleado/proyecto al actualizarse.
