-- models/marts/dim_locations.sql                                                               
    with distinct_locations as (                                                                    
        select distinct                                                                             
            latitude,                                                                               
            longitude                                                                               
        from "dataforge_dw"."gold"."stg_field_orders"                                                          
        where latitude is not null and longitude is not null                                        
    )                                                                                               
                                                                                                    
    select                                                                                          
        -- Chave Substituta para a Localização Geográfica                                           
        md5(concat(latitude::text, '_', longitude::text)) as sk_localizacao,                        
        latitude,                                                                                   
        longitude                                                                                   
                                                                                                    
    from distinct_locations