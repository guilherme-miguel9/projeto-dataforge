with localizacoes as (
    select distinct
        obj_ligacao,
        rua,
        nro_casa,
        latitude,
        longitude,
        complemento,
        ponto_ref,
        local,
        bairro,
        sigla_edificio,
        nro_sala,
        andar,
        complemento_endereco,
        nro_poste,
        min(data_leitura) over (partition by coalesce(obj_ligacao, concat(latitude::text, '_', longitude::text))) as data_inicio_validade
    from {{ ref('stg_field_orders') }}
    where obj_ligacao is not null or latitude is not null
)

select
    md5(concat_ws('||',
        coalesce(obj_ligacao, ''),
        coalesce(rua, ''),
        coalesce(nro_casa, ''),
        coalesce(latitude::text, ''),
        coalesce(longitude::text, ''),
        data_inicio_validade::text
    )) as id_localizacao,
    obj_ligacao,
    rua,
    nro_casa,
    latitude,
    longitude,
    complemento,
    ponto_ref,
    local,
    bairro,
    sigla_edificio,
    nro_sala,
    andar,
    complemento_endereco,
    nro_poste,
    data_inicio_validade,
    null::date as data_fim_validade,
    'Sim' as versao_atual

from localizacoes
