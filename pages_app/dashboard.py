import streamlit as st
import plotly.express as px

from core.db import read_sql


def render():
    st.title("Dashboard Informativo")
    st.caption("Indicadores e análises sobre os gastos parlamentares coletados.")

    try:
        anos_df = read_sql("SELECT DISTINCT ano FROM despesas ORDER BY ano DESC")
    except Exception as exc:
        st.error(f"Não foi possível consultar o banco: {exc}")
        return

    if anos_df.empty:
        st.warning(
            "Nenhum dado encontrado. Vá até a página 'Importação de Dados' e execute a coleta primeiro."
        )
        return

    ano = st.selectbox("Ano de referência", anos_df["ano"].tolist(), index=0)

    df = read_sql(
        """
        SELECT e.id_despesa, e.id_deputado, d.nome, d.sigla_partido, d.sigla_uf,
               e.tipo_despesa, e.valor_liquido, e.data_documento, e.mes,
               e.nome_fornecedor, e.cnpj_cpf_fornecedor
        FROM despesas e
        JOIN deputados d ON d.id_deputado = e.id_deputado
        WHERE e.ano = :ano
        """,
        {"ano": int(ano)},
    )

    if df.empty:
        st.info("Sem despesas registradas para o ano selecionado.")
        return

    total_gasto = df["valor_liquido"].sum()
    total_despesas = len(df)
    qtd_deputados = df["id_deputado"].nunique()
    media_deputado = total_gasto / qtd_deputados if qtd_deputados else 0

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Gasto", f"R$ {total_gasto:,.2f}")
    col2.metric("Total de Despesas", f"{total_despesas:,}")
    col3.metric("Deputados", qtd_deputados)
    col4.metric("Média por Deputado", f"R$ {media_deputado:,.2f}")

    st.markdown("---")

    col1, col2 = st.columns(2)
    with col1:
        top10 = (
            df.groupby("nome")["valor_liquido"]
            .sum()
            .sort_values(ascending=False)
            .head(10)
            .reset_index()
        )
        fig = px.bar(
            top10, x="valor_liquido", y="nome", orientation="h", title="Top 10 Deputados por Gastos"
        )
        fig.update_layout(yaxis={"categoryorder": "total ascending"})
        st.plotly_chart(fig, width="stretch")

    with col2:
        partidos = df.groupby("sigla_partido")["valor_liquido"].sum().sort_values(ascending=False).reset_index()
        fig = px.bar(partidos, x="sigla_partido", y="valor_liquido", title="Gastos por Partido")
        st.plotly_chart(fig, width="stretch")

    col3, col4 = st.columns(2)
    with col3:
        ufs = df.groupby("sigla_uf")["valor_liquido"].sum().sort_values(ascending=False).reset_index()
        fig = px.bar(ufs, x="sigla_uf", y="valor_liquido", title="Gastos por UF")
        st.plotly_chart(fig, width="stretch")

    with col4:
        categorias = (
            df.groupby("tipo_despesa")["valor_liquido"].sum().sort_values(ascending=False).head(10).reset_index()
        )
        fig = px.bar(categorias, x="valor_liquido", y="tipo_despesa", orientation="h", title="Top Categorias de Despesa")
        fig.update_layout(yaxis={"categoryorder": "total ascending"})
        st.plotly_chart(fig, width="stretch")

    st.markdown("### Evolução Mensal")
    mensal = df.groupby("mes")["valor_liquido"].agg(["sum", "count"]).reset_index()
    col5, col6 = st.columns(2)
    with col5:
        fig = px.line(mensal, x="mes", y="sum", markers=True, title="Evolução Mensal dos Gastos (R$)")
        st.plotly_chart(fig, width="stretch")
    with col6:
        fig = px.line(mensal, x="mes", y="count", markers=True, title="Quantidade de Despesas por Mês")
        st.plotly_chart(fig, width="stretch")

    st.markdown("### Fornecedores com Maior Concentração de Valores")
    fornecedores = (
        df.groupby("nome_fornecedor")["valor_liquido"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
        .reset_index()
    )
    st.dataframe(fornecedores, width="stretch")
