-- Fails if any cleaned trip has an amount of 0 or less
select *
from {{ ref('stg_green_taxi') }}
where total_amount <= 0