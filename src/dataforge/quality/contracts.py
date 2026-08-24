from numpy import dtypes
from pydantic import BaseModel, Field
from typing import List
import json
import pandas as pd


class FieldOrderContract(BaseModel):
    ordem_id: int = Field(ge=1, description='A ordem_id deverá ser maior que 0')
    contratos: int = Field(ge=1, description='O contrato deverá ser maior que 0')
    nome_cliente: str = Field(min_length=1, max_length=50, description='O nome não poderá ser nulo')
    val_fat: float = Field(ge=1, description='O valor da fatura não podera ser nulo/vazio')
    latitude: float = Field(description='A latitude não pode estar nulo.')
    longitude: float = Field(description='A longitude não pode estar nulo.')
    hora_leitura: str = Field(description='Não pode ser nulo')
    status_leitura: str = Field(description='Status da leitura não pode ser nulo')

class CustomerContract(BaseModel):
    id: int = Field(ge=0, description='id deverá ser > 0')
    first_name : str = Field(min_length=1, max_length= 50, description = 'Nome não pode ser nulo')
    last_name : str = Field(min_length=1, max_length= 50, description = 'Sobrenome não pode ser nulo')
    email : str = Field(min_length=1, max_length= 50, description = 'Email não pode ser nulo')
    age : int = Field(ge=0, description = 'Idade não pode ser nulo')
    
