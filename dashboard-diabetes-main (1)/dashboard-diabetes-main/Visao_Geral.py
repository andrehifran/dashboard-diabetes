import pandas as pd
import streamlit as st
from fpdf import FPDF

df = pd.read_csv("data/dados_diabetes.csv")

# Exemplo simples de filtro global (substitua conforme necessário)
df_filtrado = df  # ← aplique filtros se quiser

def exportar_pdf(dados):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    for _, row in dados.iterrows():
        pdf.cell(200, 10, txt=str(row.to_dict()), ln=True)
    pdf.output("relatorio.pdf")

if st.button("📄 Exportar como PDF"):
    exportar_pdf(df_filtrado)
    st.success("PDF gerado! Verifique a pasta do projeto.")
