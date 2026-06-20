import os
from urllib.parse import quote_plus

import streamlit as st
from sqlalchemy import create_engine, text
from sqlalchemy.sql.elements import TextClause
import pandas as pd


def _config_value(key: str, default: str) -> str:
    if "db" in st.secrets and key in st.secrets["db"]:
        return st.secrets["db"][key]
    return os.environ.get(f"DB_{key.upper()}", default)


DB_CONFIG = {
    "host": _config_value("host", "127.0.0.1"),
    "port": int(_config_value("port", "3306")),
    "user": _config_value("user", "integrador"),
    "password": _config_value("password", ""),
    "database": _config_value("database", "projeto_integrador"),
}


def get_engine():
    user = quote_plus(DB_CONFIG["user"])
    password = quote_plus(DB_CONFIG["password"])
    url = (
        f"mysql+mysqlconnector://{user}:{password}"
        f"@{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['database']}"
    )
    return create_engine(url, pool_pre_ping=True)


@st.cache_resource
def get_cached_engine():
    return get_engine()


def test_connection() -> tuple[bool, str]:
    try:
        engine = get_engine()
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return True, "Conexão estabelecida com sucesso."
    except Exception as exc:
        return False, str(exc)


def read_sql(query: str | TextClause, params: dict | None = None) -> pd.DataFrame:
    engine = get_cached_engine()
    stmt = query if isinstance(query, TextClause) else text(query)
    with engine.connect() as conn:
        return pd.read_sql(stmt, conn, params=params or {})


def execute(query: str, params: dict | None = None):
    engine = get_cached_engine()
    with engine.begin() as conn:
        conn.execute(text(query), params or {})
