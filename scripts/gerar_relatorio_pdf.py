"""Gera o PDF do Relatório Final do Projeto Integrador.

Reaproveita o texto consolidado em "projeto_integrador_gastos_publicos v3.MD"
e os artefatos visuais reais da aplicação (diagramas Graphviz gerados em
assets/relatorio/ e screenshots do dashboard/ML capturados da aplicação em
execução) para montar o documento final entregável.

Uso:
    .venv/bin/python scripts/gerar_relatorio_pdf.py
"""

from pathlib import Path

from fpdf import FPDF
from fpdf.enums import XPos, YPos

ROOT = Path(__file__).resolve().parent.parent
ASSETS = ROOT / "assets" / "relatorio"
SAIDA = ASSETS / "relatorio_final_projeto_integrador.pdf"

ALUNO = "Eric Rocha Pitman Junior"
MATRICULA = "2486031008"
CURSO = "Projeto Integrador em Big Data e Inteligência Analítica [202691]"
PROFESSOR = "Francisco Filho"

AZUL = (44, 62, 112)
CINZA = (90, 90, 90)
PRETO = (20, 20, 20)

FONT_DIR = Path("/System/Library/Fonts/Supplemental")


class RelatorioPDF(FPDF):
    def __init__(self):
        super().__init__(format="A4")
        self.add_font("Arial", "", str(FONT_DIR / "Arial.ttf"))
        self.add_font("Arial", "B", str(FONT_DIR / "Arial Bold.ttf"))
        self.add_font("Arial", "I", str(FONT_DIR / "Arial Italic.ttf"))
        self.set_auto_page_break(auto=True, margin=20)
        self.set_margins(20, 18, 20)

    def multi_cell(self, w=0, h=None, text="", *args, **kwargs):
        kwargs.setdefault("new_x", XPos.LMARGIN)
        kwargs.setdefault("new_y", YPos.NEXT)
        return super().multi_cell(w, h, text, *args, **kwargs)

    def header(self):
        if self.page_no() <= 1:
            return
        self.set_font("Arial", "", 8)
        self.set_text_color(*CINZA)
        self.cell(0, 8, "Relatório Final - Projeto Integrador em Big Data e Inteligência Analítica", align="L")
        self.ln(10)
        self.set_draw_color(*AZUL)
        self.set_line_width(0.3)
        self.line(20, 16, 190, 16)

    def footer(self):
        if self.page_no() <= 1:
            return
        self.set_y(-15)
        self.set_font("Arial", "", 8)
        self.set_text_color(*CINZA)
        self.cell(0, 10, f"Página {self.page_no()}", align="C")

    # ---- helpers de layout -------------------------------------------------
    def titulo_capitulo(self, numero: str, texto: str):
        self.set_font("Arial", "B", 15)
        self.set_text_color(*AZUL)
        self.ln(4)
        self.multi_cell(0, 8, f"{numero}. {texto}")
        self.set_draw_color(*AZUL)
        self.set_line_width(0.5)
        y = self.get_y() + 1
        self.line(20, y, 190, y)
        self.ln(5)
        self.set_text_color(*PRETO)

    def subtitulo(self, texto: str):
        self.set_font("Arial", "B", 12)
        self.set_text_color(*AZUL)
        self.ln(2)
        self.multi_cell(0, 7, texto)
        self.ln(1)
        self.set_text_color(*PRETO)

    def paragrafo(self, texto: str, justify: bool = True):
        self.set_font("Arial", "", 10.5)
        self.set_text_color(*PRETO)
        self.multi_cell(0, 5.8, texto, align="J" if justify else "L")
        self.ln(2)

    def bullet_list(self, itens):
        self.set_font("Arial", "", 10.5)
        self.set_text_color(*PRETO)
        for item in itens:
            x = self.get_x()
            self.cell(5, 5.8, "-")
            self.multi_cell(0, 5.8, item)
            self.set_x(x)
        self.ln(1)

    def destaque(self, texto: str):
        self.set_fill_color(238, 242, 251)
        self.set_font("Arial", "I", 10)
        self.set_text_color(*AZUL)
        self.set_x(self.l_margin)
        self.multi_cell(0, 5.8, texto, fill=True)
        self.ln(2)
        self.set_text_color(*PRETO)

    def figura(self, caminho: Path, legenda: str, largura: float = 165):
        if self.get_y() > 230:
            self.add_page()
        self.image(str(caminho), x=(210 - largura) / 2, w=largura)
        self.ln(1)
        self.set_font("Arial", "I", 9)
        self.set_text_color(*CINZA)
        self.multi_cell(0, 5, legenda, align="C")
        self.ln(3)
        self.set_text_color(*PRETO)

    def quebrar_se_necessario(self, altura_estimada: float):
        if self.get_y() + altura_estimada > 270:
            self.add_page()


