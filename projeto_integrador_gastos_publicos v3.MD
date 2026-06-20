
Curso: Projeto Integrador em Big Data e Inteligência Analítica [202691]
Prof: Francisco Filho
Aluno: Eric Rocha Pitman Junior
Matricula: 2486031008


RELATÓRIO PARCIAL – ENTREGA 1

PIPELINE DE INTELIGÊNCIA ANALÍTICA EM GASTOS PÚBLICOS

1. INTRODUÇÃO
O acesso a dados públicos tem crescido significativamente nos últimos anos, permitindo que estudantes, pesquisadores e organizações desenvolvam análises baseadas em informações disponibilizadas por órgãos governamentais. Dentro desse contexto, as APIs de dados abertos representam uma importante fonte de informações estruturadas, possibilitando a construção de soluções voltadas à análise, monitoramento e apoio à tomada de decisão.
Para este projeto foi escolhida a API de Dados Abertos da Câmara dos Deputados, que disponibiliza informações relacionadas aos parlamentares e às despesas realizadas durante o exercício de suas atividades. A escolha do tema ocorreu em função da relevância das informações para estudos sobre transparência pública e também pela possibilidade de aplicação prática dos conceitos estudados na disciplina de Big Data e Inteligência Analítica.
Nesta primeira etapa do projeto o foco esteve na construção da base necessária para as análises futuras. Para isso foi desenvolvida uma rotina de coleta automatizada capaz de acessar a API, recuperar os dados de interesse, realizar tratamentos iniciais e armazenar as informações em um banco de dados relacional.
Durante o desenvolvimento foram identificados alguns desafios técnicos, principalmente relacionados à paginação das consultas e ao tratamento dos dados retornados pela API. Esses desafios exigiram a implementação de mecanismos de validação e organização dos registros coletados, garantindo maior consistência para as etapas posteriores do trabalho.
A solução desenvolvida segue o conceito de ETL (Extract, Transform and Load), amplamente utilizado em projetos de Engenharia de Dados. Nesse modelo, os dados são extraídos da fonte original, transformados conforme as necessidades do projeto e posteriormente armazenados em uma estrutura adequada para futuras análises.
A expectativa é que a base construída nesta entrega sirva como fundamento para a próxima etapa do projeto, na qual serão desenvolvidas análises exploratórias, visualizações e aplicações de técnicas de Inteligência Analítica sobre os dados coletados.
2. OBJETIVO DA COLETA
O principal objetivo da coleta foi construir uma base de dados estruturada contendo informações sobre despesas parlamentares disponibilizadas pela Câmara dos Deputados. A intenção não foi apenas obter os registros disponíveis na API, mas também organizar esses dados de forma adequada para utilização em análises futuras.
Para atingir esse objetivo foram coletadas informações relacionadas aos parlamentares, suas respectivas unidades federativas, partidos políticos e registros de despesas realizadas. Além disso, foram considerados atributos financeiros e temporais que poderão ser utilizados posteriormente em análises estatísticas e processos de mineração de dados.
Os dados coletados permitem investigar diferentes aspectos dos gastos parlamentares, incluindo a distribuição das despesas entre parlamentares, possíveis diferenças entre partidos políticos, comportamento por unidade federativa e concentração de gastos em determinadas categorias de despesa.
Outro objetivo importante desta etapa foi validar a viabilidade técnica da coleta automatizada por meio da API pública. Dessa forma, buscou-se verificar a consistência dos dados retornados, a estabilidade das consultas realizadas e a adequação da estrutura disponibilizada para construção do banco de dados do projeto.
Como delimitação metodológica, a coleta foi realizada considerando apenas um recorte temporal específico definido durante o desenvolvimento do script. Essa estratégia foi adotada para reduzir o volume inicial de processamento, facilitar os testes realizados no ambiente Google Colab e garantir maior controle sobre os dados utilizados nesta etapa do projeto.
A base produzida servirá como fonte para as análises previstas na segunda entrega, incluindo geração de indicadores, visualizações gráficas e aplicação de técnicas de aprendizado de máquina.

