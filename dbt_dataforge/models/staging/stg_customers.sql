with source_data as (
    select * from {{ source('raw_silver', 'customers') }}
)

select
    id as customer_id,
    first_name,
    last_name,
    email,
    age
from source_data
