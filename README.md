Matias Rabanal

# Descripción

Aplicación de consola desarrollada en Python que permite gestionar la información
de una empresa: empleados, departamentos, proyectos y registros de horas trabajadas.
Fue construida aplicando Programación Orientada a Objetos y se conecta a una base
de datos relacional (SQLite o MySQL/MariaDB), según la configuración del archivo `.env`.

El sistema permite registrar, consultar, actualizar y eliminar (CRUD) cada una de
estas entidades, y mantiene las relaciones entre ellas:

- Un **departamento** tiene muchos **empleados**; cada empleado pertenece como máximo a uno.
- Un **registro de trabajo** relaciona a un **empleado** con un **proyecto**, indicando
fecha, horas y descripción.

# instrucciones para ejecutar en entorno limpio

py --version
git --version

py -m venv .venv


source .venv/Scripts/activate


python -m pip install -r requirements.txt
