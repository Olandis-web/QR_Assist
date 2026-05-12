import flet as ft
from database import conexion
from database import usuarios

def vista_usuarios():
    '''Muestra el contenido de el formulario de empleados.'''

    nombre = ft.TextField(
        label = "Nombres", 
        border_color = "white"
        )
    
    apellido = ft.TextField(
        label = "Apellidos", 
        border_color = "white"
        )
    
    username = ft.TextField(
        label = "UserName", 
        border_color = "white"
        )
        
    contrasena = ft.TextField(
        label = "Contraseña", 
        border_color = "white"
        )
    
    rol = ft.Dropdown(
        label = "Rol", 
        border_color = "white",
        options = [
            ft.dropdown.Option("Administrador"),
            ft.dropdown.Option("Operador")
        ]
    )
                                
    busqueda = ft.TextField(
        label = "Buscar por nombre",
        suffix_icon = ft.Icons.SEARCH,
        border = ft.InputBorder.UNDERLINE,
        label_style = ft.TextStyle(color = "white")
    )

    def seleccionar(usuario):
        """Funcion que permite seleccionar los datos de las tablas y que 
        aparezcan en el formulario"""

        nombre.value = usuario[1]
        apellido.value = usuario[2]
        username.value = usuario[3]
        contrasena.value = usuario[4]
        rol.value = usuario[5]
        
        nombre.update()
        apellido.update()
        username.update()
        contrasena.update()
        rol.update()

    rows = [
            ft.DataRow(
                on_select_change = lambda e, usuario = usuario:
                seleccionar(usuario),

                cells = [
                    ft.DataCell(ft.Text(f"{usuario[0]}", color = "white")),
                    ft.DataCell(ft.Text(f"{usuario[1]}", color = "white")),
                    ft.DataCell(ft.Text(f"{usuario[2]}", color = "white")),
                    ft.DataCell(ft.Text(f"{usuario[3]}", color = "white")),
                    ft.DataCell(ft.Text(f"{usuario[4]}", color = "white")),
                    ft.DataCell(ft.Text(f"{usuario[5]}", color = "white")),
                ]
            )
            for usuario in usuarios.obtener_datos()
        ]


    datatable = ft.DataTable(
        expand = True,
        column_spacing = 90,
        horizontal_margin = 40,
        border = ft.Border.all(2, "white"),
        data_row_color = {ft.ControlState.SELECTED: "white",
                          ft.ControlState.PRESSED: "blue"},
                          show_checkbox_column = False,

                          columns = [
                            ft.DataColumn(ft.Text("ID", color = "white", weight = "bold")),
                            ft.DataColumn(ft.Text("Nombres", color = "white", weight = "bold")),
                            ft.DataColumn(ft.Text("Apellidos", color = "white", weight = "bold")),
                            ft.DataColumn(ft.Text("Username", color = "white", weight = "bold")),
                            ft.DataColumn(ft.Text("Contraseña", color = "white", weight = "bold")),
                            ft.DataColumn(ft.Text("Rol", color = "white", weight = "bold"))
                          ],

                          rows=rows

    )               

    volver = ft.TextButton("Volver",
        icon = ft.Icons.ARROW_BACK,
        style = ft.ButtonStyle(
        color = "white",
        bgcolor = ft.Colors.BLUE_GREY_500
        
    ),
    on_click = lambda e: volver_menu(e.page)
    )
        

    form = ft.Container(
        width = 260,
        padding = 10,
        bgcolor = ft.Colors.BLUE_GREY_900,
    

        content = ft.Column(
            spacing = 15,
            controls = [
                ft.Row(
                    controls = [volver],
                    alignment = ft.MainAxisAlignment.START
                ),

                ft.Row(
                    controls = [
                        ft.Text("Ingrese los datos",
                            size = 32,
                            color = "white",
                            weight = ft.FontWeight.BOLD,    
                        )
                    ],
                    alignment = ft.MainAxisAlignment.CENTER,
                ),

                ft.Container(height = 20),

                nombre,
                apellido,
                username,
                contrasena,
                rol,
            ]    
        )      
    )


    table = ft.Container(
        expand = True,
        bgcolor = ft.Colors.BLUE_GREY_900,
        padding = 20,

        content = ft.Column(
            controls = [
                ft.Container(
                    padding = 1,
                    content = ft.Row(
                        controls = [
                            busqueda,
                            ft.IconButton(tooltip = "Agregar",
                                icon = ft.Icons.SAVE,
                                icon_color = "white"         
                            ),

                            ft.IconButton(tooltip = "Actualizar",
                                icon = ft.Icons.UPDATE,
                                icon_color = "white"         
                            ),

                            ft.IconButton(tooltip = "Eliminar",
                                icon = ft.Icons.DELETE,
                                icon_color = "white"         
                            )

                        ]
                    )
                ),
                ft.Column(
                    expand = True,
                    scroll = "auto",
                    controls = [
                        datatable
                    ]
                )
            ]
        )
    )

    return ft.Row(
            controls = [
                table,
                form
            ],
        expand = True,
        
    )
    

def volver_menu(page):
    """Esta funcion se encarga de volver al menu principal luego de realizar cualquier
    accion dentro de esta vista"""

    from interfaz.menu import vista_menu
    
    page.controls.clear()
    page.add(vista_menu(page))
    page.update()