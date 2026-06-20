import pandas as pd
import plotly.express as px
import streamlit as st
from sklearn.ensemble import IsolationForest

from core.db import read_sql


def _formatar_brl(valor: float) -> str:
    return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


def _abrir_popup_analise_fornecedor(nome_fornecedor: str, tipo_despesa: str, df: pd.DataFrame) -> None:
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


def _detectar_anomalias(df: pd.DataFrame, contaminacao: float) -> pd.DataFrame:
    """Treina um IsolationForest por tipo_despesa, já que cada categoria tem uma
    faixa de valores típica diferente (ex.: combustível vs. passagem aérea)."""
    resultados = []
    for tipo, grupo in df.groupby("tipo_despesa"):
        if len(grupo) < 10:
            continue
        modelo = IsolationForest(contamination=contaminacao, random_state=42)
        X = grupo[["valor_liquido"]]
        grupo = grupo.copy()
        grupo["score_anomalia"] = modelo.fit_predict(X)
        grupo["score_anomalia"] = (grupo["score_anomalia"] == -1)
        resultados.append(grupo)
    return pd.concat(resultados, ignore_index=True) if resultados else df.iloc[0:0]


def render():
    st.title("Análise com Machine Learning")
    st.caption("Detecção de despesas atípicas (outliers) usando Isolation Forest.")

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
    contaminacao = st.slider(
        "Sensibilidade (% esperado de despesas atípicas por categoria)",
        min_value=0.01,
        max_value=0.10,
        value=0.03,
        step=0.01,
    )

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

    df_resultado = _detectar_anomalias(df, contaminacao)
    anomalias = df_resultado[df_resultado["score_anomalia"]].sort_values(
        "valor_liquido", ascending=False
    )

    col1, col2, col3 = st.columns(3)
    col1.metric("Despesas analisadas", len(df_resultado))
    col2.metric("Despesas atípicas encontradas", len(anomalias))
    col3.metric("Valor total atípico", _formatar_brl(anomalias["valor_liquido"].sum()))

    st.markdown("---")
    st.markdown(
        "Para cada tipo de despesa, o modelo aprende a faixa de valores considerada "
        "normal e aponta os lançamentos que se destacam do padrão do grupo — sem usar "
        "nenhum rótulo manual de fraude."
    )

    if not anomalias.empty:
        fig = px.scatter(
            df_resultado,
            x="data_documento",
            y="valor_liquido",
            color="score_anomalia",
            facet_col="tipo_despesa" if df_resultado["tipo_despesa"].nunique() <= 4 else None,
            title="Despesas no tempo: normais vs. atípicas",
            labels={"score_anomalia": "Atípica"},
        )
        st.plotly_chart(fig, width="stretch")

        st.markdown("### Maiores despesas atípicas")
        tabela = anomalias[
            ["id_despesa", "nome", "sigla_partido", "sigla_uf", "tipo_despesa", "nome_fornecedor", "valor_liquido", "data_documento"]
        ].head(30).copy()
        tabela["valor_liquido"] = tabela["valor_liquido"].apply(_formatar_brl)
        tabela["data_documento"] = pd.to_datetime(tabela["data_documento"]).dt.strftime("%d/%m/%Y")

        col_widths = [2, 1, 1, 2, 2.5, 0.5, 1, 1]
        cabecalho = st.columns(col_widths)
        for col, titulo in zip(
            cabecalho,
            ["Deputado", "Partido", "UF", "Tipo de Despesa", "Fornecedor", "", "Valor", "Data"],
        ):
            col.markdown(f"**{titulo}**")

        for _, linha_despesa in tabela.iterrows():
            linha = st.columns(col_widths)
            linha[0].write(linha_despesa["nome"])
            linha[1].write(linha_despesa["sigla_partido"])
            linha[2].write(linha_despesa["sigla_uf"])
            linha[3].write(linha_despesa["tipo_despesa"])
            linha[4].write(linha_despesa["nome_fornecedor"])
            if linha[5].button("🔍", key=f"analise_ml_{linha_despesa['id_despesa']}", help="Ver análise detalhada deste fornecedor"):
                _abrir_popup_analise_fornecedor(
                    linha_despesa["nome_fornecedor"], linha_despesa["tipo_despesa"], df
                )
            linha[6].write(linha_despesa["valor_liquido"])
            linha[7].write(linha_despesa["data_documento"])
    else:
        st.info("Nenhuma despesa atípica encontrada com a sensibilidade atual.")
