with distinct_agents as (
    select distinct
        cod_leit,
        nome_leit
    from {{ ref('stg_field_orders') }}
    where cod_leit is not null
)

select
    md5(concat(cod_leit, '_', coalesce(nome_leit, ''))) as id_agente,
    cod_leit,
    nome_leit

from distinct_agents
