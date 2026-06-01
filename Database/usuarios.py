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


def insertar_usuario(id_empleado, nombres, apellidos, username, contrasena, rol):
    """Funcion que inserta informacion a la base de datos mediante el formularion de usuarios"""
    
    conectar = conexion.conexion()
    cursor = conectar.cursor()

    cursor.execute(
        "EXEC Inserta_Usuario ?, ?, ?, ?, ?, ?",
        (id_empleado, nombres, apellidos, username, contrasena, rol)
    )

    conectar.commit()
    conectar.close()

    

def actualizar_usuario(id_usuario,id_empleado, nombres, apellidos, username, contrasena, rol):
    """Funcion que actualiza informacion a la base de datos mediante el formularion de usuarios"""

    conectar = conexion.conexion()
    cursor = conectar.cursor()

    cursor.execute("EXEC Actualiza_Usuario ?, ?, ?, ?, ?, ?, ?",
                   (id_usuario, id_empleado, nombres, apellidos, username, contrasena, rol)
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

def validar(username, contrasena):
    """Funcion para validar el inicion de sesion de los usuarios"""

    conectar = conexion.conexion()
    cursor = conectar.cursor()

    cursor.execute("""Select * FROM Usuarios 
                   Where Username = ? 
                   AND Contraseña = ?""",

                   (username, contrasena)
                )
    
    usuario = cursor.fetchone()
    conectar.close()

    return usuario

def verifica_usuario(id_empleado):
    """Verifica si un empleado ya es un usuario"""

    conectar = conexion.conexion()
    cursor = conectar.cursor()

    cursor.execute("Select * from usuarios WHERE ID_Empleado = ?",(id_empleado,))

    resultado = cursor.fetchone()
    conectar.close()

    return resultado
    