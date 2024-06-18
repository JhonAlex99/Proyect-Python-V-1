import sys
import os

ruta_conexion_bd = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "conexion"))
sys.path.append(ruta_conexion_bd)

from conexion import cerrar, obtener_conexion

def alta(tabla):
    conexion = obtener_conexion()
    print(f"Valor de tabla, {tabla}")
    if conexion is None:
        print("No se pudo establecer la conexión a la base de datos.")
        return

    try:
        cursor = conexion.cursor()

        # Tabla Clientes
        if tabla == "Clientes":
            nombre = input("Ingrese el nombre del cliente: ")
            apellido = input("Ingrese el apellido del cliente: ")
            codigo_postal = input("Introduce tu código postal: ")
            cif_nie = input("Introduce tu NIF/NIE: ")
 

            sql = "INSERT INTO clientes (nombre, apellido, codigo_postal, cif_nie) VALUES ( %s, %s, %s, %s)"
            valores = (nombre, apellido,codigo_postal,cif_nie)
            cursor.execute(sql, valores)
            conexion.commit()
            print("Cliente agregado exitosamente.")

        # Tabla Código Postal
        if tabla == "Codigo Postal":
            codigo = input("Escriba un código postal: ")
            descripcion = input("Escriba una descripción: ")

            sql = "INSERT INTO codigo_postal (codigo, descripcion) VALUES (%s, %s)"
            val = (codigo, descripcion)
            cursor.execute(sql, val)
            conexion.commit()
            print("Datos introducidos correctamente.")

        # Tabla Población
        if tabla == "Poblacion":
            codigo = input("Escriba un código postal: ")
            descripcion = input("Escriba una descripción: ")

            sql = "INSERT INTO poblaciones (codigo, descripcion) VALUES (%s, %s)"
            val = (codigo, descripcion)
            cursor.execute(sql, val)
            conexion.commit()
            print("Datos introducidos correctamente.")

        # Tabla Provincias
        if tabla == "Provincias":
            codigo = input("Codigo de provincia: ")
            descripcion = input("Escriba una descripción: ")

            sql = "INSERT INTO provincias (codigo, descripcion) VALUES (%s, %s)"
            val = (codigo, descripcion)
            cursor.execute(sql, val)
            conexion.commit()
            print("Datos introducidos correctamente.")

        # Tabla Banco
        if tabla == "Entidades Bancarias":
            codigo_banco = input("escriba el codigo de su banco: ")
            iban = input("Escriba el número de cuenta: ")
            nombre_banco = input("Introduce el nombre de tu banco: ")
            swift_bci = input("Escriba el código internacional: ")

            sql = "INSERT INTO bancos (codigo_banco , iban, nombre_banco, swift_bci) VALUES (%s, %s, %s, %s)"
            val = (codigo_banco,iban,nombre_banco, swift_bci)
            cursor.execute(sql, val)
            conexion.commit()
            print("Datos introducidos correctamente.")

        # Tabla Dirección Envío
        if tabla == "Direcciones de Envío":
            codigo_cliente_de_envio = input("Escriba el código de cliente : ")
            direccion_envio = input("Escriba la dirección de envío: ")
            codigo_postal_de_envio = input("Escriba el código postal de envío: ")
            nombre_cliente = input("Nombre Cliente: ")
            poblacion_envio = input("Ingrese sus digitos de poblacion de envío: ")
            provincia_envio = input("Ingrese sus digitos de provincia de envío: ")

            sql = "INSERT INTO direccion_envio (codigo_cliente, direccion_envio, codigo_postal, nombre_cliente, poblacion, provincia) VALUES (%s, %s, %s , %s , %s , %s)"
            val = (codigo_cliente_de_envio, direccion_envio, codigo_postal_de_envio,nombre_cliente,poblacion_envio,provincia_envio)
            cursor.execute(sql, val)
            conexion.commit()
            print("Datos introducidos correctamente.")

    except Exception as e:
        print("Error al insertar datos: ", e)
    finally:
        cursor.close()
        cerrar(conexion)

if __name__ == "__main__":
    tabla = input("Seleccione la tabla en la que desea insertar datos: \n1. Clientes\n2. Codigo Postal\n3. Poblacion\n4. Provincias\n5. Banco\n6. Dirección de envio\n")
    alta(tabla)
