import polars as pl
from sqlalchemy import create_engine, text

from dataforge.utils.logger import get_logger
from dataforge.utils.paths import PROCESSED_DATA_DIR

log = get_logger("postgres_loader")

# URL de conexão com o banco no Docker
DB_URL = "postgresql+psycopg2://postgres:postgrespassword@localhost:5433/dataforge_dw"


def load_silver_to_postgres():
    """Executa o carregamento dos Parquets da Silver para o PostgreSQL."""
    engine = create_engine(DB_URL)

    # 1. Cria o schema 'raw_silver' no PostgreSQL se ele não existir
    with engine.connect() as conn:
        conn.execute(text("CREATE SCHEMA IF NOT EXISTS raw_silver;"))
        conn.commit()
    log.info("Schema 'raw_silver' verificado/criado com sucesso no PostgreSQL.")

    # 2. Carrega as Ordens de Serviço da Silver
    orders_path = (
        PROCESSED_DATA_DIR / "silver" / "field_orders" / "ordens_consolidados.parquet"
    )
    if orders_path.exists():
        df_orders = pl.read_parquet(orders_path)
        with engine.connect() as conn:
            conn.execute(text("TRUNCATE TABLE raw_silver.field_orders;"))
            conn.commit()
        df_orders.to_pandas().to_sql(
            name="field_orders",
            con=engine,
            schema="raw_silver",
            if_exists="append",
            index=False,
        )
        log.info(
            f"Tabela 'raw_silver.field_orders' carregada com {len(df_orders)} linhas."
        )
    else:
        log.warning(f"Arquivo não encontrado: {orders_path}")

    # 3. Carrega os Clientes da API da Silver
    customers_path = (
        PROCESSED_DATA_DIR / "silver" / "customers" / "customers_data.parquet"
    )
    if customers_path.exists():
        df_customers = pl.read_parquet(customers_path)
        with engine.connect() as conn:
            conn.execute(text("TRUNCATE TABLE raw_silver.customers;"))
            conn.commit()
        df_customers.to_pandas().to_sql(
            name="customers",
            con=engine,
            schema="raw_silver",
            if_exists="append",
            index=False,
        )
        log.info(
            f"Tabela 'raw_silver.customers' carregada com {len(df_customers)} linhas."
        )
    else:
        log.warning(f"Arquivo não encontrado: {customers_path}")


if __name__ == "__main__":
    load_silver_to_postgres()
