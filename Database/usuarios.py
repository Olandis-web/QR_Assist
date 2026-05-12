import pyodbc
from database import conexion

def obtener_datos():
    """Esta funcion muestra la informacion de la base de datos en la tabla"""

    conectar = conexion.conexion()
    cursor = conectar.cursor()
    
    cursor.execute("Select Distinct * from Usuarios")

    datos = cursor.fetchall()
    
    conectar.close()

    return datos