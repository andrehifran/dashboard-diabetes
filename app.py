
import streamlit as st
import pandas as pd
import plotly.express as px
from fpdf import FPDF
import unicodedata
from utils.mapa import mostrar_mapa

st.set_page_config(page_title="Dashboard Diabetes", layout="wide")

# --- Função para remover acentos ---
def remover_acentos(texto):
    return unicodedata.normalize('NFKD', str(texto)).encode('ASCII', 'ignore').decode('ASCII')

# --- LOGIN ---
senha = st.sidebar.text_input("🔐 Digite a senha:", type="password")
if senha != "1234":
    st.warning("Acesso negado. Informe a senha correta.")
    st.stop()

# --- DADOS ---
df = pd.read_csv("data/dados_diabetes.csv")
df_coords = pd.read_csv("data/coordenadas_cidades.csv")
df_porc = pd.read_csv("data/porcentagem_por_sexo.csv")
df = df.merge(df_coords, on="Cidade", how="left")

# --- MENU LATERAL ---
aba = st.sidebar.radio("📂 Navegação", [
    "Visão Geral",
    "Gráfico de Sexo",
    "Evolução Temporal",
    "Mapa dos Pacientes"
])

# --- VISÃO GERAL ---
if aba == "Visão Geral":
    st.title("📋 Visão Geral")
    if "Sexo" in df.columns:
        df["Ícone Sexo"] = df["Sexo"].map({"Feminino": "👩", "Masculino": "🧔"})

    colunas = ['Nome', 'Cidade', 'Estado', 'Sexo', 'CID', 'Data da Consulta']
    colunas = [col for col in colunas if col in df.columns]
    if "Ícone Sexo" in df.columns:
        colunas = ["Ícone Sexo"] + colunas

    st.dataframe(df[colunas], use_container_width=True)

    def exportar_pdf(dados):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)

        for _, row in dados[["Nome", "Cidade", "Estado"]].iterrows():
            linha = f"{row['Nome']} - {row['Cidade']} - {row['Estado']}"
            linha_segura = linha.encode('latin1', 'ignore').decode('latin1')  # <<<<< AQUI é o segredo
            linha = remover_acentos(linha)
            pdf.cell(200, 10, txt=linha, ln=True)
        pdf.output("relatorio.pdf")

    if st.button("📄 Exportar como PDF"):
        try:
            exportar_pdf(df)
            st.success("PDF gerado com sucesso!")
        except Exception as e:
            st.error(f"Erro ao gerar PDF: {e}")

# --- GRÁFICO DE SEXO ---
elif aba == "Gráfico de Sexo":
    st.title("📊 Distribuição por Sexo")
    fig = px.pie(df_porc, names="Sexo", values="Porcentagem", hole=0.4,
                 color_discrete_map={"Feminino": "#ff69b4", "Masculino": "#1f77b4"})
    fig.update_layout(paper_bgcolor="#0f1117", plot_bgcolor="#0f1117", font_color="white")
    st.plotly_chart(fig, use_container_width=True)

# --- EVOLUÇÃO TEMPORAL ---
elif aba == "Evolução Temporal":
    st.title("📈 Evolução de Pacientes")
    df['Data da Consulta'] = pd.to_datetime(df['Data da Consulta'], errors='coerce')
    evol = df.groupby(df['Data da Consulta'].dt.to_period('M')).size().reset_index()
    evol.columns = ['Mês', 'Total']
    evol['Mês'] = evol['Mês'].astype(str)
    fig = px.line(evol, x='Mês', y='Total', markers=True)
    fig.update_layout(paper_bgcolor="#0f1117", plot_bgcolor="#0f1117", font_color="white")
    st.plotly_chart(fig, use_container_width=True)

# --- MAPA ---
elif aba == "Mapa dos Pacientes":
    st.title("🗺️ Mapa de Pacientes")
    mostrar_mapa(df)

