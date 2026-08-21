
import requests
from pathlib import Path
import json
from dataforge.utils.paths import RAW_DATA_DIR     








def extract_customers_from_api(limit_per_page: int = 10, max_pages: int = 3) -> list[Path]:
    url = "https://dummyjson.com/users"
    output_dir = RAW_DATA_DIR / "api_customers"
    output_dir.mkdir(parents=True, exist_ok=True)

    saved_files = []

    for page in range(1, max_pages + 1):
        skip = (page - 1) * limit_per_page
        params = {"limit": limit_per_page, "skip": skip}

        response = requests.get(url, params=params, timeout=10)

        if response.status_code == 200:
            data = response.json()
            users = data.get("users", [])

            # Sem dados na página
            if not users:
                break

            # Cria o arquivo com os dados da API
            file_path = output_dir / f"customers_page_{page}.json"
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent = 4)
            
            saved_files.append(file_path)

            # Para verificar se já foi coletado todos os dados
            if skip + len(users) >= data.get("total", 0):
                break
        else:
            print(f"Falha ao obter dados da API: Status {response.status_code}")
            break
    
    return saved_files


if __name__ == "__main__":
    arquivos = extract_customers_from_api(limit_per_page=10, max_pages=3)
    print(f"Total de páginas extraidas: {len(arquivos)}")


    