3. API ESCOLHIDA E JUSTIFICATIVA
Para o desenvolvimento deste projeto foi escolhida a API de Dados Abertos da Câmara dos Deputados. A decisão foi tomada após a análise das opções de bases públicas disponibilizadas para consulta, levando em consideração critérios como disponibilidade dos dados, facilidade de acesso, qualidade da documentação e potencial para aplicação das técnicas estudadas na disciplina.
Outro fator que influenciou a escolha foi a possibilidade de trabalhar com dados reais relacionados à administração pública, permitindo desenvolver um projeto com aplicação prática e potencial para futuras análises sobre gastos parlamentares. Além disso, a estrutura da API mostrou-se adequada para a construção de um pipeline de dados completo, envolvendo coleta, tratamento, armazenamento e posterior análise das informações.
3.1 Disponibilidade dos Dados
Durante a fase inicial do projeto foi realizada uma análise exploratória da documentação da API para identificar quais conjuntos de dados poderiam ser utilizados. Verificou-se que a plataforma disponibiliza informações relacionadas a parlamentares, despesas, partidos políticos, legislaturas, proposições e eventos legislativos.
Como o objetivo desta etapa estava relacionado à construção de uma base para análise de gastos públicos, foram priorizados os dados referentes aos deputados e às despesas parlamentares. Os dados são disponibilizados em formato JSON, facilitando a integração com aplicações desenvolvidas em Python.
3.2 Estrutura dos Dados
Um dos aspectos observados durante a avaliação da API foi a organização dos dados disponibilizados. Os registros apresentam identificadores únicos, atributos bem definidos e relacionamentos que permitem a construção de um modelo relacional consistente.
Essa característica facilitou o processo de modelagem da base de dados e permitiu estabelecer associações entre parlamentares e suas respectivas despesas, contribuindo para a organização das informações coletadas.
3.3 Potencial Analítico
A base escolhida apresenta potencial para diferentes tipos de análise que serão explorados nas próximas etapas do projeto. Entre as possibilidades identificadas estão análises descritivas dos gastos parlamentares, construção de indicadores, elaboração de dashboards interativos e aplicação de técnicas de agrupamento e detecção de padrões.
Além disso, a existência de informações temporais e financeiras permite realizar comparações entre períodos, categorias de despesas e perfis de parlamentares, ampliando as possibilidades de exploração analítica dos dados.
3.4 Documentação
Outro aspecto que contribuiu para a escolha da API foi a qualidade da documentação disponibilizada pela Câmara dos Deputados. A documentação apresenta descrição dos endpoints, parâmetros de consulta, exemplos de requisições e estrutura das respostas retornadas.
Durante o desenvolvimento do projeto a documentação foi utilizada como principal referência para implementação da rotina de coleta, reduzindo o tempo necessário para integração e facilitando a compreensão do funcionamento dos serviços disponibilizados.

4. ENDPOINTS UTILIZADOS
Após a análise da documentação da API da Câmara dos Deputados foram selecionados os endpoints que apresentavam as informações necessárias para os objetivos definidos neste projeto. A escolha priorizou recursos capazes de fornecer dados cadastrais dos parlamentares e informações relacionadas às despesas realizadas durante o exercício de suas atividades.
Os endpoints utilizados foram suficientes para construir a base de dados proposta nesta etapa e permitiram estabelecer o relacionamento entre os parlamentares e os registros de despesas coletados.

4.1 Endpoint de Deputados

Objetivo: Obter informações cadastrais dos parlamentares.
Endpoint: /api/v2/deputados
Principais campos utilizados:
•	id
•	nome
•	siglaPartido
•	siglaUf

4.2 Endpoint de Despesas Parlamentares

Objetivo: Obter registros detalhados de despesas associadas a cada parlamentar.
Endpoint: /api/v2/deputados/{id}/despesas
Principais campos utilizados:
•	tipoDespesa
•	valorLiquido
•	dataDocumento
•	nomeFornecedor
•	cnpjCpfFornecedor

