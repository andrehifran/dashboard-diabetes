# 📊 Dashboard de Pacientes com Diabetes

Este é um dashboard interativo construído com [Streamlit](https://streamlit.io) para visualizar dados de pacientes com diabetes de forma clara, moderna e profissional.

![Dashboard Screenshot](https://via.placeholder.com/1200x600.png?text=Dashboard+Preview)

---

## 🔍 Funcionalidades

- Filtros interativos por **Cidade** e **Faixa Etária**
- Gráfico de **pizza ou barras** com distribuição por sexo
- **Mapa interativo** com geolocalização dos pacientes
- Gráfico de **linha temporal** mostrando evolução de consultas
- Exportação de dados para CSV
- Tema escuro customizado

---

## 🗂 Estrutura do Projeto

```
dashboard_diabetes/
├── dashboards.py               # Código principal
├── requirements.txt            # Dependências
├── .streamlit/
│   └── config.toml             # Tema escuro
├── data/
│   ├── dados_diabetes.csv
│   ├── coordenadas_cidades.csv
│   └── porcentagem_por_sexo.csv
├── utils/
│   ├── mapa.py
│   └── __init__.py
```

---

## ▶️ Como Rodar Localmente

1. Clone o repositório:

```bash
git clone https://github.com/seu-usuario/dashboard_diabetes.git
cd dashboard_diabetes
```

2. Instale as dependências:

```bash
pip install -r requirements.txt
```

3. Rode o app:

```bash
streamlit run dashboards.py
```

---

## ☁️ Deploy Online com Streamlit Cloud

1. Suba este repositório no GitHub
2. Acesse: [https://streamlit.io/cloud](https://streamlit.io/cloud)
3. Clique em **+ New app**
4. Defina o caminho do script: `dashboard_diabetes/dashboards.py`
5. Clique em **Deploy**

---

## 📁 Requisitos

- Python 3.10+
- Streamlit
- Pandas
- Plotly

---

## ✨ Autor

Desenvolvido por [Andre Alexandre Hifran].  
Quer me contratar ou colaborar? Me envie uma mensagem!
