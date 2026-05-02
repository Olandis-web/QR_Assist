import pyodbc

def conexion():
    """Funcion para aplicar la conexion con la base de datos.
    La idea no es solo crearla, sino que esta nos permita realizar acciones
    en el sistema"""

    try:
        conexion = pyodbc.connect(
            "DRIVER={ODBC Driver 17 for SQL Server};"\
            "SERVER=localhost;"\
            "DATABASE=qr_assist;"\
            "Trusted_Connection=Yes;"
    )
        print("Conexion exitosa")
        return conexion
    

    except pyodbc.Error as error:
        print("Error al conectar con la base de datos", error)
        return None

conexion()