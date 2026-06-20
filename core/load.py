import pandas as pd
from sqlalchemy import text

from core.db import get_cached_engine

# Etapa "Load" do pipeline ETL: grava os DataFrames já tratados (core/etl.py)
# no MySQL e registra uma linha de auditoria para cada execução da coleta.


def salvar_deputados(df: pd.DataFrame) -> int:
    """Insere ou atualiza (upsert) os deputados, evitando duplicidade quando a
    coleta é executada mais de uma vez para o mesmo ano."""
    if df.empty:
        return 0
    engine = get_cached_engine()
    with engine.begin() as conn:
        for _, row in df.iterrows():
            conn.execute(
                text(
                    """
                    INSERT INTO deputados (id_deputado, nome, sigla_partido, sigla_uf, url_foto, email)
                    VALUES (:id_deputado, :nome, :sigla_partido, :sigla_uf, :url_foto, :email)
                    ON DUPLICATE KEY UPDATE
                        nome = VALUES(nome),
                        sigla_partido = VALUES(sigla_partido),
                        sigla_uf = VALUES(sigla_uf),
                        url_foto = VALUES(url_foto),
                        email = VALUES(email)
                    """
                ),
                {
                    "id_deputado": int(row["id_deputado"]),
                    "nome": row["nome"],
                    "sigla_partido": row["sigla_partido"],
                    "sigla_uf": row["sigla_uf"],
                    "url_foto": row["url_foto"],
                    "email": row["email"],
                },
            )
    return len(df)


def salvar_despesas(df: pd.DataFrame, ano: int) -> int:
    """Substitui as despesas do ano informado (delete + insert), garantindo que
    reexecuções da coleta não dupliquem registros do mesmo período."""
    engine = get_cached_engine()
    with engine.begin() as conn:
        conn.execute(text("DELETE FROM despesas WHERE ano = :ano"), {"ano": ano})
        if not df.empty:
            df.to_sql("despesas", conn, if_exists="append", index=False)
    return len(df)


def registrar_log(ano: int, qtd_deputados: int, qtd_despesas: int, status: str, mensagem: str):
    """Grava uma linha de auditoria (sucesso ou erro) para cada execução da importação."""
    engine = get_cached_engine()
    with engine.begin() as conn:
        conn.execute(
            text(
                """
                INSERT INTO log_importacao
                    (ano_referencia, qtd_deputados, qtd_despesas, status, mensagem, finalizado_em)
                VALUES (:ano, :qtd_dep, :qtd_desp, :status, :msg, NOW())
                """
            ),
            {
                "ano": ano,
                "qtd_dep": qtd_deputados,
                "qtd_desp": qtd_despesas,
                "status": status,
                "msg": mensagem,
            },
        )
