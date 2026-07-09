"""Generación de reportes PDF para QR Assist."""

from datetime import datetime, timedelta
from collections import Counter
from io import BytesIO
from pathlib import Path

import matplotlib.pyplot as plt
from platformdirs import user_documents_dir
from reportlab.lib import colors
from reportlab.lib.enums import TA_RIGHT
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import (
    Paragraph,
    Image,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

from database import empleados, usuarios, reportes


AZUL_OSCURO = colors.HexColor("#17324D")
AZUL = colors.HexColor("#2563A6")
CELESTE = colors.HexColor("#EAF3FB")
GRIS = colors.HexColor("#5B6770")
VERDE = colors.HexColor("#1F8A70")
ROJO = colors.HexColor("#C0392B")


def _carpeta_reportes() -> Path:
    """Crea y devuelve la carpeta de descargas de reportes de la aplicación."""
    carpeta = Path(user_documents_dir()) / "QR Assist" / "Reportes"
    carpeta.mkdir(parents=True, exist_ok=True)
    return carpeta


def _estilos():
    base = getSampleStyleSheet()
    return {
        "titulo": ParagraphStyle(
            "TituloQR",
            parent=base["Title"],
            fontName="Helvetica-Bold",
            fontSize=21,
            leading=25,
            textColor=AZUL_OSCURO,
            spaceAfter=2,
        ),
        "subtitulo": ParagraphStyle(
            "SubtituloQR",
            parent=base["Normal"],
            fontName="Helvetica",
            fontSize=9,
            leading=12,
            textColor=GRIS,
        ),
        "dato": ParagraphStyle(
            "DatoQR",
            parent=base["Normal"],
            fontName="Helvetica",
            fontSize=8,
            leading=10,
            textColor=AZUL_OSCURO,
        ),
        "pie": ParagraphStyle(
            "PieQR",
            parent=base["Normal"],
            fontName="Helvetica",
            fontSize=7,
            textColor=GRIS,
            alignment=TA_RIGHT,
        ),
    }


def _cabecera(canvas, documento):
    """Dibuja una cabecera y pie consistente en cada página."""
    canvas.saveState()
    ancho, alto = landscape(A4)
    canvas.setFillColor(AZUL_OSCURO)
    canvas.rect(0, alto - 0.45 * cm, ancho, 0.45 * cm, fill=1, stroke=0)
    canvas.setFillColor(GRIS)
    canvas.setFont("Helvetica", 7)
    canvas.drawString(documento.leftMargin, 0.55 * cm, "QR Assist · Reporte generado automáticamente")
    canvas.drawRightString(ancho - documento.rightMargin, 0.55 * cm, f"Página {documento.page}")
    canvas.restoreState()


def _tabla(datos, encabezados, anchos):
    filas = [encabezados]
    for fila in datos:
        filas.append([Paragraph(str(valor or "—"), _estilos()["dato"]) for valor in fila])

    tabla = Table(filas, colWidths=anchos, repeatRows=1, hAlign="LEFT")
    tabla.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), AZUL_OSCURO),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("FONTSIZE", (0, 0), (-1, 0), 8),
                ("ALIGN", (0, 0), (0, -1), "CENTER"),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("TOPPADDING", (0, 0), (-1, 0), 7),
                ("BOTTOMPADDING", (0, 0), (-1, 0), 7),
                ("TOPPADDING", (0, 1), (-1, -1), 6),
                ("BOTTOMPADDING", (0, 1), (-1, -1), 6),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, CELESTE]),
                ("GRID", (0, 0), (-1, -1), 0.25, colors.HexColor("#C9D9E7")),
            ]
        )
    )
    return tabla


def _grafico_pastel(titulo, valores, colores):
    """Convierte una distribución de datos en un gráfico circular para el PDF."""
    valores = {str(clave): cantidad for clave, cantidad in valores.items() if cantidad > 0}
    figura, eje = plt.subplots(figsize=(4.2, 2.65), dpi=150)
    figura.patch.set_facecolor("white")

    if valores:
        etiquetas = list(valores)
        cantidades = list(valores.values())
        eje.pie(
            cantidades,
            labels=etiquetas,
            colors=[colores[indice % len(colores)] for indice in range(len(etiquetas))],
            autopct=lambda porcentaje: f"{porcentaje:.0f}%" if porcentaje else "",
            startangle=90,
            counterclock=False,
            textprops={"fontsize": 8, "color": "#17324D"},
            wedgeprops={"edgecolor": "white", "linewidth": 1.5},
        )
    else:
        eje.text(0.5, 0.5, "Sin registros", ha="center", va="center", color="#5B6770")

    eje.set_title(titulo, loc="left", fontsize=11, fontweight="bold", color="#17324D", pad=10)
    eje.set_aspect("equal")
    buffer = BytesIO()
    figura.savefig(buffer, format="png", bbox_inches="tight", facecolor="white")
    plt.close(figura)
    buffer.seek(0)
    imagen = Image(buffer, width=8.8 * cm, height=5.55 * cm)
    imagen._buffer = buffer  # Mantiene el contenido disponible hasta construir el PDF.
    return imagen


