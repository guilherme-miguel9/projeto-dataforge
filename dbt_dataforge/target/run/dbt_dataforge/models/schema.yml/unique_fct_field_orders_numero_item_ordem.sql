
    
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    

select
    numero_item_ordem as unique_field,
    count(*) as n_records

from "dataforge_dw"."gold"."fct_field_orders"
where numero_item_ordem is not null
group by numero_item_ordem
having count(*) > 1



  
  
      
    ) dbt_internal_test