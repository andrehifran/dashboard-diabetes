import streamlit as st
import plotly.express as px

def mostrar_mapa(df):
    st.subheader("🗺️ Mapa Interativo de Pacientes em Rondônia")

    cidade = st.sidebar.selectbox(
        "🏙️ Selecione a Cidade",
        sorted(df['Cidade'].dropna().unique()),
        key="mapa_cidade"
    )

    faixa = st.sidebar.selectbox(
        "🎂 Selecione a Faixa Etária",
        sorted(df['Faixa Etária'].dropna().unique()),
        key="mapa_faixa"
    )

    dados = df[
        (df['Cidade'] == cidade) &
        (df['Faixa Etária'] == faixa)
    ].dropna(subset=['Latitude', 'Longitude'])

    if dados.empty:
        st.warning("⚠️ Nenhum dado com coordenadas encontrado.")
        return

    lat_centro = dados['Latitude'].mean()
    lon_centro = dados['Longitude'].mean()

    fig = px.scatter_map(
        dados,
        lat='Latitude',
        lon='Longitude',
        color='Sexo',
        hover_name='Nome',
        zoom=6,
        height=600,
        map_style='open-street-map'
    )

    fig.update_layout(
        mapbox_center={"lat": lat_centro, "lon": lon_centro},
        margin={"r": 0, "t": 30, "l": 0, "b": 0}
    )

    st.plotly_chart(fig, use_container_width=True)
