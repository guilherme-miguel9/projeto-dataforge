import json
from datetime import UTC, datetime

import pandas as pd
from pydantic import ValidationError

from dataforge.quality.contracts import FieldOrderContract
from dataforge.utils.paths import DATA_DIR, RAW_DATA_DIR


def validate_field_orders(raw_records: list[dict]) -> tuple[list[dict], list[dict]]:
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
            "longitude": row.get("Longitude localiz.geográfica")
            or row.get("longitude"),
            "hora_leitura": str(
                row.get("Hora leit.") or row.get("hora_leitura") or "00:00:00"
            ),
            "status_leitura": str(
                row.get("FA CT OK") or row.get("status_leitura") or "OK"
            ),
            "data_leitura": str(
                row.get("Data_Atual")
                or row.get("data_leitura")
                or datetime.now(UTC).strftime("%Y-%m-%d")
            ),
            "nro_ordem": str(row.get("Nº") or row.get("nro_ordem") or ""),
            "instalacao": str(row.get("Instal") or row.get("instalacao") or ""),
            "registrador": str(row.get("Registrador") or row.get("registrador") or ""),
            "rua": str(row.get("Rua") or row.get("rua") or ""),
            "nro_casa": str(row.get("Nº da casa") or row.get("nro_casa") or ""),
            "sequencia": str(row.get("Sequência") or row.get("sequencia") or ""),
            "complemento": str(row.get("Complemento") or row.get("complemento") or ""),
            "ponto_ref": str(row.get("Ponto Ref") or row.get("ponto_ref") or ""),
            "local": str(row.get("Local") or row.get("local") or ""),
            "bairro": str(row.get("Bairro") or row.get("bairro") or ""),
            "sigla_edificio": str(
                row.get("Sigla edifício") or row.get("sigla_edificio") or ""
            ),
            "nro_sala": str(row.get("Nº sala") or row.get("nro_sala") or ""),
            "andar": str(row.get("Andar") or row.get("andar") or ""),
            "complemento_endereco": str(
                row.get("Complemento endereco") or row.get("complemento_endereco") or ""
            ),
            "obj_ligacao": str(row.get("ObjLigacao") or row.get("obj_ligacao") or ""),
            "nro_poste": str(row.get("Nº Poste") or row.get("nro_poste") or ""),
            "nro_serie": str(row.get("Nº Serie") or row.get("nro_serie") or ""),
            "unid_leit": str(row.get("Unid.leit") or row.get("unid_leit") or ""),
            "o_leitura_real": str(
                row.get("O. leitura real") or row.get("o_leitura_real") or ""
            ),
            "o_sem_leit_real": str(
                row.get("O. Sem leit real") or row.get("o_sem_leit_real") or ""
            ),
            "nota_leit": str(row.get("Nota leit.") or row.get("nota_leit") or ""),
            "seq_mod": str(row.get("Seq.Mod") or row.get("seq_mod") or ""),
            "cond_wol": str(row.get("Cond WOL") or row.get("cond_wol") or ""),
            "leit": float(row.get("Leit") or row.get("leit") or 0.0),
            "cod_leit": str(
                row.get("Codigo_Leitor")
                or row.get("cod_leit")
                or row.get("Cod_Leit")
                or ""
            ),
            "nome_leit": str(row.get("Nome leit") or row.get("nome_leit") or ""),
            "indic_foto": str(row.get("Indic Foto") or row.get("indic_foto") or ""),
            "interv_leit": str(row.get("Interv.Leit") or row.get("interv_leit") or ""),
            "cta_contr": str(row.get("Cta.contr.") or row.get("cta_contr") or ""),
            "abaixo_lim": str(row.get("Abaixo lim") or row.get("abaixo_lim") or ""),
            "excede_lim": str(row.get("Excede lim") or row.get("excede_lim") or ""),
            "desvio_leit": str(row.get("Desvio leit") or row.get("desvio_leit") or ""),
            "fat_assin": str(row.get("Fat. Assin") or row.get("fat_assin") or ""),
            "tipo_ordem": str(row.get("Tipo ordem") or row.get("tipo_ordem") or ""),
            "res_campo": str(row.get("ResCampo") or row.get("res_campo") or ""),
            "impresso": str(row.get("Impresso") or row.get("impresso") or ""),
            "coment_leitura": str(
                row.get("Coment.leitura") or row.get("coment_leitura") or ""
            ),
            "coment_fatura": str(
                row.get("Coment.fatura") or row.get("coment_fatura") or ""
            ),
            "tipo_rota": str(row.get("Tipo rota") or row.get("tipo_rota") or ""),
            "fa_ct_ok": str(row.get("FA CT OK") or row.get("fa_ct_ok") or ""),
        }

        # 2. Tentar validar com o Pydantic
        try:
            validated = FieldOrderContract(**mapped_data)
            valid_records.append(validated.model_dump())
        except ValidationError as error:
            row_with_error = dict(row)
            row_with_error["erro_validacao"] = str(error)
            row_with_error["data_quarentena"] = datetime.now(UTC).isoformat()
            quarantine_records.append(row_with_error)

    # 3. Se houver itens inválidos, salvar na pasta de quarentena
    if quarantine_records:
        quarantine_dir = DATA_DIR / "quarantine" / "field_orders"
        quarantine_dir.mkdir(parents=True, exist_ok=True)
        timestamp = datetime.now(UTC).strftime("%Y%m%d_%H%M%S")
        quarantine_file = quarantine_dir / f"quarantine_{timestamp}.json"

        with open(quarantine_file, "w", encoding="utf-8") as f:
            json.dump(quarantine_records, f, indent=4, ensure_ascii=False)
        print(
            f"⚠️ {len(quarantine_records)} registros enviados para Quarentena em: {quarantine_file.name}"
        )

    return valid_records, quarantine_records


if __name__ == "__main__":
    arquivos_lista = RAW_DATA_DIR / "field_orders"

    for arquivos in arquivos_lista.glob("*.xlsx"):
        try:
            df = pd.read_excel(arquivos)
            raw_records = df.to_dict(orient="records")

        except ValidationError as error:
            print(f"Erro ao validar arquivo {arquivos.name}: {error}")

    validos, quarentena = validate_field_orders(raw_records)
    print(f"Válidos: {len(validos)}")
    print(f"Quarentena: {len(quarentena)}")
