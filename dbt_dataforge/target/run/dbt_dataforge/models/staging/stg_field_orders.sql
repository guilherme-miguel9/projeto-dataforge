
  create view "dataforge_dw"."gold"."stg_field_orders__dbt_tmp"
    
    
  as (
    with source_data as (
    select * from "dataforge_dw"."raw_silver"."field_orders"
)

select
    -- Identificadores e Chaves
    ordem_id::text as numero_item_ordem,
    contratos::text as contrato,
    LPAD(ordem_id::text, 8, '0') as instalacao,
    
    -- Dados do Cliente
    nome_cliente::text as nome_cliente,
    
    -- Métricas e Faturamento
    val_fat::numeric(10, 2) as valor_fatura,
    hora_leitura::time as hora_leitura,
    latitude::numeric(9, 6) as latitude,
    longitude::numeric(9, 6) as longitude,
    status_leitura::text as status_leitura

from source_data
  );