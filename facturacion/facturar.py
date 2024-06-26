from datetime import datetime
import decimal
import sys
import os
from conexion import cerrar, obtener_conexion

def obtener_datos_empresa():
    conexion = obtener_conexion()
    cursor = conexion.cursor(buffered=True)
    sql = """
        SELECT e.nombre_vendedor, e.apellidos_vendedor, p.descripcion, pr.descripcion, e.cif_nie_vendedor, e.codigo_postal_empresa, e.codigo_banco
        FROM empresa e
        JOIN poblaciones p ON e.codigo_poblacion = p.codigo
        JOIN provincias pr ON e.codigo_provincia = pr.codigo
    """
    cursor.execute(sql)
    resultado = cursor.fetchall()
    cursor.close()
    conexion.close()
    for empresa in resultado:
        return {
            "nombre_vendedor": empresa[0],
            "apellidos_vendedor": empresa[1],
            "poblacion": empresa[2],
            "provincia": empresa[3],
            "cif_nie_vendedor": empresa[4],
            "codigo_postal_empresa": empresa[5],
            "codigo_banco": empresa[6],
        }

def obtener_datos_cliente(codigo_cliente):
    conexion = obtener_conexion()
    cursor = conexion.cursor(buffered=True)
    sql = """
        SELECT c.nombre, c.apellido, p.descripcion, c.cif_nie
        FROM clientes c
        JOIN poblaciones p ON c.codigo_postal = p.codigo
        WHERE c.codigo_cliente = %s
    """
    cursor.execute(sql, (codigo_cliente,))
    resultado = cursor.fetchone()
    cursor.close()
    conexion.close()
    if resultado:
        return {
            "nombre": resultado[0],
            "apellido": resultado[1],
            "poblacion": resultado[2],
            "cif_nie": resultado[3]
        }
    else:
        print(f"Cliente con código {codigo_cliente} no encontrado.")
        return None

def obtener_precio_unitario_y_nombre(producto):
    conexion = obtener_conexion()
    cursor = conexion.cursor(buffered=True)
    sql = "SELECT nombre_producto, valor_producto FROM productos WHERE codigo_producto = %s"
    cursor.execute(sql, (producto,))
    resultado = cursor.fetchone()
    cursor.close()
    conexion.close()
    if resultado and len(resultado) == 2:
        return {
            "nombre_producto": resultado[0],
            "precio_unitario": decimal.Decimal(resultado[1])
        }
    else:
        return None

def obtener_datos_productos():
    productos = []
    while True:
        producto = input("Ingrese el código del producto (o 'fin' para terminar): ")
        if producto.lower() == 'fin':
            break
        cantidad = int(input(f"Ingrese la cantidad de {producto}: "))
        datos_producto = obtener_precio_unitario_y_nombre(producto)
        if datos_producto is None:
            print(f"El producto '{producto}' no se encontró en la base de datos.")
            continue
        total = cantidad * datos_producto["precio_unitario"]
        productos.append({
            "codigo_producto": producto,
            "nombre_producto": datos_producto["nombre_producto"],
            "cantidad": cantidad,
            "precio_unitario": datos_producto["precio_unitario"],
            "total": total
        })
    return productos

def calcular_total_general(productos):
    total_general = sum(producto['total'] for producto in productos)
    iva = decimal.Decimal("1.21")  # 21% IVA
    return total_general, total_general * iva

def obtener_numero_factura():
    conexion = obtener_conexion()
    cursor = conexion.cursor(buffered=True)
    sql = "SELECT MAX(numero_factura) FROM cabecera, lineas"
    cursor.execute(sql)
    resultado = cursor.fetchone()
    cursor.close()
    conexion.close()
    if resultado[0] is not None:
        return resultado[0] + 1
    else:
        return 1

def obtener_codigo_banco():
    conexion = obtener_conexion()
    cursor = conexion.cursor(buffered=True)
    sql = "SELECT codigo_banco, iban, nombre_banco, swift_bci FROM bancos WHERE por_defecto = 1"
    cursor.execute(sql)
    resultado = cursor.fetchone()
    cursor.close()
    conexion.close()
    if resultado:
        return {
            "codigo_banco": resultado[0],
            "iban": resultado[1],
            "nombre_banco": resultado[2],
            "swift_bci": resultado[3]
        }
    else:
        print("No se encontró ningún banco en la base de datos.")
        return None

def obtener_datos_envio(codigo_cliente=None):
    conexion = obtener_conexion()
    cursor = conexion.cursor(buffered=True)

    if codigo_cliente:
        sql = """
            SELECT direccion_envio, codigo_postal, nombre_cliente, poblacion, provincia
            FROM direccion_envio
            WHERE por_defecto = '1' AND codigo_cliente = %s
        """
        cursor.execute(sql, (codigo_cliente,))
    else:
        sql = """
            SELECT direccion_envio, codigo_postal, nombre_cliente, poblacion, provincia
            FROM direccion_envio
            WHERE por_defecto = '1'
        """
        cursor.execute(sql)

    resultado = cursor.fetchone()  # Obtener solo una fila de resultado

    cursor.close()
    conexion.close()

    if resultado:
        return {
            "direccion_envio": resultado[0],
            "codigo_postal": resultado[1],
            "nombre_cliente": resultado[2],
            "poblacion": resultado[3],
            "provincia": resultado[4]
        }
    else:
        if codigo_cliente:
            print(f"No se encontró dirección de envío para el cliente con código {codigo_cliente}.")
        else:
            print("No se encontró dirección de envío por defecto en la base de datos.")
        return None

