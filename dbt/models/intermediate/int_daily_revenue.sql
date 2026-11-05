-- One row per day: number of trips and total revenue
select
    cast(pickup_datetime as date)          as pickup_date,
    count(*)                               as trip_count,
    round(sum(total_amount)::numeric, 2)   as revenue
from {{ ref('stg_green_taxi') }}
group by 1