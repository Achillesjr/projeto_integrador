import pandas as pd

# Etapa "Transform" do pipeline ETL: recebe o JSON bruto retornado pela API
# (core/coleta.py) e devolve DataFrames já tratados, prontos para persistência
# (core/load.py).

COLUNAS_DEPUTADOS = ["id", "nome", "siglaPartido", "siglaUf", "urlFoto", "email"]
COLUNAS_DESPESAS = [
    "id_deputado",
    "tipoDespesa",
    "valorLiquido",
    "dataDocumento",
    "nomeFornecedor",
    "cnpjCpfFornecedor",
]


def tratar_deputados(deputados: list[dict]) -> pd.DataFrame:
    """Seleciona e renomeia os campos cadastrais de deputados para snake_case,
    garantindo as colunas mesmo quando a API não as retorna (preenchidas com None)."""
    df = pd.DataFrame(deputados)
    for col in COLUNAS_DEPUTADOS:
        if col not in df.columns:
            df[col] = None
    df = df[COLUNAS_DEPUTADOS].copy()
    df.rename(
        columns={
            "id": "id_deputado",
            "siglaPartido": "sigla_partido",
            "siglaUf": "sigla_uf",
            "urlFoto": "url_foto",
        },
        inplace=True,
    )
    df.drop_duplicates(subset="id_deputado", inplace=True)
    return df


def tratar_despesas(despesas: list[dict], ano: int) -> pd.DataFrame:
    """Padroniza os registros de despesas: renomeia colunas para snake_case,
    converte data e valor para tipos adequados, deriva o mês e remove duplicidades."""
    if not despesas:
        return pd.DataFrame(
            columns=[
                "id_deputado",
                "ano",
                "mes",
                "tipo_despesa",
                "valor_liquido",
                "data_documento",
                "nome_fornecedor",
                "cnpj_cpf_fornecedor",
            ]
        )

    df = pd.DataFrame(despesas)
    for col in COLUNAS_DESPESAS:
        if col not in df.columns:
            df[col] = None
    df = df[COLUNAS_DESPESAS].copy()

    df.rename(
        columns={
            "tipoDespesa": "tipo_despesa",
            "valorLiquido": "valor_liquido",
            "dataDocumento": "data_documento",
            "nomeFornecedor": "nome_fornecedor",
            "cnpjCpfFornecedor": "cnpj_cpf_fornecedor",
        },
        inplace=True,
    )

    df["data_documento"] = pd.to_datetime(df["data_documento"], errors="coerce")
    df["valor_liquido"] = pd.to_numeric(df["valor_liquido"], errors="coerce")
    df["ano"] = ano
    df["mes"] = df["data_documento"].dt.month

    # Identificadores (CPF/CNPJ) permanecem como texto, nunca convertidos para numérico
    df["cnpj_cpf_fornecedor"] = df["cnpj_cpf_fornecedor"].astype("string")

    df.drop_duplicates(inplace=True)
    df.dropna(subset=["id_deputado"], inplace=True)

    return df
