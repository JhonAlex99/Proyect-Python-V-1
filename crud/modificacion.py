import sys
import os


ruta_conexion_bd = os.path.abspath(os.path.join(os.path.dirname(__file__),"..","conexion"))
sys.path.append(ruta_conexion_bd)
from conexion import obtener_conexion

def modificacion(tabla):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    #Clientes
    if tabla == "Clientes":
        codigo_cliente = input("Ingrese el código del cliente a modificar: ")
        nombre = input("Ingrese el nombre del cliente: ")
        apellido = input("Ingrese el apellido del cliente: ")
        codigo_postal = input("Modifique su código postal: ")
        cif_nie = input("Introduce tu Nif/Nie: ")
    

        sql = "UPDATE clientes SET nombre = %s, apellido = %s, codigo_postal = %s, cif_nie = %s WHERE codigo_cliente = %s"
        valores = (codigo_cliente,nombre, apellido, codigo_postal, cif_nie)
        cursor.execute(sql, valores)
        conexion.commit()
        print("Cliente modificado exitosamente.")
    #Codigo Postal
    if tabla == "Codigo Postal":
        codigo_de_codigo_postal = input("Escriba el código postal a modificar: ")
        descripcion = input("Escriba su nueva dirección: ")

        sql = "UPDATE codigo_postal SET descripcion = %s WHERE codigo = %s"
        valores = ( descripcion, codigo_de_codigo_postal)
        cursor.execute(sql, valores)
        conexion.commit()
        print("Código postal modificado exitosamente.")
    #Poblacion
    if tabla == "Poblacion":
        codigo_poblacion = input("Escriba el código de población a modificar: ")
        descripcion_poblacion = input("Escriba su nueva población: ")

        sql = "UPDATE poblaciones SET  descripcion = %s WHERE  codigo = %s"
        valores = (descripcion_poblacion, codigo_poblacion)
        cursor.execute(sql, valores)
        conexion.commit()
        print("Población modificada exitosamente.")
    #Provincias
    if tabla == "Provincias":
        
        codigo_provincia = input("Escriba el código de provincia a modificar: ")
        descripcion_provincia = input("Escriba su nueva provincia: ")

        sql = "UPDATE provincias SET descripcion = %s WHERE codigo = %s"
        valores = ( descripcion_provincia, codigo_provincia)
        cursor.execute(sql, valores)
        conexion.commit()
        print("Provincia modificada exitosamente.")
    #Entidades Bancarias
    if tabla == "Entidades Bancarias":
        codigo_banco = input("Ingrese el código del banco a modificar: ")
        iban = input("Escriba su nuevo número de cuenta: ")
        nombre_banco = input("Escriba su nuevo nombre del banco: ")
        swift = input("Escriba su nuevo código internacional: ")

        sql = "UPDATE bancos SET  iban = %s, nombre_banco = %s, swift_bci = %s WHERE codigo_banco = %s"
        valores = (iban, nombre_banco, swift, codigo_banco)
        cursor.execute(sql, valores)
        conexion.commit()
        print("Banco modificado exitosamente.")
    #Direccion de envío
    if tabla == "Direcciones de Envío":
        codigo_cliente_envio = input("Ingrese el código del cliente de la dirección de envío a modificar: ")
        direccion_envio = input("Modifique su dirección de envío: ")
        codigo_postal_envio = input("Modifique su código postal de envío: ")
        nombre_cliente_envio = input("Escriba el nombre de la persona que recibe su envío: ")
        poblacion_envio = input("Introduzca o modifque el código postal de su población")
        provincia_envio = input("Introduzca o Modifique los dos digitos de su provincia")

        sql = "UPDATE direccion_envio SET direccion_envio = %s, codigo_postal = %s, nombre_cliente = %s, poblacion = %s, provincia = %s WHERE codigo_cliente = %s"
        valores = (direccion_envio,codigo_postal_envio,nombre_cliente_envio,poblacion_envio,provincia_envio,codigo_cliente_envio)
        cursor.execute(sql, valores)
        conexion.commit()
        print("Dirección de envío modificada exitosamente.")

    cursor.close()
    conexion.close()
    input("Presione Enter para continuar...")