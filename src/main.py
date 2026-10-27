from menus.menu_usuario import menu_privado, solicitar_login
from persistencia.conexion import ERRORES_BD
from persistencia.crear_bd import crear_tablas


def main():
    try:
        crear_tablas()
    except (ValueError, *ERRORES_BD):
        print("No fue posible conectar con la base de datos. Revise su archivo .env.")
        return

    while True:
        usuario_actual = solicitar_login()
        if usuario_actual is None:
            if input("Enter para reintentar o 0 para salir: ").strip() == "0":
                print("Adios.")
                return
            continue
        opcion = menu_privado(usuario_actual)
        usuario_actual = None
        if opcion == "0":
            print("Adios.")
            return
        print("Sesión cerrada. Ingrese nuevamente.")


if __name__ == "__main__":
    main()
