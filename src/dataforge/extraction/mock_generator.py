import random
from datetime import UTC, datetime, timedelta

import pandas as pd

from dataforge.utils.paths import RAW_DATA_DIR

# Listas auxiliares para gerar valores aleatórios
NAMES = [
    "João Silva",
    "Maria Santos",
    "Pedro Oliveira",
    "Ana Costa",
    "Carlos Souza",
    "Juliana Lima",
]
STREETS = ["Rua das Flores", "Av. Brasil", "Rua Bahia", "Av. Paulista", "Rua do Sol"]
NEIGHBORHOODS = ["Centro", "Boa Vista", "Jardins", "Copacabana", "Industrial"]
READERS = ["Carlos Leiturista", "Marcos Fiscal", "Fernanda Campo"]


def generate_mock_sales_file(filename: str, num_records: int = 50) -> str:
    """Gera uma planilha Excel sintética simulando ordens de serviço/leituras de campo."""
    rows = []

    for i in range(1, num_records + 1):
        row = {
            "Nº": i,
            "Nº item da ordem": random.randint(100000, 999999),
            "Instal": random.randint(10000, 99999),
            "Registrador": f"REG-{random.randint(100, 999)}",
            "Rua": random.choice(STREETS),
            "Nº da casa": random.randint(1, 2000),
            "Sequência": i,
            "Contrato": random.randint(1000000, 9999999),
            "Latitude localiz.geográfica": round(random.uniform(-23.6, -23.4), 6),
            "Longitude localiz.geográfica": round(random.uniform(-46.7, -46.5), 6),
            "Val Fat": round(random.uniform(45.0, 1200.0), 2),
            "NomeCliente": random.choice(NAMES),
            "Complemento": random.choice(["Casa", "Apto 101", "Bloco B", ""]),
            "Ponto Ref": random.choice(["Próximo à padaria", "Em frente ao posto", ""]),
            "Local": "Urbano",
            "Bairro": random.choice(NEIGHBORHOODS),
            "Sigla edifício": "",
            "Nº sala": "",
            "Andar": "",
            "Complemento endereco": "",
            "ObjLigacao": random.randint(1000, 9999),
            "Nº Poste": f"P-{random.randint(100, 999)}",
            "Nº Serie": f"SN-{random.randint(10000, 99999)}",
            "Unid.leit": "UL-01",
            "O. leitura real": random.choice(["S", "N"]),
            "O. Sem leit real": "N",
            "Nota leit.": "",
            "Hora leit.": (
                datetime.now(UTC) - timedelta(minutes=random.randint(5, 500))
            ).strftime("%H:%M:%S"),
            "Seq.Mod": 1,
            "Cond WOL": "Normal",
            "Leit": random.randint(1000, 5000),
            "Nome leit": random.choice(READERS),
            "Indic Foto": random.choice(["S", "N"]),
            "Interv.Leit": 30,
            "Cta.contr.": random.randint(100000, 999999),
            "Abaixo lim": "N",
            "Excede lim": "N",
            "Desvio leit": "N",
            "Fat. Assin": "S",
            "Tipo ordem": "Leitura Regular",
            "ResCampo": "Executado",
            "Impresso": "S",
            "Coment.leitura": "",
            "Coment.fatura": "",
            "Tipo rota": "Convencional",
            "FA CT OK": random.choice(["S", "OK", "Sim"]),
        }
        rows.append(row)

    # 1. Definir o diretório de saída e garantir que ele exista
    output_dir = RAW_DATA_DIR / "field_orders"
    output_dir.mkdir(parents=True, exist_ok=True)
    file_path = output_dir / filename

    # 2. Criar o DataFrame e salvar como Excel
    df = pd.DataFrame(rows)
    df.to_excel(file_path, index=False)

    return str(file_path)


if __name__ == "__main__":
    # Gerando 2 arquivos de teste para simularmos lotes diferentes
    file1 = generate_mock_sales_file("ordens_campo_lote1.xlsx", num_records=30)
    file2 = generate_mock_sales_file("ordens_campo_lote2.xlsx", num_records=40)
    print("Arquivos gerados com sucesso:")
    print(f"{file1}")
    print(f"{file2}")
