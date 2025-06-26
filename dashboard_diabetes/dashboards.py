# dashboards.py
import streamlit as st
import pandas as pd
import plotly.express as px
from utils.mapa import mostrar_mapa

st.set_page_config(page_title="Dashboard Diabetes", layout="wide")

st.title("📊 Dashboard de Pacientes com Diabetes")

# Carregando os dados
try:
    df = pd.read_csv("data/dados_diabetes.csv")
    df_coords = pd.read_csv("data/coordenadas_cidades.csv")
    df_porc = pd.read_csv("data/porcentagem_por_sexo.csv")
except FileNotFoundError as e:
    st.error(f"❌ Arquivo não encontrado: {e.filename}")
    st.stop()

# Verificando colunas e unindo coordenadas
if 'Cidade' not in df.columns or 'Cidade' not in df_coords.columns:
    st.error("❌ Coluna 'Cidade' ausente em um dos arquivos.")
    st.stop()

df = df.merge(df_coords, on="Cidade", how="left")

# Filtros
st.sidebar.header("🔍 Filtros")
cidades = sorted(df['Cidade'].dropna().unique())
faixas = sorted(df['Faixa Etária'].dropna().unique())

cidade_selecionada = st.sidebar.multiselect("🏙️ Cidade", cidades)
faixa_selecionada = st.sidebar.multiselect("🎂 Faixa Etária", faixas)

df_filtrado = df.copy()
if cidade_selecionada:
    df_filtrado = df_filtrado[df_filtrado['Cidade'].isin(cidade_selecionada)]
if faixa_selecionada:
    df_filtrado = df_filtrado[df_filtrado['Faixa Etária'].isin(faixa_selecionada)]

# Navegação
aba = st.sidebar.radio("Menu", ["Visão Geral", "Gráfico de Sexo", "Evolução Temporal", "Mapa dos Pacientes"])

if aba == "Visão Geral":
    st.subheader("👥 Total de Pacientes")
    col1, col2 = st.columns(2)
    col1.metric("Pacientes", len(df_filtrado))
    col2.metric("Cidades", df_filtrado['Cidade'].nunique())

    colunas = ['Nome', 'Cidade', 'Estado', 'Faixa Etária', 'Sexo', 'CID', 'Data da Consulta']
    colunas = [c for c in colunas if c in df_filtrado.columns]
    st.dataframe(df_filtrado[colunas], use_container_width=True)

    st.download_button("⬇️ Baixar CSV", df_filtrado.to_csv(index=False), "dados_filtrados.csv")

elif aba == "Gráfico de Sexo":
    if 'Faixa Etária' in df_porc.columns:
        df_pizza = df_porc[
            (df_porc['Cidade'].isin(cidade_selecionada)) &
            (df_porc['Faixa Etária'].isin(faixa_selecionada))
        ]
    else:
        df_pizza = df_porc[df_porc['Cidade'].isin(cidade_selecionada)]

    if not df_pizza.empty:
        tipo = st.radio("Tipo de gráfico", ["Pizza", "Barras"])
        if tipo == "Pizza":
            fig = px.pie(df_pizza, names="Sexo", values="Porcentagem", hole=0.4,
                         color="Sexo", color_discrete_map={"Feminino": "#ff69b4", "Masculino": "#1f77b4"},
                         title="Distribuição por Sexo", template="plotly_dark")
        else:
            fig = px.bar(df_pizza, x="Sexo", y="Porcentagem", color="Sexo",
                         color_discrete_map={"Feminino": "#ff69b4", "Masculino": "#1f77b4"},
                         title="Distribuição por Sexo", template="plotly_dark")

        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("⚠️ Nenhum dado para os filtros selecionados.")

elif aba == "Evolução Temporal":
    st.subheader("📈 Evolução por Data")
    df_filtrado['Data da Consulta'] = pd.to_datetime(df_filtrado['Data da Consulta'], errors='coerce')
    evolucao = df_filtrado.groupby(df_filtrado['Data da Consulta'].dt.to_period('M')).size().reset_index()
    evolucao.columns = ['Mês', 'Total']
    evolucao['Mês'] = evolucao['Mês'].astype(str)

    fig = px.line(evolucao, x='Mês', y='Total', markers=True,
                  title="📅 Evolução Mensal de Pacientes", template="plotly_dark")
    st.plotly_chart(fig, use_container_width=True)

elif aba == "Mapa dos Pacientes":
    mostrar_mapa(df_filtrado)
