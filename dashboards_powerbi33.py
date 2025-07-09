import streamlit as st
import pandas as pd
import plotly.express as px
from utils.mapa import mostrar_mapa

st.set_page_config(page_title="Dashboard Diabetes", layout="wide")

st.markdown("## 💼 Dashboard Estilo Power BI - Diabetes")
st.markdown("> Análise de pacientes com estilo moderno e profissional.")

# Carregando os dados
try:
    df = pd.read_csv("data/dados_diabetes.csv")
    df_coords = pd.read_csv("data/coordenadas_cidades.csv")
    df_porc = pd.read_csv("data/porcentagem_por_sexo.csv")
except FileNotFoundError as e:
    st.error(f"❌ Arquivo não encontrado: {e.filename}")
    st.stop()

if 'Cidade' not in df.columns or 'Cidade' not in df_coords.columns:
    st.error("❌ Coluna 'Cidade' ausente.")
    st.stop()

df = df.merge(df_coords, on="Cidade", how="left")

# Filtros
st.sidebar.header("🎛️ Filtros")
cidades = sorted(df['Cidade'].dropna().unique())
faixas = sorted(df['Faixa Etária'].dropna().unique())

cidade_selecionada = st.sidebar.multiselect("🏙️ Cidade", cidades, default=cidades)
faixa_selecionada = st.sidebar.multiselect("🎂 Faixa Etária", faixas, default=faixas)

if st.sidebar.button("🔄 Limpar Filtros"):
    st.experimental_rerun()

df_filtrado = df[df['Cidade'].isin(cidade_selecionada) & df['Faixa Etária'].isin(faixa_selecionada)]

# Indicadores com estilo Power BI
col1, col2, col3, col4 = st.columns(4)
col1.markdown(f"<div style='background:#1e1e1e;padding:1rem;border-radius:8px;text-align:center;'><h4 style='color:white;'>Pacientes</h4><h2 style='color:#00ffea;'>{len(df_filtrado)}</h2></div>", unsafe_allow_html=True)
col2.markdown(f"<div style='background:#112233;padding:1rem;border-radius:8px;text-align:center;'><h4 style='color:white;'>Cidades</h4><h2 style='color:#ffaa00;'>{df_filtrado['Cidade'].nunique()}</h2></div>", unsafe_allow_html=True)
col3.markdown(f"<div style='background:#331144;padding:1rem;border-radius:8px;text-align:center;'><h4 style='color:white;'>Faixas Etárias</h4><h2 style='color:#cc33ff;'>{df_filtrado['Faixa Etária'].nunique()}</h2></div>", unsafe_allow_html=True)
col4.markdown(f"<div style='background:#222222;padding:1rem;border-radius:8px;text-align:center;'><h4 style='color:white;'>CID únicos</h4><h2 style='color:#66ff66;'>{df_filtrado['CID'].nunique()}</h2></div>", unsafe_allow_html=True)

# Menu principal
aba = st.sidebar.radio("📁 Menu", ["Visão Geral", "Gráfico de Sexo", "Evolução Temporal", "Mapa dos Pacientes"])

if aba == "Visão Geral":
    st.subheader("📋 Tabela de Pacientes Filtrados")
    sexo_emoji = {"Feminino": "👩", "Masculino": "🧔"}
    if "Sexo" in df_filtrado.columns:
        df_filtrado["Ícone Sexo"] = df_filtrado["Sexo"].map(sexo_emoji)

    colunas = ['Nome', 'Cidade', 'Estado', 'Faixa Etária', 'Sexo', 'CID', 'Data da Consulta']
    colunas = [c for c in colunas if c in df_filtrado.columns]
    mostrar = ["Ícone Sexo"] + colunas if "Ícone Sexo" in df_filtrado.columns else colunas

    st.dataframe(df_filtrado[mostrar], use_container_width=True)
    st.download_button("⬇️ Baixar dados como CSV", df_filtrado.to_csv(index=False), "dados_filtrados.csv")

elif aba == "Gráfico de Sexo":
    st.subheader("📊 Distribuição por Sexo")

    df_grafico = df_porc.copy()

    if "Cidade" in df_grafico.columns and cidade_selecionada:
        df_grafico = df_grafico[df_grafico["Cidade"].isin(cidade_selecionada)]
    if "Faixa Etária" in df_grafico.columns and faixa_selecionada:
        df_grafico = df_grafico[df_grafico["Faixa Etária"].isin(faixa_selecionada)]

    df_grafico = df_grafico.dropna(subset=["Sexo", "Porcentagem"])
    df_grafico = df_grafico[df_grafico["Sexo"].astype(str).str.strip() != ""]

    # Normaliza porcentagem: corrige vírgula, remove % e converte
    df_grafico["Porcentagem"] = (
        df_grafico["Porcentagem"]
        .astype(str)
        .str.replace(",", ".", regex=False)
        .str.replace("%", "", regex=False)
    )
    df_grafico["Porcentagem"] = pd.to_numeric(df_grafico["Porcentagem"], errors="coerce")
    df_grafico = df_grafico.dropna(subset=["Porcentagem"])
    df_grafico = df_grafico[df_grafico["Porcentagem"] > 0]

    st.write("🔍 Dados para o gráfico:")
    st.dataframe(df_grafico)

    if df_grafico.empty:
        st.warning("⚠️ Nenhum dado válido para os filtros selecionados.")
    else:
        tipo = st.radio("📈 Tipo de gráfico", ["Pizza", "Barras"])

        try:
            if tipo == "Pizza":
                fig = px.pie(
                    df_grafico,
                    names="Sexo",
                    values="Porcentagem",
                    hole=0.4,
                    color="Sexo",
                    color_discrete_map={"Feminino": "#ff69b4", "Masculino": "#1f77b4"},
                )
                fig.update_traces(textinfo="label+percent")
            else:
                fig = px.bar(
                    df_grafico,
                    x="Sexo",
                    y="Porcentagem",
                    text_auto=".2f",
                    color="Sexo",
                    color_discrete_map={"Feminino": "#ff69b4", "Masculino": "#1f77b4"},
                )

            fig.update_layout(paper_bgcolor="#0f1117", plot_bgcolor="#0f1117", font_color="white")
            st.plotly_chart(fig, use_container_width=True)

        except Exception as e:
            st.error("❌ Erro ao gerar o gráfico.")
            st.exception(e)

elif aba == "Evolução Temporal":
    st.subheader("📈 Evolução por Data de Consulta")
    df_filtrado['Data da Consulta'] = pd.to_datetime(df_filtrado['Data da Consulta'], errors='coerce')
    evolucao = df_filtrado.groupby(df_filtrado['Data da Consulta'].dt.to_period('M')).size().reset_index()
    evolucao.columns = ['Mês', 'Total']
    evolucao['Mês'] = evolucao['Mês'].astype(str)

    fig = px.line(evolucao, x='Mês', y='Total', markers=True, text='Total')
    fig.update_layout(title="📅 Evolução Mensal", paper_bgcolor="#0f1117",
                      plot_bgcolor="#0f1117", font_color="white", title_x=0.5)
    st.plotly_chart(fig, use_container_width=True)

elif aba == "Mapa dos Pacientes":
    mostrar_mapa(df_filtrado)
# --- FIM DO DASHBOARD ---
