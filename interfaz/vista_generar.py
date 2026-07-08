import flet as ft
import random
import string
import qrcode
from database import conexion
from database import empleados

def crear_codigo():
    """Crea un codigo QR aleatorio"""

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
                                    icon = ft.Icons.PRINT,
                                    tooltip = "Imprimir QR",
                                    icon_color = "white",

                                    on_click = lambda e, 
                                    empleado = empleado:

                                    imprimir_qr(e, empleado)

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

    def imprimir_qr(e, empleado):
        """Funcion que sirve para el QR temporal y lo envia a imprimir"""

        from database.empleados import temporal_qr

        codigo = empleado[4]

        if not codigo:
            return

        temporal_qr(codigo, empleado)


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
                                    icon = ft.Icons.PRINT,
                                    tooltip = "Imprimir QR",
                                    on_click = lambda e, empleado = empleado: imprimir_qr(e, empleado)
                                )
                            ),
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


    def generar_qr (e, empleado):
        """Funcion que genera un QR aleatorio para los empleados y muestra su carnet"""

        if verifica_qr(empleado[0]):
            return 

        codigo = crear_codigo()
        guardar_qr(empleado[0], codigo)
        actualiza_tabla()
        datatable.update()
        
        
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
                            ft.DataColumn(ft.Text("Imprimir QR", color = "white", weight = "bold"))
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