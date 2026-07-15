import pyodbc
from database import conexion
import matplotlib.pyplot as plt



def total_empleados():
    """Retorna la cantidad de empleados activos y el total registrados"""

    conectar = conexion.conexion()
    cursor = conectar.cursor()

    cursor.execute("SELECT COUNT(*) FROM Empleados WHERE Estado = 'Activo'")
    activos = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM Empleados")
    total = cursor.fetchone()[0]

    conectar.close()
    return activos, total


def presentes():
    """Retorna la cantidad de empleados presentes hoy (A tiempo y Tardanza)"""

    conectar = conexion.conexion()
    cursor = conectar.cursor()

    cursor.execute("""
        SELECT COUNT(*) FROM Asistencia a
        JOIN Empleados e ON a.ID_Empleado = e.ID_Empleado
        WHERE a.Fecha = CAST(GETDATE() AS DATE)
        AND a.Estado IN ('A tiempo', 'Tardanza')
        AND e.Estado = 'Activo'
    """)

    total = cursor.fetchone()[0]
    conectar.close()
    return total


def tardanzas():
    """Retorna la cantidad de tardanzas registradas hoy"""

    conectar = conexion.conexion()
    cursor = conectar.cursor()

    cursor.execute("""
        SELECT COUNT(*) FROM Asistencia a
        JOIN Empleados e ON a.ID_Empleado = e.ID_Empleado
        WHERE a.Fecha = CAST(GETDATE() AS DATE)
        AND a.Estado = 'Tardanza'
        AND e.Estado = 'Activo'
    """)

    total = cursor.fetchone()[0]
    conectar.close()
    return total


def ausentes():
    """Retorna empleados activos sin ningún registro de asistencia hoy"""

    conectar = conexion.conexion()
    cursor = conectar.cursor()

    cursor.execute("""
        SELECT COUNT(*) FROM Empleados
        WHERE Estado = 'Activo'
        AND ID_Empleado NOT IN (
            SELECT ID_Empleado FROM Asistencia
            WHERE Fecha = CAST(GETDATE() AS DATE)
        )
    """)

    total = cursor.fetchone()[0]
    conectar.close()
    return total


def sin_qr():
    """Retorna la cantidad de empleados sin QR asignado"""

    conectar = conexion.conexion()
    cursor = conectar.cursor()

    cursor.execute("""
        SELECT COUNT(*) FROM Empleados
        WHERE Codigo_qr IS NULL OR Codigo_qr = ''
    """)

    total = cursor.fetchone()[0]
    conectar.close()
    return total


def ultimos_registros():
    """Retorna los últimos 10 registros de asistencia con nombre y cargo del empleado"""

    conectar = conexion.conexion()
    cursor = conectar.cursor()

    cursor.execute("""
        SELECT TOP 10
            e.Nombres,
            e.Apellidos,
            e.Cargo,
            a.Hora_Entrada,
            a.Estado,
            a.Fecha
        FROM Asistencia a
        JOIN Empleados e ON a.ID_Empleado = e.ID_Empleado
        ORDER BY a.Fecha DESC, a.Hora_Entrada DESC
    """)

    datos = cursor.fetchall()
    conectar.close()
    return datos

def top_puntuales():
    """Muestra cuales son los 5 empleados mas puntuales"""
    conectar = conexion.conexion()
    cursor = conectar.cursor()
    cursor.execute("""
        SELECT TOP 5
            e.Nombres, e.Apellidos,
            COUNT(*) AS Dias_a_tiempo
        FROM Asistencia a
        JOIN Empleados e ON a.ID_Empleado = e.ID_Empleado
        WHERE a.Estado = 'A tiempo'
        AND e.Estado = 'Activo'
        AND MONTH(a.Fecha) = MONTH(GETDATE())
        AND YEAR(a.Fecha) = YEAR(GETDATE())
        GROUP BY e.Nombres, e.Apellidos
        ORDER BY Dias_a_tiempo DESC
    """)
    datos = cursor.fetchall()
    conectar.close()
    return datos


def top_incidencias():
    """Muestra los empleados que mas faltan al trabajo"""
    conectar = conexion.conexion()
    cursor = conectar.cursor()
    cursor.execute("""
        SELECT TOP 5
            e.Nombres, e.Apellidos,
            COUNT(*) AS Total_incidencias
        FROM Asistencia a
        JOIN Empleados e ON a.ID_Empleado = e.ID_Empleado
        WHERE a.Estado IN ('Tardanza', 'Ausente')
        AND e.Estado = 'Activo'
        AND MONTH(a.Fecha) = MONTH(GETDATE())
        AND YEAR(a.Fecha) = YEAR(GETDATE())
        GROUP BY e.Nombres, e.Apellidos
        ORDER BY Total_incidencias DESC
    """)
    datos = cursor.fetchall()
    conectar.close()
    return datos

