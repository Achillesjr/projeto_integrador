-- Projeto Integrador - Gastos Públicos
-- Schema MySQL: tabelas, chaves e índices
-- Banco: projeto_integrador

CREATE TABLE IF NOT EXISTS deputados (
    id_deputado     INT PRIMARY KEY,
    nome            VARCHAR(150) NOT NULL,
    sigla_partido   VARCHAR(20),
    sigla_uf        VARCHAR(2),
    url_foto        VARCHAR(255),
    email           VARCHAR(150),
    data_atualizacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS despesas (
    id_despesa          BIGINT AUTO_INCREMENT PRIMARY KEY,
    id_deputado         INT NOT NULL,
    ano                 SMALLINT NOT NULL,
    mes                 TINYINT,
    tipo_despesa        VARCHAR(150),
    valor_liquido       DECIMAL(12,2),
    data_documento      DATE,
    nome_fornecedor     VARCHAR(200),
    cnpj_cpf_fornecedor VARCHAR(20),
    data_importacao     TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_despesas_deputado
        FOREIGN KEY (id_deputado) REFERENCES deputados(id_deputado)
        ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- idx_despesas_id_deputado é criado automaticamente pela FK acima
CREATE INDEX idx_despesas_data_documento ON despesas (data_documento);
CREATE INDEX idx_despesas_ano_mes ON despesas (ano, mes);
CREATE INDEX idx_deputados_partido ON deputados (sigla_partido);
CREATE INDEX idx_deputados_uf ON deputados (sigla_uf);

-- Tabela de controle das execuções de importação (auditoria do pipeline)
CREATE TABLE IF NOT EXISTS log_importacao (
    id_execucao      BIGINT AUTO_INCREMENT PRIMARY KEY,
    ano_referencia   SMALLINT NOT NULL,
    qtd_deputados    INT,
    qtd_despesas     INT,
    status           VARCHAR(20),
    mensagem         TEXT,
    iniciado_em      TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    finalizado_em    TIMESTAMP NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