def montar_capa(pdf: RelatorioPDF):
    pdf.add_page()
    pdf.ln(30)
    pdf.set_font("Arial", "B", 13)
    pdf.set_text_color(*CINZA)
    pdf.multi_cell(0, 7, CURSO, align="C")
    pdf.multi_cell(0, 7, f"Professor: {PROFESSOR}", align="C")
    pdf.ln(25)

    pdf.set_font("Arial", "B", 22)
    pdf.set_text_color(*AZUL)
    pdf.multi_cell(0, 11, "RELATÓRIO FINAL DO PROJETO", align="C")
    pdf.set_font("Arial", "B", 16)
    pdf.multi_cell(0, 9, "PIPELINE DE INTELIGÊNCIA ANALÍTICA EM\nGASTOS PÚBLICOS", align="C")
    pdf.ln(6)
    pdf.set_font("Arial", "", 12)
    pdf.set_text_color(*PRETO)
    pdf.multi_cell(
        0,
        7,
        "Coleta, modelagem, dashboard interativo e detecção de\n"
        "despesas atípicas com Machine Learning sobre dados abertos\n"
        "da Câmara dos Deputados",
        align="C",
    )

    pdf.ln(35)
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 7, f"Aluno: {ALUNO}", align="C")
    pdf.ln(7)
    pdf.cell(0, 7, f"Matrícula: {MATRICULA}", align="C")
    pdf.ln(20)

    pdf.set_font("Arial", "", 10)
    pdf.set_text_color(*CINZA)
    pdf.cell(0, 6, "Junho de 2026", align="C")


def montar_sumario_executivo(pdf: RelatorioPDF):
    pdf.add_page()
    pdf.titulo_capitulo("1", "INTRODUÇÃO")
    pdf.paragrafo(
        "Este relatório consolida as duas entregas do Projeto Integrador da disciplina de Big Data "
        "e Inteligência Analítica, documentando o pipeline completo de dados construído sobre a API "
        "de Dados Abertos da Câmara dos Deputados: da coleta automatizada via API e armazenamento em "
        "banco relacional MySQL, passando pela modelagem dos dados, até a aplicação web interativa "
        "com dashboard analítico e um módulo de Machine Learning para detecção de despesas atípicas."
    )
    pdf.paragrafo(
        "A escolha do tema — gastos parlamentares — se deu pela relevância das informações para "
        "estudos de transparência pública e pela disponibilidade de uma API bem documentada, "
        "permitindo a aplicação prática de conceitos de Engenharia de Dados, Business Intelligence "
        "e Aprendizado de Máquina sobre uma base de dados real."
    )
    pdf.paragrafo(
        "O documento está organizado seguindo o fluxo do próprio pipeline: origem e justificativa "
        "dos dados, estratégia de coleta e tratamento, modelo de dados, arquitetura da aplicação "
        "analítica, dashboard, técnica de Machine Learning aplicada, resultados obtidos e, por fim, "
        "a declaração detalhada sobre o uso de ferramentas de Inteligência Artificial como apoio ao "
        "longo do desenvolvimento."
    )

    pdf.subtitulo("Objetivo Geral")
    pdf.destaque(
        "Desenvolver uma solução analítica capaz de coletar, armazenar, tratar, analisar e "
        "interpretar dados públicos relacionados a gastos governamentais, utilizando técnicas de "
        "Engenharia de Dados, Business Intelligence e Machine Learning."
    )

    pdf.subtitulo("Objetivos Específicos")
    pdf.bullet_list(
        [
            "Consumir dados de uma API pública (Dados Abertos da Câmara dos Deputados);",
            "Desenvolver rotina automatizada de coleta, com paginação e tratamento de erros;",
            "Modelar e implementar uma base de dados relacional (MySQL);",
            "Construir um dicionário de dados e o Diagrama Entidade-Relacionamento (DER);",
            "Realizar análise exploratória e construir indicadores;",
            "Construir um dashboard interativo com gráficos e leitura textual automática;",
            "Aplicar uma técnica de Machine Learning adequada à detecção de anomalias;",
            "Interpretar os resultados obtidos e discutir limitações;",
            "Apresentar tecnicamente toda a solução desenvolvida neste relatório.",
        ]
    )


