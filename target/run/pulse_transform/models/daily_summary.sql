
  
    

  create  table "pulse"."public_public"."daily_summary__dbt_tmp"
  
  
    as
  
  (
    with latest_weather as (
    select
        city,
        temperature,
        condition,
        ingested_at
    from "pulse"."public_public"."stg_weather"
    order by ingested_at desc
    limit 1
),
latest_sports as (
    select
        home_team,
        away_team,
        home_score,
        away_score,
        game_date,
        ingested_at
    from "pulse"."public_public"."stg_sports"
    order by game_date desc
    limit 10
),
top_crypto as (
    select
        coin,
        price_usd,
        ingested_at
    from "pulse"."public_public"."stg_crypto"
    order by price_usd desc
    limit 5
)

select
    w.city as weather_city,
    w.temperature as weather_temperature,
    w.condition as weather_condition,
    w.ingested_at as weather_ingested_at,
    s.home_team,
    s.away_team,
    s.home_score,
    s.away_score,
    s.game_date as sports_game_date,
    s.ingested_at as sports_ingested_at,
    c.coin as crypto_coin,
    c.price_usd as crypto_price_usd,
    c.ingested_at as crypto_ingested_at
from latest_weather w
cross join latest_sports s
cross join top_crypto c
  );
  