def _bloque_graficos(graficos):
    """Organiza los gráficos en una cuadrícula limpia dentro del reporte."""
    filas = [graficos[indice : indice + 2] for indice in range(0, len(graficos), 2)]
    if filas and len(filas[-1]) == 1:
        filas[-1].append("")
    bloque = Table(filas, colWidths=[9.35 * cm, 9.35 * cm], hAlign="LEFT")
    bloque.setStyle(
        TableStyle(
            [
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ("BOX", (0, 0), (-1, -1), 0.35, colors.HexColor("#D7E3ED")),
                ("INNERGRID", (0, 0), (-1, -1), 0.35, colors.HexColor("#D7E3ED")),
                ("TOPPADDING", (0, 0), (-1, -1), 8),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
            ]
        )
    )
    return bloque


def _crear_reporte(nombre_archivo, titulo, descripcion, resumen, graficos, tabla):
    ruta = _carpeta_reportes() / nombre_archivo
    estilos = _estilos()
    documento = SimpleDocTemplate(
        str(ruta),
        pagesize=landscape(A4),
        leftMargin=1.25 * cm,
        rightMargin=1.25 * cm,
        topMargin=1.3 * cm,
        bottomMargin=1.25 * cm,
        title=titulo,
        author="QR Assist",
    )
    fecha = datetime.now().strftime("%d/%m/%Y %H:%M")
    historia = [
        Paragraph("QR ASSIST", ParagraphStyle("Marca", fontName="Helvetica-Bold", fontSize=9, textColor=AZUL)),
        Spacer(1, 0.12 * cm),
        Paragraph(titulo, estilos["titulo"]),
        Paragraph(f"{descripcion}<br/>Generado el {fecha}", estilos["subtitulo"]),
        Spacer(1, 0.45 * cm),
        resumen,
        Spacer(1, 0.45 * cm),
        Paragraph("Resumen visual", ParagraphStyle("EncabezadoGrafico", fontName="Helvetica-Bold", fontSize=12, textColor=AZUL_OSCURO)),
        Spacer(1, 0.18 * cm),
        _bloque_graficos(graficos),
        Spacer(1, 0.45 * cm),
        Paragraph("Detalle de registros", ParagraphStyle("EncabezadoTabla", fontName="Helvetica-Bold", fontSize=12, textColor=AZUL_OSCURO)),
        Spacer(1, 0.18 * cm),
        tabla,
        Spacer(1, 0.2 * cm),
        Paragraph("Documento confidencial para uso administrativo.", estilos["pie"]),
    ]
    documento.build(historia, onFirstPage=_cabecera, onLaterPages=_cabecera)
    return ruta


def generar_reporte_empleados() -> Path:
    """Genera un PDF visual con todos los empleados registrados en SQL Server."""
    registros = empleados.obtener_datos()
    activos = sum(1 for empleado in registros if empleado[5] == "Activo")
    con_qr = sum(1 for empleado in registros if empleado[4])
    estados = Counter(empleado[5] or "Sin estado" for empleado in registros)
    qr = Counter("Con QR" if empleado[4] else "Pendiente" for empleado in registros)
    resumen = Table(
        [[f"TOTAL\n{len(registros)}", f"ACTIVOS\n{activos}", f"CON CÓDIGO QR\n{con_qr}"]],
        colWidths=[5.2 * cm, 5.2 * cm, 5.2 * cm],
    )
    resumen.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (0, 0), CELESTE),
                ("BACKGROUND", (1, 0), (1, 0), colors.HexColor("#E8F5EE")),
                ("BACKGROUND", (2, 0), (2, 0), colors.HexColor("#FFF4E5")),
                ("TEXTCOLOR", (0, 0), (-1, -1), AZUL_OSCURO),
                ("FONTNAME", (0, 0), (-1, -1), "Helvetica-Bold"),
                ("FONTSIZE", (0, 0), (-1, -1), 10),
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("TOPPADDING", (0, 0), (-1, -1), 10),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
            ]
        )
    )
    datos = [(fila[0], fila[1], fila[2], fila[3], "Asignado" if fila[4] else "Pendiente", fila[5]) for fila in registros]
    tabla = _tabla(
        datos,
        ["ID", "NOMBRES", "APELLIDOS", "CARGO", "CÓDIGO QR", "ESTADO"],
        [1.2 * cm, 4.3 * cm, 4.3 * cm, 4.5 * cm, 3.5 * cm, 3 * cm],
    )
    graficos = [
        _grafico_pastel("Empleados por estado", estados, ["#1F8A70", "#E07A24", "#C0392B", "#5B8DEF"]),
        _grafico_pastel("Asignación de códigos QR", qr, ["#2563A6", "#E07A24"]),
    ]
    return _crear_reporte(
        "reporte_empleados.pdf",
        "Reporte de empleados",
        "Listado general de empleados registrados en QR Assist.",
        resumen,
        graficos,
        tabla,
    )