def montar_api(pdf: RelatorioPDF):
    pdf.add_page()
    pdf.titulo_capitulo("2", "API ESCOLHIDA, ENDPOINTS E ESTRATÉGIA DE COLETA")
    pdf.paragrafo(
        "Foi escolhida a API de Dados Abertos da Câmara dos Deputados "
        "(https://dadosabertos.camara.leg.br/api/v2), em formato JSON, por reunir critérios "
        "decisivos para o projeto: dados reais sobre administração pública, documentação completa "
        "dos endpoints e parâmetros, estrutura adequada à construção de um pipeline ETL ponta a "
        "ponta e potencial analítico relevante para estudos de transparência pública."
    )

    pdf.subtitulo("Endpoints utilizados")
    pdf.bullet_list(
        [
            "/api/v2/deputados — dados cadastrais dos parlamentares "
            "(id, nome, siglaPartido, siglaUf);",
            "/api/v2/deputados/{id}/despesas — despesas associadas a cada parlamentar "
            "(tipoDespesa, valorLiquido, dataDocumento, nomeFornecedor, cnpjCpfFornecedor).",
        ]
    )

    pdf.subtitulo("Estratégia de coleta e paginação")
    pdf.paragrafo(
        "A coleta foi dividida em duas etapas: primeiro a consulta ao endpoint de deputados, "
        "para obter a lista de parlamentares; em seguida, para cada deputado identificado, uma "
        "nova consulta ao endpoint de despesas. A API retorna os registros em múltiplas páginas "
        "quando o volume é elevado, exigindo paginação automática — o script segue o link 'next' "
        "retornado em 'links' até esgotar as páginas disponíveis. Falhas de conexão, timeout e "
        "respostas inválidas são tratadas com blocos try/except, registrando o problema sem "
        "interromper a execução de todo o processo de coleta."
    )

    pdf.subtitulo("Tratamentos aplicados aos dados")
    pdf.bullet_list(
        [
            "Identificação e tratamento de valores nulos (substituição, exclusão ou manutenção "
            "controlada, conforme a relevância do campo);",
            "Conversão de datas de texto para o tipo DateTime, viabilizando análises temporais;",
            "Conversão de valores monetários para tipos numéricos compatíveis com estatística;",
            "Remoção de duplicidades via combinações de identificadores e atributos-chave;",
            "Padronização de nomes de colunas em snake_case "
            "(ex.: valorLiquido -> valor_liquido).",
        ]
    )

    pdf.figura(
        ASSETS / "diagrama_etl.png",
        "Figura 1 - Arquitetura do pipeline ETL: da API da Câmara dos Deputados até a base "
        "pronta para análise no MySQL.",
        140,
    )


