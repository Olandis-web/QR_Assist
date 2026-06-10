
import flet as ft
from interfaz_usuario import menu_usuario

def main(page: ft.Page):
    '''Se encarga de insertar las caracteristicas principales de la pagina 
       del inicio'''

    page.title = "QR Assist"
    page.bgcolor = ft.Colors.BLUE_GREY_900
    page.window.maximized = True

    page.add(menu_usuario.vista_menu(page))

ft.run(main)


