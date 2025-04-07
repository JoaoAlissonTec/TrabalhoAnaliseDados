import streamlit as st
import pandas as pd

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
             Se você está aqui, é porque deseja analisar seus dados de uma forma mais simplificada, correto?
             ## Vamos começar!
             Para dar início, faça o upload do seu arquivo CSV ou Excel na barra lateral esquerda. Logo após, você poderá visualizar os dados e criar gráficos para análise.
            ''')

def data():
    st.title("Seus dados")
    if data_frame is not None:
        colunas_para_exibir = st.multiselect(
            "Selecione as colunas para exibir",
            options=data_frame.columns.tolist(),
            default=[data_frame.columns[0]],  # Exibir a primeira coluna por padrão
        )

        if colunas_para_exibir:
            data_frame_filtrado = data_frame[colunas_para_exibir]
            st.write("Aqui estão os dados que você carregou:")
            st.dataframe(data_frame_filtrado)
        else:
            st.warning("Selecione pelo menos uma coluna para exibir os dados.")
    else:
        st.warning("Por favor, carregue um arquivo CSV ou Excel para visualizar os dados.")

def dashboard():
    st.title("Dashboard")
    if data_frame is not None:
        st.write("Selecione as colunas que deseja analisar:")
        colunas_para_analisar = st.multiselect(
            "Selecione uma coluna",
            options=data_frame.columns.tolist(),
            max_selections=2,
        )
        if len(colunas_para_analisar) == 2:
            st.write(f"Analisando a coluna: {colunas_para_analisar}")
            st.bar_chart(
                data_frame[colunas_para_analisar], 
                x=colunas_para_analisar[0], 
                y=colunas_para_analisar[1],
                height=400
            )
        else:
            st.warning("Selecione uma coluna para visualizar o gráfico.")
    else:
        st.warning("Por favor, carregue um arquivo CSV ou Excel para visualizar os dados.")


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