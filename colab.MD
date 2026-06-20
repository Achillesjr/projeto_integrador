!pip install pandas requests

import requests
import pandas as pd
import sqlite3
import time

BASE_URL = "https://dadosabertos.camara.leg.br/api/v2"
ANO_ANALISE = 2025
QTD_DEPUTADOS = 20

import sqlite3
import pandas as pd

conn = None # Initialize conn to None
try:
    conn = sqlite3.connect('gastos_publicos.db')

    # Check if tables exist
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='deputados'")
    deputados_exists = cursor.fetchone()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='despesas'")
    despesas_exists = cursor.fetchone()

    if not deputados_exists or not despesas_exists:
        print("Error: The 'deputados' or 'despesas' tables do not exist in 'gastos_publicos.db'\n")
        print("Please ensure that the data collection and persistence cell (cell `idU3ws2HZixl`) has been run successfully in this session.\n")
        # Create empty DataFrames to avoid NameError in subsequent cells
        df_deputados = pd.DataFrame()
        df_despesas = pd.DataFrame()
    else:
        # Load deputados data
        df_deputados = pd.read_sql_query('SELECT * FROM deputados', conn)

        # Load despesas data
        df_despesas = pd.read_sql_query('SELECT * FROM despesas', conn)

        print('DataFrames df_deputados and df_despesas loaded successfully from gastos_publicos.db\n')

        # Display the first few rows to confirm loading
        print('First 5 rows of df_deputados:')
        display(df_deputados.head())

        print('\nFirst 5 rows of df_despesas:')
        display(df_despesas.head())

except sqlite3.DatabaseError as e:
    print(f"An error occurred while accessing the database: {e}\n")
    print("Please ensure that the data collection and persistence cell (cell `idU3ws2HZixl`) has been run successfully in this session.\n")
    df_deputados = pd.DataFrame()
    df_despesas = pd.DataFrame()
except Exception as e:
    print(f"An unexpected error occurred: {e}\n")
    df_deputados = pd.DataFrame()
    df_despesas = pd.DataFrame()
finally:
    if conn:
        conn.close()

import requests
import pandas as pd
import sqlite3
import time

# BASE_URL is defined in cell 37500890
# ANO_ANALISE is defined in cell 37500890
# QTD_DEPUTADOS is defined in cell 37500890

#Função para obter todos os deputados

def obter_deputados():

    #qtd_deputados = 20 #Here you should define how many records you want to read...
    url = f"{BASE_URL}/deputados?pagina=1&itens={QTD_DEPUTADOS}"
    deputados = []

    while url:

        try:

            response = requests.get(url, timeout=30)

            if response.status_code != 200:
                print(f"Erro HTTP {response.status_code}")
                break

            dados = response.json()

            deputados.extend(dados["dados"])

            proxima_pagina = None

            if "links" in dados:
                for link in dados["links"]:
                    if link["rel"] == "next":
                        proxima_pagina = link["href"]

            url = proxima_pagina

            time.sleep(0.5)

        except requests.exceptions.RequestException as erro:
            print(f"Erro de conexão: {erro}")
            break

    return pd.DataFrame(deputados)

#Função para obter despesas

def obter_despesas(id_deputado):

    url = f"{BASE_URL}/deputados/{id_deputado}/despesas?ano={ANO_ANALISE}"

    despesas = []

    while url:

        try:

            response = requests.get(url, timeout=30)

            if response.status_code != 200:
                break

            dados = response.json()

            despesas.extend(dados["dados"])

            proxima_pagina = None

            if "links" in dados:
                for link in dados["links"]:
                    if link["rel"] == "next":
                        proxima_pagina = link["href"]

            url = proxima_pagina

            time.sleep(0.2)

        except requests.exceptions.RequestException as erro:
            print(f"Erro deputado {id_deputado}: {erro}")
            break

    return despesas


#Coleta principal


print("Iniciando coleta dos deputados...")

df_deputados = obter_deputados()

print(f"Deputados coletados: {len(df_deputados)}")

todas_despesas = []

for _, deputado in df_deputados.iterrows():

    id_deputado = deputado["id"]

    print(
        f"Coletando despesas do deputado {id_deputado}"
    )

    despesas = obter_despesas(id_deputado)

    for despesa in despesas:

        despesa["id_deputado"] = id_deputado

    todas_despesas.extend(despesas)

print(
    f"Total de despesas coletadas: {len(todas_despesas)}"
)

df_despesas = pd.DataFrame(todas_despesas)

# ----------------------------------------
# Tratamento dos dados
# ----------------------------------------

if not df_despesas.empty:

    if "dataDocumento" in df_despesas.columns:
        df_despesas["dataDocumento"] = pd.to_datetime(
            df_despesas["dataDocumento"],
            errors="coerce"
        )

    if "valorLiquido" in df_despesas.columns:
        df_despesas["valorLiquido"] = pd.to_numeric(
            df_despesas["valorLiquido"],
            errors="coerce"
        )

    df_despesas.drop_duplicates(inplace=True)


#Persistência SQLite


print("Criando banco SQLite...")

conn = sqlite3.connect("gastos_publicos.db")

df_deputados.to_sql(
    "deputados",
    conn,
    if_exists="replace",
    index=False
)

df_despesas.to_sql(
    "despesas",
    conn,
    if_exists="replace",
    index=False
)

conn.close()

print("Processo concluído com sucesso.")


#Evidências para o relatório


print("\nPrimeiros deputados:")
print(df_deputados.head())

print("\nPrimeiras despesas:")
print(df_despesas.head())

import matplotlib.pyplot as plt
import seaborn as sns

# Mesclar os dataframes de deputados e despesas para obter o partido de cada deputado
df_merged = pd.merge(df_despesas, df_deputados[['id', 'siglaPartido']], left_on='id_deputado', right_on='id', how='left')

# Calcular o total de gastos por partido
gastos_por_partido = df_merged.groupby('siglaPartido')['valorLiquido'].sum().sort_values(ascending=False).reset_index()

# Criar o gráfico de barras
plt.figure(figsize=(15, 8))
sns.barplot(x='siglaPartido', y='valorLiquido', data=gastos_por_partido, palette='viridis', hue='siglaPartido', legend=False)
plt.title('Total de Gastos por Partido', fontsize=16)
plt.xlabel('Partido', fontsize=12)
plt.ylabel('Total de Gastos (R$)', fontsize=12)
plt.xticks(rotation=90) # Rotacionar os rótulos do eixo X para melhor visualização
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.show()

display(gastos_por_partido.head())

df_deputados = ...
df_despesas = ...

# Ensure df_despesas exists and is a DataFrame before attempting operations
if 'df_despesas' in locals() and isinstance(df_despesas, pd.DataFrame) and not df_despesas.empty:
    if "dataDocumento" in df_despesas.columns:
        df_despesas["dataDocumento"] = pd.to_datetime(
            df_despesas["dataDocumento"],
            errors="coerce"
        )
    if "valorLiquido" in df_despesas.columns:
        df_despesas["valorLiquido"] = pd.to_numeric(
            df_despesas["valorLiquido"],
            errors="coerce"
        )
    df_despesas.drop_duplicates(inplace=True)
    print("df_despesas cleaning operations applied.")
else:
    print("df_despesas is not defined, not a DataFrame, or is empty. Cleaning operations skipped.")