4.3 Estratégia de Coleta
A estratégia adotada foi dividida em duas etapas. Inicialmente foi realizada a consulta ao endpoint de deputados para obtenção da lista de parlamentares disponíveis na API. Em seguida, para cada deputado identificado, foi executada uma nova consulta ao endpoint de despesas, permitindo recuperar os registros financeiros associados ao respectivo parlamentar.
Durante os testes realizados foi possível observar que a API retorna os dados em múltiplas páginas quando o volume de registros é elevado. Por esse motivo, foi necessário implementar uma rotina de paginação automática para garantir que todas as informações disponíveis fossem recuperadas corretamente.
Além disso, foi definido um recorte temporal para a coleta das despesas, restringindo os registros ao período selecionado para análise. Essa decisão teve como objetivo reduzir o volume de processamento inicial e facilitar a validação do pipeline desenvolvido nesta primeira etapa do projeto.
 
Figura 1 – Arquitetura da solução desenvolvida para coleta, transformação e armazenamento dos dados provenientes da API da Câmara dos Deputados. A Figura 1 apresenta a arquitetura geral do pipeline de dados implementado. O fluxo inicia na API de Dados Abertos da Câmara dos Deputados, passando pelas etapas de coleta automatizada, transformação dos dados e persistência em banco MySQL, resultando em uma base estruturada para futuras análises.

4.4 Delimitação Temporal e Critério de Amostragem
Para esta primeira etapa foi adotado um recorte temporal considerando apenas as despesas registradas no ano de 2025. A utilização desse filtro permitiu trabalhar com uma base mais recente e ao mesmo tempo manter um volume de dados compatível com o ambiente utilizado para desenvolvimento e testes.
Também foi adotado um limite de amostragem durante a fase inicial de validação do código. Essa estratégia possibilitou verificar o funcionamento da coleta, dos tratamentos aplicados e do armazenamento dos dados antes da execução sobre conjuntos maiores de registros.
A utilização de amostras controladas é uma prática comum em projetos de Engenharia de Dados, especialmente durante as etapas de desenvolvimento, validação e ajuste dos pipelines de processamento.

A escolha do ano de 2025 ocorreu por se tratar do período mais recente com dados disponíveis durante o desenvolvimento do projeto. A utilização de informações atuais contribui para que as análises realizadas nas próximas etapas representem com maior fidelidade o cenário recente dos gastos parlamentares.

5. EXPLICAÇÃO DO SCRIPT DE COLETA

O script foi desenvolvido em Python utilizando as bibliotecas Requests, Pandas, SQLAlchemy e o conector MySQL.
A arquitetura do código foi organizada em módulos independentes.

  
Figura 2 – Fluxo operacional da rotina automatizada de coleta de dados.

5.1 Conexão com a API

A comunicação com a API ocorre por meio de requisições HTTP GET. 
Foi implementada validação do código de resposta HTTP para garantir sucesso da operação. Respostas diferentes de HTTP 200 são registradas como erro.

5.2 Paginação

A API limita a quantidade de registros retornados por requisição. Para contornar essa limitação foi implementado mecanismo de paginação automática. O script identifica a existência de páginas subsequentes e continua realizando requisições até que todos os registros sejam coletados.

5.3 Tratamento de Erros
Durante o desenvolvimento do script foram considerados cenários como falhas de conexão, indisponibilidade temporária da API, respostas inválidas e interrupções durante o processo de coleta.
Para esses casos foram implementadas estruturas de tratamento de exceções utilizando os recursos nativos do Python. Quando uma ocorrência é identificada, o sistema exibe mensagens informativas no terminal e continua a execução sempre que possível, evitando que uma falha isolada interrompa todo o processo de coleta.
Essa abordagem contribui para aumentar a robustez do pipeline e facilita a identificação de eventuais problemas durante a execução.
5.4 Conversão para Estrutura Tabular

Os dados recebidos em formato JSON são convertidos para DataFrames Pandas.
Essa conversão permite:
•	Limpeza dos dados;
•	Validação dos campos;
•	Transformações necessárias;
•	Exportação para banco de dados.

5.5 Persistência

Optou-se pela utilização do MySQL para o armazenamento dos dados deste projeto, por se tratar de um
banco relacional robusto, já disponível no ambiente de desenvolvimento, e adequado tanto ao volume de
dados utilizado nos testes iniciais quanto a uma futura evolução para ambiente de produção.

A escolha permitiu concentrar os esforços na construção e validação do pipeline de coleta já sobre uma
solução de armazenamento próxima da que seria utilizada em um cenário profissional.

