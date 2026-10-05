with stg as (
    select * from {{ ref('stg_field_orders') }}
),

dim_tempo as (
    select * from {{ ref('dim_tempo') }}
),

dim_cliente as (
    select * from {{ ref('dim_cliente') }}
),

dim_agente as (
    select * from {{ ref('dim_agente') }}
),

dim_instalacao as (
    select * from {{ ref('dim_instalacao_contrato') }}
),

dim_status as (
    select * from {{ ref('dim_status_leitura') }}
),

dim_medidor as (
    select * from {{ ref('dim_medidor') }}
),

dim_localizacao as (
    select * from {{ ref('dim_localizacao') }}
)

select
    -- Chave Técnica da Linha do Fato
    md5(concat_ws('||',
        stg.nro_item_ordem,
        coalesce(stg.instal, ''),
        coalesce(stg.data_leitura::text, ''),
        coalesce(stg.hora_leit::text, ''),
        coalesce(stg.registrador, '')
    )) as id_fato_leitura,

    -- Coluna de Particionamento
    extract(year from stg.data_leitura)::int as ano,

    -- Chaves Estrangeiras (FKs)
    dt.id_tempo as fk_tempo,
    di.id_instalacao as fk_instalacao,
    dl.id_localizacao as fk_localizacao,
    dc.id_cliente as fk_cliente,
    dm.id_medidor as fk_medidor,
    da.id_agente as fk_agente,
    ds.id_status as fk_status,

    -- Métricas
    stg.leit,
    stg.desvio_leit,
    stg.interv_leit,
    stg.abaixo_lim,
    stg.excede_lim,
    stg.nota_leit,
    stg.hora_leit,
    stg.val_fat,

    -- Identificadores Degenerados
    stg.nro_ordem,
    stg.nro_item_ordem,
    stg.o_leitura_real

from stg

left join dim_tempo dt
    on dt.data_completa = stg.data_leitura

left join dim_cliente dc
    on dc.nome_cliente = stg.nome_cliente

left join dim_agente da
    on da.cod_leit = stg.cod_leit
    and coalesce(da.nome_leit, '') = coalesce(stg.nome_leit, '')

left join dim_instalacao di
    on di.instal = stg.instal
    and coalesce(di.contrato, '') = coalesce(stg.contrato, '')

left join dim_status ds
    on  coalesce(ds.cond_wol, '') = coalesce(stg.cond_wol, '')
    and coalesce(ds.tipo_ordem, '') = coalesce(stg.tipo_ordem, '')
    and coalesce(ds.res_campo, '') = coalesce(stg.res_campo, '')
    and coalesce(ds.impresso, '') = coalesce(stg.impresso, '')
    and coalesce(ds.tipo_rota, '') = coalesce(stg.tipo_rota, '')
    and coalesce(ds.fa_ct_ok, '') = coalesce(stg.fa_ct_ok, '')
    and coalesce(ds.o_sem_leit_real, '') = coalesce(stg.o_sem_leit_real, '')
    and coalesce(ds.indic_foto, '') = coalesce(stg.indic_foto, '')
    and coalesce(ds.coment_leitura, '') = coalesce(stg.coment_leitura, '')
    and coalesce(ds.coment_fatura, '') = coalesce(stg.coment_fatura, '')

-- Join temporal SCD Tipo 2 (vigência na data da leitura)
left join dim_medidor dm
    on  dm.nro_serie = stg.nro_serie
    and stg.data_leitura >= dm.data_inicio_validade
    and (stg.data_leitura <= dm.data_fim_validade or dm.data_fim_validade is null)

left join dim_localizacao dl
    on  coalesce(dl.obj_ligacao, concat(dl.latitude::text, '_', dl.longitude::text)) = coalesce(stg.obj_ligacao, concat(stg.latitude::text, '_', stg.longitude::text))
    and stg.data_leitura >= dl.data_inicio_validade
    and (stg.data_leitura <= dl.data_fim_validade or dl.data_fim_validade is null)
