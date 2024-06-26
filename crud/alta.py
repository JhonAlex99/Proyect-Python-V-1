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
            nombre = input("Nombre : ")
            apellido = input("Apellido : ")
            codigo_postal = input("Código postal : ")
            cif_nie = input("Introduce tu NIF/NIE: ")
 

            sql = "INSERT INTO clientes (nombre, apellido, codigo_postal, cif_nie) VALUES ( %s, %s, %s, %s)"
            valores = (nombre, apellido,codigo_postal,cif_nie)
            cursor.execute(sql, valores)
            conexion.commit()
            print("Cliente agregado exitosamente.")

        # Tabla Código Postal
        if tabla == "Codigo Postal":
            codigo = input("Código postal: ")
            descripcion = input("Descripción: ")

            sql = "INSERT INTO codigo_postal (codigo, descripcion) VALUES (%s, %s)"
            val = (codigo, descripcion)
            cursor.execute(sql, val)
            conexion.commit()
            print("Datos introducidos correctamente.")

        # Tabla Población
        if tabla == "Poblacion":
            codigo = input("Código postal: ")
            descripcion = input("Descripción: ")

            sql = "INSERT INTO poblaciones (codigo, descripcion) VALUES (%s, %s)"
            val = (codigo, descripcion)
            cursor.execute(sql, val)
            conexion.commit()
            print("Datos introducidos correctamente.")

        # Tabla Provincias
        if tabla == "Provincias":
            codigo = input("Codigo de provincia: ")
            descripcion = input("Descripción: ")

            sql = "INSERT INTO provincias (codigo, descripcion) VALUES (%s, %s)"
            val = (codigo, descripcion)
            cursor.execute(sql, val)
            conexion.commit()
            print("Datos introducidos correctamente.")

        # Tabla Banco
        if tabla == "Entidades Bancarias":
            codigo_banco = input("Código de su banco: ")
            iban = input("Número de cuenta: ")
            nombre_banco = input("Nombre banco: ")
            swift_bci = input("Código internacional: ")

            sql_update = "UPDATE bancos SET por_defecto = 0 WHERE codigo_banco = %s"
            cursor.execute(sql_update, (codigo_banco,))

            sql = "INSERT INTO bancos (codigo_banco , iban, nombre_banco, swift_bci, por_defecto) VALUES (%s, %s, %s, %s, %s)"
            val = (codigo_banco,iban,nombre_banco, swift_bci, 1)
            cursor.execute(sql, val)
            conexion.commit()
            print("Datos introducidos correctamente.")

        # Tabla Dirección Envío
        if tabla == "Direcciones de Envío":
            codigo_cliente_de_envio = input("Código de cliente : ")
            direccion_envio = input("Dirección de envío: ")
            codigo_postal_de_envio = input("Código postal de envío: ")
            nombre_cliente = input("Nombre Cliente: ")
            poblacion_envio = input("Ingrese sus digitos de poblacion de envío: ")
            provincia_envio = input("Ingrese sus digitos de provincia de envío: ")

              # Establecer todas las direcciones anteriores del cliente a por_defecto = 0
            sql_update = "UPDATE direccion_envio SET por_defecto = 0 WHERE codigo_cliente = %s"
            cursor.execute(sql_update, (codigo_cliente_de_envio,))

    # Insertar la nueva dirección con por_defecto = 1

            sql = "INSERT INTO direccion_envio (codigo_cliente, direccion_envio, codigo_postal, nombre_cliente, poblacion, provincia, por_defecto) VALUES (%s, %s, %s , %s , %s , %s, %s)"
            val = (codigo_cliente_de_envio, direccion_envio, codigo_postal_de_envio,nombre_cliente,poblacion_envio,provincia_envio,1)
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
