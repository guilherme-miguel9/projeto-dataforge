import io                                                                                     
import pandas as pd         
import polars as pl                                                                  
from dataforge.storage.s3_client import get_s3_client, upload_file_to_s3                                         
from dataforge.quality.validator import validate_field_orders
from dataforge.utils.paths import PROCESSED_DATA_DIR                                                                                                  
                                                                                                  
def process_bronze_to_silver():         
    from datetime import datetime

    year = datetime.now().year
    month = datetime.now().month
                                                          
    client = get_s3_client()                                                                  
    all_valid_records = []

    # 1. Listar os objetos da Bronze na pasta de ordens de campo                              
    response = client.list_objects_v2(Bucket="bronze", Prefix="field_orders/")                
    objects = response.get("Contents", [])                                                    
                                                                                                  
    if not objects:                                                                           
        print("Nenhum arquivo encontrado no bucket bronze.")                                  
        return                                                                                
                                                                                                  
    for obj in objects:                                                                       
        key = obj["Key"]                                                                      
                                                                                                  
        # Ignora se não for arquivo .xlsx                                                     
        if not key.endswith(".xlsx"):                                                         
            continue                                                                          
                                                                                                  
        print(f"Lendo arquivo da Bronze: s3://bronze/{key} ({obj['Size']} bytes)")         
                                                                                                  
        # 2. Baixa os bytes do Excel diretamente para a memória RAM                           
        file_buffer = io.BytesIO()                                                            
        client.download_fileobj(Bucket="bronze", Key=key, Fileobj=file_buffer)                
        file_buffer.seek(0)                                                                   
                                                                                                  
        # 3. Lê com Pandas                                                                    
        df = pd.read_excel(file_buffer)
        raw_records = df.to_dict(orient="records")                                                    
        validos, quarentena = validate_field_orders(raw_records)                                      
        all_valid_records.extend(validos)                                        
        print(f"   Linhas carregadas no Pandas: {len(df)} linhas")
    
    df_silver = pl.DataFrame(all_valid_records)

    silver_dir = PROCESSED_DATA_DIR / "silver" / "field_orders"
    silver_dir.mkdir(parents=True, exist_ok=True)
    parquet_path = silver_dir / "ordens_consolidados.parquet"

    df_silver.write_parquet(parquet_path, compression="snappy")
    print(f'Parquet salvo em: {parquet_path}')

    s3_key = f'field_orders/ano={year}/mes={month}/ordens_consolidadads.parquet'
    upload_file_to_s3(local_path=parquet_path, bucket_name= 'silver', s3_key=s3_key)


                                                                                                  
                                                                                                  
if __name__ == "__main__":                                                                    
    process_bronze_to_silver()
