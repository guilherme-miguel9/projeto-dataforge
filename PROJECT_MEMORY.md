# 🧠 PROJECT_MEMORY.md — Memória Persistente do Projeto DataForge

> **Documento de Contexto Contínuo**: Este arquivo armazena todas as decisões arquiteturais, preferências de mentoria, histórico de desenvolvimento, infraestrutura e estado atual do projeto para retomada instantânea de sessões futuras.

---

## 👤 1. Perfil do Desenvolvedor & Diretrizes de Mentoria

- **Desenvolvedor**: Guilherme Miguel (@guilherme-miguel9)
- **Perfil**: Engenheiro de Dados focado em boas práticas de mercado, arquitetura escalável e código limpo.
- **Regras de Ouro de Mentoria (Tech Lead IA)**:
  1. **NUNCA entregar código pronto de uma vez**: Ensinar por etapas progressivas, dividindo problemas complexos em passos pequenos.
  2. **Pseudocódigo Primeiro**: Orientar o desenvolvedor a pensar e escrever a lógica/pseudocódigo antes de digitar a sintaxe.
  3. **Explicar o "Porquê"**: Contextualizar a dor real de negócio/engenharia antes de introduzir ferramentas ou padrões.
  4. **Segurança & Privacidade**: Manter dados confidenciais protegidos; nunca comitar e-mails pessoais no Git ou no `pyproject.toml`.

---

## 🏗️ 2. Infraestrutura & Configurações de Ambiente

- **Sistema Operacional**: macOS (Darwin) com Apple Silicon.
- **Gerenciador de Pacotes**: Poetry 2.4.1 (Python `>=3.11, <3.15`).
- **Configuração Poetry**: `package-mode = false` no `pyproject.toml` (modo aplicação) e `pythonpath = ["src"]` para o PyTest.

### 🐳 Serviços & Banco de Dados
1. **MinIO (Object Storage S3)** (ou AWS S3 / MinIO Corporativo):
   - Configurado dinamicamente via `.env` (`S3_ENDPOINT_URL`, `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`).
   - Buckets gerenciados: `bronze`, `silver`, `gold`, `quarantine`.
2. **PostgreSQL Corporativo / Produção (Data Warehouse)**:
   - Conexão desacoplada do Docker e gerenciada via variáveis de ambiente (`.env`).
   - Database: `dataforge_dw` (ou configurado no `.env`)
   - Port: Padrão `5432` (ou porta corporativa).
   - Schemas: `raw_silver` (Staging de carga ELT) e **`leitura_star`** (Camada Analítica / Star Schema gerenciada pelo dbt).

---

## 🏛️ 3. Arquitetura da Solução & Decisões Técnicas (ADRs)

| Componente | Ferramenta / Técnica | Decisão Arquitetural & Motivo |
| :--- | :--- | :--- |
| **Ingestão Incremental** | `detector.py` | Hashing **SHA-256** com registro em `ingestion_manifest.json` para garantir idempotência e evitar reprocessar planilhas já ingeridas. |
| **Data Lake Bronze** | MinIO / S3 | Armazenamento de dados brutos e imutáveis particionados por ano/mês (`field_orders` em Excel e `api_customers` em JSON). |
| **Quality Gate & DLQ** | Pydantic v2 | Modelos estritos (`FieldOrderContract` e `CustomerContract`). Registros inválidos são isolados na **Quarentena (Dead Letter Queue)** sem travar a esteira. |
| **Data Lake Silver** | Polars + Parquet Snappy | Conversão de dados válidos para formato colunar Parquet compactado com Snappy (**~80% menor que o Excel original**). Deduplicação com `.unique()`. |
| **Carga DW Idempotente** | `postgres_loader.py` | Carga parametrizada via `.env` com **`TRUNCATE TABLE` + `append`** na `raw_silver`. |
| **Modelagem Gold (Star Schema)** | **dbt-core + dbt-postgres** | Esquema Estrela no schema **`leitura_star`**: `dim_tempo`, `dim_cliente` (SCD1), `dim_agente` (SCD1), `dim_instalacao_contrato` (SCD1), `dim_status_leitura` (Junk SCD1), `dim_medidor` (SCD2), `dim_localizacao` (SCD2) e `fato_leitura` (particionada por ano com join temporal). |
| **Testes de DW** | dbt tests (`schema.yml`) | **8 testes automatizados** de qualidade (unicidade, não-nulidade e integridade referencial de chaves estrangeiras entre Fato e Dimensões). |
| **Orquestrador Master** | `src/dataforge/pipeline.py` | Maestro sequencial que executa as 5 etapas com telemetria de tempo (`time.perf_counter()`), concluindo em **~6.88 segundos**. |
| **Qualidade & Linters** | Ruff | 100% limpo com regras de Python moderno (`datetime.now(UTC)`). |
| **Testes Automatizados** | PyTest (`tests/`) | 5 testes unitários e de regras de negócio passando em menos de 1 segundo. |
| **CI/CD** | GitHub Actions (`.github/workflows/ci.yml`) | Esteira de integração contínua rodando na nuvem a cada `git push` com Poetry 2.x, Ruff e PyTest (**Selo Verde `Passing`**). |

---

## 📊 4. Estado Atual das Fases do Roadmap

- [x] **Fase 0**: Setup de Ambiente, Poetry, Estrutura `src/`, Docker Compose.
- [x] **Fase 1**: Ingestão de Fontes Heterogêneas (Excel + API REST) & Detecção Incremental SHA-256.
- [x] **Fase 2**: Contratos de Dados Pydantic & Roteamento para Quarentena (DLQ).
- [x] **Fase 3**: Data Lake Medallion (MinIO Bronze & Silver Parquet com Polars).
- [x] **Fase 4**: Idempotência, Deduplicação por Chave Única & Logs Estruturados JSON.
- [x] **Fase 5**: Data Warehouse PostgreSQL & Camada Gold Star Schema com dbt (8/8 testes aprovados).
- [x] **Fase 6**: Orquestrador Master de Pipeline End-to-End (`pipeline.py`).
- [x] **Fase 7**: Suíte de Testes com PyTest & Esteira CI/CD no GitHub Actions.
- [x] **Fase 8**: Documentação Executiva, Badges e README.md de Alto Impacto.

---

## 🔮 5. Próximos Passos & Backlog Futuro

1. **Consumo no Power BI (Fase 7 do Roadmap original)**:
   - Conectar o Power BI Desktop no PostgreSQL (`localhost:5433`, banco `dataforge_dw`, schema `gold`).
   - Importar o Star Schema (`fct_field_orders`, `dim_customers`, `dim_locations`).
   - Construir métricas analíticas e visuais de ordens de serviço e leituras de campo.
2. **Evoluções Possíveis**:
   - Agendamento do pipeline com Apache Airflow ou Prefect.
   - Implementação de monitoramento com Prometheus e Grafana.
