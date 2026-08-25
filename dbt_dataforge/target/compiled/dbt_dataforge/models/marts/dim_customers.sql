-- models/marts/dim_customers.sql                                                               
    with orders_customers as (                                                                      
        select distinct                                                                             
            contrato,                                                                               
            nome_cliente                                                                            
        from "dataforge_dw"."gold"."stg_field_orders"                                                          
    ),                                                                                              
                                                                                                    
    api_customers as (                                                                              
        select                                                                                      
            customer_id,                                                                            
            first_name,                                                                             
            last_name,                                                                              
            email,                                                                                  
            age                                                                                     
        from "dataforge_dw"."gold"."stg_customers"                                                             
    )                                                                                               
                                                                                                    
    select                                                                                          
        -- Cria uma Chave Substituta (Surrogate Key) para o Cliente                                 
        md5(o.contrato) as sk_cliente,                                                              
        o.contrato as id_contrato,                                                                  
        o.nome_cliente,                                                                             
        c.email,                                                                                    
        c.age as idade                                                                              
                                                                                                    
    from orders_customers o                                                                         
    left join api_customers c                                                                       
        on lower(split_part(o.nome_cliente, ' ', 1)) = lower(c.first_name)