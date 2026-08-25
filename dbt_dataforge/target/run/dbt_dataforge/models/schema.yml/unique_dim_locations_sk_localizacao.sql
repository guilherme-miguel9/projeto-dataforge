
    
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    

select
    sk_localizacao as unique_field,
    count(*) as n_records

from "dataforge_dw"."gold"."dim_locations"
where sk_localizacao is not null
group by sk_localizacao
having count(*) > 1



  
  
      
    ) dbt_internal_test