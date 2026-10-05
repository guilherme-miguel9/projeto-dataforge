with distinct_clients as (
    select distinct
        nome_cliente
    from {{ ref('stg_field_orders') }}
    where nome_cliente is not null
)

select
    md5(nome_cliente) as id_cliente,
    nome_cliente

from distinct_clients
