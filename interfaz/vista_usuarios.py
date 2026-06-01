import flet as ft
from database import conexion
from database import usuarios

def vista_usuarios(page, id_empleado = None, nombres = "", apellidos = ""):
    '''Muestra el contenido de el formulario de usuarios.'''

    nombre = ft.TextField(
        value = nombres,
        label = "Nombres", 
        border_color = "white"
        )
    
    apellido = ft.TextField(
        value = apellidos,
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

    def buscar(e):
        """Funcion para hacer funcionar la barra de busqueda"""
        
        nom = busqueda.value.lower()
        datatable.rows.clear()

        for usuario in usuarios.obtener_datos():
            nombre = f"{usuario[1]} {usuario[2]}".lower()

            if nom in nombre:
                datatable.rows.append(
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
                )
                datatable.update()
                                
    busqueda = ft.TextField(
        label = "Buscar por nombre",
        suffix_icon = ft.Icons.SEARCH,
        border = ft.InputBorder.UNDERLINE,
        label_style = ft.TextStyle(color = "white"),
        on_submit = buscar
    )

    id_usuario = None
    empleado_id = id_empleado

    def seleccionar(usuario):
        """Funcion que permite seleccionar los datos de las tablas y que 
        aparezcan en el formulario"""

        nonlocal id_usuario
        id_usuario = usuario[0]

        nombre.value = usuario[2]
        apellido.value = usuario[3]
        username.value = usuario[4]
        contrasena.value = usuario[5]
        rol.value = usuario[6]
        
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
                    ft.DataCell(ft.Text(f"{usuario[6]}", color = "white")),
                ]
            )
            for usuario in usuarios.obtener_datos()
        ]
    
    def actualiza_tabla():
        """Funcion que actualiza la tabla luego de insertar , actualizar o eliminar un usuario"""

        datatable.rows.clear()
        for usuario in usuarios.obtener_datos():

                datatable.rows.append(

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
                            ft.DataCell(ft.Text(f"{usuario[6]}", color = "white")),
                        ]
                    ) 
                )

    def mensaje(page, mensaje):
        """Muestra los mensajes de confirmacion de guardado, actualizacion y eliminacion de usuarios"""

        snack = ft.SnackBar(
            content = ft.Text(mensaje, color = "white"),
            bgcolor = "green",
            open = True
        )
        page.overlay.append(snack)
        page.update()


    def limpiar():
        """Esta funcion limpia el formulario luego de realizar cualquier accion"""
        nombre.value = ""
        apellido.value = ""
        username.value = ""
        contrasena.value = ""
        rol.value = None

        nombre.update()
        apellido.update()
        username.update()
        contrasena.update()
        rol.update()


    def agregar_usuario(e):
        """Funcion encargada de invocar el procedimiento almacenado de insertar plasmado en usuarios.py
        de la carpeta database. Ademas de utilizar otras funciones para limpiar formulario y actualizar 
        la tabla del modulo"""

        usuarios.insertar_usuario(
            empleado_id,
            nombre.value,
            apellido.value,
            username.value,
            contrasena.value,
            rol.value
        )

        actualiza_tabla()
        mensaje(e.page, "Usuario insertado correctamente")
        datatable.update()
        limpiar()
        table.update()

    def actualizacion_usuario(e):
        """Funcion para invocar el procedimiento almacenado de actualizar usuarios plasmado en empleados.py
        de la carpeta database. Ademas de utilizar otras funciones para limpiar formulario y actualizar 
        la tabla del modulo"""

        if id_usuario is None:
            return
        
        dialog = ft.AlertDialog(
            modal = True,
            title = ft.Text("Confirmacion"),
            content = ft.Text("Esta seguro de actualizar este usuario?")
        )

        def cancelar(e):
            """Funcion para cuando se presiona el boton de cancelar de la ventana emergente"""

            dialog.open = False
            e.page.update()
        
        def actualizar(e):
            """Funcion para realizar la accion de actualizar usuarios luego de las ventanas emergentes"""

            usuarios.actualizar_usuario(
                id_usuario,
                empleado_id,
                nombre.value,
                apellido.value,
                username.value,
                contrasena.value,
                rol.value
            )
            actualiza_tabla()

            mensaje(e.page, "Usuario actualizado correctamente")
            datatable.update()
            limpiar()
            table.update()
            dialog.open = False
            e.page.update()


        dialog.actions = [
            ft.TextButton(
                "Cancelar",
                on_click = cancelar
            ),

            ft.TextButton(
                "Confirmar",
                on_click = actualizar
            )
        ]   

        e.page.overlay.append(dialog)
        dialog.open = True
        e.page.update()

    def eliminacion_usuario(e):
        """Funcion para invocar el procedimiento almacenado de eliminar usuarios plasmado en empleados.py
        de la carpeta database. Ademas de utilizar otras funciones para limpiar formulario y actualizar 
        la tabla del modulo"""

        if id_usuario is None:
            return
        
        dialog = ft.AlertDialog(
            modal = True,
            title = ft.Text("Confirmacion"),
            content = ft.Text("Esta seguro de eliminar este usuario?")
        )

        def cancelar(e):
            """Funcion para cuando se presiona el boton de cancelar de la ventana emergente"""

            dialog.open = False
            e.page.update()
        
        def eliminar(e):
            """Funcion para realizar la accion de eliminar usuarios luego de la ventana emergente"""
        
            usuarios.eliminar_usuario(id_usuario)

            actualiza_tabla()
            mensaje(e.page, "Usuario eliminado correctamente")
            datatable.update()
            limpiar()
            table.update()

            dialog.open = False
            e.page.update()

        dialog.actions = [
            ft.TextButton(
                "Cancelar",
                on_click = cancelar
            ),

            ft.TextButton(
                "Confirmar",
                on_click = eliminar
            )
        ]
        e.page.overlay.append(dialog)
        dialog.open = True
        e.page.update()

    datatable = ft.DataTable(
        expand = True,
        column_spacing = 70,
        horizontal_margin = 30,
        border = ft.Border.all(2, "white"),
        data_row_color = {ft.ControlState.SELECTED: "white",
                          ft.ControlState.PRESSED: "blue"},
                          show_checkbox_column = False,

                          columns = [
                            ft.DataColumn(ft.Text("ID", color = "white", weight = "bold")),
                            ft.DataColumn(ft.Text("ID_Empleado", color = "white", weight = "bold")),
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
        padding = 1,

        content = ft.Column(
            controls = [
                ft.Container(
                    padding = 1,
                    content = ft.Row(
                        controls = [
                            busqueda,
                            ft.IconButton(tooltip = "Agregar",
                                on_click = agregar_usuario,
                                icon = ft.Icons.SAVE,
                                icon_color = "white"         
                            ),

                            ft.IconButton(tooltip = "Actualizar",
                                on_click = actualizacion_usuario,
                                icon = ft.Icons.UPDATE,
                                icon_color = "white"         
                            ),

                            ft.IconButton(tooltip = "Eliminar",
                                on_click = eliminacion_usuario,
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