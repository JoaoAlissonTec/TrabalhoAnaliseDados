import pandas as pd
from reportlab.lib.pagesizes import A4
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Table, TableStyle, Spacer
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.lib import colors
from datetime import datetime
from io import BytesIO


def create_pdf(data_frame: pd.DataFrame, name: str):
    buffer = BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=40,
        leftMargin=40,
        topMargin=60,
        bottomMargin=40
    )

    styles = getSampleStyleSheet()
    estilo_titulo = ParagraphStyle(
        name='TituloEmpresa',
        fontSize=22,
        leading=26,
        alignment=TA_CENTER,
        textColor=colors.HexColor("#1F4E78"),
        spaceAfter=6,
        fontName="Helvetica-Bold"
    )

    estilo_data = ParagraphStyle(
        name='DataRelatorio',
        fontSize=10,
        alignment=TA_CENTER,
        textColor=colors.grey,
        spaceAfter=20
    )

    estilo_rodape = ParagraphStyle(
        name='Rodape',
        fontSize=9,
        alignment=TA_CENTER,
        textColor=colors.grey,
    )

    titulo = Paragraph(f"Relatório - {name}", estilo_titulo)
    data_hoje = datetime.now().strftime("%d/%m/%Y")
    data_relatorio = Paragraph(f"Emitido em: {data_hoje}", estilo_data)

    dados_tabela = [data_frame.columns.tolist()] + data_frame.values.tolist()
    tabela = Table(dados_tabela, hAlign='CENTER', colWidths='*')

    estilo_tabela = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#003366")),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
        ('BACKGROUND', (0, 1), (-1, -1), colors.whitesmoke),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
    ])
    tabela.setStyle(estilo_tabela)

    rodape = Paragraph("Relatório gerado automaticamente por " + name, estilo_rodape)

    elementos = [titulo, data_relatorio, tabela, Spacer(1, 20), rodape]

    doc.build(elementos)
    buffer.seek(0)
    return buffer

def baixar_pdf(df, empresa):
    pdf_bytes = create_pdf(df, empresa)

    return pdf_bytes
