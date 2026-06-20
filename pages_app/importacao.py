import html

import streamlit as st

from core.coleta import obter_deputados, obter_despesas
from core.etl import tratar_deputados, tratar_despesas
from core.load import salvar_deputados, salvar_despesas, registrar_log

MAX_LINHAS_TERMINAL = 5


def _render_terminal(placeholder, linhas: list[str]) -> None:
    ultimas = linhas[-MAX_LINHAS_TERMINAL:]
    corpo = "\n".join(html.escape(l) for l in ultimas)
    placeholder.markdown(
        f"""
        <div style="
            background-color:#0d1117;
            color:#39ff14;
            font-family: 'Courier New', monospace;
            font-size: 13px;
            padding: 10px 14px;
            border-radius: 6px;
            height: 130px;
            overflow: hidden;
            white-space: pre-wrap;
            border: 1px solid #30363d;
        ">{corpo}</div>
        """,
        unsafe_allow_html=True,
    )


ETAPAS = [
    {
        "titulo": "1. Conectando à API",
        "explicacao": (
            "O script realiza requisições HTTP GET à API de Dados Abertos da Câmara dos "
            "Deputados (`BASE_URL`). O código de resposta é validado: 200 indica sucesso; "
            "outros códigos (400, 401, 404, 500) são tratados como erro e registrados em log, "
            "sem interromper o restante da execução."
        ),
    },
    {
        "titulo": "2. Coletando deputados",
        "explicacao": (
            "Consulta ao endpoint `/deputados`. Como a API pagina os resultados, o script "
            "segue automaticamente o link `next` retornado em `links` até esgotar as páginas. "
            "Os campos relevantes (id, nome, siglaPartido, siglaUf) são extraídos do JSON."
        ),
    },
    {
        "titulo": "3. Coletando despesas",
        "explicacao": (
            "Para cada deputado coletado, é feita uma nova consulta a "
            "`/deputados/{id}/despesas?ano=AAAA`, também com paginação automática. Falhas de "
            "conexão de um deputado específico são capturadas e não interrompem a coleta dos "
            "demais."
        ),
    },
    {
        "titulo": "4. Tratando os dados",
        "explicacao": (
            "Conversão de `dataDocumento` para tipo data, `valorLiquido` para numérico, "
            "remoção de duplicidades e padronização dos nomes de colunas para snake_case. "
            "Identificadores como CPF/CNPJ são mantidos como texto (nunca numéricos)."
        ),
    },
    {
        "titulo": "5. Persistindo no MySQL",
        "explicacao": (
            "Os dados tratados são gravados nas tabelas `deputados` (upsert por id_deputado) "
            "e `despesas` (substituição dos registros do ano selecionado), garantindo que "
            "reexecuções não gerem duplicidade. Uma linha de auditoria é gravada em "
            "`log_importacao`."
        ),
    },
]


def render():
    st.title("Importação de Dados")
    st.caption("Pipeline ETL: Extração via API → Tratamento → Carga no MySQL")

    st.markdown("### Parâmetros da coleta")
    col1, col2 = st.columns(2)
    with col1:
        ano = st.number_input("Ano de referência", min_value=2019, max_value=2030, value=2025, step=1)
    with col2:
        qtd_deputados = st.slider("Quantidade de deputados a coletar", min_value=1, max_value=1000, value=20, step=1)

    st.markdown("### Etapas do processo")
    st.caption("Clique em cada etapa para ver uma explicação rápida do que ela faz.")

    cols = st.columns(len(ETAPAS))
    for col, etapa in zip(cols, ETAPAS):
        with col:
            with st.popover(etapa["titulo"], width="stretch"):
                st.write(etapa["explicacao"])

    st.markdown("---")

    if st.button("▶ Executar importação", type="primary"):
        st.caption("Console de execução")
        log_area = st.empty()
        progress = st.progress(0, text="Iniciando...")
        mensagens: list[str] = []

        def log(msg):
            mensagens.append(msg)
            _render_terminal(log_area, mensagens)

        try:
            progress.progress(10, text="Conectando à API e coletando deputados...")
            deputados_raw = obter_deputados(qtd_deputados, log=log)
            log(f"Deputados coletados (bruto): {len(deputados_raw)}")

            df_deputados = tratar_deputados(deputados_raw)
            log(f"Deputados após tratamento: {len(df_deputados)}")

            progress.progress(35, text="Coletando despesas por deputado...")
            total_dep = len(df_deputados)
            todas_despesas = []
            for posicao, (_, dep) in enumerate(df_deputados.iterrows(), start=1):
                log(f"[{posicao}/{total_dep}] Coletando despesas de {dep['nome']} (id {dep['id_deputado']})...")
                despesas = obter_despesas(int(dep["id_deputado"]), int(ano), log=log)
                for d in despesas:
                    d["id_deputado"] = int(dep["id_deputado"])
                todas_despesas.extend(despesas)
                log(f"[{posicao}/{total_dep}] {dep['nome']}: {len(despesas)} despesas encontradas.")
                progress.progress(
                    35 + int(30 * posicao / max(total_dep, 1)),
                    text=f"Coletando despesas por deputado... ({posicao}/{total_dep})",
                )
            log(f"Despesas coletadas (bruto): {len(todas_despesas)}")

            progress.progress(65, text="Tratando despesas...")
            df_despesas = tratar_despesas(todas_despesas, ano=int(ano))
            log(f"Despesas após tratamento: {len(df_despesas)}")

            progress.progress(85, text="Persistindo no MySQL...")
            n_dep = salvar_deputados(df_deputados)
            n_desp = salvar_despesas(df_despesas, ano=int(ano))
            registrar_log(int(ano), n_dep, n_desp, "SUCESSO", "Importação concluída via dashboard.")

            progress.progress(100, text="Concluído!")
            st.success(
                f"Importação concluída: {n_dep} deputados e {n_desp} despesas "
                f"gravados no MySQL para o ano {ano}."
            )
        except Exception as exc:
            registrar_log(int(ano), 0, 0, "ERRO", str(exc))
            st.error(f"Falha na importação: {exc}")
