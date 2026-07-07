import flet as ft
from interfaz.vista_empleados import vista_empleados
from interfaz.vista_usuarios import vista_usuarios
from interfaz.vista_reportes import vista_reportes
from interfaz.vista_generar import vista_generar
import sesion
import asyncio

def vista_menu(page):
    '''Esta funcion muestra el menu principal, con la division de la barra lateral y la parte del contenido.
    La barra lateral contiene los atajos hacia los formularios para hacer las acciones del sistema'''

    def cerrar_sesion(e):
        """Permite cerrar sesion dentro del programa"""

        import sesion
        from interfaz.login import login

        sesion.usuario_actual = None

        page.clean()
        page.add(login(page))
        page.update()

    def cambio_menu(contenido):
        '''Esta funcion se encarga de lograr el cambio de pagina 
        hacia los elementos elgidos'''

        area_principal.content = ft.Container(
            expand=True,
            alignment=ft.Alignment.CENTER,
            content=ft.ProgressRing(),
        )
        page.update()

        async def cargar():
            await asyncio.sleep(0.5)

            area_principal.content = contenido
            page.update()

        page.run_task(cargar)

        return area_principal
    

    area_principal = ft.Container(
        expand = True,
        bgcolor = ft.Colors.BLUE_GREY_900,
        padding = 10,
    )


    barra = ft.Container(
        width = 250,
        padding = 20,
        bgcolor = ft.Colors.BLUE_GREY_800,
        content = ft.Column([
            
            ft.Row(
                controls= [
                    ft.Icon(ft.Icons.QR_CODE, color = "white", size = 35),
                    ft.Text("QR Assist", color = "white", size = 28, weight = "bold")
                ],
                alignment = ft.MainAxisAlignment.CENTER,
            ),

            ft.Divider(color = ft.Colors.WHITE24),
    
            ft.ElevatedButton(
                "Empleados",
                icon = ft.Icons.BADGE,
                width = 200,
                height = 45,
                style = ft.ButtonStyle(
                    shape = ft.RoundedRectangleBorder(radius = 5),
                ),
                on_click = lambda e: cambio_menu(vista_empleados())
            
            ),
                

            ft.ElevatedButton(
                "Reportes",
                icon = ft.Icons.WATCH_LATER,
                width = 200,
                height = 45,
                style = ft.ButtonStyle(
                    shape = ft.RoundedRectangleBorder(radius = 5),
                ),
                on_click = lambda e: cambio_menu(vista_reportes(page, cambio_menu))
           
            ),

            ft.ElevatedButton(
                "Usuarios",
                icon = ft.Icons.PERSON,
                width = 200,
                height = 45,
                style = ft.ButtonStyle(
                    shape = ft.RoundedRectangleBorder(radius = 5),
                ),
                on_click = lambda e: cambio_menu(vista_usuarios(page))
            ),

            ft.ElevatedButton(
                "Generar QRs",
                icon = ft.Icons.QR_CODE_2,
                width = 200,
                height = 54,
                style = ft.ButtonStyle(
                    shape = ft.RoundedRectangleBorder(radius = 5),
                ),
                on_click = lambda e: cambio_menu(vista_generar(page))
            ),           

            ft.Container(expand = True),
            ft.Divider(color = ft.Colors.WHITE24),

            ft.Row(
                alignment = ft.MainAxisAlignment.CENTER,
                vertical_alignment = ft.CrossAxisAlignment.CENTER,
                controls = [
                    ft.PopupMenuButton(
                        content = ft.CircleAvatar(
                            radius = 22,
                            bgcolor = ft.Colors.BLUE,
                            content = ft.Text(
                                sesion.usuario_actual["nombre"][0],
                                size = 18,
                                weight = "bold",
                                color = "white",
                            ),
                        ),
                        items = [
                            ft.PopupMenuItem(),
                            ft.PopupMenuItem(
                                content = ft.Row(
                                    controls = [
                                        ft.Icon(ft.Icons.LOGOUT),
                                        ft.Text("Cerrar sesión"),
                                    ]
                                ),
                                on_click = cerrar_sesion,
                            ),
                        ],
                    ),

                    ft.Column(
                        spacing = 0,
                        expand = True,
                        horizontal_alignment = ft.CrossAxisAlignment.START,
                        controls = [
                            ft.Text(
                                sesion.usuario_actual["nombre"],
                                color = "white",
                                weight = "bold",
                                size = 14,
                                max_lines = 1,
                                overflow = ft.TextOverflow.ELLIPSIS,
                            ),

                            ft.Text(    
                                sesion.usuario_actual["apellido"],
                                color = "white",
                                weight = "bold",
                                size = 14,
                                max_lines = 1,
                                overflow = ft.TextOverflow.ELLIPSIS,
                            ),
                        ],
                    ),
                ],
            ),

            ft.Text(
                sesion.usuario_actual["rol"],
                color = "white54",
                size = 14,
                text_align = ft.TextAlign.RIGHT,
            ),
        ])  
    )


    return ft.Row([
        barra,
        area_principal
    ],
    expand = True
    )