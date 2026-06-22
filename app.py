import streamlit as st

from pages_app import (
    projeto,
    definicoes,
    codigo,
    importacao,
    dados_importados,
    dashboard,
    ml_analise,
    relatorio_final,
)

st.set_page_config(
    page_title="Gastos Públicos - Câmara dos Deputados",
    page_icon="📊",
    layout="wide",
)

PAGINAS = {
    "O Projeto": projeto,
    "Definições do Sistema": definicoes,
    "O Código Python": codigo,
    "Importação de Dados": importacao,
    "Dados Importados": dados_importados,
    "Dashboard Informativo": dashboard,
    "Análise com Machine Learning": ml_analise,
    "Relatório final do projeto": relatorio_final,
}

st.sidebar.title("📊 Gastos Públicos")
st.sidebar.caption("Projeto Integrador - Big Data e Inteligência Analítica")
pagina_escolhida = st.sidebar.radio("Etapas do projeto", list(PAGINAS.keys()))
st.sidebar.divider()
st.sidebar.caption("Fonte: API de Dados Abertos da Câmara dos Deputados")

PAGINAS[pagina_escolhida].render()