def montar_modelo_dados(pdf: RelatorioPDF):
    pdf.add_page()
    pdf.titulo_capitulo("3", "MODELO DE DADOS E DICIONÁRIO DE DADOS")
    pdf.paragrafo(
        "O modelo relacional foi estruturado em três tabelas: DEPUTADOS (dados cadastrais dos "
        "parlamentares), DESPESAS (registros financeiros, em relação 1:N com DEPUTADOS através da "
        "chave estrangeira id_deputado) e LOG_IMPORTACAO (tabela de auditoria das execuções do "
        "pipeline de coleta, sem chave estrangeira para as demais). Essa separação reduz "
        "redundâncias e mantém o modelo simples o suficiente para evoluir caso novas fontes de "
        "dados sejam incorporadas no futuro."
    )

    pdf.figura(
        ASSETS / "diagrama_der.png",
        "Figura 2 - Diagrama Entidade-Relacionamento (DER) da base de dados do projeto.",
        150,
    )

    pdf.subtitulo("Dicionário de Dados (principais campos)")
    pdf.set_font("Arial", "", 9.5)
    linhas = [
        ("id_deputado", "INTEGER", "Identificador único do parlamentar"),
        ("nome", "TEXT", "Nome do parlamentar"),
        ("sigla_partido", "TEXT", "Partido político"),
        ("sigla_uf", "TEXT", "Unidade Federativa"),
        ("tipo_despesa", "TEXT", "Categoria da despesa"),
        ("valor_liquido", "REAL", "Valor efetivamente pago"),
        ("data_documento", "DATE", "Data da despesa"),
        ("nome_fornecedor", "TEXT", "Beneficiário do pagamento"),
        ("cnpj_cpf_fornecedor", "TEXT", "Documento do fornecedor"),
    ]
    larguras = (45, 30, 95)
    pdf.set_fill_color(44, 62, 112)
    pdf.set_text_color(255, 255, 255)
    pdf.set_font("Arial", "B", 9.5)
    for titulo, largura in zip(("Campo", "Tipo", "Descrição"), larguras):
        pdf.cell(largura, 7, titulo, border=1, fill=True, align="C")
    pdf.ln()
    pdf.set_text_color(*PRETO)
    pdf.set_font("Arial", "", 9.5)
    for campo, tipo, descricao in linhas:
        pdf.cell(larguras[0], 6.5, campo, border=1)
        pdf.cell(larguras[1], 6.5, tipo, border=1, align="C")
        pdf.cell(larguras[2], 6.5, descricao, border=1)
        pdf.ln()
    pdf.ln(3)

    pdf.subtitulo("Persistência")
    pdf.paragrafo(
        "Os dados tratados são persistidos em banco MySQL através de SQLAlchemy/"
        "mysql-connector-python. A escolha do MySQL se justifica pelo suporte a múltiplos "
        "usuários e conexões concorrentes, pelos recursos de integridade referencial (chaves "
        "primárias, estrangeiras e índices) e pela maior aderência a um cenário de produção real, "
        "em comparação a uma solução de armazenamento simplificada."
    )


def montar_arquitetura_app(pdf: RelatorioPDF):
    pdf.add_page()
    pdf.titulo_capitulo("4", "ARQUITETURA DA APLICAÇÃO ANALÍTICA")
    pdf.paragrafo(
        "A camada de apresentação foi construída com Streamlit, permitindo montar uma aplicação "
        "web multipáginas inteiramente em Python, sem necessidade de HTML, CSS ou frameworks de "
        "frontend dedicados. A aplicação está dividida em sete páginas, acessadas por um menu "
        "lateral, cada uma consultando o MySQL de forma independente através da mesma camada de "
        "acesso a dados construída na primeira entrega:"
    )
    pdf.bullet_list(
        [
            "O Projeto — apresentação geral do trabalho;",
            "Definições do Sistema — documentação da API, do banco, do pipeline ETL e do "
            "módulo de Machine Learning;",
            "O Código Python — código-fonte da coleta, exposto para consulta;",
            "Importação de Dados — dispara a coleta e a gravação no MySQL sob demanda;",
            "Dados Importados — exibe em tabela o que já foi salvo no banco;",
            "Dashboard Informativo — indicadores e gráficos sobre os gastos;",
            "Análise com Machine Learning — detecção de despesas atípicas;",
            "Relatório Final do Projeto — leitura e download deste relatório em PDF.",
        ]
    )
    pdf.subtitulo("Bibliotecas utilizadas")
    pdf.bullet_list(
        [
            "requests, pandas, SQLAlchemy, mysql-connector-python — coleta e persistência "
            "(Entrega 1);",
            "streamlit — construção da aplicação web multipáginas e componentes de interface;",
            "plotly (plotly.express) — gráficos interativos do dashboard e da página de ML;",
            "scikit-learn (IsolationForest) — detecção de despesas atípicas;",
            "graphviz — diagramas do pipeline ETL, do DER e do fluxo de Machine Learning.",
        ]
    )


