import flet as ft
from interfaz.vista_empleados import vista_empleados
from interfaz.vista_usuarios import vista_usuarios


def vista_reportes():
    '''Esta funcion muestra el menu principal, con la division de la barra lateral y la parte del contenido.
    La barra lateral contiene los atajos hacia los formularios para hacer las acciones del sistema'''

    dashboards = ft.Container(
        expand = True,
        bgcolor = ft.Colors.BLUE_GREY_900,
        padding = 10,

        content = ft.Row(
            expand = True,
            controls = [

                ft.Column(
                    width = 250,
                    spacing = 15,

                    controls = [
                        ft.Container(
                            width = 220,
                            height = 120,
                            bgcolor = ft.Colors.BLUE_GREY_800,
                            border_radius = 15,
                            padding = 15,
                            content = ft.Column([
                                ft.Text("Empleados", color = "white"),
                                ft.Text("00",
                                    size = 35,
                                    color = "white",
                                    weight = "bold"
                                )
                            ])
                        ),

                        ft.Container(
                            width = 220,
                            height = 120,
                            bgcolor = ft.Colors.BLUE_GREY_800,
                            border_radius = 15,
                            padding = 15,
                            content = ft.Column([
                                ft.Text("Presentes", color = "white"),
                                ft.Text("00",
                                        size = 35,
                                        color = "green",
                                        weight = "bold"
                                )
                            ])
                        ),
                        
                        ft.Container(
                            width = 220,
                            height = 120,
                            bgcolor = ft.Colors.BLUE_GREY_800,
                            border_radius = 15,
                            padding = 15,
                            content = ft.Column([
                                ft.Text("Tardanzas", color = "white"),
                                ft.Text("00",
                                        size = 35,
                                        color = "orange",
                                        weight = "bold"
                                )
                            ])
                        ),

                        ft.Container(
                            width = 220,
                            height = 120,
                            bgcolor = ft.Colors.BLUE_GREY_800,
                            border_radius = 15,
                            padding = 15,
                            content = ft.Column([
                                ft.Text("Ausentes", color = "white"),
                                ft.Text("00",
                                        size = 35,
                                        color = "red",
                                        weight = "bold"
                                )
                            ])
                        )
                    ]    
                ),

                ft.Column(
                    expand = True,
                    spacing = 15,
                    controls = [
                        ft.Container(
                            expand = True,
                            height = 300,
                            bgcolor = ft.Colors.BLUE_GREY_800,
                            border_radius = 15,
                            padding = 20,
                            content = ft.Text(
                                "Grafico",
                                color = "white",
                                size = 20
                            )
                        ),

                            ft.Container(
                            expand = True,
                            height = 300,
                            bgcolor = ft.Colors.BLUE_GREY_800,
                            border_radius = 15,
                            padding = 20,
                            content = ft.Text(
                                "Ultimos registros",
                                color = "white",
                                size = 20
                            )
                        )
                    ]
                )
            ]
        )
    )       



    return ft.Row([
        dashboards
    ],
    expand = True
    )