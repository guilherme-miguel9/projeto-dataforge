# from sqlalchemy.dialects.oracle import RAW
from pathlib import Path

import boto3
from botocore.exceptions import ClientError, NoCredentialsError


def get_s3_client():
    s3_client = boto3.client(
        "s3",
        endpoint_url="http://localhost:9000",
        aws_access_key_id="minioadmin",
        aws_secret_access_key="minioadmin",
    )
    return s3_client


def init_s3_buckets():
    client = get_s3_client()

    try:
        list_bucket = client.list_buckets()
        list_bucket_content = list_bucket.get("Buckets", [])

        buckets_existentes = [bucket["Name"] for bucket in list_bucket_content]

        buckets_criar = ["bronze", "silver", "gold", "quarantine"]

        for bucket in buckets_criar:
            if bucket not in buckets_existentes:
                client.create_bucket(Bucket=bucket)
                print(f"Bucket {bucket} criado")
            else:
                print(f"Bucker já existente {bucket}")

        return list_bucket

    except NoCredentialsError:
        print("Erro: Credenciais do MinIO inválidas ou não fornecidas.")
        return None
    except ClientError as e:
        print(f"Erro na API do MinIO: {e}")
        return None
    except Exception as e:  # noqa: BLE001
        print(f"Erro ao conectar com o MinIO: {e}")
        return None


def upload_file_to_s3(local_path: Path | str, bucket_name: str, s3_key: str) -> bool:
    client = get_s3_client()

    try:
        client.upload_file(str(local_path), bucket_name, s3_key)

        print(f"Arquivo {local_path} enviado com sucesso! s3://{bucket_name}/{s3_key}")
        return True

    except FileNotFoundError:
        print("O arquivo local não foi encontrado.")
        return False
    except NoCredentialsError:
        print("Credenciais do MinIO não encontradas.")
        return False
    except ClientError as e:
        print(f"Erro no MinIO: {e}")


if __name__ == "__main__":
    from datetime import datetime

    from dataforge.utils.paths import RAW_DATA_DIR

    year = datetime.now().year  # noqa: DTZ005
    month = datetime.now().month  # noqa: DTZ005

    print("Iniciando os Buckets no MinIO\n")
    init_s3_buckets()

    print("Realizando teste para tentar camada bronze via excel... \n")
    pasta_lotes = RAW_DATA_DIR / "field_orders"

    for arquivos in pasta_lotes.glob("*.xlsx"):
        s3_key = f"field_orders/ano={year}/mes={month}/{arquivos.name}"
        upload_file_to_s3(local_path=arquivos, bucket_name="bronze", s3_key=s3_key)

    print("Concluído a camada Bronze Excel\n")

    print("Realizando teste para tentar camada bronze via api de clientes... \n")
    pasta_api = RAW_DATA_DIR / "api_customers"
    for arquivos in pasta_api.glob("*.json"):
        s3_key = f"api_customers/ano={year}/mes={month}/{arquivos.name}"
        upload_file_to_s3(local_path=arquivos, bucket_name="bronze", s3_key=s3_key)

    print("Concluído upload da API")
