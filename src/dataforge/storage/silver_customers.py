import io                                                                                       
import json                                                                                     
from datetime import datetime                                                                   
from pathlib import Path                                                                        
import polars as pl                                                                             
from pydantic import ValidationError                                                            
                                                                                                    
from dataforge.storage.s3_client import get_s3_client, upload_file_to_s3                        
from dataforge.quality.contracts import CustomerContract                                        
from dataforge.utils.paths import PROCESSED_DATA_DIR                                            
from dataforge.utils.logger import get_logger

log = get_logger('SilverCustomers')

def process_bronze_to_silver_customers():
    client = get_s3_client()
    all_valid_customers = []
    year = datetime.now().year
    month = datetime.now().month

    response = client.list_objects_v2(Bucket='bronze', Prefix='api_customers/')
    objects = response.get("Contents", [])    

    if not objects:
        log.info('Nenhum arquivo foi encontrado.')
        return None

    for obj in objects:
        key = obj["Key"]
        if not key.endswith(".json"):
            continue
            
        log.info(f"Processando arquivo: {key}")
        
        file_buffer = io.BytesIO()                                                            
        client.download_fileobj(Bucket="bronze", Key=key, Fileobj=file_buffer)                
        file_buffer.seek(0)
    
        data = json.load(file_buffer)

        users = data.get("users", [])

        for user in users:
            mapping_buttons = {
                "id": user.get('id'),
                "first_name": user.get('firstName'),
                "last_name": user.get('lastName'),
                "email": user.get('email'),
                "age": user.get('age'),
            }
            try:
                CustomerContract(**mapping_buttons)
                all_valid_customers.append(mapping_buttons)
            except ValidationError as e:
                log.warning(f"Linha inválida no arquivo {key}: {mapping_buttons} -> {e}")

    df_customers = pl.DataFrame(all_valid_customers)
    df_customers = df_customers.unique(subset=["id"], keep="first")

    silver_dir = PROCESSED_DATA_DIR / "silver" / "customers"
    silver_dir.mkdir(parents=True, exist_ok=True)
    parquet_path = silver_dir / "customers_data.parquet"

    df_customers.write_parquet(parquet_path)
    log.info(f"Arquivo Parquet gerado em: {parquet_path}")

    s3_key = f'customers/ano={year}/mes={month}/customers_data.parquet'
    upload_file_to_s3(local_path=parquet_path, bucket_name= 'silver', s3_key=s3_key)


if __name__ == "__main__":
    process_bronze_to_silver_customers()