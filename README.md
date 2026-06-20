# 📊 Gastos Públicos — Câmara dos Deputados

Projeto Integrador da disciplina **Big Data e Inteligência Analítica**.
Pipeline completo de dados (ETL) que coleta, trata, armazena e analisa
informações de despesas parlamentares a partir da **API de Dados Abertos da
Câmara dos Deputados**, com uma interface interativa construída em
[Streamlit](https://streamlit.io/).

> Curso Tecnólogo em Big Data e Inteligência Analítica [202691]
> Prof. Francisco Filho — Aluno: Eric Rocha Pitman Junior (matrícula 2486031008)

## Objetivo

Desenvolver uma solução analítica capaz de coletar, armazenar, tratar,
analisar e interpretar dados públicos relacionados a gastos governamentais,
aplicando técnicas de Engenharia de Dados, Business Intelligence e Machine
Learning.

## Visão geral do pipeline

```
API Câmara dos Deputados → Coleta (core/coleta.py) → Transformação (core/etl.py)
→ Carga em MySQL (core/load.py) → Dashboard/Análise (Streamlit)
```

- **Extract**: consulta paginada aos endpoints `/deputados` e
  `/deputados/{id}/despesas`, com tratamento de erros HTTP.
- **Transform**: normalização dos JSONs em DataFrames Pandas (colunas
  padronizadas, tipos consistentes).
- **Load**: persistência em banco relacional MySQL (tabelas `deputados`,
  `despesas` e `log_importacao`).
- **Analyze**: dashboard interativo com indicadores, evolução temporal,
  ranking de gastos e comparação por partido/UF/fornecedor.

## Estrutura do projeto

```
app.py                  # Entry point Streamlit (menu lateral + roteamento de páginas)
core/
  coleta.py             # Extração de dados via API (paginação, retries, log)
  etl.py                # Tratamento/transformação dos dados coletados
  load.py               # Carga dos dados tratados no MySQL
  db.py                 # Conexão SQLAlchemy + leitura de credenciais (st.secrets/env)
pages_app/
  projeto.py            # Página "O Projeto" — objetivos e escopo
  definicoes.py         # Página "Definições do Sistema" — config e teste de conexão
  codigo.py             # Página "O Código Python" — explicação do pipeline
  importacao.py         # Página "Importação de Dados" — dispara o ETL via UI
  dados_importados.py   # Página "Dados Importados" — consulta ao banco
  dashboard.py          # Página "Dashboard Informativo" — KPIs e gráficos
sql/
  schema.sql            # DDL das tabelas (deputados, despesas, log_importacao)
docs/
  modelo_dados_producao.md  # Modelo de dados / dicionário de dados
```

## Tecnologias

- **Python** — Streamlit, Pandas, Requests, SQLAlchemy, mysql-connector-python, Plotly
- **MySQL** — armazenamento relacional dos dados coletados
- **API de Dados Abertos da Câmara dos Deputados** — fonte dos dados (`https://dadosabertos.camara.leg.br/api/v2`)

## Modelo de dados (resumo)

- `deputados`: dados cadastrais do parlamentar (nome, partido, UF, etc.)
- `despesas`: lançamentos financeiros vinculados a um deputado (`FK`), com
  tipo de despesa, valor líquido, fornecedor e data do documento
- `log_importacao`: auditoria de cada execução do pipeline de importação

Detalhes completos em [sql/schema.sql](sql/schema.sql) e
[docs/modelo_dados_producao.md](docs/modelo_dados_producao.md).

## Como executar localmente

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Configure as credenciais do MySQL em `.streamlit/secrets.toml` (use
[.streamlit/secrets.toml.example](.streamlit/secrets.toml.example) como
modelo) ou via variáveis de ambiente `DB_HOST`, `DB_PORT`, `DB_USER`,
`DB_PASSWORD`, `DB_NAME`.

Crie o schema no MySQL:

```bash
mysql -h <host> -u <usuario> -p <database> < sql/schema.sql
```

Rode a aplicação:

```bash
streamlit run app.py
```

## Deploy (Streamlit Community Cloud)

1. Suba o repositório no GitHub (já feito).
2. Em [streamlit.io/cloud](https://streamlit.io/cloud), crie um novo app
   apontando para este repositório, branch `main` e arquivo `app.py`.
3. Em **Settings → Secrets**, cole as credenciais no mesmo formato de
   [.streamlit/secrets.toml.example](.streamlit/secrets.toml.example):
   ```toml
   [db]
   host = "..."
   port = 3306
   user = "..."
   password = "..."
   database = "..."
   ```
4. O banco MySQL precisa aceitar conexões remotas e liberar a porta 3306 para
   o IP de saída do Streamlit Cloud.

## Segurança

- Nenhuma credencial é mantida no código-fonte: `core/db.py` lê de
  `st.secrets` (produção) com fallback para variáveis de ambiente (local).
- `.streamlit/secrets.toml` e `.env` estão no `.gitignore` — nunca devem ser
  versionados.

## Status do projeto

- ✅ **Entrega 1** — coleta automatizada, modelagem e armazenamento em MySQL
- 🔄 **Entrega 2** — dashboard com indicadores, evolução temporal e aplicação
  de técnica de Machine Learning (em andamento)
