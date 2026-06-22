from pathlib import Path

import streamlit as st

CAMINHO_PDF = Path(__file__).resolve().parent.parent / "assets" / "relatorio" / "relatorio_final_projeto_integrador.pdf"


def render():
    st.title("Relatório Final do Projeto")
    st.caption("Documento consolidado das duas entregas: coleta, modelagem, dashboard e Machine Learning.")

    if not CAMINHO_PDF.exists():
        st.error(
            "O arquivo do relatório não foi encontrado em "
            f"`{CAMINHO_PDF.relative_to(CAMINHO_PDF.parent.parent.parent)}`. "
            "Gere-o executando `scripts/gerar_relatorio_pdf.py`."
        )
        return

    dados_pdf = CAMINHO_PDF.read_bytes()

    st.download_button(
        "⬇️ Baixar Relatório Final (PDF)",
        data=dados_pdf,
        file_name="relatorio_final_projeto_integrador.pdf",
        mime="application/pdf",
        width="content",
    )

    st.markdown("---")
    st.markdown("### Leitura do relatório")
    st.pdf(dados_pdf, height=900)