Após validação, os dados são armazenados em banco MySQL. A utilização do MySQL foi escolhida por:
•	Suporte a múltiplos usuários e conexões concorrentes;
•	Recursos completos de integridade referencial (chaves estrangeiras, índices);
•	Maior aderência a um ambiente de produção real;
•	Boa integração com Python por meio de SQLAlchemy/mysql-connector.



6. TRATAMENTOS REALIZADOS NOS DADOS

Após a coleta foram realizadas etapas de preparação dos dados.
 
Figura 3 – Processo ETL aplicado aos dados coletados.

Além dos tratamentos descritos anteriormente, foram realizadas verificações exploratórias sobre a estrutura dos dados retornados pela API. Essa etapa permitiu identificar inconsistências de preenchimento, diferenças de formatação entre campos e registros com informações ausentes.
A análise preliminar dos dados também auxiliou na definição dos tipos de dados utilizados no banco MySQL, contribuindo para uma estrutura mais consistente e adequada às análises previstas para a próxima etapa do projeto.

6.1 Tratamento de Valores Nulos

Foi realizada identificação de campos ausentes. Dependendo da relevância do atributo foram adotadas estratégias de:
•	Substituição;
•	Exclusão;
•	Manutenção controlada.

6.2 Conversão de Datas

Campos originalmente recebidos como texto foram convertidos para formato DateTime.
Essa transformação permitirá análises temporais futuras.

6.3 Conversão Numérica

Valores monetários foram convertidos para tipos numéricos compatíveis com operações estatísticas.

6.4 Remoção de Duplicidades

Foi realizada verificação de registros repetidos utilizando combinações de identificadores e atributos-chave.

6.5 Padronização de Campos

Nomes de colunas foram padronizados seguindo convenção snake_case.
Exemplo:
valorLiquido → valor_liquido
dataDocumento → data_documento




7. MODELO DE DADOS
O modelo de dados desenvolvido para esta primeira etapa foi construído com o objetivo de organizar as informações coletadas pela API da Câmara dos Deputados de forma simples e consistente. Como o foco principal estava na validação da coleta automatizada e na construção da base inicial do projeto, foram definidas duas entidades principais: DEPUTADOS e DESPESAS.

A entidade DEPUTADOS armazena as informações cadastrais dos parlamentares retornadas pela API. Nela foram mantidos atributos necessários para identificação dos registros e futuras análises, como nome do parlamentar, partido político e unidade federativa de representação.

Principais atributos:
• id_deputado
• nome
• sigla_partido
• sigla_uf

A entidade DESPESAS armazena os registros financeiros associados aos parlamentares. Cada registro representa uma despesa individual retornada pela API e contém informações relacionadas ao valor, data e tipo da despesa realizada.

Principais atributos:
• id_deputado
• tipo_despesa
• valor_liquido
• data_documento
• nome_fornecedor
• cnpj_cpf_fornecedor

A estrutura adotada permite relacionar cada despesa ao respectivo parlamentar por meio do identificador do deputado, possibilitando consultas e análises futuras sobre gastos públicos.
O modelo foi construído seguindo princípios básicos de modelagem relacional, buscando reduzir redundâncias e facilitar a manutenção dos dados armazenados.

DER Proposto (Erp)
       


























Figura 4 – Modelo Entidade-Relacionamento da base de dados desenvolvida.

Diagrama Entidade-Relacionamento (DER): O modelo de dados foi estruturado seguindo os princípios de normalização relacional, separando as informações cadastrais dos parlamentares das informações transacionais de despesas.

Justificativa da Modelagem: A entidade DEPUTADOS armazena informações cadastrais dos parlamentares. A entidade DESPESAS armazena informações transacionais referentes aos gastos realizados.
Foi adotado relacionamento do tipo 1:N entre as entidades DEPUTADOS e DESPESAS. Isso significa que um parlamentar pode possuir diversos registros de despesas, enquanto cada despesa está associada a apenas um parlamentar.
Essa estrutura foi considerada suficiente para os objetivos desta primeira etapa do projeto e permite expandir o modelo futuramente caso seja necessário incorporar novas entidades ou fontes de dados.
Tabela Deputados

Representa os parlamentares.
•	Chave Primária:
•	id_deputado

