import subprocess
import time
import uuid
from datetime import UTC, datetime

from dataforge.extraction.api_extractor import extract_customers_from_api
from dataforge.extraction.detector import get_new_files, update_manifest
from dataforge.storage.postgres_loader import load_silver_to_postgres
from dataforge.storage.s3_client import init_s3_buckets, upload_file_to_s3
from dataforge.storage.silver_customers import process_bronze_to_silver_customers
from dataforge.storage.silver_processor import process_bronze_to_silver
from dataforge.utils.logger import get_logger
from dataforge.utils.paths import BASE_DIR, PROCESSED_DATA_DIR, RAW_DATA_DIR

log = get_logger("PipelineOrchestrator")


def run_dbt_command(command: str) -> bool:
    dbt_dir = BASE_DIR / "dbt_dataforge"
    cmd = ["poetry", "run", "dbt", command, "--profiles-dir", "."]

    log.info(f"Executando dbt {command}...")
    result = subprocess.run(
        cmd, cwd=dbt_dir, capture_output=True, text=True, check=False
    )

    if result.returncode == 0:
        log.info(f"dbt {command} concluído com sucesso!")
        return True
    else:
        log.error(f"Erro no dbt {command}:\n{result.stderr or result.stdout}")
        return False


def run_pipeline():

    execution_id = str(uuid.uuid4())[:8]
    start_total = time.perf_counter()
    log.info(f"Iniciando o pipeline DATAfORGE - Execution ID: {execution_id}")

    log.info("[Etapa 1] Ingestão & Detecção de Fontes heterogêneas")

    source_dir_field_orders = RAW_DATA_DIR / "field_orders"
    source_dir_api_customers = RAW_DATA_DIR / "api_customers"
    manifest_file = PROCESSED_DATA_DIR / "metadata" / "ingestion_manifest.json"
    new_files = get_new_files(source_dir_field_orders, manifest_file)
    log.info(f"Novos arquivos detectados: {len(new_files)}")

    for f in new_files:
        update_manifest(f, manifest_file)

    # Extração de clientes pela API
    extract_customers_from_api(limit_per_page=10, max_pages=3)

    log.info("[Etapa 2] Upload para a Camada Bronze (MinIO)")
    init_s3_buckets()
    now = datetime.now(UTC)
    try:
        for arq in (source_dir_field_orders).glob("*.xlsx"):
            s3_key = f"field_orders/ano={now.year}/mes={now.month}/{arq.name}"
            upload_file_to_s3(str(arq), "bronze", s3_key)
            log.info("Subiu arquivos do Excel com sucesso!")
    except FileNotFoundError as e:
        log.error(f"Erro ao subir arquivos do Excel: {e}")

    try:
        for arq in (source_dir_api_customers).glob("*.json"):
            s3_key = f"api_customers/ano={now.year}/mes={now.month}/{arq.name}"
            upload_file_to_s3(str(arq), "bronze", s3_key)
            log.info("Subiu arquivos da API com sucesso!")
    except FileNotFoundError as e:
        log.error(f"Erro ao subir arquivos da API: {e}")

    log.info("[Etapa 3] Processamento da Camada Silver (Parquet)")
    process_bronze_to_silver()
    process_bronze_to_silver_customers()

    log.info("[Etapa 4] Carga no PostgreSQL (raw_silver)")
    load_silver_to_postgres()

    log.info("[Etapa 5] Modelagem Dimensional & Testes com dbt")
    if not run_dbt_command("run"):
        raise RuntimeError("Falha na execução dos modelos com DBT")
    if not run_dbt_command("test"):
        raise RuntimeError("Falha nos testes automatizados do DBT")

    total_time = time.perf_counter() - start_total
    log.info(f"Pipeline concluído com sucesso em {total_time:.2f} segundos")


if __name__ == "__main__":
    run_pipeline()
