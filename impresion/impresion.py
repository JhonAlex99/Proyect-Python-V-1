import mysql.connector
import sys
import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib.units import inch

# Ajustar la ruta para la conexión a la base de datos
ruta_conexion_bd = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "conexion"))
sys.path.append(ruta_conexion_bd)
from conexion import obtener_conexion, cerrar

def imprimir(numero_factura):
    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)

    # Consulta de cabecera
    sql_cabecera = "SELECT * FROM cabecera WHERE numero_factura = %s"
    cursor.execute(sql_cabecera, (numero_factura,))
    cabecera = cursor.fetchone()

    # Consulta de líneas
    sql_lineas = "SELECT * FROM lineas WHERE numero_factura_lineas = %s"
    cursor.execute(sql_lineas, (numero_factura,))
    lineas = cursor.fetchall()

    cursor.close()
    conexion.close()

    return cabecera, lineas

# Función para calcular el IVA de 21.0%
def calcular_iva(lineas):
    total_iva = 0
    for linea in lineas:
        if linea['iva'] == 21.0:
            total_iva += linea['total_producto'] * (linea['iva'] / 100)
    return total_iva

# Función para generar el PDF
def generar_pdf(cabecera, lineas, numero_factura):
    pdf_filename = f"factura_{numero_factura}.pdf"
    doc = SimpleDocTemplate(pdf_filename, pagesize=letter)
    elements = []

    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name='CenteredTitle', alignment=1, fontSize=20, spaceAfter=20))
    styles.add(ParagraphStyle(name='LeftAligned', alignment=0, fontSize=12, spaceAfter=0))
    styles.add(ParagraphStyle(name='RightAligned', alignment=2, fontSize=12, spaceAfter=0))
    styles.add(ParagraphStyle(name='Justified', alignment=4, fontSize=12, spaceAfter=0))
    styles.add(ParagraphStyle('SmallLeading', parent=styles['LeftAligned'], leading=10))

    # Ruta del logo de la empresa
    logo_path = "./impresion/onizea_logo.jpg"  # Cambia esta ruta a la del logo de tu empresa

    # Intentar agregar el logo, si no está disponible, omitir
    if os.path.exists(logo_path):
        elements.append(Image(logo_path, width=1*inch, height=1*inch, hAlign='RIGHT'))
    else:
        print(f"Advertencia: No se encontró el logo en {logo_path}")

    # Título
    elements.append(Paragraph("Factura", styles['CenteredTitle']))

    
    # Información de la empresa y factura
    empresa_info = [
        [Paragraph(f"Nombre: {cabecera['nombre_vendedor']}", styles['SmallLeading']),
         Paragraph(f"Nº DE FACTURA: {numero_factura}", styles['RightAligned'])],
        [Paragraph(f"Población: {cabecera['poblacion_empresa']}", styles['SmallLeading']),
         Paragraph(f"FECHA: {cabecera['fecha']}", styles['RightAligned'])],
        [Paragraph(f"Provincia: {cabecera['provincia_empresa']}", styles['SmallLeading']), ''],
        [Paragraph(f"Código Postal: {cabecera['codigo_postal_empresa']}", styles['SmallLeading']), ''],

    ]
    # Lista completa con el título y los datos
    table_empresa = Table(empresa_info, colWidths=[3.5*inch, 3.5*inch])
    elements.append(table_empresa)
    elements.append(Spacer(1, 12))

    # Información del cliente y dirección de envío
    cliente_info = [
        [Paragraph(f"Nombre: {cabecera['nombre_cliente']}", styles['SmallLeading']),
         Paragraph(f"Nombre: {cabecera['nombre_cliente_envio']}", styles['SmallLeading'])],
        [Paragraph(f"Dirección: {cabecera['direccion_envio']}", styles['SmallLeading'])],
        [Paragraph(f"Código Postal: {cabecera['codigo_postal']}", styles['SmallLeading']),
         Paragraph(f"Código Postal: {cabecera['codigo_postal_envio']}", styles['SmallLeading'])],
        [Paragraph(f"Población: {cabecera['poblacion_cliente']}", styles['SmallLeading']),
         Paragraph(f"Población: {cabecera['poblacion_envio']}", styles['SmallLeading'])],
        [Paragraph(f"Provincia: {cabecera['provincia_cliente']}", styles['SmallLeading']),
         Paragraph(f"Provincia: {cabecera['provincia_envio']}", styles['SmallLeading'])]
    ]
    table_cliente = Table(cliente_info, colWidths=[3.5*inch, 3.5*inch])
    elements.append(table_cliente)
    elements.append(Spacer(1, 12))

     # Detalles de la línea
    line_headers = ["CÓDIGO PRODUCTO", "CANT.", "DESCRIPCIÓN", "PRECIO UNITARIO", "IMPORTE"]
    line_data = [line_headers] + [[linea['codigo_producto'], linea['cantidad'], linea['nombre_producto_lineas'], linea['valor_producto_lineas'], linea['total_producto']] for linea in lineas]
    line_table = Table(line_data, hAlign='CENTER', colWidths=[2*inch, 1*inch, 1.5*inch, 1.5*inch, 1.5*inch])
    line_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.lightgrey),
        ('ALIGN', (0,0), (-1,0), 'CENTER'),
        ('ALIGN', (3,1), (-1,-1), 'RIGHT'),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('TEXTCOLOR', (0,0), (-1,0), colors.black),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0,0), (-1,0), 12),
        ('GRID', (0,0), (-1,-1), 1, colors.black),
        ('MARGIN',(1,1),(2,4),'LEFT')
    ]))
    elements.append(line_table)
    elements.append(Spacer(1, 12))

    # Calcular el IVA de 21.0%
    total_iva_21 = calcular_iva(lineas)

    # Subtotal, IVA y Total
    elements.append(Paragraph(f"Subtotal: {cabecera['importe_producto']}", styles['RightAligned']))
    elements.append(Paragraph(f"IVA 21.0%: {total_iva_21:.2f}", styles['RightAligned']))
    elements.append(Paragraph(f"TOTAL: {cabecera['total_factura']}", styles['RightAligned']))

    elements.append(Spacer(1, 20))

    # Firma
    elements.append(Paragraph("Firma:", styles['Normal']))
    elements.append(Spacer(1, 40))

    # Condiciones y forma de pago
    payment_conditions = [
        "CONDICIONES Y FORMA DE PAGO",
        "El pago se realizará en un plazo de 15 días",
        f"Banco: {cabecera['nombre_banco']}",
        f"IBAN: {cabecera['iban']}",
        f"SWIFT/BIC: {cabecera['swift_bci']}"
    ]
    for condition in payment_conditions:
        elements.append(Paragraph(condition, styles['Normal']))

    doc.build(elements)
    print(f"PDF generado: {pdf_filename}")

# Uso del script
if __name__ == "__main__":
    numero_factura = input("Introduce el número de factura: ")
    cabecera, lineas = imprimir(numero_factura)
    generar_pdf(cabecera, lineas, numero_factura)