Atributos:
•	nome
•	partido
•	uf

Tabela Despesas

Representa os gastos parlamentares.
•	Chave Primária:
•	id_despesa
•	Chave Estrangeira:
•	id_deputado

Atributos:
•	tipo_despesa
•	valor_liquido
•	data_documento
•	fornecedor

Relacionamento
•	Deputado (1) -------- (N) Despesa
•	Um parlamentar pode possuir diversas despesas registradas.
•	Cada despesa pertence a apenas um parlamentar.


8. DICIONÁRIO INICIAL DE DADOS
Tabela 3 – Dicionário Inicial de Dados
Campo	Tipo	Descrição	Exemplo
id_deputado	INTEGER	Identificador único do parlamentar	204521
nome	TEXT	Nome do parlamentar	João Silva
sigla_partido	TEXT	Partido político	PL
sigla_uf	TEXT	Unidade Federativa	DF
tipo_despesa	TEXT	Categoria da despesa	Combustíveis
valor_liquido	REAL	Valor efetivamente pago	1250,75
data_documento	DATE	Data da despesa	2025-03-15
nome_fornecedor	TEXT	Beneficiário do pagamento	Posto Exemplo Ltda
cnpj_cpf_fornecedor	TEXT	Documento do fornecedor	12.345.678/0001-90

9. EVIDÊNCIAS DA EXECUÇÃO

Após a implementação do script, foram realizados testes de execução no ambiente Google Colab com o objetivo de validar todas as etapas do pipeline desenvolvido.

Durante os testes foi possível confirmar o funcionamento das rotinas de conexão com a API, coleta dos dados, tratamento inicial das informações e persistência em banco MySQL.

As evidências apresentadas neste relatório incluem:

• Execução do script de coleta no ambiente Google Colab;
• Conversão dos dados retornados pela API para estruturas DataFrame utilizando a biblioteca Pandas;
• Verificação da quantidade de registros coletados;
• Visualização dos primeiros registros obtidos;
• Criação e armazenamento do banco MySQL contendo as tabelas geradas pelo processo de coleta.

As capturas de tela apresentadas nas figuras correspondentes demonstram o funcionamento das etapas implementadas e servem como validação prática da solução desenvolvida.
9.1 Limitações Encontradas Durante a Coleta
Durante a implementação da rotina de coleta foram identificadas algumas limitações inerentes ao processo de obtenção de dados por meio de APIs públicas. A principal limitação refere-se à necessidade de paginação das consultas, uma vez que a API não retorna todos os registros em uma única requisição. Dessa forma, tornou-se necessário implementar mecanismos automáticos para navegação entre páginas.
Também foram observadas situações envolvendo campos nulos ou incompletos em determinados registros, exigindo procedimentos adicionais de validação e tratamento. 
Outra limitação está relacionada à dependência da disponibilidade dos serviços da API. Interrupções temporárias, lentidão ou indisponibilidade do serviço podem impactar diretamente o processo de coleta.
Por fim, destaca-se que alterações futuras na estrutura dos endpoints ou nos formatos de resposta poderão exigir adaptações no código desenvolvido.

10. RESULTADOS PRELIMINARES

A execução da rotina de coleta permitiu validar a integração com a API da Câmara dos Deputados e confirmar a viabilidade da construção da base de dados proposta para o projeto.

Os testes realizados demonstraram que o pipeline foi capaz de recuperar os registros disponibilizados pela API, converter as informações para estruturas tabulares utilizando Pandas e armazenar os dados em banco MySQL para utilização posterior.

Também foi possível validar os mecanismos de paginação implementados, garantindo a recuperação dos registros distribuídos em múltiplas páginas de resposta.

Os resultados obtidos nesta etapa servem como evidência da viabilidade técnica da solução proposta e estabelecem a base necessária para as análises previstas na próxima entrega.

11. CONSIDERAÇÕES PARCIAIS
A execução desta primeira etapa permitiu compreender melhor o funcionamento da API da Câmara dos Deputados e os desafios envolvidos na construção de um pipeline de dados. Além da implementação da coleta automatizada, foi possível realizar os primeiros testes de armazenamento e organização das informações, criando uma base consistente para continuidade do projeto.
Na próxima etapa serão realizadas análises exploratórias dos dados coletados, construção de visualizações gráficas e aplicação de técnicas de Inteligência Analítica com o objetivo de identificar padrões e gerar informações relevantes a partir da base construída.
12. FLUXOGRAMA DO PIPELINE ETL (Fluxo Geral da Solução)

