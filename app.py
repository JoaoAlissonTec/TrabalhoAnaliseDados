import streamlit as st
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

data = st.sidebar.file_uploader("Adicionar arquivo", type=["csv", "xlsx"], accept_multiple_files=False)

if data is not None:
    if data.name.endswith("xlsx"):
        data_frame = pd.read_excel(data, engine="openpyxl")
    elif data.name.endswith("csv"):
        data_frame = pd.read_csv(data, encoding="utf-8")
else:
    data_frame = None

def home():
    st.title("Olá, seja bem-vindo! :wave:")
    st.write('''
             Importe sua planilha de forma rápida e prática para transformar dados brutos em informações visuais.
             Nosso sistema lê automaticamente os dados e apresenta tudo em uma tabela organizada e gráficos interativos, facilitando a análise e tomada de decisões.
             Comece agora carregando sua planilha!
             ## Vamos começar!
             Para dar início, faça o upload do seu arquivo CSV ou Excel na barra lateral esquerda. Logo após, você poderá visualizar os dados e criar gráficos para análise.
            ''')

def data():
    st.title("Seus dados")
    business_name = st.text_input("Nome da empresa", placeholder="Digite o nome da empresa")
    st.divider()
    if data_frame is not None:
        colunas_para_exibir = st.multiselect(
            "Selecione as colunas para exibir",
            options=data_frame.columns.tolist(),
            default=[data_frame.columns[0]],
        )

        if colunas_para_exibir:
            data_frame_filtrado = data_frame[colunas_para_exibir]
            st.write("Aqui estão os dados que você carregou:")
            st.dataframe(data_frame_filtrado)
            st.download_button(
                label="Imprimir PDF",
                data=baixar_pdf(data_frame_filtrado, business_name),
                file_name=f"relatorio_{business_name}.pdf",
                icon=":material/download:",
                mime="application/pdf",
            )
        else:
            st.warning("Selecione pelo menos uma coluna para exibir os dados.")
    else:
        st.warning("Por favor, carregue um arquivo CSV ou Excel para visualizar os dados.")

def dashboard():
    st.title("Dashboard")
    st.divider()
    if data_frame is not None:
        colunas_para_analisar = st.multiselect(
            "Selecione uma coluna",
            options=data_frame.columns.tolist(),
            max_selections=2,
        )
        if len(colunas_para_analisar) == 2:
            st.subheader("Gráfico de barras")
            st.write(f"Analisando a coluna: {colunas_para_analisar}")
            st.bar_chart(
                data_frame[colunas_para_analisar], 
                x=colunas_para_analisar[0], 
                y=colunas_para_analisar[1],
                height=400
            )
            st.subheader("Gráfico de dispersão")
            st.write(f"Analisando a coluna: {colunas_para_analisar}")
            st.scatter_chart(
                data_frame[colunas_para_analisar], 
                x=colunas_para_analisar[0], 
                y=colunas_para_analisar[1],
                height=400,
                use_container_width=True
            )
        else:
            st.warning("Selecione uma coluna para visualizar o gráfico.")
    else:
        st.warning("Por favor, carregue um arquivo CSV ou Excel para visualizar os dados.")

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


pg = st.navigation(    
    [
        st.Page(home, title="Início", icon=":material/home:"), 
        st.Page(data, title="Dados", icon=":material/database:"), 
        st.Page(dashboard, title="Dashboard", icon=":material/monitoring:"),
    ], 
    position="sidebar", 
    expanded=True
)
pg.run()