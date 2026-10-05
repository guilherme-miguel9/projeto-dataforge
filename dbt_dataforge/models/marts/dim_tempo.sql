with distinct_dates as (
    select distinct
        data_leitura as data_completa
    from {{ ref('stg_field_orders') }}
    where data_leitura is not null
)

select
    to_char(data_completa, 'YYYYMMDD')::int as id_tempo,
    data_completa,
    extract(year from data_completa)::int as ano,
    extract(month from data_completa)::int as mes,
    extract(day from data_completa)::int as dia,
    extract(quarter from data_completa)::int as trimestre,
    to_char(data_completa, 'TMDy') as dia_semana

from distinct_dates
