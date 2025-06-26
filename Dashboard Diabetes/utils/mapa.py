import plotly.express as px
import streamlit as st

def mostrar_mapa(df):
    # Garante que só usa linhas com coordenadas válidas
    df = df.dropna(subset=['Latitude', 'Longitude'])

    # Cria o mapa com Plotly
    fig = px.scatter_mapbox(
        df,
        lat='Latitude',
        lon='Longitude',
        color='Sexo',
        hover_name='Cidade',
        zoom=5,
        height=600,
        color_discrete_map={
            "Feminino": "#ff69b4",
            "Masculino": "#1f77b4"
        }
    )

    # Configura o estilo e layout do mapa
    fig.update_layout(
        mapbox_style="open-street-map",
        margin={"r":0,"t":0,"l":0,"b":0},
        paper_bgcolor="#0f1117"
    )

    # Exibe no Streamlit
    st.plotly_chart(fig, use_container_width=True)