def montar_dashboard(pdf: RelatorioPDF):
    pdf.add_page()
    pdf.titulo_capitulo("5", "DASHBOARD INFORMATIVO")
    pdf.paragrafo(
        "O Dashboard Informativo reúne os principais indicadores extraídos da base de despesas. "
        "O usuário escolhe o ano de referência e todos os números e gráficos da tela são "
        "recalculados automaticamente. Entre os indicadores estão o total gasto, a quantidade de "
        "despesas, o número de deputados envolvidos e a média de gasto por parlamentar, além de "
        "gráficos para os deputados com maior gasto, a distribuição por partido e por estado, as "
        "categorias de despesa que mais pesam no total e a evolução mês a mês."
    )
    pdf.figura(
        ASSETS / "dashboard_kpis_graficos.png",
        "Figura 3 - Dashboard Informativo: indicadores (KPIs) e gráficos de Top 10 Deputados, "
        "Gastos por Partido, Gastos por UF e Top Categorias de Despesa (captura real da "
        "aplicação em execução, com dados de 2025).",
    )

    pdf.paragrafo(
        "Logo abaixo dos painéis de Top 10 Deputados, Partido, UF e Categoria, foi adicionado um "
        "texto calculado automaticamente a partir do próprio recorte exibido, apontando qual "
        "deputado, partido, UF e categoria lideram o ano selecionado. O mesmo princípio se aplica "
        "à evolução mensal: a aplicação identifica o mês de maior gasto e indica se a tendência "
        "entre o início e o fim do período é de alta ou de queda. Como esse texto é recalculado a "
        "cada seleção de ano, ele sempre reflete os dados realmente exibidos na tela."
    )
    pdf.figura(
        ASSETS / "dashboard_evolucao.png",
        "Figura 4 - Interpretação textual automática dos gráficos e evolução mensal dos gastos "
        "(valor e quantidade de despesas por mês), capturas reais da aplicação.",
    )

    pdf.paragrafo(
        "Uma seção que ganhou destaque foi a lista de fornecedores com maior concentração de "
        "valores. Ao lado de cada fornecedor, um ícone de lupa abre uma janela com a análise "
        "detalhada daquele fornecedor: quantos deputados utilizaram seus serviços, o total pago, a "
        "distribuição por UF, os maiores utilizadores e a evolução mensal do gasto — permitindo "
        "investigar uma relação específica entre parlamentar e fornecedor sem sair da tela "
        "principal."
    )
    pdf.figura(
        ASSETS / "dashboard_fornecedores.png",
        "Figura 5 - Fornecedores com maior concentração de valores, com acesso direto à análise "
        "detalhada de cada um (captura real da aplicação).",
    )


