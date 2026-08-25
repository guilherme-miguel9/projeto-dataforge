import pytest
from pydantic import ValidationError

from dataforge.quality.contracts import CustomerContract
from dataforge.quality.validator import validate_field_orders


def test_customer_contract_valid():
    """Garante que um cliente com dados válidos seja instanciado sem erro."""
    customer = CustomerContract(
        id=1,
        first_name="Carlos",
        last_name="Silva",
        email="carlos.silva@email.com",
        age=32,
    )
    assert customer.first_name == "Carlos"
    assert customer.email == "carlos.silva@email.com"


def test_customer_contract_invalid_age():
    """Garante que o Pydantic levante ValidationError para idades negativas."""
    with pytest.raises(ValidationError):
        CustomerContract(
            id=1,
            first_name="Carlos",
            last_name="Silva",
            email="carlos@email.com",
            age=-5,  # <-- Inválido! Idade não pode ser negativa
        )


def test_validator_routes_to_quarantine():
    """Garante que faturas negativas vão para a quarentena e faturas boas vão para os válidos."""
    raw_data = [
        # Linha VÁLIDA (contratos é número int!)
        {
            "ordem_id": 1001,
            "contratos": 12345,
            "nome_cliente": "Ana Costa",
            "val_fat": 150.50,
            "latitude": -23.5505,
            "longitude": -46.6333,
            "hora_leitura": "10:30:00",
            "status_leitura": "OK",
        },
        # Linha INVÁLIDA (Fatura negativa < 1)
        {
            "ordem_id": 1002,
            "contratos": 99999,
            "nome_cliente": "João Errado",
            "val_fat": -50.00,  # <-- Erro! Fatura negativa
            "latitude": -23.5505,
            "longitude": -46.6333,
            "hora_leitura": "10:30:00",
            "status_leitura": "OK",
        },
    ]

    validos, quarentena = validate_field_orders(raw_data)

    assert len(validos) == 1
    assert len(quarentena) == 1
    assert validos[0]["nome_cliente"] == "Ana Costa"
    assert "val_fat" in quarentena[0]["erro_validacao"]
