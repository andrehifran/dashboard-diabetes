import streamlit as st
import pandas as pd
import plotly.express as px
from utils.mapa import mostrar_mapa

st.set_page_config(page_title="Dashboard Diabetes", layout="wide")

st.title("📊 Dashboard de Pacientes com Diabetes")

# Carregar dados
try:
    df = pd.read_csv("data/dados_diabetes.csv")
    df_coords = pd.read_csv("data/coordenadas_cidades.csv")
    df_porc = pd.read_csv("data/porcentagem_por_sexo.csv")
except FileNotFoundError as e:
    st.error(f"❌ Arquivo não encontrado: {e.filename}")
    st.stop()

# Unir coordenadas
if 'Cidade' not in df.columns or 'Cidade' not in df_coords.columns:
    st.error("❌ Coluna 'Cidade' ausente.")
    st.stop()

df = df.merge(df_coords, on="Cidade", how="left")

# Filtros globais
st.sidebar.header("🎛️ Filtros")
cidades = sorted(df['Cidade'].dropna().unique())
faixas = sorted(df['Faixa Etária'].dropna().unique())

cidade_selecionada = st.sidebar.multiselect("🏙️ Cidade", cidades, default=cidades)
faixa_selecionada = st.sidebar.multiselect("🎂 Faixa Etária", faixas, default=faixas)

df_filtrado = df[df['Cidade'].isin(cidade_selecionada) & df['Faixa Etária'].isin(faixa_selecionada)]

# Navegação
aba = st.sidebar.radio("📁 Menu", ["Visão Geral", "Gráfico de Sexo", "Evolução Temporal", "Mapa dos Pacientes"])

if aba == "Visão Geral":
    st.subheader("📋 Visão Geral")
    st.dataframe(df_filtrado, use_container_width=True)

elif aba == "Gráfico de Sexo":
    st.subheader("📊 Distribuição por Sexo")

    df_grafico = df_porc[df_porc['Cidade'].isin(cidade_selecionada)]

    if 'Faixa Etária' in df_porc.columns:
        df_grafico = df_grafico[df_grafico['Faixa Etária'].isin(faixa_selecionada)]

    # Limpeza e validação dos dados
    df_grafico = df_grafico.dropna(subset=["Sexo", "Porcentagem"])
    df_grafico["Porcentagem"] = pd.to_numeric(df_grafico["Porcentagem"], errors="coerce")
    df_grafico = df_grafico.dropna(subset=["Porcentagem"])

    st.write("🔎 Dados usados no gráfico de pizza:")
    st.dataframe(df_grafico)

    if df_grafico.empty:
        st.warning("⚠️ Nenhum dado válido para o gráfico.")
    else:
        fig = px.pie(df_grafico,
                     names="Sexo",
                     values="Porcentagem",
                     hole=0.4,
                     textinfo="label+percent",
                     color="Sexo",
                     color_discrete_map={"Feminino": "#ff69b4", "Masculino": "#1f77b4"})
        fig.update_layout(paper_bgcolor="#0f1117", plot_bgcolor="#0f1117", font_color="white")
        st.plotly_chart(fig, use_container_width=True)

elif aba == "Evolução Temporal":
    st.subheader("📈 Evolução de Pacientes")
    df_filtrado['Data da Consulta'] = pd.to_datetime(df_filtrado['Data da Consulta'], errors='coerce')
    evol = df_filtrado.groupby(df_filtrado['Data da Consulta'].dt.to_period('M')).size().reset_index()
    evol.columns = ['Mês', 'Total']
    evol['Mês'] = evol['Mês'].astype(str)
    fig = px.line(evol, x='Mês', y='Total', markers=True)
    st.plotly_chart(fig, use_container_width=True)

elif aba == "Mapa dos Pacientes":
    st.subheader("🗺️ Mapa de Pacientes")
    mostrar_mapa(df_filtrado)
