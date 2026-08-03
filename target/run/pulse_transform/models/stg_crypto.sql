
  
    

  create  table "pulse"."public_public"."stg_crypto__dbt_tmp"
  
  
    as
  
  (
    with source as (
    select
        id,
        source,
        raw_json,
        ingested_at,
        raw_json::jsonb as payload
    from "pulse"."public"."raw_crypto"
),
flattened as (
    select
        id,
        source,
        raw_json,
        ingested_at,
        key as coin,
        nullif(value ->> 'usd', '') as price_usd
    from source,
    jsonb_each(payload)
)
select
    row_number() over (order by id, coin) as id,
    source,
    coin,
    cast(price_usd as float) as price_usd,
    ingested_at,
    raw_json
from flattened
  );
  