def generar_pie(presentes, tardanzas, ausentes):
    """Funcion que permite crear y mandar el PieChart a Vista_reportes"""

    fig, ax = plt.subplots(figsize = (4, 3))
    fig.patch.set_facecolor("#37474f")
    ax.set_facecolor("#37474f")

    valores = [
        presentes if presentes > 0 else 0.1,
        tardanzas if tardanzas > 0 else 0.1,
        ausentes if ausentes > 0 else 0.1
    ]
    colores = ["#388e3c", "#f57c00", "#c62828"]

    ax.pie(
        valores,
        colors = colores,
        autopct = "%1.0f%%",
        textprops = dict(color = "white", fontsize = 10),
        wedgeprops = dict(width = 0.6)
    )

    plt.savefig("pie_asistencia.png", bbox_inches = "tight", facecolor = "#37474f")
    plt.close()



def asistencia_semanal():
    """Permite obtener la asistencia semanal a traves de la base de datos"""

    conectar = conexion.conexion()
    cursor = conectar.cursor()

    cursor.execute("""
        SELECT a.Fecha, a.Estado, COUNT(*) AS Total
        FROM Asistencia a
        JOIN Empleados e ON a.ID_Empleado = e.ID_Empleado
        WHERE a.Fecha >= DATEADD(DAY, -6, CAST(GETDATE() AS DATE))
        AND e.Estado = 'Activo'
        GROUP BY a.Fecha, a.Estado
        ORDER BY a.Fecha
""")
    
    datos = cursor.fetchall()
    conectar.close()

    return datos


def generar_barchart():
    """Funcion que permite crear y madar el BarChart a vista_reportes""" 

    datos = asistencia_semanal()

    dias  = ["Lun", "Mar", "Mie", "Jue", "Vie"]  
    a_tiempo = [0, 0, 0, 0, 0]
    tardanza = [0, 0, 0, 0, 0]
    ausente = [0, 0, 0, 0, 0]

    for fila in datos:
        fecha, estado, total = fila
        dia_semana = fecha.weekday()

        if dia_semana > 4:
            continue

        if estado == "A tiempo":
            a_tiempo[dia_semana] = total
        
        elif estado == "Tardanza":
            tardanza[dia_semana] = total

        elif estado == "Ausente":
            ausente[dia_semana] = total

    fig, ax = plt.subplots(figsize = (5, 2.5))
    fig.patch.set_facecolor("#37474f")
    ax.set_facecolor("#37474f")

    x = range(5)
    w = 0.25

    ax.bar([i - w for i in x], a_tiempo, width = w, color = "#388e3c", label = "A tiempo")
    ax.bar([i     for i in x], tardanza, width = w, color = "#f57c00", label = "Tardanza")
    ax.bar([i + w for i in x], ausente, width = w, color = "#c62828", label = "Ausente")

    ax.set_xticks(list(x))
    ax.set_xticklabels(dias, color = "white", fontsize = 10)
    ax.tick_params(colors = "white")
    ax.spines["bottom"].set_color("#546e7a")
    ax.spines["left"].set_color("#546e7a")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.yaxis.label.set_color("white")
    ax.legend(facecolor = "#263238", labelcolor = "white", fontsize = 9)
    ax.yaxis.set_major_locator(plt.MaxNLocator(integer = True))
    ax.set_ylim(bottom = 0)

    plt.savefig("bar_asistencia.png", bbox_inches = "tight", facecolor = "#37474f")
    plt.close()

def no_activos():
    """Muestra la cantidad de empleados que estan inactivos o en licencia para no ser contados en la 
    vista de reportes"""

    conectar = conexion.conexion()
    cursor = conectar.cursor()

    cursor.execute(
        """SELECT 
                SUM(CASE WHEN Estado = 'Licencia' THEN 1 ELSE 0 END) AS Licencia,
                SUM(CASE WHEN Estado = 'Inactivo' THEN 1 ELSE 0 END) AS Inactivo
            FROM Empleados
            """)
    
    resultado = cursor.fetchone()
    conectar.close()

    return resultado