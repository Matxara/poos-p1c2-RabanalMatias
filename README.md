# EcoTech Solutions – Sistema de gestión

Aplicación de consola en Python que gestiona empleados, departamentos, proyectos y
registros de horas trabajadas. Está construida con Programación Orientada a Objetos,
se conecta a una base de datos relacional (SQLite o MariaDB/MySQL, según el archivo
`.env`), consume dos APIs externas y aplica medidas de seguridad en el acceso y en el
manejo de datos.


## Resumen del proyecto

### Funcionalidades
- **CRUD** de empleados (con teléfono de 9 dígitos), departamentos, proyectos y registros de trabajo (fechas entre 2020 y 2027).
- **Asignaciones**: el administrador asigna empleados a proyectos. Cada empleado ve solo sus proyectos y solo puede registrar horas en los proyectos que tiene asignados.
- **Login con contraseñas cifradas (bcrypt)** y dos roles:
  - `admin` (el gerente/administrador): gestiona todo, crea cuentas y calcula pagos.
  - `empleado` (funcionario): ve y modifica su propia ficha, ve sus proyectos y registra sus horas.
- **Tipo de cambio** (dólar y euro) desde `mindicador.cl`, con deserialización a objetos, historial en base de datos y respaldo con el último valor guardado si la API falla.
- **Clima** de una ciudad desde OpenWeatherMap, con llave en `.env`, validación de ciudad y país, historial y respaldo local.
- **Cálculo de pago** (solo administrador): horas totales de un empleado × valor por hora en CLP, convertido a dólar o euro con el tipo de cambio vigente.
- **Manejo de errores HTTP**: mensajes distintos para 400, 401, 403, 404, 429, errores 5xx, tiempo agotado, falta de conexión y respuesta ilegible.

### Arquitectura por capas
| Carpeta | Responsabilidad |
|---|---|
| `src/dependencia/` | Clases de dominio (`Persona`, `Empleado`, `Departamento`, `Proyecto`, `RegistroTrabajo`, `Usuario`, `Indicador`, `Clima`) y validaciones (`reglas.py`). |
| `src/persistencia/` | Conexión, creación de tablas y DAOs (consultas parametrizadas). |
| `src/servicios/` | Lógica de negocio, permisos por rol, autenticación y clientes de API. |
| `src/menus/` | Menús de consola. |
| `src/main.py` | Punto de entrada: login y menú principal. |
| `src/semilla_bd.py` | Crea las tablas, el primer administrador y datos de ejemplo opcionales. |


## Instrucciones para ejecutar en un entorno limpio

1. ##Verificar herramientas

   py --versión

   git --version

2. ##Crear y activar el entorno virtual

   py -m venv .venv

   source .venv/Scripts/activate

3. ##Instalar dependencias

   python -m pip install -r requirements.txt

4. ##Crear el archivo .env .env.example y completándolo

5. ##Preparar la base de datos y el primer administrador

   se ejecuta dentro de visual code: py src/semilla_bd.py

   El programa pide los datos del administrador y pregunta si se cargan datos de ejemplo

6. ##Ejecutar la aplicación

   py src/main.py

##MariaDB La base de datos debe existir antes de ejecutar:

DB_ENGINE=mysql
DB_HOST=localhost
DB_PORT=3307
DB_NAME=ecotech
DB_USER=root
DB_PASSWORD=


Clima (OpenWeatherMap):

OPENWEATHER_API_KEY=su_llave

La llave se crea gratis en openweathermap.org