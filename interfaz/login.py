import flet as ft
from database import usuarios
from interfaz import vista_limitacion
import asyncio


def login(page: ft.Page):
    """Funcion para la ejecucion y diseno de la ventana de log in de usuarios"""

    
    async def iniciar_sesion(e):
        """Funcion que permite validar los usuarios para iniciar sesion"""

        resultado = usuarios.validar(
            user.value,
            contrasena.value
        )

        if resultado:

            carga = ft.AlertDialog(
                modal = True,
                content = ft.Row(
                    [
                    ft.ProgressRing(),
                    ft.Text("Cargando sistema")
                ],
                    alignment = ft.MainAxisAlignment.CENTER
                )
            )
            page.overlay.append(carga)
            carga.open = True
            page.update()

            await asyncio.sleep(2)
            carga.open = False
            page.update()
            page.controls.clear()

            rol = resultado[6]

            if rol =="Administrador":
            
                from interfaz.menu import vista_menu
                
                page.add(vista_menu(page))
                page.update()

            else: 
                from interfaz_usuario.menu_usuario import vista_menu
                page.add(vista_menu(page))
                page.update()
                       
        else: 
            snack = ft.SnackBar(
                content = ft.Text("Usuario o Contraseña no encontrado", color = "white"),
                bgcolor = "red"
            )
            page.overlay.append(snack)
            snack.open = True
            page.update()

    user = ft.TextField(
    width = 300,
    label = "Username",
    prefix_icon = ft.Icons.PERSON,
    )

    button = ft.ElevatedButton(
        "Log In",
        bgcolor = ft.Colors.BLUE_GREY_600,
        width = 150,
        height = 60,
        color = ft.Colors.WHITE,
        style = ft.ButtonStyle(
            shape = ft.RoundedRectangleBorder(radius = 5)
        ),
        on_click = iniciar_sesion
    )

    contrasena = ft.TextField(
        width = 300,
        label = "Contrasena",
        password = True,
        prefix_icon = ft.Icons.PASSWORD,
        on_submit = iniciar_sesion
    )

    form = ft.Container(
        bgcolor = ft.Colors.BLUE_GREY_900,
        width = 800,
        height = 600,
        padding = 20,

        content = ft.Column(
            spacing = 20,
            controls =[ 
                ft.Row(
                    controls = [
                        ft.Icon(ft.Icons.QR_CODE, color = "white", size = 60),
                        ft.Text("QR Assist", color = "white", size = 50, weight = "bold")
                    ],
                    alignment = ft.MainAxisAlignment.CENTER
                    
                ),

                user,
                contrasena,
                button
            ],
            alignment = ft.MainAxisAlignment.CENTER,
            horizontal_alignment = ft.CrossAxisAlignment.CENTER
        )    
    )

    return ft.Row(
        controls = [form],
        alignment = ft.MainAxisAlignment.CENTER,
        vertical_alignment = ft.CrossAxisAlignment.CENTER,
        expand = True,
    )