def montar_ml(pdf: RelatorioPDF):
    pdf.add_page()
    pdf.titulo_capitulo("6", "MÓDULO DE MACHINE LEARNING - DETECÇÃO DE DESPESAS ATÍPICAS")
    pdf.subtitulo("6.1 Por que Isolation Forest")
    pdf.paragrafo(
        "A técnica escolhida foi o Isolation Forest, do scikit-learn, por três motivos: (1) não "
        "exige rótulos prontos indicando despesas irregulares — o próprio algoritmo aprende, de "
        "forma não supervisionada, o que se distancia do padrão; (2) é uma técnica consolidada "
        "para detecção de outliers em dados tabulares, isolando rapidamente pontos que se afastam "
        "do grosso dos dados através de partições aleatórias da árvore de decisão; (3) é leve o "
        "suficiente para ser treinado novamente a cada interação do usuário (mudança de ano ou de "
        "sensibilidade), sem necessidade de persistir um modelo treinado em disco."
    )

    pdf.subtitulo("6.2 Como o modelo foi aplicado")
    pdf.paragrafo(
        "Em vez de um único modelo para toda a base, optou-se por treinar um Isolation Forest "
        "separado para cada tipo de despesa, já que categorias como combustível, divulgação "
        "parlamentar ou passagem aérea têm faixas de valor muito diferentes entre si — um modelo "
        "único provavelmente marcaria como atípica qualquer categoria naturalmente mais cara. Para "
        "cada categoria com ao menos dez registros no ano selecionado, o modelo usa o valor "
        "líquido da despesa como variável de entrada e classifica cada lançamento entre normal e "
        "atípico, conforme a sensibilidade (parâmetro contamination) ajustada pelo usuário na "
        "tela."
    )
    pdf.figura(
        ASSETS / "diagrama_ml.png",
        "Figura 6 - Fluxo de processamento do módulo de Machine Learning: da base de despesas no "
        "MySQL até a classificação final em normal ou atípica.",
        130,
    )

    pdf.subtitulo("6.3 Como os resultados são exibidos")
    pdf.paragrafo(
        "Os resultados aparecem primeiro como indicadores resumidos — total de despesas "
        "analisadas, quantas foram marcadas como atípicas e o valor somado dessas ocorrências — "
        "seguidos por um gráfico de dispersão que mostra as despesas ao longo do tempo, separando "
        "visualmente o normal do atípico, e por uma tabela com as maiores despesas atípicas "
        "encontradas. Assim como no dashboard, a aplicação interpreta o próprio resultado do "
        "modelo: calcula qual percentual das despesas do ano foi marcado como atípico, qual "
        "categoria concentra mais ocorrências e qual fornecedor aparece com mais frequência entre "
        "os lançamentos destacados."
    )
    pdf.figura(
        ASSETS / "ml_kpis_grafico.png",
        "Figura 7 - Página de Machine Learning: indicadores, interpretação textual automática do "
        "resultado do modelo e gráfico de dispersão de despesas normais vs. atípicas no tempo "
        "(captura real da aplicação, ano de 2025).",
    )
    pdf.figura(
        ASSETS / "ml_tabela.png",
        "Figura 8 - Tabela com as maiores despesas atípicas encontradas pelo modelo, com acesso "
        "direto à análise detalhada do fornecedor (captura real da aplicação).",
    )

    pdf.subtitulo("6.4 Limitações do modelo")
    pdf.paragrafo(
        "O parâmetro de sensibilidade (contamination) é definido manualmente pelo usuário — o "
        "modelo não 'sabe' qual a proporção real de despesas irregulares, apenas isola os pontos "
        "mais distantes do padrão observado, na proporção indicada. Categorias com poucos "
        "registros no ano selecionado (menos de dez lançamentos) ficam fora da análise, por falta "
        "de volume para um padrão confiável. Por fim, uma despesa atípica não é, necessariamente, "
        "uma despesa irregular: o resultado deve ser interpretado como um indicativo para "
        "investigação adicional, e não como uma conclusão definitiva sobre a regularidade do "
        "gasto."
    )


def montar_resultados(pdf: RelatorioPDF):
    pdf.add_page()
    pdf.titulo_capitulo("7", "RESULTADOS E CONSIDERAÇÕES FINAIS")
    pdf.paragrafo(
        "A execução do pipeline permitiu validar a integração com a API da Câmara dos Deputados, "
        "a construção da base relacional no MySQL e o funcionamento de todas as camadas da "
        "aplicação analítica — dashboard interativo, leitura textual automática dos gráficos e "
        "módulo de Machine Learning. Treinar o Isolation Forest separadamente por categoria de "
        "despesa se mostrou a decisão correta: os valores variam tanto entre tipos de despesa que "
        "um modelo único provavelmente geraria muitos falsos positivos."
    )
    pdf.paragrafo(
        "A possibilidade de investigar um fornecedor específico, tanto pelo dashboard quanto pela "
        "própria tela de anomalias, aproxima a aplicação de uma ferramenta real de apoio à "
        "fiscalização, e não apenas de um exercício acadêmico isolado."
    )
    pdf.subtitulo("Próximos passos possíveis")
    pdf.bullet_list(
        [
            "Incorporar variáveis de sazonalidade mensal ou o histórico do próprio fornecedor "
            "no modelo;",
            "Testar modelos de séries temporais para prever gastos futuros;",
            "Aplicar técnicas de agrupamento (clusterização) para perfis de gasto entre "
            "parlamentares.",
        ]
    )


