# Modelo de Dados — MySQL (Produção)

Projeto Integrador em Big Data e Inteligência Analítica — Pipeline de Gastos Públicos
Fonte: API de Dados Abertos da Câmara dos Deputados (`https://dadosabertos.camara.leg.br/api/v2`)

## 1. Visão Geral

A base é composta por três tabelas relacionais (MySQL/InnoDB, `utf8mb4`):

- **deputados** — dados cadastrais dos parlamentares;
- **despesas** — registros financeiros de despesas parlamentares, 1:N com `deputados`;
- **log_importacao** — auditoria de cada execução do pipeline de coleta (ETL).

DDL completo em [`sql/schema.sql`](../sql/schema.sql).

## 2. Diagrama Entidade-Relacionamento (DER)

```
┌────────────────────────┐        ┌──────────────────────────────┐
│       DEPUTADOS         │        │           DESPESAS             │
├────────────────────────┤        ├──────────────────────────────┤
│ PK id_deputado (INT)    │◄──────┤ PK id_despesa (BIGINT, AI)      │
│    nome                 │  1   N│ FK id_deputado (INT)            │
│    sigla_partido        │       │    ano (SMALLINT)               │
│    sigla_uf              │       │    mes (TINYINT)                 │
│    url_foto              │       │    tipo_despesa                  │
│    email                 │       │    valor_liquido (DECIMAL 12,2) │
│    data_atualizacao      │       │    data_documento (DATE)        │
└────────────────────────┘        │    nome_fornecedor               │
                                    │    cnpj_cpf_fornecedor           │
                                    │    data_importacao               │
                                    └──────────────────────────────┘

┌────────────────────────────────┐
│         LOG_IMPORTACAO          │
├────────────────────────────────┤
│ PK id_execucao (BIGINT, AI)      │
│    ano_referencia                │
│    qtd_deputados                 │
│    qtd_despesas                  │
│    status (SUCESSO/ERRO)          │
│    mensagem                       │
│    iniciado_em / finalizado_em    │
└────────────────────────────────┘
```

Relacionamento: **Deputado (1) — (N) Despesa**. Um parlamentar pode possuir diversas
despesas; cada despesa pertence a exatamente um parlamentar (`ON DELETE CASCADE`).

## 3. Tabelas

### 3.1 `deputados`

| Campo | Tipo | Restrição | Descrição |
|---|---|---|---|
| id_deputado | INT | PK | Identificador único do parlamentar (fornecido pela API) |
| nome | VARCHAR(150) | NOT NULL | Nome do parlamentar |
| sigla_partido | VARCHAR(20) | — | Partido político |
| sigla_uf | VARCHAR(2) | — | Unidade federativa de representação |
| url_foto | VARCHAR(255) | — | URL da foto oficial |
| email | VARCHAR(150) | — | E-mail institucional |
| data_atualizacao | TIMESTAMP | auto | Última atualização do registro |

Índices: `idx_deputados_partido` (sigla_partido), `idx_deputados_uf` (sigla_uf).

### 3.2 `despesas`

| Campo | Tipo | Restrição | Descrição |
|---|---|---|---|
| id_despesa | BIGINT | PK, AUTO_INCREMENT | Identificador interno da despesa |
| id_deputado | INT | FK → deputados.id_deputado | Parlamentar associado |
| ano | SMALLINT | NOT NULL | Ano de referência da coleta |
| mes | TINYINT | — | Mês extraído de `data_documento` |
| tipo_despesa | VARCHAR(150) | — | Categoria da despesa (ex.: Combustíveis) |
| valor_liquido | DECIMAL(12,2) | — | Valor efetivamente pago |
| data_documento | DATE | — | Data do documento fiscal |
| nome_fornecedor | VARCHAR(200) | — | Beneficiário do pagamento |
| cnpj_cpf_fornecedor | VARCHAR(20) | — | Documento do fornecedor (texto, não numérico) |
| data_importacao | TIMESTAMP | auto | Data/hora da carga no banco |

Índices: `idx_despesas_id_deputado` (criado automaticamente pela FK), `idx_despesas_data_documento`,
`idx_despesas_ano_mes`.

### 3.3 `log_importacao`

| Campo | Tipo | Descrição |
|---|---|---|
| id_execucao | BIGINT (PK, AI) | Identificador da execução |
| ano_referencia | SMALLINT | Ano coletado |
| qtd_deputados | INT | Quantidade de deputados processados |
| qtd_despesas | INT | Quantidade de despesas gravadas |
| status | VARCHAR(20) | SUCESSO / ERRO |
| mensagem | TEXT | Detalhe da execução ou erro |
| iniciado_em / finalizado_em | TIMESTAMP | Janela de execução do pipeline |

## 4. Dicionário de Dados (resumo)

| Campo | Tipo | Descrição | Exemplo |
|---|---|---|---|
| id_deputado | Inteiro | Identificador único do parlamentar | 204521 |
| nome | Texto | Nome do parlamentar | João Silva |
| sigla_partido | Texto | Partido político | PL |
| sigla_uf | Texto | Unidade Federativa | DF |
| tipo_despesa | Texto | Categoria da despesa | Combustíveis |
| valor_liquido | Numérico | Valor efetivamente pago | 1250.75 |
| data_documento | Data | Data da despesa | 2025-03-15 |
| nome_fornecedor | Texto | Beneficiário do pagamento | Posto Exemplo Ltda |
| cnpj_cpf_fornecedor | Texto | Documento do fornecedor (nunca numérico) | 12.345.678/0001-90 |

## 5. Recomendações para Ambiente de Produção

- **Usuário de aplicação com privilégios mínimos**: conceder apenas `SELECT, INSERT, UPDATE, DELETE`
  no schema `projeto_integrador` ao usuário usado pela aplicação (não usar usuário administrativo).
- **Charset/collation**: manter `utf8mb4` / `utf8mb4_unicode_ci` para suportar acentuação e caracteres
  especiais dos dados públicos.
- **Particionamento**: caso o volume de despesas cresça significativamente (múltiplos anos), considerar
  particionamento de `despesas` por `ano` (`PARTITION BY RANGE`).
- **Backup**: rotina de `mysqldump` ou snapshot gerenciado, com retenção compatível com a política de
  dados públicos auditáveis.
- **Segredos**: credenciais de conexão (host, usuário, senha) devem ser geridas via variáveis de
  ambiente/secret manager, nunca hardcoded no código-fonte em produção (diferente do ambiente de
  desenvolvimento deste projeto acadêmico).
- **Monitoramento de execuções**: a tabela `log_importacao` pode evoluir para alimentar alertas em caso
  de falhas recorrentes de coleta.
- **Idempotência**: a carga de `despesas` é feita por substituição completa dos registros do `ano`
  selecionado (`DELETE` + `INSERT`), evitando duplicidade em reexecuções do pipeline.
