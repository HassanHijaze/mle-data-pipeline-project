-- Keep only trips in Jan–Mar 2025 with a positive amount
select
    lpep_pickup_datetime  as pickup_datetime,
    lpep_dropoff_datetime as dropoff_datetime,
    total_amount,
    source_file
from {{ source('raw', 'green_taxi') }}
where lpep_pickup_datetime >= '2025-01-01'
  and lpep_pickup_datetime <  '2025-04-01'
  and total_amount > 0