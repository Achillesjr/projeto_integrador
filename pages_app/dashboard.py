import streamlit as st
import plotly.express as px

from core.db import read_sql


def _formatar_brl(valor: float) -> str:
    return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


def _abrir_popup_analise_fornecedor(nome_fornecedor: str, tipo_despesa: str, df) -> None:
    @st.dialog(f"Análise: {nome_fornecedor}", width="large")
    def _dialog():
        filtro = df[(df["nome_fornecedor"] == nome_fornecedor) & (df["tipo_despesa"] == tipo_despesa)]
        st.caption(f"Tipo de despesa: {tipo_despesa}")

        col1, col2 = st.columns(2)
        col1.metric("Deputados que utilizaram", filtro["id_deputado"].nunique())
        col2.metric("Total Gasto", _formatar_brl(filtro["valor_liquido"].sum()))

        st.markdown("---")

        col_estados, col_utilizadores = st.columns(2)
        with col_estados:
            st.markdown("**Estados (UF) envolvidos**")
            estados = (
                filtro.groupby("sigla_uf")
                .agg(valor_liquido=("valor_liquido", "sum"), qtd_deputados=("id_deputado", "nunique"))
                .sort_values("valor_liquido", ascending=False)
                .reset_index()
            )
            estados["UF"] = estados["sigla_uf"] + " (" + estados["qtd_deputados"].astype(str) + ")"
            estados["Valor"] = estados["valor_liquido"].apply(_formatar_brl)
            st.dataframe(estados[["UF", "Valor"]], width="stretch", hide_index=True)

        with col_utilizadores:
            st.markdown("**Maiores Utilizadores (por Deputado)**")
            utilizadores = (
                filtro.groupby(["nome", "sigla_partido"])["valor_liquido"]
                .sum()
                .sort_values(ascending=False)
                .head(10)
                .reset_index()
            )
            utilizadores["Deputado"] = utilizadores["nome"] + " (" + utilizadores["sigla_partido"] + ")"
            utilizadores["Valor"] = utilizadores["valor_liquido"].apply(_formatar_brl)
            st.dataframe(utilizadores[["Deputado", "Valor"]], width="stretch", hide_index=True)

        st.markdown("---")
        st.markdown("**Uso por Mês**")
        mensal = filtro.groupby("mes")["valor_liquido"].sum().reset_index().sort_values("mes")
        fig = px.bar(mensal, x="mes", y="valor_liquido", title="Gasto Mensal com este Fornecedor")
        st.plotly_chart(fig, width="stretch")

    _dialog()


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
        df.groupby(["nome_fornecedor", "tipo_despesa"])["valor_liquido"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
        .reset_index()
    )
    fornecedores["valor_liquido"] = fornecedores["valor_liquido"].apply(_formatar_brl)

    col_widths = [3, 2, 2, 1]
    cabecalho = st.columns(col_widths)
    for col, titulo in zip(cabecalho, ["Fornecedor", "Tipo de Despesa", "Valor Líquido", "Análise"]):
        col.markdown(f"**{titulo}**")

    for _, linha_fornecedor in fornecedores.iterrows():
        linha = st.columns(col_widths)
        linha[0].write(linha_fornecedor["nome_fornecedor"])
        linha[1].write(linha_fornecedor["tipo_despesa"])
        linha[2].write(linha_fornecedor["valor_liquido"])
        if linha[3].button(
            "🔍",
            key=f"analise_{linha_fornecedor['nome_fornecedor']}_{linha_fornecedor['tipo_despesa']}",
            help="Ver análise detalhada deste fornecedor",
        ):
            _abrir_popup_analise_fornecedor(
                linha_fornecedor["nome_fornecedor"], linha_fornecedor["tipo_despesa"], df
            )
