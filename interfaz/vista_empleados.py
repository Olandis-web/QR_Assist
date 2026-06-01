import flet as ft
from database import conexion
from database import empleados
from database import usuarios

def vista_empleados():
    '''Muestra el contenido de el formulario de empleados.'''

    nombre = ft.TextField(
        label = "Nombres", 
        border_color = "white"
        )
    
    apellido = ft.TextField(
        label = "Apellidos", 
        border_color = "white"
        )
    
    cargo = ft.TextField(
        label = "Cargo",
        border_color = "white"
        )
        
    qr = ft.TextField(
        label = "Codigo QR", 
        border_color = "white"
        )
    
    estado = ft.Dropdown(
        label = "Estado", 
        border_color = "white",
        options = [
            ft.dropdown.Option("Activo"),
            ft.dropdown.Option("Inactivo"),
            ft.dropdown.Option("Licencia")
        ]
    )

    def buscar(e):
        """Funcion para hacer funcionar la barra de busqueda"""
        
        nom = busqueda.value.lower()
        datatable.rows.clear()

        for empleado in empleados.obtener_datos():
            nombre = f"{empleado [1]} {empleado[2]}".lower()

            if nom in nombre:

                usuario_existente = usuarios.verifica_usuario(
                    empleado[0]
                )

                datatable.rows.append(
                    ft.DataRow(
                        on_select_change = lambda e, empleado = empleado:
                        seleccionar(empleado),

                        cells = [
                            ft.DataCell(ft.Text(f"{empleado[0]}", color = "white")),
                            ft.DataCell(ft.Text(f"{empleado[1]}", color = "white")),
                            ft.DataCell(ft.Text(f"{empleado[2]}", color = "white")),
                            ft.DataCell(ft.Text(f"{empleado[3]}", color = "white")),
                            ft.DataCell(ft.Text(f"{empleado[4]}", color = "white")),
                            ft.DataCell(ft.Text(f"{empleado[5]}", color = "white")),

                            ft.DataCell(
                                ft.IconButton(
                                    icon = ft.Icons.PERSON_ADD,
                                    tooltip = "Crear Usuario",
                                    icon_color = "white",

                                    on_click = lambda e, 
                                    empleado = empleado:

                                    creacion_usuario(e, empleado)

                                )
                                if not usuario_existente 
                                
                                else 
                                    ft.Text("Listo",color = "green")
                            )
                            
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

    id_empleado = None
    def seleccionar(empleado):
        """Funcion que permite seleccionar los datos de las tablas y que 
        aparezcan en el formulario"""

        nonlocal id_empleado
        id_empleado = empleado[0]

        nombre.value = empleado[1]
        apellido.value = empleado[2]
        cargo.value = empleado[3]
        qr.value = empleado[4]
        estado.value = empleado[5]
        
        nombre.update()
        apellido.update()
        cargo.update()
        qr.update()
        estado.update()

    def actualiza_tabla():
        """Funcion que actualiza la tabla luego de insertar , actualizar o eliminar un empleado"""

        datatable.rows.clear()
        for empleado in empleados.obtener_datos():
                
                usuario_existente = usuarios.verifica_usuario(
                    empleado[0]
                )

                datatable.rows.append(

                    ft.DataRow(

                        on_select_change = lambda e, empleado = empleado:
                        seleccionar(empleado),

                        cells = [
                            ft.DataCell(ft.Text(f"{empleado[0]}", color = "white")),
                            ft.DataCell(ft.Text(f"{empleado[1]}", color = "white")),
                            ft.DataCell(ft.Text(f"{empleado[2]}", color = "white")),
                            ft.DataCell(ft.Text(f"{empleado[3]}", color = "white")),
                            ft.DataCell(ft.Text(f"{empleado[4]}", color = "white")),
                            ft.DataCell(ft.Text(f"{empleado[5]}", color = "white")),

                            ft.DataCell(
                                ft.IconButton(
                                    icon = ft.Icons.PERSON_ADD,
                                    tooltip = "Crear Usuario",
                                    icon_color = "white",

                                    on_click = lambda e,
                                    empleado = empleado:

                                    creacion_usuario(e, empleado)
                                )
                                if not usuario_existente

                                else
                                ft.Text("Listo", color = "green")
                            )
                        ]
                    ) 
                )


    def mensaje(page, mensaje):
        """Muestra los mensajes de confirmacion de guardado, actualizacion y eliminacion de empleados"""

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
        cargo.value = ""
        qr.value = ""
        estado.value = None

        nombre.update()
        apellido.update()
        cargo.update()
        qr.update()
        estado.update()

    
    def agregar_empleado(e):
        """Funcion encargada de invocar el procedimiento almacenado de insertar plasmado en empleados.py
        de la carpeta database. Ademas de utilizar otras funciones para limpiar formulario y actualizar 
        la tabla del modulo"""

        empleados.insertar_empleado(
            nombre.value,
            apellido.value,
            cargo.value,
            qr.value,
            estado.value
        )

        actualiza_tabla()
        mensaje(e.page, "Empleado insertado correctamente")
        datatable.update()
        limpiar()
        table.update()

    
    def actualizacion_empleado(e):
        """Funcion para invocar el procedimiento almacenado de actualizar empleados plasmado en empleados.py
        de la carpeta database. Ademas de utilizar otras funciones para limpiar formulario y actualizar 
        la tabla del modulo"""

        if id_empleado is None:
            return
        
        dialog = ft.AlertDialog(
            modal = True,
            title = ft.Text("Confirmacion"),
            content = ft.Text("Esta seguro de actualizar este empleado?")
        )
        
        def cancelar(e):
            """Funcion para cuando se presiona el boton de cancelar de la ventana emergente"""

            dialog.open = False
            e.page.update()
        
        def actualizar(e):
            """Funcion para realizar la accion de actualizar empleados luego de las ventanas emergentes"""

            empleados.actualizar_empleado(
                id_empleado,
                nombre.value,
                apellido.value,
                cargo.value,
                qr.value,
                estado.value
            )
            actualiza_tabla()

            mensaje(e.page, "Empleado actualizado correctamente")
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


    def eliminacion_empleado(e):
        """Funcion para invocar el procedimiento almacenado de eliminar empleados plasmado en empleados.py
        de la carpeta database. Ademas de utilizar otras funciones para limpiar formulario y actualizar 
        la tabla del modulo"""

        if id_empleado is None:
            return
        
        dialog = ft.AlertDialog(
            modal = True,
            title = ft.Text("Confirmacion"),
            content = ft.Text("Esta seguro de eliminar este empleado?")
        )

        def cancelar(e):
            """Funcion para cuando se presiona el boton de cancelar de la ventana emergente"""

            dialog.open = False
            e.page.update()
        
        def eliminar(e):
            """Funcion para realizar la accion de eliminar empleados luego de la ventana emergente"""
        
            empleados.eliminar_empleado(id_empleado)

            actualiza_tabla()
            mensaje(e.page, "Empleado eliminado correctamente")
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

    def creacion_usuario(e, empleado):
        """Permite crear el usuario de un empleado"""

        existencia = usuarios.verifica_usuario(
            empleado[0]
        )

        if existencia:
            snack = ft.SnackBar(
                content = ft.Text(
                    "Este empleado ya tiene usuario",
                    color = "white"
                ),
                bgcolor = "red",
                open = True
            )

            e.page.overlay.append(snack)
            e.page.update()

            return

        from interfaz.vista_usuarios import vista_usuarios

        e.page.controls[0].controls[1].content = vista_usuarios(
                e.page,
                empleado[0],
                empleado[1],
                empleado[2]
            )
        e.page.update()

        
    datatable = ft.DataTable(
        expand = True,
        column_spacing = 50,
        horizontal_margin = 30,
        border = ft.Border.all(2, "white"),
        data_row_color = {ft.ControlState.SELECTED: "white",
                          ft.ControlState.PRESSED: "blue"},
                          show_checkbox_column = False,

                          columns = [
                            ft.DataColumn(ft.Text("ID", color = "white", weight = "bold")),
                            ft.DataColumn(ft.Text("Nombres", color = "white", weight = "bold")),
                            ft.DataColumn(ft.Text("Apellidos", color = "white", weight = "bold")),
                            ft.DataColumn(ft.Text("Cargo", color = "white", weight = "bold")),
                            ft.DataColumn(ft.Text("QR", color = "white", weight = "bold")),
                            ft.DataColumn(ft.Text("Estado", color = "white", weight = "bold")),
                            ft.DataColumn(ft.Text("Acciones", color = "white", weight = "bold"))
                          ],

                        rows = []
    )     
    actualiza_tabla()          

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
                cargo,
                qr,
                estado,
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
                                on_click = agregar_empleado,
                                icon = ft.Icons.SAVE,
                                icon_color = "white"         
                            ),

                            ft.IconButton(tooltip = "Actualizar",
                                on_click = actualizacion_empleado,
                                icon = ft.Icons.UPDATE,
                                icon_color = "white"         
                            ),

                            ft.IconButton(tooltip = "Eliminar",
                                on_click = eliminacion_empleado,
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
    
    page.controls.clean()
    page.add(vista_menu(page))
    page.update()