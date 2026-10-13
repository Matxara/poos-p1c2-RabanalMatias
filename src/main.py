from menus.menu_departamento import menu_departamento
from menus.menu_empleado import menu_empleado
from menus.menu_proyecto import menu_proyecto
from menus.menu_registro import menu_registro
from persistencia.conexion import ERRORES_BD
from persistencia.crear_bd import crear_tablas


def mostrar_menu():
    print("\n===== ECOTECH SOLUTIONS =====")
    print("1. Empleados")
    print("2. Departamentos")
    print("3. Proyectos")
    print("4. Registros de trabajo")
    print("0. Salir")


def main():
    try:
        crear_tablas()
    except (ValueError, *ERRORES_BD):
        print("No fue posible conectar con la base de datos. Revise su archivo .env.")
        return

while True:
        mostrar_menu()
        opcion = input("Seleccione una opción: ").strip()
        if opcion == "1":
            menu_empleado()
        elif opcion == "2":
            menu_departamento()
        elif opcion == "3":
            menu_proyecto()
        elif opcion == "4":
            menu_registro()
        elif opcion == "0":
            print("Adios.")
            break
        else:
            print("Opción no válida.")


if __name__ == "__main__":
    main()