def generar_reporte_usuarios() -> Path:
    """Genera un PDF de usuarios sin incluir contraseñas."""
    registros = usuarios.obtener_datos()
    administradores = sum(1 for usuario in registros if usuario[6] == "Administrador")
    roles = Counter(usuario[6] or "Sin rol" for usuario in registros)
    resumen = Table(
        [[f"TOTAL DE USUARIOS\n{len(registros)}", f"ADMINISTRADORES\n{administradores}"]],
        colWidths=[6.5 * cm, 6.5 * cm],
    )
    resumen.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (0, 0), CELESTE),
                ("BACKGROUND", (1, 0), (1, 0), colors.HexColor("#E8F5EE")),
                ("TEXTCOLOR", (0, 0), (-1, -1), AZUL_OSCURO),
                ("FONTNAME", (0, 0), (-1, -1), "Helvetica-Bold"),
                ("FONTSIZE", (0, 0), (-1, -1), 10),
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ("TOPPADDING", (0, 0), (-1, -1), 10),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
            ]
        )
    )
    datos = [(fila[0], fila[1], fila[2], fila[3], fila[4], fila[6]) for fila in registros]
    tabla = _tabla(
        datos,
        ["ID", "ID EMPLEADO", "NOMBRES", "APELLIDOS", "USUARIO", "ROL"],
        [1.2 * cm, 2.4 * cm, 4.3 * cm, 4.3 * cm, 4.5 * cm, 3.5 * cm],
    )
    graficos = [
        _grafico_pastel("Usuarios por rol", roles, ["#2563A6", "#1F8A70", "#E07A24", "#8E5EA2"]),
    ]
    return _crear_reporte(
        "reporte_usuarios.pdf",
        "Reporte de usuarios",
        "Listado de cuentas de acceso registradas. Las contraseñas no se incluyen por seguridad.",
        resumen,
        graficos,
        tabla,
    )


def generar_reporte_asistencia_semanal() -> Path:
    """Genera un PDF con el reporte de asistencia semanal."""
    from datetime import date

    hoy = date.today()
    lunes = hoy - timedelta(days=hoy.weekday())

    conectar = reportes.conexion.conexion()
    cursor = conectar.cursor()
    cursor.execute("""
        SELECT e.Nombres, e.Apellidos, e.Cargo,
               a.Fecha, a.Hora_Entrada, a.Estado
        FROM Asistencia a
        JOIN Empleados e ON a.ID_Empleado = e.ID_Empleado
        WHERE a.Fecha >= ? AND a.Fecha <= ?
        ORDER BY a.Fecha, e.Apellidos, e.Nombres
    """, (lunes, hoy))
    registros = cursor.fetchall()
    conectar.close()

    total_asistencias = len(registros)
    a_tiempo = sum(1 for r in registros if r[5] == "A tiempo")
    tardanza = sum(1 for r in registros if r[5] == "Tardanza")
    ausente = sum(1 for r in registros if r[5] == "Ausente")

    resumen = Table(
        [[f"TOTAL\n{total_asistencias}", f"A TIEMPO\n{a_tiempo}", f"TARDANZA\n{tardanza}", f"AUSENTE\n{ausente}"]],
        colWidths=[3.9 * cm, 3.9 * cm, 3.9 * cm, 3.9 * cm],
    )
    resumen.setStyle(
        TableStyle([
            ("BACKGROUND", (0, 0), (0, 0), CELESTE),
            ("BACKGROUND", (1, 0), (1, 0), colors.HexColor("#E8F5EE")),
            ("BACKGROUND", (2, 0), (2, 0), colors.HexColor("#FFF4E5")),
            ("BACKGROUND", (3, 0), (3, 0), colors.HexColor("#FFEBEE")),
            ("TEXTCOLOR", (0, 0), (-1, -1), AZUL_OSCURO),
            ("FONTNAME", (0, 0), (-1, -1), "Helvetica-Bold"),
            ("FONTSIZE", (0, 0), (-1, -1), 10),
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("TOPPADDING", (0, 0), (-1, -1), 10),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
        ])
    )

    datos = [(r[0], r[1], r[2], str(r[3]), str(r[4])[:8], r[5]) for r in registros]
    tabla = _tabla(
        datos,
        ["NOMBRES", "APELLIDOS", "CARGO", "FECHA", "HORA", "ESTADO"],
        [3.5 * cm, 3.5 * cm, 3.5 * cm, 2.8 * cm, 2.5 * cm, 2.5 * cm],
    )

    estados = Counter(r[5] for r in registros)
    graficos = [
        _grafico_pastel("Distribución semanal", estados, ["#1F8A70", "#E07A24", "#C0392B"]),
    ]

    return _crear_reporte(
        "reporte_asistencia_semanal.pdf",
        "Reporte de asistencia semanal",
        f"Resumen de asistencia desde {lunes} hasta {hoy}.",
        resumen,
        graficos,
        tabla,
    )


