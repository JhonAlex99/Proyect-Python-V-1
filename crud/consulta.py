import sys
import os


ruta_conexion_bd = os.path.abspath(os.path.join(os.path.dirname(__file__),"..","conexion"))
sys.path.append(ruta_conexion_bd)
from conexion import obtener_conexion


def consultas(tabla):
    conexion = obtener_conexion()
    if conexion is None:
        print("No se pudo establecer la conexión a la base de datos.")
        return
    
    try:
        cursor = conexion.cursor()
 
    # Tabla Clientes
        if tabla == "Clientes":
            sql = "SELECT * FROM clientes"
            cursor.execute(sql)
            resultado = cursor.fetchall()
            for cliente in resultado:
                print(f"Código Cliente: {cliente[0]}, Nombre: {cliente[1]}, Apellido: {cliente[2]}, Código Postal: {cliente[3]}, CIF o NIE: {cliente[4]}")
    
    # Tabla Código Postal
        if tabla == "Codigo Postal":
            sql = "SELECT * FROM codigo_postal"
            cursor.execute(sql)
            resultado = cursor.fetchall()
            for codigopostal in resultado:
                print(f"Código-Postal: {codigopostal[0]}, Provincia: {codigopostal[1]}")
    
    # Tabla Población
        if tabla == "Poblacion":
            sql = "SELECT * FROM poblaciones"
            cursor.execute(sql)
            resultado = cursor.fetchall()
            for poblacion in resultado:
                print(f"Código-Postal: {poblacion[0]}, Población: {poblacion[1]}")

    # Tabla Provincias
        if tabla == "Provincias":
            sql = "SELECT * FROM provincias"
            cursor.execute(sql)
            resultado = cursor.fetchall()
            for provincia in resultado:
                print(f"Código de Provincia: {provincia[0]}, Provincia: {provincia[1]}")
    
    # Tabla Banco
        if tabla == "Entidades Bancarias":
            sql = "SELECT * FROM bancos"
            cursor.execute(sql)
            resultado = cursor.fetchall()
            for banco in resultado:
                print(f"Código del banco: {banco[0]}, IBAN: {banco[1]}, Nombre del Banco: {banco[2]}, SWIFT-BCI: {banco[3]}")

    # Tabla Dirección Envío
        if tabla == "Direcciones de Envío":
            sql = "SELECT * FROM direccion_envio"
            cursor.execute(sql)
            resultado = cursor.fetchall()
            for direccion in resultado:
                print(f"Código Cliente: {direccion[0]}, Dirección de Envío: {direccion[1]}, Código Postal: {direccion[2]}, Nombre del Cliente: {direccion[3]}, Código-Población: {direccion[4]}, Código-Provincia: {direccion[5]}")

    except Exception as e:
        print("Error al consultar datos: ", e)
    finally:
        cursor.close()
        conexion.close()
    input("Presione Enter para continuar...")
