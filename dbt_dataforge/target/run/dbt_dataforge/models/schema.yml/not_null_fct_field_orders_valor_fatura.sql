
    
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select valor_fatura
from "dataforge_dw"."gold"."fct_field_orders"
where valor_fatura is null



  
  
      
    ) dbt_internal_test