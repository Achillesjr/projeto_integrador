import graphviz
import streamlit as st

from core.coleta import BASE_URL
from core.db import DB_CONFIG, test_connection


def _grafico_etl() -> graphviz.Digraph:
    g = graphviz.Digraph()
    g.attr(rankdir="TB", bgcolor="transparent")
    g.attr(
        "node",
        shape="box",
        style="filled",
        fillcolor="#eef2fb",
        color="#2c3e70",
        fontname="Helvetica",
        fontsize="11",
    )
    g.attr("edge", color="#2c3e70")

    g.node("api", "API Câmara dos\nDeputados")
    g.node("req", "Requisição HTTP\n(requests.get)")
    g.node("extracao", "Extração JSON\n(response.json())")
    g.node("paginacao", "Paginação e Tratamento\nde Erros")
    g.node("df", "DataFrame\n(Pandas)")
    g.node("limpeza", "Limpeza de Dados\nNulos | Duplicidades | Conversões")
    g.node("mysql", "Persistência MySQL\n(SQLAlchemy)")
    g.node("pronto", "Base Pronta para\nAnálise e Dashboard")

    with g.subgraph() as s:
        s.attr(rank="same")
        s.node("api")
        s.node("req")
    with g.subgraph() as s:
        s.attr(rank="same")
        s.node("extracao")
        s.node("paginacao")
    with g.subgraph() as s:
        s.attr(rank="same")
        s.node("df")
        s.node("limpeza")
    with g.subgraph() as s:
        s.attr(rank="same")
        s.node("mysql")
        s.node("pronto")

    g.edge("api", "req")
    g.edge("req", "extracao")
    g.edge("extracao", "paginacao")
    g.edge("paginacao", "df")
    g.edge("df", "limpeza")
    g.edge("limpeza", "mysql")
    g.edge("mysql", "pronto")

    return g


def _grafico_der() -> graphviz.Digraph:
    g = graphviz.Digraph()
    g.attr(rankdir="LR", bgcolor="transparent")
    g.attr("node", shape="plaintext", fontname="Helvetica")

    g.node(
        "deputados",
        label="""<
        <table border="1" cellborder="0" cellspacing="0" cellpadding="4">
            <tr><td bgcolor="#2c3e70" colspan="1"><font color="white"><b>DEPUTADOS</b></font></td></tr>
            <tr><td align="left"><u>PK id_deputado</u></td></tr>
            <tr><td align="left">nome</td></tr>
            <tr><td align="left">sigla_partido</td></tr>
            <tr><td align="left">sigla_uf</td></tr>
            <tr><td align="left">url_foto</td></tr>
            <tr><td align="left">email</td></tr>
        </table>
        >""",
    )

    g.node(
        "despesas",
        label="""<
        <table border="1" cellborder="0" cellspacing="0" cellpadding="4">
            <tr><td bgcolor="#2c3e70" colspan="1"><font color="white"><b>DESPESAS</b></font></td></tr>
            <tr><td align="left"><u>PK id_despesa</u></td></tr>
            <tr><td align="left"><i>FK id_deputado</i></td></tr>
            <tr><td align="left">ano / mes</td></tr>
            <tr><td align="left">tipo_despesa</td></tr>
            <tr><td align="left">valor_liquido</td></tr>
            <tr><td align="left">data_documento</td></tr>
            <tr><td align="left">nome_fornecedor</td></tr>
            <tr><td align="left">cnpj_cpf_fornecedor</td></tr>
        </table>
        >""",
    )

    g.node(
        "log",
        label="""<
        <table border="1" cellborder="0" cellspacing="0" cellpadding="4">
            <tr><td bgcolor="#6c7a96" colspan="1"><font color="white"><b>LOG_IMPORTACAO</b></font></td></tr>
            <tr><td align="left"><u>PK id_execucao</u></td></tr>
            <tr><td align="left">ano_referencia</td></tr>
            <tr><td align="left">qtd_deputados</td></tr>
            <tr><td align="left">qtd_despesas</td></tr>
            <tr><td align="left">status</td></tr>
        </table>
        >""",
    )

    g.edge("deputados", "despesas", label="1 : N", color="#2c3e70", fontname="Helvetica", fontsize="10")
    g.edge(
        "log",
        "despesas",
        label="auditoria\n(sem FK)",
        color="#6c7a96",
        style="dashed",
        arrowhead="none",
        fontname="Helvetica",
        fontsize="9",
    )

    return g


def _grafico_ml() -> graphviz.Digraph:
    g = graphviz.Digraph()
    g.attr(rankdir="TB", bgcolor="transparent")
    g.attr(
        "node",
        shape="box",
        style="filled",
        fillcolor="#eef2fb",
        color="#2c3e70",
        fontname="Helvetica",
        fontsize="11",
    )
    g.attr("edge", color="#2c3e70")

    g.node("base", "Base de Despesas\n(MySQL)")
    g.node("agrupa", "Agrupamento por\ntipo_despesa")
    g.node("feature", "Feature: valor_liquido\n(por categoria)")
    g.node("modelo", "IsolationForest\n(scikit-learn)")
    g.node("score", "Classificação:\nNormal | Atípica")
    g.node("saida", "Dashboard de\nAnomalias")

    g.edge("base", "agrupa")
    g.edge("agrupa", "feature")
    g.edge("feature", "modelo")
    g.edge("modelo", "score")
    g.edge("score", "saida")

    return g


