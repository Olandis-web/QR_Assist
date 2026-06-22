import flet as ft
from interfaz_usuario.camara import CamaraApp


def vista_menu(page :ft.Page, id_empleado_login):
    
    '''Esta funcion muestra el menu principal, con la division de la barra lateral y la parte del contenido.
    '''
    def cambio_menu(contenido):
        '''Esta funcion se encarga de lograr el cambio de pagina 
        hacia los elementos elegidos'''
        
        # Detiene la cámara antes de cambiar de vista    
        if hasattr(area_principal.content, "detener_camara"):
            area_principal.content.detener_camara()        
            
        area_principal.content = contenido
        page.update()
    
    
    # Contenedor donde se cargan las vistas del sistema   
    area_principal = ft.Container(
        expand = True,
        bgcolor = ft.Colors.BLUE_GREY_900,
        padding = 20,
        alignment = ft.alignment.Alignment(0,0),
        content=ft.Container()

    )
    
    # Barra lateral de navegación 
    barra = ft.Container(
        width = 250,
        padding = 20,
        bgcolor = ft.Colors.BLUE_GREY_700,
        content = ft.Column([
            
            # Logo y nombre del sistema
            ft.Row(
                controls= [
                    ft.Icon(ft.Icons.QR_CODE, color = "white", size = 35),
                    ft.Text("QR Assist", color = "white", size = 28, weight = "bold")
                  
                ],
                alignment = ft.MainAxisAlignment.CENTER,
            ),

            ft.Divider(color = ft.Colors.WHITE24),
            
            # Mensaje de bienvenida
            ft.Container(
                padding=ft.padding.only(top=10, bottom=10),
                content=ft.Text(
                    "Bienvenido/a al sistema", 
                    color="white", 
                    size=13,
                    weight = "bold",
                    text_align=ft.TextAlign.CENTER
                    
                    
                    )
                ),
            
            ft.Container(expand=True),
           
           # Botón para abrir el módulo de asistencia
            ft.ElevatedButton(
                "Asistencia",
                icon = ft.Icons.WATCH_LATER,
                width = 200,
                height = 45,
                style = ft.ButtonStyle(
                    shape = ft.RoundedRectangleBorder(radius = 5),
                ),
                on_click = lambda e: cambio_menu(CamaraApp(page,id_empleado_login))
           
            ),

            ft.Container(expand = True),
            ft.Divider(color = ft.Colors.WHITE24),
            
            # Información del usuario administrador
            ft.ListTile(
                leading = ft.CircleAvatar(
                    content = ft.Text("AD", color = "white"),
                    bgcolor = ft.Colors.BLUE_700,
                ),
                title = ft.Text("Nombre Apellido", color = "white", size = 13),
                subtitle = ft.Text("empleado@QrAssist.com", color = "white54", size = 11)
            )

        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER )
    )

# Retorna la estructura principal del menú
    return ft.Row([
        barra,
        area_principal
    ],
    expand = True
    )


       
    
