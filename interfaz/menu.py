import flet as ft

def vista_menu (page):
    '''Esta funcion muestra el menu principal, con la division de la barra lateral y la parte del contenido.
    La barra lateral contiene los atajos hacia los formularios para hacer las acciones del sistema'''

    area_principal = ft.Container(
        expand = True,
        bgcolor = ft.Colors.BLUE_GREY_800,
        padding = 20,
        content = ft.Text("Selecciona una opcion del menu", color = "white")
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
    
            ft.ExpansionTile(
                leading = ft.Icon(ft.Icons.BADGE, color = "white", size = 22),
                title = ft.Text ("Empleados"),
                controls_padding = ft.padding.only(left = 36),
                controls = [
                    ft.ListTile(title=ft.Text("Insertar", color="white")),
                    ft.ListTile(title=ft.Text("Actualizar", color = "white")),
                    ft.ListTile(title=ft.Text("Eliminar", color = "white"))
                ]
            ),

            ft.ExpansionTile(
                leading = ft.Icon(ft.Icons.WATCH_LATER , color = "white", size = 22),
                title = ft.Text("Asistencia"),
                controls_padding = ft.padding.only(left = 36),
            ),

            ft.ExpansionTile(
                leading = ft.Icon(ft.Icons.PERSON, color = "white", size = 22),
                title = ft.Text("Usuarios"),
                controls_padding = ft.padding.only(left = 36),
                controls = [
                    ft.ListTile(title=ft.Text("Insertar", color ="white", )),
                    ft.ListTile(title=ft.Text("Actualizar", color = "white")),
                    ft.ListTile(title=ft.Text("Eliminar", color = "White"))
                ],
            ),

            ft.ExpansionTile(
                leading = ft.Icon(ft.Icons.REPORT , color = "white", size = 22),
                title = ft.Text("Reportes"),
                controls_padding = ft.padding.only(left = 36),
                controls = [
                    ft.ListTile(title = ft.Text("Semanal", color = "White")),
                ]
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

    def cambio_menu(contenido):
        '''Esta funcion se encarga de lograr el cambio de pagina 
        hacia los elementos elgidos'''

        area_principal.content = contenido
        page.update()
        
    