def render():
    st.title("Definições do Sistema")
    st.caption("Configuração da API consumida e do banco de dados utilizado pelo pipeline.")

    st.markdown("## API de Dados Abertos da Câmara dos Deputados")
    st.code(f"BASE_URL = {BASE_URL!r}", language="python")

    st.markdown("### Endpoints utilizados")
    st.table(
        [
            {
                "Endpoint": "/deputados",
                "Objetivo": "Obter informações cadastrais dos parlamentares",
                "Principais campos": "id, nome, siglaPartido, siglaUf",
            },
            {
                "Endpoint": "/deputados/{id}/despesas",
                "Objetivo": "Obter despesas associadas a cada parlamentar",
                "Principais campos": "tipoDespesa, valorLiquido, dataDocumento, nomeFornecedor, cnpjCpfFornecedor",
            },
        ]
    )

    st.markdown(
        """
        **Parâmetros suportados:**
        - `pagina` / `itens`: controle de paginação (a API limita registros por requisição,
          o script percorre automaticamente o link `next` retornado em `links`);
        - `ano`: filtro temporal aplicado na consulta de despesas.
        """
    )

    st.markdown("## Banco de Dados (MySQL)")
    safe_config = {k: v for k, v in DB_CONFIG.items() if k != "password"}
    safe_config["password"] = "•" * 10
    st.json(safe_config)

    if st.button("Testar conexão com o banco"):
        ok, msg = test_connection()
        if ok:
            st.success(msg)
        else:
            st.error(msg)

    st.markdown("## Estrutura de Dados")
    st.markdown(
        """
        - Tabela `deputados` — dados cadastrais (PK `id_deputado`);
        - Tabela `despesas` — registros financeiros (PK `id_despesa`, FK `id_deputado`);
        - Tabela `log_importacao` — auditoria de cada execução do pipeline de coleta.

        Veja o detalhamento completo em `docs/modelo_dados_producao.md` e o DDL em `sql/schema.sql`.
        """
    )

    st.markdown("## Arquitetura do Pipeline (ETL)")
    st.graphviz_chart(_grafico_etl(), width="content")

    st.markdown(
        """
        A arquitetura do pipeline segue o padrão **ETL (Extract, Transform, Load)**, amplamente
        utilizado em projetos de Engenharia de Dados para obtenção, preparação e armazenamento de
        informações provenientes de fontes externas.
        """
    )

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(
            """
            **⇒ Extract**
            Coleta dos dados diretamente da API através de requisições HTTP, com paginação
            automática e tratamento de erros de conexão.
            """
        )
    with col2:
        st.markdown(
            """
            **⇒ Transform**
            Normalização, remoção de inconsistências, padronização de tipos, tratamento de nulos
            e validação dos registros antes da carga.
            """
        )
    with col3:
        st.markdown(
            """
            **⇒ Load**
            Persistência em banco MySQL, organizado em tabelas relacionais, para consumo
            posterior por ferramentas analíticas e pelo dashboard.
            """
        )

    st.markdown("## Diagrama Entidade-Relacionamento (DER)")
    st.caption("Demonstra como os dados estão ligados no banco de dados.")
    st.graphviz_chart(_grafico_der(), width="content")
    st.markdown(
        """
        - **Deputado (1) — (N) Despesa**: um parlamentar pode possuir diversas despesas
          registradas; cada despesa pertence a exatamente um parlamentar (`id_deputado` como
          chave estrangeira, com `ON DELETE CASCADE`);
        - **log_importacao**: tabela de auditoria das execuções do pipeline, sem chave
          estrangeira para as demais tabelas — relação meramente informativa de contexto.
        """
    )

    st.markdown("## Machine Learning: Detecção de Despesas Atípicas")
    st.caption("Componente analítico do projeto, disponível na página 'Análise com Machine Learning'.")

    st.markdown(
        """
        Para extrair valor analítico além dos gráficos descritivos do dashboard, o projeto aplica
        uma técnica de **aprendizado de máquina não supervisionado** sobre os dados de despesas:
        o algoritmo **Isolation Forest**, da biblioteca `scikit-learn`.

        **Por que Isolation Forest?**
        - Não exige rótulos manuais de "fraude" ou "irregularidade" — o modelo aprende sozinho
          o que é um padrão normal de gasto;
        - É indicado para **detecção de anomalias** em dados tabulares, isolando rapidamente
          observações raras (outliers) através de partições aleatórias da árvore de decisão;
        - É leve e rápido o suficiente para ser recalculado a cada interação do usuário no
          dashboard (mudança de ano ou de sensibilidade), sem necessidade de treinamento prévio
          persistido em disco.

        **Como é aplicado neste projeto:**
        1. As despesas do ano selecionado são agrupadas por `tipo_despesa` (ex.: combustível,
           passagem aérea, divulgação), pois cada categoria possui uma faixa de valores típica
           muito diferente;
        2. Para cada grupo com volume suficiente de registros, um modelo `IsolationForest` é
           treinado usando `valor_liquido` como variável (*feature*);
        3. O modelo classifica cada despesa como **normal** ou **atípica**, de acordo com o
           parâmetro de sensibilidade (`contamination`) definido pelo usuário;
        4. As despesas atípicas são exibidas em destaque — em gráfico de dispersão ao longo do
           tempo e em tabela ordenada pelo maior valor — para apoiar a verificação de possíveis
           irregularidades.
        """
    )

    st.graphviz_chart(_grafico_ml(), width="content")
    st.markdown(
        """
        - **Entrada**: despesas já tratadas e persistidas no MySQL pelo pipeline ETL;
        - **Treinamento**: um modelo `IsolationForest` por categoria de despesa, executado em
          tempo real a cada consulta (sem necessidade de retreinamento manual);
        - **Saída**: rótulo binário (normal/atípica) consumido diretamente pelos gráficos e
          tabelas da página de Machine Learning do dashboard.
        """
    )
