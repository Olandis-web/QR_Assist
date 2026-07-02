import flet as ft
import random
import string
import qrcode
from database import conexion
from database import empleados

def crear_codigo():

    return ''.join(
        random.choices(
            string.ascii_uppercase + string.digits,
            k=16
        )
    )

def vista_generar(page):
    '''Muestra el contenido de el formulario de empleados.'''

    def buscar(e):
        """Funcion para hacer funcionar la barra de busqueda"""
        
        nom = busqueda.value.lower()
        datatable.rows.clear()

        for empleado in empleados.obtener_datos():
            nombre = f"{empleado [1]} {empleado[2]}".lower()

            if nom in nombre:

                datatable.rows.append(
                    ft.DataRow(
                        
                        cells = [
                            ft.DataCell(ft.Text(f"{empleado[0]}", color = "white")),
                            ft.DataCell(ft.Text(f"{empleado[1]}", color = "white")),
                            ft.DataCell(ft.Text(f"{empleado[2]}", color = "white")),
                            ft.DataCell(ft.Text(f"{empleado[3]}", color = "white")),
                            ft.DataCell(ft.Text(f"{empleado[5]}", color = "white")),

                            ft.DataCell(
                                ft.IconButton(
                                    icon = ft.Icons.QR_CODE_2,
                                    tooltip = "Generar QR",
                                    icon_color = "white",

                                    on_click = lambda e, 
                                    empleado = empleado:

                                    generar_qr(e, empleado)

                                )
                                if not verifica_qr(empleado[0])

                                else 
                                ft.Text("Listo", color ="green")
                            ),

                            ft.DataCell(
                                ft.IconButton(
                                    icon = ft.Icons.VISIBILITY,
                                    tooltip = "Ver QR",
                                    icon_color = "white",

                                    on_click = lambda e, 
                                    empleado = empleado:

                                    ver_qr(e, empleado)

                                )
                            )
                            
                        ]
                    )
                )
                datatable.update()
                                
    busqueda = ft.TextField(
        label = "Buscar empleado",
        suffix_icon = ft.Icons.SEARCH,
        border = ft.InputBorder.UNDERLINE,
        label_style = ft.TextStyle(color = "white"),
        on_submit = buscar
    )

    id_empleado = None

    def ver_qr(e, empleado):
        """Funcion que sirve para ver el QR de los empleados (boton)"""

        ruta = f"qr/qr_{empleado[0]}.png"

        carnet = ft.AlertDialog(
            title = ft.Text("QR del empleado"),

            content = ft.Column(
                tight = True,
                controls = [
                    ft.Text(
                        f"{empleado[1]}_{empleado[2]}"
                    ),

                    ft.Image(
                        src = ruta,
                        width = 200,
                        height = 200
                    )
                ]
            )
        )
        
        page.overlay.append(carnet)
        carnet.open = True
        page.update()

    def verifica_qr(id_empleado):
        """Funcion para verificar si el empleado ya tiene un QR"""

        conec = conexion.conexion()
        cursor = conec.cursor()

        cursor.execute("SELECT Codigo_qr from Empleados WHERE ID_Empleado = ?", (id_empleado,))

        resultado = cursor.fetchone()
        conec.close()

        if resultado and resultado[0]:
            return True
        
        return False


    def actualiza_tabla():
        """Funcion que actualiza la tabla luego de insertar , actualizar o eliminar un empleado"""

        datatable.rows.clear()
        for empleado in empleados.obtener_datos():

                datatable.rows.append(

                    ft.DataRow(

                        cells = [
                            ft.DataCell(ft.Text(f"{empleado[0]}", color = "white")),
                            ft.DataCell(ft.Text(f"{empleado[1]}", color = "white")),
                            ft.DataCell(ft.Text(f"{empleado[2]}", color = "white")),
                            ft.DataCell(ft.Text(f"{empleado[3]}", color = "white")),
                            ft.DataCell(ft.Text(f"{empleado[5]}", color = "white")),

                            ft.DataCell(
                                ft.IconButton(
                                    icon = ft.Icons.QR_CODE_2_ROUNDED,
                                    tooltip = "Generar QR",
                                    icon_color = "white",

                                    on_click = lambda e,
                                    empleado = empleado:

                                    generar_qr(e, empleado)
                                )
                                if not verifica_qr(empleado[0])

                                else 
                                ft.Text("Listo", color ="green")
                            ),

                            ft.DataCell(
                                ft.IconButton(
                                    icon = ft.Icons.VISIBILITY,
                                    tooltip = "Ver QR",
                                    on_click = lambda e, empleado = empleado: ver_qr(e, empleado)
                                )
                            )
                        ]
                    ) 
                )

    def guardar_qr(id_empleado, codigo_qr):
        """Funcion que sirve para guardar el QR a la tabla de empleados"""

        conec = conexion.conexion()
        cursor = conec.cursor()

        cursor.execute("UPDATE Empleados SET codigo_qr = ? WHERE ID_Empleado = ?", (codigo_qr, id_empleado))

        conec.commit()
        conec.close()


    def cerrar_carnet(e, carnet):
        """Sirve para cerrar la ventana del carnet"""
        
        carnet.open = False
        page.update()


    def generar_qr (e, empleado):
        """Funcion que genera un QR aleatorio para los empleados y muestra su carnet"""

        if verifica_qr(empleado[0]):
            return 

        codigo = crear_codigo()
        qr = qrcode.make(codigo)
        ruta = f"qr/qr_{empleado[0]}.png"
        qr.save(ruta)
        guardar_qr(empleado[0], codigo)
        actualiza_tabla()
        datatable.update()


        carnet = ft.AlertDialog(
            modal = True,

            title = ft.Text(
                "Carnet de Empleado",
                weight = "bold"
            ),

            content = ft.Container(
                width = 350,

                content = ft.Column(
                    tight = True,

                    controls = [
                        ft.Text(f"{empleado[1]} {empleado[2]}",
                                size = 20,
                                weight = "bold"),

                            ft.Text(f"Cargo: {empleado[3]}"),

                            ft.Text(f"Codigo: {codigo}"),

                            ft.Image(
                                src = ruta,
                                width = 200,
                                height = 200,
                                fit = "contain"
                            )
                    ]
                )
            ),

            actions = [
                ft.TextButton(
                    "Imprimir"
                ),

                ft.TextButton(
                    "Cerrar",
                    on_click = lambda x: cerrar_carnet(e, carnet)
                )
            ]
        )
        page.overlay.append(carnet)
        carnet.open = True
        page.update()
        
        
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
                            ft.DataColumn(ft.Text("Estado", color = "white", weight = "bold")),
                            ft.DataColumn(ft.Text("Generar QR", color = "white", weight = "bold")),
                            ft.DataColumn(ft.Text("Ver QR", color = "white", weight = "bold"))
                          ],

                        rows = []
    )     
    actualiza_tabla()          

    table = ft.Container(
        expand = True,
        bgcolor = ft.Colors.BLUE_GREY_900,
        padding = 20,

        content = ft.Column(
            controls = [
                busqueda,

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

    return ft.Column(
            controls = [
                table
            ],
        expand = True,
        
    )

def volver_menu(page):
    """Esta funcion se encarga de volver al menu principal luego de realizar cualquier
    accion dentro de esta vista"""

    from interfaz.menu import vista_menu
    
    page.clean()
    page.add(vista_menu(page))
    page.update()