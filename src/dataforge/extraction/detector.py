from dataforge.utils.paths import PROCESSED_DATA_DIR
from dataforge.utils.paths import RAW_DATA_DIR
from pathlib import Path
import hashlib
import json
from datetime import datetime
import os


def update_manifest(file_path: Path, manifest_path: Path, status: str = "INGESTED"):                                  
        """Registra o arquivo e seus metadados no manifesto JSON."""                                                      
        manifest = load_manifest(manifest_path)                                                                           
        file_hash = compute_file_hash(file_path)                                                                          
                                                                                                                          
        # Adiciona os metadados do arquivo na chave do hash                                                               
        manifest[file_hash] = {                                                                                           
            "file_name": file_path.name,                                                                                  
            "file_size_bytes": file_path.stat().st_size,                                                                  
            "ingested_at": datetime.now().isoformat(),                                                                    
            "status": status                                                                                              
        }                                                                                                                 
                                                                                                                          
        manifest_path.parent.mkdir(parents=True, exist_ok=True)                                                           
        with open(manifest_path, "w", encoding="utf-8") as f:                                                             
            json.dump(manifest, f, indent=4)


def get_new_files(directory: Path, manifest_path: Path) -> list[Path]:                                                
        """Retorna apenas os arquivos que ainda NÃO estão registrados no manifesto."""                                    
        manifest = load_manifest(manifest_path)                                                                           
        new_files = []                                                                                                    
                                                                                                                          
        for file_path in directory.glob("*.xlsx"):                                                                        
            file_hash = compute_file_hash(file_path)                                                                      
            # Se o hash NÃO está no manifesto, significa que é um arquivo novo!                                           
            if file_hash not in manifest:                                                                                 
                new_files.append(file_path)                                                                               
                                                                                                                          
        return new_files  


def compute_file_hash(file_path: Path) -> str:
    hasher = hashlib.sha256()
    with open(file_path, "rb") as f:
        while chunk := f.read(8192):
            hasher.update(chunk)


    return hasher.hexdigest()

def load_manifest(manifest_path: Path) -> dict:
    if not manifest_path.exists():
        return {}
    with open(manifest_path, "r", encoding="utf-8") as f:
        return json.load(f)

class Detector: 
    ...





if __name__ == "__main__":

    source_dir = RAW_DATA_DIR / "field_orders"                                                                        
    manifest_file = PROCESSED_DATA_DIR / "metadata" / "ingestion_manifest.json"  
    

    novos = get_new_files(source_dir, manifest_file)                                                                  
    print(f"Arquivos novos encontrados: {len(novos)}")

    for f in novos:                                                                                                   
        print(f"  🆕 {f.name}")                                                                                       
        update_manifest(f, manifest_file)                                                                             
        print(f"  ✅ Registrado no manifesto!") 

    print("\n--- Testando segunda execução (Idempotência) ---")                                                       
    novos_segunda_vez = get_new_files(source_dir, manifest_file)                                                      
    print(f"Arquivos novos na segunda execução: {len(novos_segunda_vez)} (Esperado: 0)")

        

    
        