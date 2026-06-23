import flet as ft
from interfaz.vista_empleados import vista_empleados
from interfaz.vista_usuarios import vista_usuarios


def vista_reportes(page):
    '''Muestra el dashboard de reportes con cards de métricas, gráfico semanal,
    botones de exportación y tabla de últimos registros de asistencia.'''

    contenido = ft.Container(
        expand = True,
        bgcolor = ft.Colors.BLUE_GREY_900,
        padding = 16,

        content = ft.Column(
            expand = True,
            spacing = 12,

            controls = [

                ft.Row(
                    expand = True,
                    spacing = 16,

                    controls = [

                        # ── COLUMNA IZQUIERDA — CARDS ──────────────────────────
                        ft.Column(
                            width = 160,
                            spacing = 8,

                            controls = [

                                ft.Container(
                                    width = 140,
                                    bgcolor = ft.Colors.BLUE_GREY_800,
                                    border_radius = 10,
                                    padding = 15,
                                    content = ft.Column(
                                        spacing = 4,
                                        controls = [
                                            ft.Text("Empleados activos", color = "white54", size = 12),
                                            ft.Text("00", color = "white", size = 35, weight = "bold")
                                        ]
                                    )
                                ),

                                ft.Container(
                                    width = 140,
                                    bgcolor = ft.Colors.BLUE_GREY_800,
                                    border_radius = 10,
                                    padding = 15,
                                    content = ft.Column(
                                        spacing = 4,
                                        controls = [
                                            ft.Text("Presentes hoy", color = "white54", size = 12),
                                            ft.Text("00", color = "green", size = 35, weight = "bold")
                                        ]
                                    )
                                ),

                                ft.Container(
                                    width = 140,
                                    bgcolor = ft.Colors.BLUE_GREY_800,
                                    border_radius = 10,
                                    padding = 15,
                                    content = ft.Column(
                                        spacing = 4,
                                        controls = [
                                            ft.Text("Tardanzas hoy", color = "white54", size = 12),
                                            ft.Text("00", color = "orange", size = 35, weight = "bold")
                                        ]
                                    )
                                ),

                                ft.Container(
                                    width = 140,
                                    bgcolor = ft.Colors.BLUE_GREY_800,
                                    border_radius = 10,
                                    padding = 15,
                                    content = ft.Column(
                                        spacing = 4,
                                        controls = [
                                            ft.Text("Ausentes hoy", color = "white54", size = 12),
                                            ft.Text("00", color = "red", size = 35, weight = "bold")
                                        ]
                                    )
                                ),

                                ft.Container(
                                    width = 140,
                                    bgcolor = ft.Colors.BLUE_GREY_800,
                                    border_radius = 10,
                                    padding = 15,
                                    content = ft.Column(
                                        spacing = 4,
                                        controls = [
                                            ft.Text("Sin QR asignado", color = "white54", size = 12),
                                            ft.Text("00", color = "#ff7043", size = 35, weight = "bold")
                                        ]
                                    )
                                ),
                            ]
                        ),

                        # ── COLUMNA DERECHA ────────────────────────────────────
                        ft.Column(
                            expand = True,
                            spacing = 12,

                            controls = [

                                # Gráfico semanal
                                ft.Container(
                                    expand = True,
                                    bgcolor = ft.Colors.BLUE_GREY_800,
                                    border_radius = 10,
                                    padding = 20,
                                    content = ft.Column(
                                        controls = [
                                            ft.Text("Asistencia semanal", color = "white54", size = 12),
                                            ft.Text(
                                                "Gráfico por implementar",
                                                color = "white38",
                                                size = 13,
                                                italic = True
                                            )
                                        ]
                                    )
                                ),

                                # Mini-cards

                                # Exportar reportes
                                ft.Container(
                                    bgcolor = ft.Colors.BLUE_GREY_800,
                                    border_radius = 10,
                                    padding = 16,
                                    content = ft.Column(
                                        spacing = 14,
                                        controls = [

                                            ft.Text("Exportar reportes", color = "white54", size = 12),

                                            # Empleados
                                            ft.Column(
                                                spacing = 8,
                                                controls = [
                                                    ft.Row(
                                                        spacing = 6,
                                                        controls = [
                                                            ft.Icon(ft.Icons.PEOPLE, color = "white54", size = 15),
                                                            ft.Text("Empleados", color = "white70", size = 12)
                                                        ]
                                                    ),
                                                    ft.Row(
                                                        spacing = 8,
                                                        controls = [
                                                            ft.ElevatedButton(
                                                                content = ft.Row(
                                                                    spacing = 6,
                                                                    controls = [
                                                                        ft.Icon(ft.Icons.PICTURE_AS_PDF, color = "#ffcdd2", size = 16),
                                                                        ft.Text("PDF", color = "#ffcdd2", size = 12)
                                                                    ]
                                                                ),
                                                                bgcolor = "#b71c1c",
                                                                on_click = None,
                                                                style = ft.ButtonStyle(shape = ft.RoundedRectangleBorder(radius = 8))
                                                            ),
                                                            ft.ElevatedButton(
                                                                content = ft.Row(
                                                                    spacing = 6,
                                                                    controls = [
                                                                        ft.Icon(ft.Icons.TABLE_CHART, color = "#c8e6c9", size = 16),
                                                                        ft.Text("Excel", color = "#c8e6c9", size = 12)
                                                                    ]
                                                                ),
                                                                bgcolor = "#1b5e20",
                                                                on_click = None,
                                                                style = ft.ButtonStyle(shape = ft.RoundedRectangleBorder(radius = 8))
                                                            )
                                                        ]
                                                    )
                                                ]
                                            ),

                                            ft.Divider(color = "white12", height = 1),

                                            # Usuarios
                                            ft.Column(
                                                spacing = 8,
                                                controls = [
                                                    ft.Row(
                                                        spacing = 6,
                                                        controls = [
                                                            ft.Icon(ft.Icons.MANAGE_ACCOUNTS, color = "white54", size = 15),
                                                            ft.Text("Usuarios", color = "white70", size = 12)
                                                        ]
                                                    ),
                                                    ft.Row(
                                                        spacing = 8,
                                                        controls = [
                                                            ft.ElevatedButton(
                                                                content = ft.Row(
                                                                    spacing = 6,
                                                                    controls = [
                                                                        ft.Icon(ft.Icons.PICTURE_AS_PDF, color = "#ffcdd2", size = 16),
                                                                        ft.Text("PDF", color = "#ffcdd2", size = 12)
                                                                    ]
                                                                ),
                                                                bgcolor = "#b71c1c",
                                                                on_click = None,
                                                                style = ft.ButtonStyle(shape = ft.RoundedRectangleBorder(radius = 8))
                                                            ),
                                                            ft.ElevatedButton(
                                                                content = ft.Row(
                                                                    spacing = 6,
                                                                    controls = [
                                                                        ft.Icon(ft.Icons.TABLE_CHART, color = "#c8e6c9", size = 16),
                                                                        ft.Text("Excel", color = "#c8e6c9", size = 12)
                                                                    ]
                                                                ),
                                                                bgcolor = "#1b5e20",
                                                                on_click = None,
                                                                style = ft.ButtonStyle(shape = ft.RoundedRectangleBorder(radius = 8))
                                                            )
                                                        ]
                                                    )
                                                ]
                                            ),

                                            ft.Divider(color = "white12", height = 1),

                                            # Asistencia (pendiente — botones desactivados)
                                            ft.Column(
                                                spacing = 8,
                                                controls = [
                                                    ft.Row(
                                                        spacing = 6,
                                                        controls = [
                                                            ft.Icon(ft.Icons.CALENDAR_MONTH, color = "white54", size = 15),
                                                            ft.Text("Asistencia", color = "white70", size = 12)
                                                        ]
                                                    ),
                                                    ft.Row(
                                                        spacing = 8,
                                                        controls = [
                                                            ft.ElevatedButton(
                                                                content = ft.Row(
                                                                    spacing = 6,
                                                                    controls = [
                                                                        ft.Icon(ft.Icons.PICTURE_AS_PDF, color = "#546e7a", size = 16),
                                                                        ft.Text("Diario", color = "#546e7a", size = 12)
                                                                    ]
                                                                ),
                                                                bgcolor = "#37474f",
                                                                disabled = True,
                                                                style = ft.ButtonStyle(shape = ft.RoundedRectangleBorder(radius = 8))
                                                            ),
                                                            ft.ElevatedButton(
                                                                content = ft.Row(
                                                                    spacing = 6,
                                                                    controls = [
                                                                        ft.Icon(ft.Icons.PICTURE_AS_PDF, color = "#546e7a", size = 16),
                                                                        ft.Text("Semanal", color = "#546e7a", size = 12)
                                                                    ]
                                                                ),
                                                                bgcolor = "#37474f",
                                                                disabled = True,
                                                                style = ft.ButtonStyle(shape = ft.RoundedRectangleBorder(radius = 8))
                                                            ),
                                                            ft.ElevatedButton(
                                                                content = ft.Row(
                                                                    spacing = 6,
                                                                    controls = [
                                                                        ft.Icon(ft.Icons.PICTURE_AS_PDF, color = "#546e7a", size = 16),
                                                                        ft.Text("Mensual", color = "#546e7a", size = 12)
                                                                    ]
                                                                ),
                                                                bgcolor = "#37474f",
                                                                disabled = True,
                                                                style = ft.ButtonStyle(shape = ft.RoundedRectangleBorder(radius = 8))
                                                            )
                                                        ]
                                                    )
                                                ]
                                            ),

                                        ]
                                    )
                                ),

                            ]
                        ),

                    ]
                ),

                # ── TABLA DE ÚLTIMOS REGISTROS — ANCHO COMPLETO ────────────────
                ft.Container(
                    bgcolor = ft.Colors.BLUE_GREY_800,
                    border_radius = 10,
                    padding = 16,
                    content = ft.Column(
                        controls = [
                            ft.Text("Últimos registros de asistencia", color = "white54", size = 12),
                            ft.Column(
                                scroll = "auto",
                                controls = [
                                    ft.DataTable(
                                        expand = True,
                                        column_spacing = 40,
                                        horizontal_margin = 10,
                                        heading_row_color = ft.Colors.BLUE_GREY_700,

                                        columns = [
                                            ft.DataColumn(ft.Text("Empleado",     color = "white", weight = "bold")),
                                            ft.DataColumn(ft.Text("Cargo",        color = "white", weight = "bold")),
                                            ft.DataColumn(ft.Text("Hora entrada", color = "white", weight = "bold")),
                                            ft.DataColumn(ft.Text("Estado",       color = "white", weight = "bold")),
                                            ft.DataColumn(ft.Text("Fecha",        color = "white", weight = "bold")),
                                        ],

                                        rows = []
                                        # Las filas se llenarán con datos reales desde la BD
                                    )
                                ]
                            )
                        ]
                    )
                ),

            ]
        )
    )

    return ft.Row(
        controls = [contenido],
        expand = True
    )

