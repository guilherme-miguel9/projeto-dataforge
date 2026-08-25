
    
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select numero_item_ordem
from "dataforge_dw"."gold"."fct_field_orders"
where numero_item_ordem is null



  
  
      
    ) dbt_internal_test