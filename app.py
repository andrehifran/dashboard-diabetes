import streamlit as st

st.set_page_config(page_title="Dashboard - Login", layout="centered")

def autenticar():
    st.title("🔐 Acesso Restrito")
    senha = st.text_input("Digite a senha:", type="password")
    if senha == "1234":
        st.success("Acesso autorizado! Use o menu lateral acima para navegar.")
    elif senha:
        st.error("Senha incorreta")
        st.stop()
        

autenticar()