def guardar_factura(cabecera, lineas):
    conexion = obtener_conexion()
    cursor = conexion.cursor()

    sql_cabecera = """
        INSERT INTO cabecera (numero_factura, codigo_cliente, codigo_postal, nombre_cliente, poblacion_cliente, provincia_cliente, fecha, importe_producto, total_factura, iban, nombre_banco,
        nombre_vendedor, apellidos_vendedor, poblacion_empresa, provincia_empresa, cif_nie_vendedor, codigo_postal_empresa, codigo_banco, swift_bci, direccion_envio, codigo_postal_envio, nombre_cliente_envio, poblacion_envio, provincia_envio)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    cursor.execute(sql_cabecera, (
        cabecera["numero_factura"], cabecera["codigo_cliente"], cabecera["codigo_postal"], cabecera["nombre_cliente"], cabecera["poblacion_cliente"], cabecera["provincia_cliente"], cabecera["fecha"], cabecera["importe_producto"], cabecera["total_factura"],
        cabecera["iban"], cabecera["nombre_banco"], cabecera["nombre_vendedor"], cabecera["apellidos_vendedor"], cabecera["poblacion_empresa"], cabecera["provincia_empresa"],
        cabecera["cif_nie_vendedor"], cabecera["codigo_postal_empresa"], cabecera["codigo_banco"], cabecera["swift_bci"],cabecera["direccion_envio"], cabecera["codigo_postal_envio"],
        cabecera["nombre_cliente_envio"],cabecera["poblacion_envio"],cabecera["provincia_envio"]
    ))

    sql_lineas = """
        INSERT INTO lineas ( numero_factura_lineas, codigo_producto, cantidad, nombre_producto_lineas, valor_producto_lineas, total_producto, iva)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """
   
    numero_factura_insertado = cursor.lastrowid

    for linea in lineas:
        cursor.execute(sql_lineas, (
            cabecera["numero_factura"],  # Usamos el número de factura insertado en cabecera
            linea["codigo_producto"],
            linea["cantidad"],
            linea["nombre_producto"],
            linea["precio_unitario"],
            linea["total"],
            21
        ))

    conexion.commit()
    cursor.close()
    conexion.close()
    return numero_factura_insertado

def facturar1():
    
    datos_empresa = obtener_datos_empresa()
    codigo_banco = obtener_codigo_banco()
    if not codigo_banco:
        return  # Si no se encuentra ningún banco, termina la ejecución
        
    codigo_cliente = input("Introduce el código del cliente: ")
    datos_cliente = obtener_datos_cliente(codigo_cliente)
    if datos_cliente is None:
        return  # Si el cliente no se encuentra, termina la ejecución
    
    datos_envio = obtener_datos_envio(codigo_cliente)

    fecha_factura = datetime.now().strftime("%Y-%m-%d")
    productos = obtener_datos_productos()
    if not productos:
        print("No se han añadido productos.")
        return  # Si no se han añadido productos, termina la ejecución

    total_general, total_con_iva = calcular_total_general(productos)
    numero_factura = obtener_numero_factura()

   

    cabecera = {
        "numero_factura": numero_factura,
        "codigo_cliente": codigo_cliente,
        "codigo_postal": datos_cliente["poblacion"],
        "nombre_cliente": datos_cliente["nombre"],
        "poblacion_cliente": datos_cliente["poblacion"],
        "provincia_cliente": datos_cliente["poblacion"],
        "fecha": fecha_factura,
        "importe_producto": total_general,
        "total_factura": total_con_iva,
        "iban": codigo_banco["iban"],  
        "nombre_banco": codigo_banco["nombre_banco"],  
        "nombre_vendedor": datos_empresa["nombre_vendedor"],
        "apellidos_vendedor": datos_empresa["apellidos_vendedor"],
        "poblacion_empresa": datos_empresa["poblacion"],
        "provincia_empresa": datos_empresa["provincia"],
        "cif_nie_vendedor": datos_empresa["cif_nie_vendedor"],
        "codigo_postal_empresa": datos_empresa["codigo_postal_empresa"],
        "codigo_banco": codigo_banco["codigo_banco"],
        "swift_bci" : codigo_banco["swift_bci"],
        "direccion_envio" : datos_envio["direccion_envio"],
        "codigo_postal_envio" : datos_envio["codigo_postal"],
        "nombre_cliente_envio" : datos_envio["nombre_cliente"],
        "poblacion_envio" : datos_envio["poblacion"],
        "provincia_envio" : datos_envio["provincia"],
    }
    


    guardar_factura(cabecera, productos)

    print("\n--- FACTURA ---")
    print(f"Fecha: {fecha_factura}\n")
    print("Datos de la Empresa:")
    for key, value in datos_empresa.items():
        print(f"{key}: {value}")

    print("\nDatos del Cliente:")
    for key, value in datos_cliente.items():
        print(f"{key}: {value}")

    print("\nDatos del Envio:")
    for key, value in datos_envio.items():
        print(f"{key}: {value}")

    print("\nLíneas de Factura:")
    for producto in productos:
        print(f"Producto: {producto['nombre_producto']}, Cantidad: {producto['cantidad']}, Precio Unitario: {producto['precio_unitario']:.2f}, Total: {producto['total']:.2f}")

    print(f"\nTotal General: {total_general:.2f}")
    print(f"Total con IVA (21%): {total_con_iva:.2f}")

    print(f"\nEl ID de tu compra es: {numero_factura}")

    input("\nPresione Enter para continuar...")

# Ejecutar la función principal
if __name__ == "__main__":
    facturar1()
