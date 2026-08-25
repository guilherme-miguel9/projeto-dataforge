with source_data as (
    select * from "dataforge_dw"."raw_silver"."customers"
)

select
    id as customer_id,
    first_name,
    last_name,
    email,
    age
from source_data