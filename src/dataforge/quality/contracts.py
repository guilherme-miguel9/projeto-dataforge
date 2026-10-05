from pydantic import BaseModel, Field


class FieldOrderContract(BaseModel):
    ordem_id: int = Field(ge=1, description="A ordem_id deverá ser maior que 0")
    contratos: int = Field(ge=1, description="O contrato deverá ser maior que 0")
    nome_cliente: str = Field(
        min_length=1, max_length=50, description="O nome não poderá ser nulo"
    )
    val_fat: float = Field(
        ge=1, description="O valor da fatura não podera ser nulo/vazio"
    )
    latitude: float = Field(description="A latitude não pode estar nulo.")
    longitude: float = Field(description="A longitude não pode estar nulo.")
    hora_leitura: str = Field(description="Não pode ser nulo")
    status_leitura: str = Field(description="Status da leitura não pode ser nulo")

    # Campos complementares para o Star Schema de Leituras
    data_leitura: str | None = None
    nro_ordem: str | None = None
    instalacao: str | None = None
    registrador: str | None = None
    rua: str | None = None
    nro_casa: str | None = None
    sequencia: str | None = None
    complemento: str | None = None
    ponto_ref: str | None = None
    local: str | None = None
    bairro: str | None = None
    sigla_edificio: str | None = None
    nro_sala: str | None = None
    andar: str | None = None
    complemento_endereco: str | None = None
    obj_ligacao: str | None = None
    nro_poste: str | None = None
    nro_serie: str | None = None
    unid_leit: str | None = None
    o_leitura_real: str | None = None
    o_sem_leit_real: str | None = None
    nota_leit: str | None = None
    seq_mod: str | None = None
    cond_wol: str | None = None
    leit: float | None = None
    cod_leit: str | None = None
    nome_leit: str | None = None
    indic_foto: str | None = None
    interv_leit: str | None = None
    cta_contr: str | None = None
    abaixo_lim: str | None = None
    excede_lim: str | None = None
    desvio_leit: str | None = None
    fat_assin: str | None = None
    tipo_ordem: str | None = None
    res_campo: str | None = None
    impresso: str | None = None
    coment_leitura: str | None = None
    coment_fatura: str | None = None
    tipo_rota: str | None = None
    fa_ct_ok: str | None = None


class CustomerContract(BaseModel):
    id: int = Field(ge=0, description="id deverá ser > 0")
    first_name: str = Field(
        min_length=1, max_length=50, description="Nome não pode ser nulo"
    )
    last_name: str = Field(
        min_length=1, max_length=50, description="Sobrenome não pode ser nulo"
    )
    email: str = Field(
        min_length=1, max_length=50, description="Email não pode ser nulo"
    )
    age: int = Field(ge=0, description="Idade não pode ser nulo")