O pipeline desenvolvido neste projeto foi estruturado seguindo o processo ETL (Extract, Transform and Load), amplamente utilizado em projetos de Engenharia de Dados para obtenção, preparação e armazenamento de informações provenientes de diferentes fontes.

A etapa de extração teve início com a realização das consultas à API da Câmara dos Deputados. Nessa fase foram recuperados os dados cadastrais dos parlamentares e os registros de despesas disponibilizados pelo serviço.

Após a obtenção dos dados, foi executada a etapa de transformação. Durante esse processo foram realizados tratamentos voltados à padronização dos campos, conversão de tipos de dados, remoção de registros duplicados e adequação das informações para armazenamento em banco de dados.

A etapa final correspondeu ao carregamento dos dados tratados para o banco MySQL criado para o projeto. Essa estrutura permitirá que as informações sejam utilizadas posteriormente em análises exploratórias, visualizações gráficas e aplicações de técnicas de Inteligência Analítica.

A Figura correspondente apresenta de forma resumida o fluxo implementado durante a construção do pipeline.

 
Explicação Técnica
A arquitetura segue o padrão ETL (Extract, Transform, Load).

 

	Extract: Coleta dos dados diretamente da API através de requisições HTTP.
	Transform: Aplicação de tratamentos:
•	normalização;
•	remoção de inconsistências;
•	padronização de tipos;
•	tratamento de nulos;
•	validação de registros.
	Load: Persistência em banco MySQL para consumo posterior por ferramentas analíticas.

13. EXPLICAÇÃO TÉCNICA DETALHADA DO SCRIPT PYTHON

O desenvolvimento da rotina de coleta foi realizado utilizando a linguagem Python devido à sua ampla utilização em projetos de Ciência de Dados e Engenharia de Dados. A implementação foi executada no ambiente Google Colab, o que permitiu testar o funcionamento do pipeline de forma simples e integrada.

O script foi organizado em etapas bem definidas, contemplando conexão com a API, coleta dos registros, tratamento inicial dos dados e persistência em banco MySQL. Essa divisão facilitou a validação individual de cada componente e permitiu identificar eventuais falhas durante o desenvolvimento.

O ambiente Google Colab foi utilizado durante o desenvolvimento por oferecer uma estrutura pronta para execução de notebooks Python sem necessidade de configuração local. Além disso, sua integração com bibliotecas de análise de dados facilitou os testes realizados durante a implementação do pipeline.

A seguir são descritas as principais partes da implementação.

Bibliotecas Utilizadas
import requests
import pandas as pd
import time
from sqlalchemy import create_engine, text

requests
Responsável pela comunicação com a API.

pandas
Responsável pela manipulação tabular dos dados.

sqlalchemy (com mysql-connector-python)
Responsável pela conexão e persistência dos dados no banco MySQL.

time
Utilizado para controle de requisições e prevenção de sobrecarga da API.

Definição da URL Base
BASE_URL = "https://dadosabertos.camara.leg.br/api/v2"
Centraliza o endereço principal da API.
Caso a URL seja alterada futuramente, basta modificar um único ponto do código.

Função de Coleta dos Deputados

A primeira etapa da coleta consiste na consulta ao endpoint responsável por disponibilizar os dados dos parlamentares. Foi criada uma função específica para realizar essa operação, permitindo reutilização do código e maior organização da implementação.

Os dados retornados pela API são recebidos em formato JSON e posteriormente convertidos para DataFrame utilizando a biblioteca Pandas. Essa conversão facilita os tratamentos aplicados nas etapas seguintes do pipeline.

Requisição HTTP
response = requests.get(url)
Envia requisição GET ao endpoint.

Validação da Resposta
if response.status_code == 200:
Código HTTP 200 indica sucesso.
Outros códigos:
Código	Significado
200	Sucesso
400	Requisição inválida
401	Não autorizado
404	Recurso não encontrado
500	Erro interno

