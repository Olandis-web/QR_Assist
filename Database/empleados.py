import pyodbc
from database import conexion

def obtener_datos():
    """Esta funcion muestra la informacion de la base de datos en la tabla"""

    conectar = conexion.conexion()
    cursor = conectar.cursor()
    
    cursor.execute("Select * from Empleados")

    datos = cursor.fetchall()
    
    conectar.close()

    return datos

def insertar_empleado(nombres, apellidos, cargo, estado, qr=None):
    """Funcion que inserta informacion a la base de datos mediante el formularion de empleados"""
    
    conectar = conexion.conexion()
    cursor = conectar.cursor()

    cursor.execute(
        "EXEC inserta_empleado ?, ?, ?, ?, ?",
        (nombres, apellidos, cargo, qr, estado)
    )

    conectar.commit()
    conectar.close()

    

def actualizar_empleado(id_empleado, nombres, apellidos, cargo, estado, qr=None):
    """Funcion que actualiza informacion a la base de datos mediante el formularion de empleados"""

    conectar = conexion.conexion()
    cursor = conectar.cursor()

    cursor.execute("EXEC actualiza_empleado ?, ?, ?, ?, ?, ?",
                   (id_empleado, nombres, apellidos, cargo, qr, estado)
                   )

    conectar.commit()
    conectar.close()


def eliminar_empleado(id_empleado):
    """Funcion que elimina informacion a la base de datos mediante el formularion de empleados"""
    
    conectar = conexion.conexion()
    cursor = conectar.cursor()

    cursor.execute("EXEC elimina_empleado ?",
                   (id_empleado,)
                   )
    conectar.commit()
    conectar.close()


def buscar_empleado(id_empleado):
    """Funcion que busca un empleado por su ID para mostrar su nombre al leer el QR"""
        
    conectar = conexion.conexion()
    cursor = conectar.cursor()
            
    cursor.execute("""
         SELECT Nombres, Apellidos
         FROM Empleados
         WHERE ID_Empleado = ?      
         """, (id_empleado,))
    empleado = cursor.fetchone()
    conectar.close()
    return empleado

  