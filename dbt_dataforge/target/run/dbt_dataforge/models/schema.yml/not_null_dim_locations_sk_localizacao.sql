
    
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select sk_localizacao
from "dataforge_dw"."gold"."dim_locations"
where sk_localizacao is null



  
  
      
    ) dbt_internal_test