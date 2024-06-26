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
    styles.add(ParagraphStyle(name='LeftAligned', alignment=0, fontSize=12, spaceAfter=12))
    styles.add(ParagraphStyle(name='RightAligned', alignment=2, fontSize=12, spaceAfter=12))

    # Ruta del logo de la empresa
    logo_path = "ruta/al/logo.png"  # Cambia esta ruta a la del logo de tu empresa

    # Intentar agregar el logo, si no está disponible, omitir
    if os.path.exists(logo_path):
        elements.append(Image(logo_path, width=2*inch, height=2*inch))
    else:
        print(f"Advertencia: No se encontró el logo en {logo_path}")

    # Título
    elements.append(Paragraph("Factura", styles['CenteredTitle']))

    # Información de la cabecera
    header_table_data = [
        ["DE", "", "Nº DE FACTURA", cabecera['numero_factura']],
        [cabecera['nombre_vendedor'], cabecera['fecha']],
        [cabecera['poblacion_empresa'], cabecera['cif_nie_vendedor']],
        [cabecera['provincia_empresa'],  cabecera['codigo_postal_empresa']]
    ]
    header_table = Table(header_table_data, hAlign='LEFT', colWidths=[2*inch, 0.5*inch, 1.5*inch, 1.5*inch])
    header_table.setStyle(TableStyle([
        ('SPAN', (0,0), (1,0)),
        ('SPAN', (0,1), (1,1)),
        ('SPAN', (0,2), (1,2)),
        ('SPAN', (0,3), (1,3)),
        ('BACKGROUND', (2,0), (3,0), colors.lightgrey),
        ('BACKGROUND', (2,1), (3,1), colors.lightgrey),
        ('BACKGROUND', (2,2), (3,2), colors.lightgrey),
        ('BACKGROUND', (2,3), (3,3), colors.lightgrey),
        ('ALIGN', (2,0), (3,3), 'RIGHT'),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('TEXTCOLOR', (2,0), (3,3), colors.black),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0,0), (-1,0), 12),
        ('GRID', (0,0), (-1,-1), 1, colors.black)
    ]))
    elements.append(header_table)
    elements.append(Spacer(1, 12))

    # Facturar a / Enviar a
    billing_table_data = [
        ["FACTURAR A", "", "ENVIAR A", ""],
        [cabecera['nombre_cliente'], "", cabecera['nombre_cliente_envio'], ""],
        [cabecera['codigo_postal'], "", cabecera['direccion_envio'], ""],
        [cabecera['poblacion_cliente'], "", cabecera['poblacion_envio'], ""],
        [cabecera['provincia_cliente'], "", cabecera['provincia_envio'], ""]
    ]
    billing_table = Table(billing_table_data, hAlign='LEFT', colWidths=[2*inch, 0.5*inch, 2*inch, 0.5*inch])
    billing_table.setStyle(TableStyle([
        ('SPAN', (0,0), (1,0)),
        ('SPAN', (2,0), (3,0)),
        ('BACKGROUND', (0,0), (3,0), colors.lightgrey),
        ('ALIGN', (0,0), (3,0), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('TEXTCOLOR', (0,0), (3,0), colors.black),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0,0), (-1,0), 12),
        ('GRID', (0,0), (-1,-1), 1, colors.black)
    ]))
    elements.append(billing_table)
    elements.append(Spacer(1, 12))

    # Detalles de la línea
    line_headers = ["CANT.", "DESCRIPCIÓN", "PRECIO UNITARIO", "IMPORTE"]
    line_data = [line_headers] + [[linea['codigo_producto'], linea['cantidad'], linea['nombre_producto_lineas'], linea['valor_producto_lineas'] ] for linea in lineas]
    line_table = Table(line_data, hAlign='LEFT', colWidths=[1*inch, 3*inch, 1.5*inch, 1.5*inch])
    line_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.lightgrey),
        ('ALIGN', (0,0), (-1,0), 'CENTER'),
        ('ALIGN', (2,1), (3,-1), 'RIGHT'),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('TEXTCOLOR', (0,0), (-1,0), colors.black),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0,0), (-1,0), 12),
        ('GRID', (0,0), (-1,-1), 1, colors.black)
    ]))
    elements.append(line_table)
    elements.append(Spacer(1, 12))

       # Calcular el IVA de 21.0%
    total_iva_21 = calcular_iva(lineas)

    # Subtotal, IVA y Total
    total_table_data = [
        ["", "", "Importe Producto", cabecera['importe_producto']],
        ["", "", "IVA 21.0%", f"{total_iva_21:.2f}"],
        ["", "", "TOTAL", cabecera['total_factura']]
    ]
    total_table = Table(total_table_data, hAlign='RIGHT', colWidths=[1*inch, 3*inch, 1.5*inch, 1.5*inch])
    total_table.setStyle(TableStyle([
        ('BACKGROUND', (2,0), (3,0), colors.lightgrey),
        ('BACKGROUND', (2,1), (3,1), colors.lightgrey),
        ('BACKGROUND', (2,2), (3,2), colors.lightgrey),
        ('ALIGN', (2,0), (3,2), 'RIGHT'),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('TEXTCOLOR', (2,0), (3,2), colors.black),
        ('FONTNAME', (2,0), (3,2), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0,0), (-1,0), 12),
        ('GRID', (0,0), (-1,-1), 1, colors.black)
    ]))
    elements.append(total_table)
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