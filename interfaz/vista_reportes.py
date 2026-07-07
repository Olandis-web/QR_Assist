import flet as ft
import time
from interfaz.vista_empleados import vista_empleados
from interfaz.vista_usuarios import vista_usuarios
from database import reportes
from database import conexion

def vista_reportes(page, cambio_menu):
    '''Muestra el dashboard de reportes con cards de métricas, gráfico semanal,
    botones de exportación y tabla de últimos registros de asistencia.'''

    def actualizar_dashboard(e):
        """Permite actualizar los datos de la vista de reportes"""



    conectar = conexion.conexion()

    activos, total = reportes.total_empleados()
    presentes = reportes.presentes()
    tardanzas = reportes.tardanzas()
    ausentes = reportes.ausentes()
    sin_qr = reportes.sin_qr()
    registros = reportes.ultimos_registros()
    puntuales = reportes.top_puntuales()
    incidencias = reportes.top_incidencias()
    reportes.generar_pie(presentes, tardanzas, ausentes)
    reportes.generar_barchart()

    conectar.close()

    lista_ranking = ft.Column(spacing = 6, controls = [])

    def obtener_puntuales(e = None):
        """Muestra el ranking de empleados mas puntuales durante el mes. Esta en el Card
        de ranking y tiene un boton para cambiar los tops"""

        lista_ranking.controls.clear()
        for i, n in enumerate(puntuales):
            lista_ranking.controls.append(
                ft.Row(
                    controls = [
                        ft.Text(f"{i+1}.", color = "white", size = 11, width = 18),
                        ft.Text(f"{n[0]}, {n[1]}", color = "white", size = 12, expand = True),
                        ft.Text(f"{n[2]} dias", color = "#aed581", size = 12)
                    ]
                )
            )

            boton_puntuales.style = ft.ButtonStyle(bgcolor = ft.Colors.BLUE_GREY_600)
            boton_incidencias.style = ft.ButtonStyle(bgcolor = ft.Colors.BLUE_GREY_800)
            lista_ranking.update()
            boton_puntuales.update()
            boton_incidencias.update()


    def obtener_incidencias(e = None):
        """Muestra el ranking de empleados mas ausentes durante el mes. Esta en el Card
        de ranking y tiene un boton para cambiar los tops"""

        lista_ranking.controls.clear()
        for i, n in enumerate(incidencias):
            lista_ranking.controls.append(
                ft.Row(
                    controls = [
                        ft.Text(f"{i+1}.", color = "white", size = 11, width = 18),
                        ft.Text(f"{n[0]}, {n[1]}", color = "white", size = 12, expand = True),
                        ft.Text(f"{n[2]} dias", color = "#ef5350", size = 12)
                    ]
                )
            )

            boton_incidencias.style = ft.ButtonStyle(bgcolor = ft.Colors.BLUE_GREY_600)
            boton_puntuales.style = ft.ButtonStyle(bgcolor = ft.Colors.BLUE_GREY_800)
            lista_ranking.update()
            boton_puntuales.update()
            boton_incidencias.update()

    boton_puntuales = ft.ElevatedButton(
    content = ft.Text(
        "Puntuales",
        color = "#aed581",
        size = 12
    ),
    bgcolor = ft.Colors.BLUE_GREY_600,
    on_click = obtener_puntuales,
    style = ft.ButtonStyle(shape = ft.RoundedRectangleBorder(radius = 6))
    )

    boton_incidencias = ft.ElevatedButton(
        content = ft.Text(
            "Incidencias",
            color = "#ef5350",
            size = 12
        ),
        bgcolor = ft.Colors.BLUE_GREY_800,
        on_click = obtener_incidencias,
        style = ft.ButtonStyle(shape = ft.RoundedRectangleBorder(radius = 6))
    )

    obtener_puntuales()



    tabla = ft.DataTable(
        expand = True,
        column_spacing = 160,
        horizontal_margin = 60,
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

    for i in registros:
        tabla.rows.append(
            ft.DataRow(
                cells = [
                    ft.DataCell(ft.Text(f"{i[0]} {i[1]}", color = "white")),
                    ft.DataCell(ft.Text(f"{i[2]}", color = "white")),
                    ft.DataCell(ft.Text(str(i[3])[:8], color = "white")),
                    ft.DataCell(ft.Text(f"{i[4]}", color = "white")),
                    ft.DataCell(ft.Text(f"{i[5]}", color = "white")),
                ]
            )
        )

    contenido = ft.Container(
        expand = True,
        bgcolor = ft.Colors.BLUE_GREY_900,
        padding = 5,

        content = ft.Column(
            expand = True,
            spacing = 12,
            horizontal_alignment = ft.CrossAxisAlignment.STRETCH,

            controls = [

                ft.Row(
                    height = 30,
                    alignment = ft.MainAxisAlignment.SPACE_BETWEEN,
                    vertical_alignment = ft.CrossAxisAlignment.CENTER,
                    controls = [
                        ft.Text("Dashboard",
                                size = 20,
                                weight = "bold",
                                color = "white"
                        ),

                        ft.IconButton(
                            icon = ft.Icons.REFRESH,
                            icon_color = "white",
                            tooltip = "Actualizar info",
                            on_click = lambda e: cambio_menu(vista_reportes(page, cambio_menu))
                        )
                    ]
                ),

                ft.Row(
                    spacing = 16,
                    controls = [

                        # ── COLUMNA IZQUIERDA — CARDS ──────────────────────────
                        ft.Column(
                            width = 160,
                            spacing = 8,

                            controls = [

                                ft.Container(
                                    width = 180,
                                    bgcolor = ft.Colors.BLUE_GREY_800,
                                    border_radius = 10,
                                    padding = 15,
                                    content = ft.Column(
                                        spacing = 4,
                                        controls = [
                                            ft.Text("Empleados activos", color = "white54", size = 14, weight = "bold"),
                                            ft.Text(str(activos), color = "white", size = 29, weight = "bold")
                                        ]
                                    )
                                ),

                                ft.Container(
                                    width = 180,
                                    bgcolor = ft.Colors.BLUE_GREY_800,
                                    border_radius = 10,
                                    padding = 15,
                                    content = ft.Column(
                                        spacing = 4,
                                        controls = [
                                            ft.Text("Presentes hoy", color = "white54", size = 14, weight = "bold"),
                                            ft.Text(str(presentes), color = "green", size = 29, weight = "bold")
                                        ]
                                    )
                                ),

                                ft.Container(
                                    width = 180,
                                    bgcolor = ft.Colors.BLUE_GREY_800,
                                    border_radius = 10,
                                    padding = 15,
                                    content = ft.Column(
                                        spacing = 4,
                                        controls = [
                                            ft.Text("Tardanzas hoy", color = "white54", size = 14, weight = "bold"),
                                            ft.Text(str(tardanzas), color = "orange", size = 29, weight = "bold")
                                        ]
                                    )
                                ),

                                ft.Container(
                                    width = 180,
                                    bgcolor = ft.Colors.BLUE_GREY_800,
                                    border_radius = 10,
                                    padding = 15,
                                    content = ft.Column(
                                        spacing = 4,
                                        controls = [
                                            ft.Text("Ausentes hoy", color = "white54", size = 14, weight = "bold"),
                                            ft.Text(str(ausentes), color = "red", size = 29, weight = "bold")
                                        ]
                                    )
                                ),

                                ft.Container(
                                    width = 180,
                                    bgcolor = ft.Colors.BLUE_GREY_800,
                                    border_radius = 10,
                                    padding = 15,
                                    content = ft.Column(
                                        spacing = 4,
                                        controls = [
                                            ft.Text("Sin QR asignado", color = "white54", size = 14, weight = "bold"),
                                            ft.Text(str(sin_qr), color = "#ff7043", size = 29, weight = "bold")
                                        ]
                                    )
                                ),
                            ]
                        ),

                        # ── COLUMNA CENTRAL ────────────────────────────────────
                        ft.Column(
                            spacing = 12,

                            controls = [

                                # Gráfico semanal
                                ft.Container(
                                    width = 450,
                                    height = 190,
                                    bgcolor = ft.Colors.BLUE_GREY_800,
                                    border_radius = 10,
                                    padding = 16,
                                    content = ft.Column(
                                        spacing = 10,
                                        controls = [
                                            ft.Text("Ranking del mes", color = "white54", size = 14, weight = "bold"),
                                            ft.Row(
                                                spacing = 8,
                                                controls = [
                                                    boton_puntuales,
                                                    boton_incidencias
                                                ]
                                            ),
                                            ft.Divider(color = "white12", height = 1),
                                            lista_ranking
                                        ]
                                    )
                                ),

                                # Mini-cards

                                # Exportar reportes
                                ft.Container(
                                    width = 450,
                                    bgcolor = ft.Colors.BLUE_GREY_800,
                                    border_radius = 10,
                                    padding = 16,
                                    content = ft.Column(
                                        scroll = "auto",
                                        spacing = 14,
                                        controls = [

                                            ft.Text("Exportar reportes", color = "white54", size = 14, weight = "bold"),

                                            # Empleados
                                            ft.Column(
                                                spacing = 8,
                                                controls = [
                                                    ft.Row(
                                                        spacing = 6,
                                                        controls = [
                                                            ft.Icon(ft.Icons.PEOPLE, color = "white54", size = 15),
                                                            ft.Text("Empleados", color = "white70", size = 12, weight = "bold")
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
                                                            ft.Text("Usuarios", color = "white70", size = 12, weight = "bold")
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
                                                            ft.Text("Asistencia", color = "white70", size = 12, weight = "bold")
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

                        ft.Column(
                            expand = True,
                            spacing = 12,
                            controls = [

                                ft.Container(
                                    height = 300,
                                    width = 600,
                                    bgcolor = ft.Colors.BLUE_GREY_800,
                                    border_radius = 10,
                                    padding = 16,

                                    content = ft.Column(
                                        horizontal_alignment = ft.CrossAxisAlignment.CENTER,
                                        controls = [
                                            ft.Text("Distribucion de hoy", color = "white54", size = 14, weight = "bold"),

                                            ft.Row(
                                                alignment = ft.MainAxisAlignment.CENTER,
                                                spacing = 16,
                                                controls = [
                                                    ft.Row(
                                                        spacing = 4,
                                                        controls = [
                                                            ft.Container(width = 10, height = 10, bgcolor = "#388e3c", border_radius = 5),
                                                            ft.Text("A tiempo", color = "white54", size = 11)
                                                        ]
                                                    ),

                                                    ft.Row(
                                                        spacing = 4,
                                                        controls = [
                                                            ft.Container(width = 10, height = 10, bgcolor = "#f57c00", border_radius = 5),
                                                            ft.Text("Tardanza", color = "white54", size = 11)
                                                        ]
                                                    ),

                                                    ft.Row(
                                                        spacing = 4,
                                                        controls = [
                                                            ft.Container(width = 10, height = 10, bgcolor = "#c62828", border_radius = 5),
                                                            ft.Text("Ausente", color = "white54", size = 11)
                                                        ]
                                                    ),   
                                                ]
                                            ),

                                            ft.Image(
                                                src = f"pie_asistencia.png",
                                                width = 400,
                                                height = 250,
                                                fit = "contain"
                                            )
                                        ]    
                                    )
                                ),

                                
                                ft.Container(
                                    height = 185, 
                                    width = 600,
                                    bgcolor = ft.Colors.BLUE_GREY_800,
                                    border_radius = 10,
                                    padding = 16,

                                    content = ft.Column(
                                        horizontal_alignment = ft.CrossAxisAlignment.CENTER,
                                        controls = [
                                            ft.Text("Asistencia semanal", color = "white54", size = 14, weight = "bold"),
                                            ft.Image(
                                                src = f"bar_asistencia.png",
                                                width = 550,
                                                height = 140,
                                                fit = "contain"
                                            )
                                        ]
                                    )
                                )
                            ]
                        )
                    ]
                ),

                # ── TABLA DE ÚLTIMOS REGISTROS — ANCHO COMPLETO ────────────────
                ft.Container(
                    height = 230,
                    bgcolor = ft.Colors.BLUE_GREY_800,
                    border_radius = 10,
                    padding = 16,
                    content = ft.Column(
                        controls = [
                            ft.Text("Últimos registros de asistencia", color = "white54", size = 14, weight = "bold"),

                            ft.Container(
                                expand = True,
                                content = ft.Column(
                                    scroll = "auto",
                                    controls = [tabla]
                                )
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

