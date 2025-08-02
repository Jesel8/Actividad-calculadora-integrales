# pdf_generator.py (Versión Corregida y Explícita)
from fpdf import FPDF
from datetime import datetime


class PDFReport(FPDF):
    """
    Clase personalizada para crear un PDF con cabecera y pie de página.
    """

    def header(self):
        self.set_font("Arial", "B", 12)
        # ### CAMBIO: Se han nombrado los parámetros para mayor claridad (border, ln, align).
        self.cell(0, 10, "Reporte de Cálculo de Integral", border=0, ln=1, align="C")
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font("Arial", "I", 8)
        page_num = self.page_no()
        # ### CAMBIO: Se han nombrado los parámetros.
        self.cell(0, 10, f"Página {page_num}", border=0, ln=0, align="C")


def create_integral_report(calc_data, graph_image_path):
    """
    Crea un reporte en PDF con los datos del cálculo y la gráfica.

    Args:
        calc_data (dict): Un diccionario con los datos del cálculo.
        graph_image_path (str): La ruta a la imagen temporal de la gráfica.
    """
    pdf = PDFReport()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)

    # Título de la sección de datos
    pdf.set_font("Arial", "B", 14)
    # ### CAMBIO: Se nombran los parámetros. Aquí 'ln=1' mueve el cursor a la siguiente línea.
    pdf.cell(0, 10, "Detalles del Cálculo", border=0, ln=1)

    # Contenido del cálculo
    pdf.set_font("Arial", "", 12)
    # ### CAMBIO: Reemplazamos 'cell' por 'multi_cell' para más seguridad y nombramos parámetros.
    pdf.multi_cell(0, 10, f"Función f(x): {calc_data['func_str']}", border=0, ln=1)
    pdf.multi_cell(
        0,
        10,
        f"Límites de Integración: de a = {calc_data['a_str']} a b = {calc_data['b_str']}",
        border=0,
        ln=1,
    )
    pdf.multi_cell(
        0,
        10,
        f"Resultado (Integral Definida): {calc_data['result_def']}",
        border=0,
        ln=1,
    )

    # ### CAMBIO: Se nombran los parámetros en el multi_cell existente.
    pdf.multi_cell(
        0,
        10,
        f"Integral Indefinida: {calc_data['result_indef_latex']}",
        border=0,
        align="L",
    )
    pdf.ln(5)

    # Gráfica de la función
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, "Gráfica de la Función", border=0, ln=1)

    # Esta línea estaba bien, pero añadimos el resto de parámetros por claridad.
    pdf.image(
        graph_image_path,
        x=None,
        y=None,
        w=170,
        h=0,
        type="",
        link="",
        alt_text="Gráfica de la función",
    )

    # Fecha de generación
    pdf.ln(10)
    pdf.set_font("Arial", "I", 10)
    today = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    # ### CAMBIO: Se nombran los parámetros.
    pdf.cell(0, 10, f"Reporte generado el: {today}", border=0, ln=1, align="R")

    return pdf

# Fin del archivo