def montar_ia(pdf: RelatorioPDF):
    pdf.add_page()
    pdf.titulo_capitulo("8", "DECLARAÇÃO E TÉCNICAS DE USO DE INTELIGÊNCIA ARTIFICIAL")
    pdf.paragrafo(
        "Em conformidade com a política da disciplina, declara-se que ferramentas de Inteligência "
        "Artificial foram utilizadas como apoio ao longo do desenvolvimento deste projeto e na "
        "redação deste relatório. A ferramenta principal foi o Claude Code, assistente de "
        "codificação da Anthropic (modelo Claude Sonnet), operado diretamente no terminal/editor "
        "do aluno. A definição do problema, a escolha das técnicas aplicadas, a validação dos "
        "resultados e a revisão de todo o conteúdo produzido permaneceram sob responsabilidade do "
        "aluno em todas as etapas."
    )

    pdf.subtitulo("8.1 Em que etapas a IA foi utilizada")
    pdf.bullet_list(
        [
            "Implementação do script de coleta (paginação, tratamento de erros e persistência "
            "em MySQL), a partir de especificações e decisões definidas pelo aluno;",
            "Construção das páginas da aplicação Streamlit (dashboard, página de Machine "
            "Learning, página de definições do sistema e diagramas Graphviz);",
            "Geração dos diagramas (ETL, DER e fluxo de Machine Learning) e das capturas de "
            "tela reais da aplicação utilizadas neste relatório;",
            "Apoio na redação e formatação deste relatório final, incluindo a consolidação do "
            "texto das duas entregas em um documento único.",
        ]
    )

    pdf.subtitulo("8.2 Como a condução pelo aluno se deu na prática")
    pdf.paragrafo(
        "O fluxo de trabalho adotado seguiu um padrão de condução ativa: o aluno definia o "
        "objetivo de cada etapa (por exemplo, 'detectar despesas fora do padrão por categoria' ou "
        "'explicar automaticamente o gráfico mais relevante de cada painel'), avaliava as opções "
        "técnicas apresentadas pela ferramenta de IA (como a escolha entre treinar um modelo único "
        "ou um modelo por categoria de despesa) e decidia qual caminho seguir antes de qualquer "
        "código ser escrito. A IA funcionou como um par de programação acelerador: implementou o "
        "código sob a orientação do aluno, mas não tomou decisões de modelagem, de arquitetura ou "
        "de interpretação dos resultados de forma autônoma."
    )
    pdf.paragrafo(
        "Após cada trecho de código gerado, o aluno executou a aplicação localmente, validou o "
        "comportamento na interface (filtros, gráficos, sensibilidade do modelo, popups de "
        "análise de fornecedor) e solicitou ajustes específicos quando o resultado não "
        "correspondia ao esperado. Esse ciclo de geração, execução e revisão se repetiu em cada "
        "página da aplicação, garantindo que o código final refletisse decisões verificadas pelo "
        "aluno, e não apenas a primeira sugestão da ferramenta."
    )

    pdf.subtitulo("8.3 Técnicas de condução e verificação adotadas")
    pdf.bullet_list(
        [
            "Especificação incremental: cada solicitação à IA partiu de um objetivo concreto e "
            "delimitado (uma página, um gráfico, uma correção pontual), evitando pedir 'o projeto "
            "inteiro' de uma só vez e mantendo o controle do aluno sobre cada decisão;",
            "Validação empírica: toda alteração no dashboard ou no módulo de Machine Learning "
            "foi testada na aplicação em execução, com dados reais, antes de ser considerada "
            "concluída;",
            "Revisão crítica do código gerado: trechos de código produzidos pela IA foram lidos "
            "e questionados pelo aluno (por exemplo, a justificativa de treinar um modelo por "
            "categoria de despesa em vez de um único modelo global);",
            "Interpretação humana dos resultados analíticos: as conclusões sobre quais "
            "deputados, partidos, UFs ou fornecedores se destacam, assim como a leitura sobre as "
            "despesas atípicas, foram formuladas e validadas pelo aluno a partir da saída dos "
            "modelos — a IA apoiou a automatização do cálculo, mas não a conclusão analítica em "
            "si;",
            "Documentação do processo: as decisões de modelagem e as justificativas técnicas "
            "registradas neste relatório foram redigidas a partir da compreensão do aluno sobre o "
            "que foi implementado, e não copiadas diretamente de sugestões da ferramenta.",
        ]
    )

    pdf.subtitulo("8.4 Limites dessa colaboração")
    pdf.paragrafo(
        "A ferramenta de IA não teve acesso a nenhuma informação fora do escopo do projeto, não "
        "tomou decisões finais sobre arquitetura, modelo de dados ou técnica analítica empregada, "
        "e todo o conteúdo gerado foi revisado antes de ser incorporado à entrega. O uso de IA "
        "seguiu o mesmo princípio de qualquer ferramenta de apoio ao desenvolvimento (como "
        "documentação oficial ou bibliotecas de terceiros): acelerar a implementação de decisões "
        "já tomadas pelo aluno, e não substituir o raciocínio analítico exigido pela disciplina."
    )