def generar_reporte_asistencia_mensual() -> Path:
    """Genera un PDF con el reporte de asistencia mensual."""
    from datetime import date

    hoy = date.today()
    inicio_mes = hoy.replace(day=1)

    conectar = reportes.conexion.conexion()
    cursor = conectar.cursor()
    cursor.execute("""
        SELECT e.Nombres, e.Apellidos, e.Cargo,
               a.Fecha, a.Hora_Entrada, a.Estado
        FROM Asistencia a
        JOIN Empleados e ON a.ID_Empleado = e.ID_Empleado
        WHERE a.Fecha >= ? AND a.Fecha <= ?
        ORDER BY a.Fecha, e.Apellidos, e.Nombres
    """, (inicio_mes, hoy))
    registros = cursor.fetchall()
    conectar.close()

    total_asistencias = len(registros)
    a_tiempo = sum(1 for r in registros if r[5] == "A tiempo")
    tardanza = sum(1 for r in registros if r[5] == "Tardanza")
    ausente = sum(1 for r in registros if r[5] == "Ausente")

    resumen = Table(
        [[f"TOTAL\n{total_asistencias}", f"A TIEMPO\n{a_tiempo}", f"TARDANZA\n{tardanza}", f"AUSENTE\n{ausente}"]],
        colWidths=[3.9 * cm, 3.9 * cm, 3.9 * cm, 3.9 * cm],
    )
    resumen.setStyle(
        TableStyle([
            ("BACKGROUND", (0, 0), (0, 0), CELESTE),
            ("BACKGROUND", (1, 0), (1, 0), colors.HexColor("#E8F5EE")),
            ("BACKGROUND", (2, 0), (2, 0), colors.HexColor("#FFF4E5")),
            ("BACKGROUND", (3, 0), (3, 0), colors.HexColor("#FFEBEE")),
            ("TEXTCOLOR", (0, 0), (-1, -1), AZUL_OSCURO),
            ("FONTNAME", (0, 0), (-1, -1), "Helvetica-Bold"),
            ("FONTSIZE", (0, 0), (-1, -1), 10),
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("TOPPADDING", (0, 0), (-1, -1), 10),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
        ])
    )

    datos = [(r[0], r[1], r[2], str(r[3]), str(r[4])[:8], r[5]) for r in registros]
    tabla = _tabla(
        datos,
        ["NOMBRES", "APELLIDOS", "CARGO", "FECHA", "HORA", "ESTADO"],
        [3.5 * cm, 3.5 * cm, 3.5 * cm, 2.8 * cm, 2.5 * cm, 2.5 * cm],
    )

    estados = Counter(r[5] for r in registros)
    graficos = [
        _grafico_pastel("Distribución mensual", estados, ["#1F8A70", "#E07A24", "#C0392B"]),
    ]

    return _crear_reporte(
        "reporte_asistencia_mensual.pdf",
        "Reporte de asistencia mensual",
        f"Resumen de asistencia desde {inicio_mes} hasta {hoy}.",
        resumen,
        graficos,
        tabla,
    )