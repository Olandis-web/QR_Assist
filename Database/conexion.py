import pyodbc


class DatabaseConnectionError(ConnectionError):
    """Indica que no fue posible abrir la conexión a SQL Server."""


def conexion():
    """Funcion para aplicar la conexion con la base de datos.
    La idea no es solo crearla, sino que esta nos permita realizar acciones
    en el sistema"""

    try:
        conexion = pyodbc.connect(
            "DRIVER={ODBC Driver 18 for SQL Server};"\
            "SERVER=localhost;"\
            "DATABASE=qr_assist;"\
            "UID=SA;"\
            "PWD=QrAssist2024!;"\
            "TrustServerCertificate=Yes;"
    )
        print("Conexion exitosa")
        return conexion
    

    except pyodbc.Error as error:
        # No devolver None: los consumidores necesitan una conexión válida y,
        # de lo contrario, fallan después con el poco útil error de .cursor().
        raise DatabaseConnectionError(
            "No se pudo conectar a la base de datos 'qr_assist'. "
            "Verifique que SQL Server esté en ejecución y que el servidor, "
            "las credenciales y el controlador ODBC estén configurados correctamente."
        ) from error