def montar_referencias(pdf: RelatorioPDF):
    pdf.add_page()
    pdf.titulo_capitulo("9", "REFERÊNCIAS")
    referencias = [
        "CÂMARA DOS DEPUTADOS. Dados Abertos da Câmara dos Deputados. Disponível em: "
        "https://dadosabertos.camara.leg.br. Acesso em: junho de 2026.",
        "MCKINNEY, Wes. Python for Data Analysis. 3. ed. Sebastopol: O'Reilly Media, 2022.",
        "PANDAS DEVELOPMENT TEAM. Pandas Documentation. Disponível em: "
        "https://pandas.pydata.org. Acesso em: junho de 2026.",
        "PYTHON SOFTWARE FOUNDATION. Python Documentation. Disponível em: "
        "https://docs.python.org. Acesso em: junho de 2026.",
        "ORACLE CORPORATION. MySQL 9.0 Reference Manual. Disponível em: "
        "https://dev.mysql.com/doc/. Acesso em: junho de 2026.",
        "SQLALCHEMY. SQLAlchemy Documentation. Disponível em: https://docs.sqlalchemy.org. "
        "Acesso em: junho de 2026.",
        "PEDREGOSA, F. et al. Scikit-learn: Machine Learning in Python. Journal of Machine "
        "Learning Research, v. 12, p. 2825-2830, 2011. Disponível em: https://scikit-learn.org. "
        "Acesso em: junho de 2026.",
        "LIU, F. T.; TING, K. M.; ZHOU, Z.-H. Isolation Forest. In: IEEE International "
        "Conference on Data Mining, 2008. Disponível em: "
        "https://scikit-learn.org/stable/modules/outlier_detection.html. Acesso em: junho de 2026.",
        "STREAMLIT. Streamlit Documentation. Disponível em: https://docs.streamlit.io. Acesso "
        "em: junho de 2026.",
        "PLOTLY TECHNOLOGIES INC. Plotly Python Open Source Graphing Library. Disponível em: "
        "https://plotly.com/python. Acesso em: junho de 2026.",
        "ANTHROPIC. Claude Code Documentation. Disponível em: https://docs.claude.com/claude-code. "
        "Acesso em: junho de 2026.",
    ]
    pdf.set_font("Arial", "", 10)
    for ref in referencias:
        pdf.multi_cell(0, 5.6, ref, align="J")
        pdf.ln(2)


def main():
    pdf = RelatorioPDF()
    montar_capa(pdf)
    montar_sumario_executivo(pdf)
    montar_api(pdf)
    montar_modelo_dados(pdf)
    montar_arquitetura_app(pdf)
    montar_dashboard(pdf)
    montar_ml(pdf)
    montar_resultados(pdf)
    montar_ia(pdf)
    montar_referencias(pdf)

    ASSETS.mkdir(parents=True, exist_ok=True)
    pdf.output(str(SAIDA))
    print(f"PDF gerado em: {SAIDA}")


if __name__ == "__main__":
    main()
