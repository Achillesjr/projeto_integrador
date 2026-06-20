import streamlit as st


def render():
    st.title("O Projeto")
    st.caption("Curso Tecnólogo em Big Data e Inteligência Analítica — Disciplina: Projeto Integrador")

    st.markdown(
        """
        ## Apresentação
        Projetos de Big Data e Inteligência Analítica não se resumem à criação de gráficos.
        Antes da visualização dos dados, é necessário compreender sua origem, realizar a coleta,
        estruturar o armazenamento, tratar inconsistências, organizar o modelo de dados e somente
        então produzir análises confiáveis.

        Este projeto desenvolve um **pipeline completo de dados**, simulando a atuação profissional
        de um analista/cientista de dados: coleta automatizada via API, modelagem e armazenamento em
        banco relacional, análise exploratória, construção de indicadores/dashboards e aplicação de
        técnicas de Machine Learning.
        """
    )

    st.markdown("## Objetivo Geral")
    st.info(
        "Desenvolver uma solução analítica capaz de coletar, armazenar, tratar, analisar e "
        "interpretar dados públicos relacionados a gastos governamentais, utilizando técnicas de "
        "Engenharia de Dados, Business Intelligence e Machine Learning."
    )

    st.markdown("## Objetivos Específicos")
    st.markdown(
        """
        - Consumir dados de uma API pública;
        - Desenvolver script automatizado de coleta de dados;
        - Tratar paginação, erros de requisição e inconsistências nos dados;
        - Modelar e implementar uma base de dados relacional (MySQL);
        - Criar um dicionário de dados;
        - Realizar análise exploratória;
        - Construir dashboards com indicadores relevantes;
        - Aplicar uma técnica de Machine Learning adequada ao problema;
        - Interpretar os resultados obtidos;
        - Apresentar tecnicamente a solução desenvolvida.
        """
    )

    st.markdown("## Alvo da Pesquisa — API Escolhida")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(
            """
            **API:** Dados Abertos da Câmara dos Deputados
            **URL Base:** `https://dadosabertos.camara.leg.br/api/v2`

            **Justificativa:** dados reais sobre administração pública, documentação completa,
            estrutura adequada para construção de um pipeline ETL ponta a ponta, e potencial
            analítico relevante para estudos de transparência pública.
            """
        )
    with col2:
        st.markdown(
            """
            **Possibilidades de análise:**
            - Despesas parlamentares por deputado;
            - Comparação entre partidos políticos;
            - Comparação entre unidades federativas (UF);
            - Concentração de gastos por categoria de despesa e fornecedor.
            """
        )

    st.markdown("## Organização do Projeto e Deliverables")
    tab1, tab2 = st.tabs(["Entrega 1 — Coleta, Modelagem e Armazenamento", "Entrega 2 — Análise, Dashboard e ML"])
    with tab1:
        st.markdown(
            """
            **Foco:** coleta, estruturação e armazenamento dos dados.

            **Entregáveis:**
            - Script de coleta dos dados (via API, com paginação e tratamento de erros);
            - Base de dados relacional (MySQL) com tabelas `deputados` e `despesas`;
            - Diagrama Entidade-Relacionamento (DER);
            - Dicionário inicial de dados;
            - Relatório parcial.
            """
        )
    with tab2:
        st.markdown(
            """
            **Foco:** transformar os dados coletados em informação útil.

            **Entregáveis:**
            - Dashboard com indicadores (KPIs), evolução temporal, ranking de gastos,
              gastos por categoria/partido/UF e análise de fornecedores;
            - Técnica de Machine Learning aplicada e interpretada (ex.: clusterização de
              perfis de gasto);
            - Relatório final consolidando as duas entregas;
            - Vídeo de apresentação do projeto.
            """
        )

    st.markdown("---")
    st.caption(
        "Use o menu lateral para navegar pelas etapas: Definições do Sistema, Importação de Dados, "
        "Dados Importados e Dashboard Informativo."
    )
