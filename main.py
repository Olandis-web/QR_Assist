import flet as ft
from interfaz import login

def main(page: ft.Page):
    '''Se encarga de insertar las caracteristicas principales de la pagina 
       del inicio'''

    page.title = "QR Assist"
    page.bgcolor = ft.Colors.BLUE_GREY_900
    page.window.maximized = True

    page.add(login.login(page))

ft.run(main)


