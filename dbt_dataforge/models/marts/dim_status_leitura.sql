with distinct_status as (
    select distinct
        cond_wol,
        tipo_ordem,
        res_campo,
        impresso,
        tipo_rota,
        fa_ct_ok,
        o_sem_leit_real,
        indic_foto,
        coment_leitura,
        coment_fatura
    from {{ ref('stg_field_orders') }}
)

select
    md5(concat_ws('||',
        coalesce(cond_wol, ''),
        coalesce(tipo_ordem, ''),
        coalesce(res_campo, ''),
        coalesce(impresso, ''),
        coalesce(tipo_rota, ''),
        coalesce(fa_ct_ok, ''),
        coalesce(o_sem_leit_real, ''),
        coalesce(indic_foto, ''),
        coalesce(coment_leitura, ''),
        coalesce(coment_fatura, '')
    )) as id_status,
    cond_wol,
    tipo_ordem,
    res_campo,
    impresso,
    tipo_rota,
    fa_ct_ok,
    o_sem_leit_real,
    indic_foto,
    coment_leitura,
    coment_fatura

from distinct_status
