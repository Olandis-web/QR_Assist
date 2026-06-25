import pyodbc
from database import conexion


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
        SELECT COUNT(*) FROM Asistencia
        WHERE Fecha = CAST(GETDATE() AS DATE)
        AND Estado IN ('A tiempo', 'Tardanza')
    """)

    total = cursor.fetchone()[0]
    conectar.close()
    return total


def tardanzas():
    """Retorna la cantidad de tardanzas registradas hoy"""

    conectar = conexion.conexion()
    cursor = conectar.cursor()

    cursor.execute("""
        SELECT COUNT(*) FROM Asistencia
        WHERE Fecha = CAST(GETDATE() AS DATE)
        AND Estado = 'Tardanza'
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
    conectar = conexion.conexion()
    cursor = conectar.cursor()
    cursor.execute("""
        SELECT TOP 5
            e.Nombres, e.Apellidos,
            COUNT(*) AS Dias_a_tiempo
        FROM Asistencia a
        JOIN Empleados e ON a.ID_Empleado = e.ID_Empleado
        WHERE a.Estado = 'A tiempo'
        AND MONTH(a.Fecha) = MONTH(GETDATE())
        AND YEAR(a.Fecha) = YEAR(GETDATE())
        GROUP BY e.Nombres, e.Apellidos
        ORDER BY Dias_a_tiempo DESC
    """)
    datos = cursor.fetchall()
    conectar.close()
    return datos


def top_incidencias():
    conectar = conexion.conexion()
    cursor = conectar.cursor()
    cursor.execute("""
        SELECT TOP 5
            e.Nombres, e.Apellidos,
            COUNT(*) AS Total_incidencias
        FROM Asistencia a
        JOIN Empleados e ON a.ID_Empleado = e.ID_Empleado
        WHERE a.Estado IN ('Tardanza', 'Ausente')
        AND MONTH(a.Fecha) = MONTH(GETDATE())
        AND YEAR(a.Fecha) = YEAR(GETDATE())
        GROUP BY e.Nombres, e.Apellidos
        ORDER BY Total_incidencias DESC
    """)
    datos = cursor.fetchall()
    conectar.close()
    return datos
