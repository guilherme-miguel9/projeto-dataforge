# Roadmap do Projeto DataForge

Este roadmap foi desenhado de forma progressiva, partindo dos fundamentos de software e engenharia de dados até uma plataforma analítica moderna, resiliente e orquestrada.

---

## Visão Geral das Fases

```
[ Fase 0: Setup & Governança do Projeto ]
                   ↓
[ Fase 1: Fontes de Dados & Ingestão Bruta ]
                   ↓
[ Fase 2: Data Quality & Quarentena (Data Contracts) ]
                   ↓
[ Fase 3: Data Lake Medallion (Bronze & Silver com MinIO/Parquet) ]
                   ↓
[ Fase 4: Idempotência, CDC & Observabilidade ]
                   ↓
[ Fase 5: Data Warehouse & Camada Gold com dbt ]
                   ↓
[ Fase 6: Orquestração de Pipelines (Airflow / Prefect) ]
                   ↓
[ Fase 7: Consumo (Power BI) & Defesa Arquitetural ]
```

---

## Detalhamento das Fases

### 🧱 Fase 0: Fundação & Ambiente de Engenharia
- **Objetivo**: Estruturar o repositório e o ecossistema de desenvolvimento com padrões profissionais de Engenharia de Software.
- **Tópicos**:
  - Definição do cenário de negócio (ex: E-commerce / Vendas com transações e cadastros).
  - Estrutura de diretórios modular e desacoplada.
  - Gerenciamento de dependências e ambiente virtual (`venv` / `uv` / `poetry`).
  - Configuração de ferramentas de qualidade de código (`ruff`/`black`, `.gitignore`, `pre-commit`).
  - Configuração do Docker Compose inicial.

---

### 📥 Fase 1: Fontes Heterogêneas & Detecção de Dados
- **Objetivo**: Extrair dados de múltiplas origens (arquivos locais e APIs) com controle de novos eventos.
- **Tópicos**:
  - Geração/Consumo de planilhas Excel (despadronizadas, múltiplas abas, cabeçalhos variáveis).
  - Consumo de API REST (paginação, rate limit, retries).
  - Mecanismos de detecção de novos arquivos e dados (hash MD5/SHA256, metadados de sistema de arquivos e watermark).
  - Extração resiliente e desacoplada.

---

### 🛡️ Fase 2: Contratos de Dados, Validação e Quarentena
- **Objetivo**: Impedir que dados corrompidos quebrem o pipeline, direcionando-os para análise sem travar a operação.
- **Tópicos**:
  - Data Contracts e Schema Enforcement (validação com Pydantic / Pandera).
  - Roteamento condicional de dados: Registros Válidos vs. Quarentena (Dead Letter Queue - DLQ).
  - Políticas de notificação e rastreabilidade de dados rejeitados.

---

### 🥉🥈 Fase 3: Data Lake Medallion (Bronze & Silver com MinIO e Parquet)
- **Objetivo**: Implementar a arquitetura Medalhão sobre Object Storage compatível com S3 (MinIO).
- **Tópicos**:
  - Subida do MinIO via Docker e configuração de buckets.
  - **Camada Bronze**: Gravação do dado cru/raw, imutável, particionado por data de ingestão.
  - Formato Parquet: vantagens em relação a CSV/JSON (compressão colunar, types, estatísticas).
  - **Camada Silver**: Leitura da Bronze, parsing, tipagem estrita, deduplicação e limpeza com Polars/Pandas.

---

### ⚙️ Fase 4: Idempotência, Processamento Incremental & Logs Estruturados
- **Objetivo**: Tornar os pipelines tolerantes a falhas, reexecutáveis sem gerar duplicatas e monitoráveis.
- **Tópicos**:
  - Garantia de Idempotência: estratégias de overwrite por partição e upsert.
  - Processamento Incremental e detecção de alterações (CDC simples / SCD Tipo 1 e 2).
  - Logging Estruturado (JSON format, `execution_id`, métricas de volumetria e tempo de execução).
  - Tratamento defensivo de exceções e atomicidade.

---

### 🥇🏛️ Fase 5: Data Warehouse & Camada Gold com dbt
- **Objetivo**: Modelar e carregar dados analíticos otimizados para consumo de BI e tomada de decisão.
- **Tópicos**:
  - Configuração do PostgreSQL (como DW analítico) via Docker.
  - Modelagem Dimensional (Metodologia Kimball: Tabelas Fato e Dimensões - Star Schema).
  - Carga da Silver para o Data Warehouse.
  - Implementação de transformações e métricas na Camada Gold com **dbt** (`dbt-core`).
  - Testes automatizados do dbt (unicidade, não-nulidade, integridade referencial) e documentação de linhagem.

---

### 🔄 Fase 6: Orquestração Profissional de Pipelines
- **Objetivo**: Automatizar o agendamento, dependências e retries com uma ferramenta de orquestração moderna.
- **Tópicos**:
  - Trade-offs de orquestradores: Cron vs. Prefect vs. Apache Airflow.
  - Configuração do orquestrador via Docker.
  - Construção de DAGs/Flows ponta a ponta (Ingestão -> Validação -> Bronze -> Silver -> Gold/dbt).
  - Configuração de retries com backoff exponencial e alertas.

---

### 📊 Fase 7: Consumo no Power BI & Defesa Arquitetural
- **Objetivo**: Fechar o ciclo de ponta a ponta conectando a ferramenta de BI e consolidando o conhecimento para entrevistas e apresentações sênior.
- **Tópicos**:
  - Conexão do Power BI ao PostgreSQL (DW / Gold).
  - Criação de modelo semântico, relacionamentos e medidas analíticas (DAX básico).
  - Simulação de incidentes de produção e plano de rollback/recuperação.
  - Sessão de "Defesa do Projeto": apresentação técnica das decisões arquiteturais e trade-offs.
