with source as (
    select
        id,
        source,
        raw_json,
        ingested_at,
        json_each(raw_json) as coin_entry
    from {{ source('pulse', 'raw_crypto') }}
)

select
    row_number() over (order by id, coin_entry.key) as id,
    source,
    coin_entry.key as coin,
    cast(json_extract(coin_entry.value, '$.usd') as float) as price_usd,
    ingested_at,
    raw_json
from source
