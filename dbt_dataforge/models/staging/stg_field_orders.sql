with source_data as (
    select * from {{ source('raw_silver', 'field_orders') }}
)

select
    -- Identificadores e Chaves Degeneradas
    coalesce(nro_ordem::text, ordem_id::text) as nro_ordem,
    ordem_id::text as nro_item_ordem,
    coalesce(nullif(instalacao, ''), LPAD(ordem_id::text, 8, '0')) as instal,
    registrador::text as registrador,
    sequencia::text as sequencia,
    contratos::text as contrato,
    cta_contr::text as cta_contr,
    fat_assin::text as fat_assin,

    -- Localização
    rua::text as rua,
    nro_casa::text as nro_casa,
    latitude::numeric(9, 6) as latitude,
    longitude::numeric(9, 6) as longitude,
    complemento::text as complemento,
    ponto_ref::text as ponto_ref,
    local::text as local,
    bairro::text as bairro,
    sigla_edificio::text as sigla_edificio,
    nro_sala::text as nro_sala,
    andar::text as andar,
    complemento_endereco::text as complemento_endereco,
    coalesce(nullif(obj_ligacao, ''), ordem_id::text) as obj_ligacao,
    nro_poste::text as nro_poste,

    -- Medidor
    coalesce(nullif(nro_serie, ''), concat('MED-', contratos::text)) as nro_serie,
    coalesce(nullif(unid_leit, ''), 'UL-01') as unid_leit,
    coalesce(nullif(seq_mod, ''), '1') as seq_mod,

    -- Agente / Leiturista
    coalesce(
        nullif(cod_leit, ''),
        case
            when nome_leit = 'Carlos Leiturista' then 'L01'
            when nome_leit = 'Marcos Fiscal' then 'L02'
            when nome_leit = 'Fernanda Campo' then 'L03'
            when nome_leit is not null and nome_leit != '' then concat('L-', substring(md5(nome_leit) from 1 for 4))
            else 'L00'
        end
    ) as cod_leit,
    coalesce(nullif(nome_leit, ''), 'Leiturista Geral') as nome_leit,

    -- Cliente
    nome_cliente::text as nome_cliente,

    -- Status e Junk Dimension
    coalesce(nullif(cond_wol, ''), 'Normal') as cond_wol,
    coalesce(nullif(tipo_ordem, ''), 'Regular') as tipo_ordem,
    coalesce(nullif(res_campo, ''), 'Executado') as res_campo,
    coalesce(nullif(impresso, ''), 'S') as impresso,
    coalesce(nullif(tipo_rota, ''), 'Convencional') as tipo_rota,
    coalesce(nullif(fa_ct_ok, ''), status_leitura, 'OK') as fa_ct_ok,
    coalesce(nullif(o_sem_leit_real, ''), 'N') as o_sem_leit_real,
    coalesce(nullif(indic_foto, ''), 'N') as indic_foto,
    coalesce(nullif(coment_leitura, ''), '') as coment_leitura,
    coalesce(nullif(coment_fatura, ''), '') as coment_fatura,

    -- Métricas e Dados da Leitura
    coalesce(leit::numeric(12, 4), 0.0) as leit,
    coalesce(nullif(desvio_leit, ''), 'N') as desvio_leit,
    coalesce(nullif(interv_leit, ''), '30') as interv_leit,
    coalesce(nullif(abaixo_lim, ''), 'N') as abaixo_lim,
    coalesce(nullif(excede_lim, ''), 'N') as excede_lim,
    coalesce(nullif(nota_leit, ''), '') as nota_leit,
    hora_leitura::time as hora_leit,
    val_fat::numeric(10, 2) as val_fat,
    coalesce(nullif(o_leitura_real, ''), 'S') as o_leitura_real,
    coalesce(data_leitura::date, current_date) as data_leitura

from source_data