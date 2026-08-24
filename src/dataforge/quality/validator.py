import json                                                                                   
from datetime import datetime                                                                 
from pathlib import Path                                                                      
from pydantic import ValidationError                                                          
from dataforge.quality.contracts import FieldOrderContract                                    
from dataforge.utils.paths import DATA_DIR                                                    
import pandas as pd                                                      
from dataforge.utils.paths import RAW_DATA_DIR

def validate_field_orders(raw_records: list[dict]) -> tuple[list[dict], list[dict]]:          
    print('to aqui')
    valid_records = []                                                                        
    quarantine_records = []                                                                   
                                                                                                  
    for row in raw_records:                                                                   
        # 1. Mapear os campos da planilha para os nomes do contrato                           
            mapped_data = {                                                                       
                "ordem_id": row.get("Nº item da ordem") or row.get("ordem_id"),                   
                "contratos": row.get("Contrato") or row.get("contratos"),                         
                "nome_cliente": row.get("NomeCliente") or row.get("nome_cliente"),                
                "val_fat": row.get("Val Fat") or row.get("val_fat"),                              
                "latitude": row.get("Latitude localiz.geográfica") or row.get("latitude"),        
                "longitude": row.get("Longitude localiz.geográfica") or row.get("longitude"),     
                "hora_leitura": row.get("Hora leit.") or row.get("hora_leitura"),                 
                "status_leitura": row.get("FA CT OK") or row.get("status_leitura"),               
            }                                                                                     
                                                                                                  
            # 2. Tentar validar com o Pydantic                                                    
            try:                                                                                  
                validated = FieldOrderContract(**mapped_data)                                     
                valid_records.append(validated.model_dump())                                      
            except ValidationError as error:                                                      
                row_with_error = dict(row)                                                        
                row_with_error["erro_validacao"] = str(error)                                     
                row_with_error["data_quarentena"] = datetime.now().isoformat()                    
                quarantine_records.append(row_with_error)                                         
                                                                                                  
        # 3. Se houver itens inválidos, salvar na pasta de quarentena                             
    if quarantine_records:                                                                    
            quarantine_dir = DATA_DIR / "quarantine" / "field_orders"                             
            quarantine_dir.mkdir(parents=True, exist_ok=True)                                     
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")                                  
            quarantine_file = quarantine_dir / f"quarantine_{timestamp}.json"                     
                                                                                                  
            with open(quarantine_file, "w", encoding="utf-8") as f:                               
                json.dump(quarantine_records, f, indent=4, ensure_ascii=False)                    
            print(f"⚠️ {len(quarantine_records)} registros enviados para Quarentena em: {quarantine_file.name}")                                                            
                                                                                                  
    return valid_records, quarantine_records                                                  
                                                                                                  
                                                                                                  
if __name__ == "__main__":
    arquivos_lista = RAW_DATA_DIR / "field_orders"                                             

    for arquivos in arquivos_lista.glob('*.xlsx'):
        try:
            df = pd.read_excel(arquivos)
            raw_records = df.to_dict(orient="records")
            
        except ValidationError as error:
            print(f"Erro ao validar arquivo {arquivos.name}: {error}")
   
        
    validos, quarentena = validate_field_orders(raw_records)
    print(f'Válidos: {len(validos)}')
    print(f'Quarentena: {len(quarentena)}')