Conversão JSON
dados = response.json()
Transforma a resposta da API em objeto Python.
Exemplo:
{
    "dados":[...]
}

Conversão para DataFrame
df = pd.DataFrame(dados["dados"])
Transforma os registros em estrutura tabular.
Exemplo:
id	nome
204521	João

Coleta das Despesas

Após a obtenção da lista de parlamentares, o script realiza consultas individuais ao endpoint de despesas para cada deputado identificado durante a primeira etapa da coleta.

Essa abordagem foi adotada porque a API disponibiliza as despesas associadas a cada parlamentar de forma separada. Dessa forma, tornou-se necessário percorrer a lista de deputados e executar novas requisições para obtenção dos registros financeiros correspondentes.

Durante esse processo também foi aplicado o filtro temporal definido para o projeto, restringindo a coleta ao período selecionado para análise.

Paginação

Durante os testes realizados foi observado que a API não retorna todos os registros em uma única resposta quando o volume de dados é elevado. Para resolver essa limitação foi implementado um mecanismo de paginação automática.

O algoritmo verifica a existência de páginas adicionais e continua realizando novas consultas até que todos os registros disponíveis sejam recuperados. Essa estratégia garante maior integridade dos dados coletados e reduz o risco de perda de informações durante a execução.

Tratamento de Erros
try:
Captura falhas de:
•	conexão;
•	timeout;
•	interrupções da API.
except requests.exceptions.RequestException:
Impede encerramento inesperado do programa.

Tratamento dos Dados
Datas
df["data_documento"] = pd.to_datetime(
    df["data_documento"]
)
Permite análises temporais.

Valores Financeiros
df["valor_liquido"] = (
    df["valor_liquido"]
    .astype(float)
)
Permite cálculos estatísticos.

Remoção de Duplicidades
df.drop_duplicates(inplace=True)
Evita registros repetidos.

Persistência MySQL
Criação da Conexão
engine = create_engine(
    "mysql+mysqlconnector://integrador:senha@localhost:3306/projeto_integrador"
)
Abre conexão com o banco relacional MySQL.

Escrita da Tabela
df.to_sql(
    "despesas",
    engine,
    if_exists="append",
    index=False
)
Insere os registros na tabela já modelada previamente via DDL (ver sql/schema.sql),
respeitando chave primária, chave estrangeira e índices definidos.

Encerramento
engine.dispose()
Libera as conexões do pool com o banco de dados.

Considerações sobre a Implementação

A construção do script permitiu colocar em prática conceitos estudados ao longo da disciplina, especialmente aqueles relacionados à integração com APIs, tratamento de dados e armazenamento de informações em banco de dados.

Além dos aspectos técnicos, o desenvolvimento do pipeline possibilitou compreender desafios comuns em projetos de dados, como tratamento de inconsistências, controle do volume de informações processadas e necessidade de validação dos registros obtidos.

A implementação desenvolvida servirá como base para as atividades previstas na segunda etapa do projeto, na qual os dados coletados serão explorados por meio de análises estatísticas, visualizações e técnicas de Inteligência Analítica.
Referências

CÂMARA DOS DEPUTADOS. Dados Abertos da Câmara dos Deputados. Disponível em: https://dadosabertos.camara.leg.br. Acesso em: junho de 2026.

MCKINNEY, Wes. Python for Data Analysis. 3. ed. Sebastopol: O'Reilly Media, 2022.
PANDAS DEVELOPMENT TEAM. Pandas Documentation. Disponível em: 
https://pandas.pydata.org. Acesso em: junho de 2026.

PYTHON SOFTWARE FOUNDATION. Python Documentation. Disponível em: https://docs.python.org. Acesso em: junho de 2026.

ORACLE CORPORATION. MySQL 9.0 Reference Manual. Disponível em: https://dev.mysql.com/doc/. Acesso em: junho de 2026.

SQLALCHEMY. SQLAlchemy Documentation. Disponível em: https://docs.sqlalchemy.org. Acesso em: junho de 2026.








