from pathlib import Path

import streamlit as st

PROJECT_ROOT = Path(__file__).resolve().parent.parent

PASTAS_IGNORADAS = {".venv", "__pycache__", ".git"}


def _listar_arquivos_py() -> dict[str, list[Path]]:
    """Agrupa os arquivos .py do projeto por pasta (raiz, core, pages_app, ...)."""
    arquivos = sorted(
        p
        for p in PROJECT_ROOT.rglob("*.py")
        if not any(parte in PASTAS_IGNORADAS for parte in p.relative_to(PROJECT_ROOT).parts)
    )

    grupos: dict[str, list[Path]] = {}
    for arquivo in arquivos:
        pasta = arquivo.parent.relative_to(PROJECT_ROOT)
        chave = "." if str(pasta) == "." else str(pasta)
        grupos.setdefault(chave, []).append(arquivo)

    return grupos


def render():
    st.title("O Código Python")
    st.caption(
        "Navegue pela árvore de diretórios para visualizar (somente leitura) os arquivos "
        "Python que compõem este sistema."
    )

    grupos = _listar_arquivos_py()

    if "arquivo_selecionado" not in st.session_state:
        primeiro_grupo = next(iter(grupos.values()))
        st.session_state.arquivo_selecionado = primeiro_grupo[0]

    col_tree, col_code = st.columns([1, 2.5])

    with col_tree:
        st.markdown("#### Estrutura do projeto")
        for pasta, arquivos in sorted(grupos.items()):
            rotulo_pasta = "📁 raiz do projeto" if pasta == "." else f"📁 {pasta}/"
            with st.expander(rotulo_pasta, expanded=True):
                for arquivo in arquivos:
                    selecionado = st.session_state.arquivo_selecionado == arquivo
                    if st.button(
                        f"{'➡️ ' if selecionado else '📄 '}{arquivo.name}",
                        key=f"btn_{arquivo}",
                        width="stretch",
                        type="primary" if selecionado else "secondary",
                    ):
                        st.session_state.arquivo_selecionado = arquivo
                        st.rerun()

    with col_code:
        arquivo = st.session_state.arquivo_selecionado
        caminho_relativo = arquivo.relative_to(PROJECT_ROOT)
        st.markdown(f"#### `{caminho_relativo}`")

        try:
            conteudo = arquivo.read_text(encoding="utf-8")
        except OSError as exc:
            st.error(f"Não foi possível ler o arquivo: {exc}")
            return

        n_linhas = conteudo.count("\n") + 1
        st.caption(f"{n_linhas} linhas — somente leitura")
        st.code(conteudo, language="python", line_numbers=True, height=500)
