import pandas as pd
from sqlalchemy import text

from core.db import get_cached_engine


def salvar_deputados(df: pd.DataFrame) -> int:
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
    engine = get_cached_engine()
    with engine.begin() as conn:
        conn.execute(text("DELETE FROM despesas WHERE ano = :ano"), {"ano": ano})
        if not df.empty:
            df.to_sql("despesas", conn, if_exists="append", index=False)
    return len(df)


def registrar_log(ano: int, qtd_deputados: int, qtd_despesas: int, status: str, mensagem: str):
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
