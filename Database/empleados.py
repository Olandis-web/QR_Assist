import pyodbc
import qrcode
import tempfile
import os
import time
from PIL import Image, ImageDraw, ImageFont
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

def buscar_por_qr(qr):
    """Busca un empleado por su codigo QR en camara"""

    conectar = conexion.conexion()
    cursor = conectar.cursor()

    cursor.execute(
        """SELECT ID_Empleado, Nombres, Apellidos
        FROM Empleados
        WHERE Codigo_qr = ?""", (qr,)
    )

    resultado = cursor.fetchone()
    conectar.close()
    return resultado

def temporal_qr(codigo, empleado):
    """Genera un QR temporal, lo imprime y elimina el archivo"""

    qr = qrcode.make(codigo).resize((180, 180))
    
    carnet = Image.new("RGB", (700, 380), "white")
    draw = ImageDraw.Draw(carnet)

    azul = (30, 60, 120)

    draw.rectangle((0, 0, 700, 70), fill = azul)
    titulo = ImageFont.load_default()
    fuente = ImageFont.load_default()

    draw.text(
        (20, 25),
        "QR ASSIST",
        fill = "white",
        font = titulo
    )

    carnet.paste(qr, (30, 110))

    draw.text(
        (250, 120),
        f"Nombre: {empleado[1]} {empleado[2]}",
        fill = "black",
        font = fuente
    )

    draw.text(
        (250, 170),
        f"Cargo: {empleado[3]}",
        fill = "black",
        font = fuente
    )

    draw.text(
        (250, 220),
        f"ID: {empleado[0]}",
        fill = "black",
        font = fuente
    )

    archivo = os.path.join(
        tempfile.gettempdir(),
        f"carnet_{empleado[0]}.png"
    )

    carnet.save(archivo)
    os.startfile(archivo, "print")
    time.sleep(5)

    if os.path.exists(archivo):
        os.remove(archivo)
    

  