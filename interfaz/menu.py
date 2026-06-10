import flet as ft
from interfaz.vista_empleados import vista_empleados
from interfaz.vista_usuarios import vista_usuarios


def vista_menu(page):
    '''Esta funcion muestra el menu principal, con la division de la barra lateral y la parte del contenido.
    La barra lateral contiene los atajos hacia los formularios para hacer las acciones del sistema'''

    def cambio_menu(contenido):
        '''Esta funcion se encarga de lograr el cambio de pagina 
        hacia los elementos elgidos'''

        area_principal.content = contenido
        page.update()

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
                "Asistencia",
                icon = ft.Icons.WATCH_LATER,
                width = 200,
                height = 45,
                style = ft.ButtonStyle(
                    shape = ft.RoundedRectangleBorder(radius = 5),
                ),
                on_click = lambda e: cambio_menu(
                    ft.Text("Seccion Asistencia", color = "white")

                )
           
            ),

            ft.ElevatedButton(
                "Usuarios",
                icon = ft.Icons.PERSON,
                width = 200,
                height = 45,
                style = ft.ButtonStyle(
                    shape = ft.RoundedRectangleBorder(radius = 5),
                ),
                on_click = lambda e: cambio_menu(vista_usuarios())
            ),

            ft.ElevatedButton(
                "Generar QRs",
                icon = ft.Icons.QR_CODE_2,
                width = 200,
                height = 54,
                style = ft.ButtonStyle(
                    shape = ft.RoundedRectangleBorder(radius = 5),
                ),
                on_click = lambda e: cambio_menu(
                    ft.Text("Seccion Generacion de QR", color = "white")
                )
            ),      

            ft.ElevatedButton(
                "Reportes",
                icon = ft.Icons.REPORT,
                width = 200,
                height = 54,
                style = ft.ButtonStyle(
                    shape = ft.RoundedRectangleBorder(radius = 5),
                ),
                on_click = lambda e: cambio_menu(
                    ft.Text("Seccion Reportes", color = "white")
                )
            ),      

            ft.Container(expand = True),
            ft.Divider(color = ft.Colors.WHITE24),

            ft.ListTile(
                leading = ft.CircleAvatar(
                    content = ft.Text("AD", color = "white"),
                    bgcolor = ft.Colors.BLUE_700,
                ),
                title = ft.Text("Administrador", color = "white", size = 13),
                subtitle = ft.Text("admin@QrAssist.com", color = "white54", size = 11)
            )

        ])  
    )


    return ft.Row([
        barra,
        area_principal
    ],
    expand = True
    )