<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>Dashboard Gastos Parlamentares</title>
<script src="https://cdn.plot.ly/plotly-2.35.2.min.js"></script>
<style>
body {font-family: Arial; margin:20px; background:#f5f5f5;}
.grid {display:grid; grid-template-columns:repeat(4,1fr); gap:15px;}
.card {background:white; padding:15px; border-radius:8px; text-align:center;}
.chart {background:white; margin-top:20px; padding:10px; border-radius:8px;}
</style>
</head>
<body>
<h1>Dashboard - Gastos Parlamentares</h1>

<div class="grid">
<div class="card"><h3>Total Gasto</h3><h2>R$ 2,711,632.98</h2></div>
<div class="card"><h3>Total de Despesas</h3><h2>2119</h2></div>
<div class="card"><h3>Deputados</h3><h2>30</h2></div>
<div class="card"><h3>Média por Deputado</h3><h2>R$ 90,387.77</h2></div>
</div>

<div id="top10" class="chart"></div>
<div id="partidos" class="chart"></div>
<div id="ufs" class="chart"></div>
<div id="mensal" class="chart"></div>
<div id="mensalqtd" class="chart"></div>

<script>
Plotly.newPlot('top10',[{
x:[118506.62, 109558.24, 108733.23999999999, 105202.69, 102974.45999999999, 96599.3, 95922.94, 94278.85, 91638.33, 91599.52],
y:["Deputado 22", "Deputado 28", "Deputado 16", "Deputado 11", "Deputado 24", "Deputado 14", "Deputado 10", "Deputado 4", "Deputado 30", "Deputado 12"],
type:'bar',orientation:'h'
}],{title:'Top 10 Deputados por Gastos'});

Plotly.newPlot('partidos',[{
x:["MDB", "PL", "PSD", "PT", "UNI\u00c3O"],
y:[318670.29, 469470.85, 370944.9, 647013.97, 905532.97],
type:'bar'
}],{title:'Gastos por Partido'});

Plotly.newPlot('ufs',[{
x:["BA", "DF", "MG", "RJ", "SP"],
y:[651443.61, 258881.78, 696191.07, 609111.02, 496005.5],
type:'bar'
}],{title:'Gastos por UF'});

Plotly.newPlot('mensal',[{
x:[1, 2, 3, 4, 5, 6],
y:[454181.98, 464254.85000000003, 453756.98, 429949.47, 432779.45999999996, 476710.24],
type:'scatter'
}],{title:'Evolução Mensal dos Gastos'});

Plotly.newPlot('mensalqtd',[{
x:[1, 2, 3, 4, 5, 6],
y:[363, 382, 346, 308, 366, 354],
type:'scatter'
}],{title:'Quantidade de Despesas por Mês'});
</script>
</body>
</html>

RESULTADOS DA ANÁLISE EXPLORATÓRIA

A base analisada é composta por 180 registros agregados de despesas parlamentares, contemplando 30 deputados distribuídos entre cinco partidos políticos e cinco unidades federativas. O período analisado compreende os meses de janeiro a junho.

A análise estatística inicial indicou valor médio de despesas de R$ 15.064,63 por registro, com mediana de R$ 14.909,12. O valor mínimo observado foi de R$ 6.286,66, enquanto o valor máximo atingiu R$ 30.410,93. O desvio padrão calculado foi de R$ 3.998,43, demonstrando variação moderada entre os registros analisados.

Ao analisar os gastos acumulados por parlamentar, observou-se que os maiores volumes de despesas ficaram concentrados em um grupo reduzido de deputados. O parlamentar identificado como Deputado 22 apresentou o maior valor acumulado no período, totalizando R$ 118.506,62.

Na análise por partido político, verificou-se que o partido UNIÃO concentrou o maior volume de gastos da amostra, seguido por PT e PL. Já na análise por unidade federativa, Minas Gerais apresentou o maior montante acumulado de despesas, seguido pelos estados da Bahia e Rio de Janeiro.

Como complemento à análise exploratória, foi aplicada a técnica de clusterização K-Means utilizando como variáveis o valor total das despesas e a quantidade de despesas registradas. O algoritmo identificou três grupos distintos de parlamentares, permitindo segmentar a amostra em perfis de gasto baixo, intermediário e elevado.

Os resultados obtidos demonstram o potencial analítico da base construída e servem como fundamento para a elaboração do dashboard interativo e demais análises previstas nesta etapa do projeto.

