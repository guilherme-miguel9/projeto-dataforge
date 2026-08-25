from dataforge.extraction.detector import (
    compute_file_hash,
    get_new_files,
    update_manifest,
)


def test_compute_file_hash_deterministic(tmp_path):
    """Garante que o hash SHA-256 seja idêntico para conteúdos iguais."""
    # O tmp_path é uma pasta temporária criada automaticamente pelo pytest
    arquivo1 = tmp_path / "ordem1.txt"
    arquivo2 = tmp_path / "ordem2.txt"

    arquivo1.write_text("conteudo da ordem de servico", encoding="utf-8")
    arquivo2.write_text("conteudo da ordem de servico", encoding="utf-8")

    hash1 = compute_file_hash(arquivo1)
    hash2 = compute_file_hash(arquivo2)

    # 1. Hashes devem ser idênticos
    assert hash1 == hash2
    # 2. SHA-256 sempre tem 64 caracteres hexadecimais
    assert len(hash1) == 64


def test_manifest_idempotency(tmp_path):
    """Garante que arquivos já cadastrados no manifesto não sejam considerados novos."""
    pasta_ordens = tmp_path / "field_orders"
    pasta_ordens.mkdir()
    arquivo_excel = pasta_ordens / "lote1.xlsx"
    arquivo_excel.write_bytes(b"bytes simulados da planilha")

    manifesto = tmp_path / "manifest.json"

    # Primeira execução: deve achar 1 arquivo novo
    novos = get_new_files(pasta_ordens, manifesto)
    assert len(novos) == 1

    # Registra no manifesto
    update_manifest(novos[0], manifesto)

    # Segunda execução: NÃO deve achar nenhum arquivo (0 novos)
    novos_segunda_vez = get_new_files(pasta_ordens, manifesto)
    assert len(novos_segunda_vez) == 0
