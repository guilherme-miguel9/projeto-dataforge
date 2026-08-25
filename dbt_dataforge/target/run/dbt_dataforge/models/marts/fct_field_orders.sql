
  
    

  create  table "dataforge_dw"."gold"."fct_field_orders__dbt_tmp"
  
  
    as
  
  (
    with stg_orders as (                                                                            
        select * from "dataforge_dw"."gold"."stg_field_orders"                                                 
    )                                                                                               
                                                                                                    
    select                                                                                          
        -- Chave Primária da Ordem                                                                  
        numero_item_ordem,                                                                          
                                                                                                    
        -- Chaves Estrangeiras (FKs) ligando com as Dimensões!                                      
        md5(contrato) as sk_cliente,                                                                
        md5(concat(latitude::text, '_', longitude::text)) as sk_localizacao,                        
                                                                                                    
        -- Métricas e Fatos                                                                         
        instalacao,                                                                                 
        valor_fatura,                                                                               
        hora_leitura,                                                                               
        status_leitura,                                                                             
                                                                                                    
        -- Data de Carga no Data Warehouse                                                          
        current_timestamp as data_processamento_dw                                                  
                                                                                                    
    from stg_orders
  );
  