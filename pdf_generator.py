# pdf_generator.py (VERSIÓN FINAL CON IMAGEN DE FÓRMULA)
from fpdf import FPDF, Align
from datetime import datetime


class PDFReport(FPDF):
    def header(self):
        self.set_font("Arial", "B", 12)
        self.cell(0, 10, "Reporte de Cálculo de Integral", border=0, ln=1, align="C")
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font("Arial", "I", 8)
        self.cell(0, 10, f"Página {self.page_no()}", border=0, ln=0, align="C")


# --- FUNCIÓN CORREGIDA PARA ACEPTAR 3 ARGUMENTOS ---
def create_integral_report(calc_data, graph_image_path, latex_image_path):
    pdf = PDFReport()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)

    # Sección de Datos
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, "Detalles del Cálculo", border=0, ln=1)
    pdf.set_font("Arial", "", 12)
    pdf.multi_cell(0, 8, f"Función f(x): {calc_data['func_str']}", border=0, ln=1)
    pdf.multi_cell(
        0,
        8,
        f"Límites de Integración: de a = {calc_data['a_str']} a b = {calc_data['b_str']}",
        border=0,
        ln=1,
    )
    pdf.multi_cell(
        0,
        8,
        f"Integral Indefinida: {calc_data['result_indef_latex']}",
        border=0,
        align="L",
    )
    pdf.ln(5)

    # Sección de Resultado Visual
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, "Resultado", border=0, ln=1)
    pdf.image(latex_image_path, w=100, x=Align.C)
    pdf.ln(10)

    # Sección de Gráfica
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, "Gráfica de la Función", border=0, ln=1)
    pdf.image(graph_image_path, w=170, x=Align.C)

    # Fecha de generación
    pdf.ln(10)
    pdf.set_font("Arial", "I", 10)
    today = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    pdf.cell(0, 10, f"Reporte generado el: {today}", border=0, ln=1, align="R")

    return pdf

# --- FUNCIÓN CORREGIDA PARA ACEPTAR 3 ARGUMENTOS ---