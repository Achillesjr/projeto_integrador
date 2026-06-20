import time
import requests

BASE_URL = "https://dadosabertos.camara.leg.br/api/v2"


def obter_deputados(qtd_deputados: int, log=print) -> list[dict]:
    """Consulta o endpoint /deputados com paginação automática.

    `qtd_deputados` é um limite TOTAL de registros coletados, não o tamanho da
    página: a API de Dados Abertos possui centenas de deputados cadastrados, e
    seguir o link `next` sem este limite faria o pipeline varrer todas as páginas
    disponíveis (centenas de requisições).
    """
    itens_por_pagina = min(qtd_deputados, 100)
    url = f"{BASE_URL}/deputados?pagina=1&itens={itens_por_pagina}"
    deputados: list[dict] = []

    while url and len(deputados) < qtd_deputados:
        try:
            response = requests.get(url, timeout=30)
            if response.status_code != 200:
                log(f"Erro HTTP {response.status_code} ao consultar deputados")
                break

            dados = response.json()
            deputados.extend(dados["dados"])

            proxima_pagina = None
            for link in dados.get("links", []):
                if link["rel"] == "next":
                    proxima_pagina = link["href"]
            url = proxima_pagina

            time.sleep(0.5)
        except requests.exceptions.RequestException as erro:
            log(f"Erro de conexão ao consultar deputados: {erro}")
            break

    return deputados[:qtd_deputados]


def obter_despesas(id_deputado: int, ano: int, log=print) -> list[dict]:
    """Consulta o endpoint /deputados/{id}/despesas filtrado por ano, com paginação."""
    url = f"{BASE_URL}/deputados/{id_deputado}/despesas?ano={ano}&itens=100"
    despesas: list[dict] = []

    while url:
        try:
            response = requests.get(url, timeout=30)
            if response.status_code != 200:
                break

            dados = response.json()
            despesas.extend(dados["dados"])

            proxima_pagina = None
            for link in dados.get("links", []):
                if link["rel"] == "next":
                    proxima_pagina = link["href"]
            url = proxima_pagina

            time.sleep(0.2)
        except requests.exceptions.RequestException as erro:
            log(f"Erro deputado {id_deputado}: {erro}")
            break

    return despesas
