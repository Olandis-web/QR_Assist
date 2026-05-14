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


def insertar_usuario(nombres, apellidos, username, contrasena, rol):
    """Funcion que inserta informacion a la base de datos mediante el formularion de usuarios"""
    
    conectar = conexion.conexion()
    cursor = conectar.cursor()

    cursor.execute(
        "EXEC Inserta_Usuario ?, ?, ?, ?, ?",
        (nombres, apellidos, username, contrasena, rol)
    )

    conectar.commit()
    conectar.close()

    

def actualizar_usuario(id_usuario, nombres, apellidos, username, contrasena, rol):
    """Funcion que actualiza informacion a la base de datos mediante el formularion de usuarios"""

    conectar = conexion.conexion()
    cursor = conectar.cursor()

    cursor.execute("EXEC Actualiza_Usuario ?, ?, ?, ?, ?, ?",
                   (id_usuario, nombres, apellidos, username, contrasena, rol)
                   )

    conectar.commit()
    conectar.close()


def eliminar_usuario(id_usuario):
    """Funcion que elimina informacion a la base de datos mediante el formularion de usuarios"""
    
    conectar = conexion.conexion()
    cursor = conectar.cursor()

    cursor.execute("EXEC Elimina_Usuario ?",
                   (id_usuario,)
                   )
    conectar.commit()
    conectar.close()