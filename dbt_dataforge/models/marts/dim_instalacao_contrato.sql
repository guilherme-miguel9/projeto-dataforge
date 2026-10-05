with distinct_installations as (
    select distinct
        instal,
        contrato,
        sequencia,
        cta_contr,
        fat_assin
    from {{ ref('stg_field_orders') }}
    where instal is not null
)

select
    md5(concat(instal, '_', coalesce(contrato, ''))) as id_instalacao,
    instal,
    contrato,
    sequencia,
    cta_contr,
    fat_assin

from distinct_installations
