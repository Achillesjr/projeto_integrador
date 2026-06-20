import time

import streamlit as st
from sqlalchemy import bindparam, text

from core.db import read_sql


def _abrir_popup_foto(nome: str, url_foto: str | None) -> None:
    @st.dialog(nome)
    def _dialog():
        col_esq, col_centro, col_dir = st.columns([1, 2, 1])
        with col_centro:
            if url_foto:
                st.image(url_foto, width=180)
            else:
                st.info("Foto não disponível para este parlamentar.")
        time.sleep(8)
        st.rerun()

    _dialog()


def render():
    st.title("Dados Importados")
    st.caption("Visualização das tabelas carregadas no MySQL.")

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

    anos_disponiveis = anos_df["ano"].tolist()
    ano_selecionado = st.selectbox("Ano de referência", anos_disponiveis, index=0)

    tab1, tab2 = st.tabs(["Deputados", "Despesas"])

    with tab1:
        df_deputados = read_sql(
            """
            SELECT DISTINCT d.id_deputado, d.nome, d.sigla_partido, d.sigla_uf, d.url_foto
            FROM deputados d
            JOIN despesas e ON e.id_deputado = d.id_deputado
            WHERE e.ano = :ano
            ORDER BY d.nome
            """,
            {"ano": int(ano_selecionado)},
        )
        col1, col2 = st.columns(2)
        col1.metric("Deputados", len(df_deputados))
        col2.metric("Partidos distintos", df_deputados["sigla_partido"].nunique())

        st.caption("Clique no nome de um deputado para visualizar a foto.")
        evento = st.dataframe(
            df_deputados[["id_deputado", "nome", "sigla_partido", "sigla_uf"]],
            width="stretch",
            hide_index=True,
            on_select="rerun",
            selection_mode="single-row",
            key="tabela_deputados",
        )

        linhas_selecionadas = evento.selection.rows if evento and evento.selection else []
        if linhas_selecionadas:
            deputado = df_deputados.iloc[linhas_selecionadas[0]]
            if st.session_state.get("ultimo_deputado_foto") != deputado["id_deputado"]:
                st.session_state["ultimo_deputado_foto"] = deputado["id_deputado"]
                _abrir_popup_foto(deputado["nome"], deputado["url_foto"])

    with tab2:
        filtro_partido = st.multiselect(
            "Filtrar por partido", sorted(df_deputados["sigla_partido"].dropna().unique())
        )

        query = """
            SELECT e.id_despesa, e.id_deputado, d.nome, d.sigla_partido, d.sigla_uf,
                   e.tipo_despesa, e.valor_liquido, e.data_documento,
                   e.nome_fornecedor, e.cnpj_cpf_fornecedor
            FROM despesas e
            JOIN deputados d ON d.id_deputado = e.id_deputado
            WHERE e.ano = :ano
        """
        params = {"ano": int(ano_selecionado)}
        stmt = text(query)
        if filtro_partido:
            stmt = text(query + " AND d.sigla_partido IN :partidos").bindparams(
                bindparam("partidos", expanding=True)
            )
            params["partidos"] = filtro_partido

        df_despesas = read_sql(stmt, params)

        col1, col2, col3 = st.columns(3)
        col1.metric("Total de despesas", len(df_despesas))
        col2.metric("Valor total (R$)", f"{df_despesas['valor_liquido'].sum():,.2f}")
        col3.metric("Fornecedores distintos", df_despesas["nome_fornecedor"].nunique())
        st.dataframe(df_despesas, width="stretch")
