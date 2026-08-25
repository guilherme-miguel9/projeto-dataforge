
    
    

select
    sk_cliente as unique_field,
    count(*) as n_records

from "dataforge_dw"."gold"."dim_customers"
where sk_cliente is not null
group by sk_cliente
having count(*) > 1


