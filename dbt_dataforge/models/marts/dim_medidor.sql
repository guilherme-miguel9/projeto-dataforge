with medidores as (
    select distinct
        nro_serie,
        unid_leit,
        seq_mod,
        registrador,
        min(data_leitura) over (partition by nro_serie, unid_leit, seq_mod, registrador) as data_inicio_validade
    from {{ ref('stg_field_orders') }}
    where nro_serie is not null
)

select
    md5(concat_ws('||',
        nro_serie,
        coalesce(unid_leit, ''),
        coalesce(seq_mod, ''),
        coalesce(registrador, ''),
        data_inicio_validade::text
    )) as id_medidor,
    nro_serie,
    unid_leit,
    seq_mod,
    registrador,
    data_inicio_validade,
    null::date as data_fim_validade,
    'Sim' as versao_atual

from medidores
