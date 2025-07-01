import streamlit as st
import pandas as pd
import plotly.express as px
from utils.mapa import mostrar_mapa

st.set_page_config(page_title="Dashboard Diabetes", layout="wide")

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
    df["Ícone Sexo"] = df["Sexo"].map({"Feminino": "👩", "Masculino": "🧔"})
    st.dataframe(df[["Ícone Sexo", "Nome", "Cidade", "Estado", "Sexo", "CID", "Data da Consulta"]])
    
    from fpdf import FPDF
    def exportar_pdf(dados):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        for _, row in dados.iterrows():
            pdf.cell(200, 10, txt=str(row.to_dict()), ln=True)
        pdf.output("relatorio.pdf")
       

    if st.button("📄 Exportar como PDF"):
        exportar_pdf(df)
        st.success("PDF gerado com sucesso!")

# --- GRÁFICO DE SEXO ---
elif aba == "Gráfico de Sexo":
    st.title("📊 Distribuição por Sexo")
    fig = px.pie(df_porc, names="Sexo", values="Porcentagem", hole=0.4,
                 color_discrete_map={"Feminino": "#ff69b4", "Masculino": "#1f77b4"})
    st.plotly_chart(fig, use_container_width=True)

# --- EVOLUÇÃO TEMPORAL ---
elif aba == "Evolução Temporal":
    st.title("📈 Evolução de Pacientes")
    df['Data da Consulta'] = pd.to_datetime(df['Data da Consulta'], errors='coerce')
    evol = df.groupby(df['Data da Consulta'].dt.to_period('M')).size().reset_index()
    evol.columns = ['Mês', 'Total']
    evol['Mês'] = evol['Mês'].astype(str)
    fig = px.line(evol, x='Mês', y='Total', markers=True)
    st.plotly_chart(fig, use_container_width=True)

# --- MAPA ---
elif aba == "Mapa dos Pacientes":
    st.title("🗺️ Mapa de Pacientes")
    mostrar_mapa(df)

try:
    from fpdf import FPDF
    def exportar_pdf(dados):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        for _, row in dados.iterrows():
            pdf.cell(200, 10, txt=str(row.to_dict()), ln=True)
        pdf.output("relatorio.pdf")
except ModuleNotFoundError:
    st.error("Biblioteca fpdf não instalada. Verifique o requirements.txt.")

