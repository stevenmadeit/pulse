
  
    

  create  table "pulse"."public_public"."stg_weather__dbt_tmp"
  
  
    as
  
  (
    with source as (
    select
        id,
        source,
        raw_json::jsonb ->> 'requested_city' as city,
        raw_json::jsonb -> 'current_weather' ->> 'temperature' as temperature,
        raw_json::jsonb -> 'current_weather' ->> 'weathercode' as weather_code,
        raw_json::jsonb ->> 'requested_latitude' as latitude,
        raw_json::jsonb ->> 'requested_longitude' as longitude,
        ingested_at,
        raw_json
    from "pulse"."public"."raw_weather"
)

select
    id,
    source,
    city,
    cast(temperature as float) as temperature,
    case cast(weather_code as integer)
        when 0 then 'clear'
        when 1 then 'mainly_clear'
        when 2 then 'partly_cloudy'
        when 3 then 'overcast'
        when 45 then 'fog'
        when 48 then 'depositing_rime_fog'
        when 51 then 'drizzle_light'
        when 53 then 'drizzle_moderate'
        when 55 then 'drizzle_dense'
        when 56 then 'freezing_drizzle_light'
        when 57 then 'freezing_drizzle_dense'
        when 61 then 'rain_slight'
        when 63 then 'rain_moderate'
        when 65 then 'rain_heavy'
        when 66 then 'freezing_rain_light'
        when 67 then 'freezing_rain_heavy'
        when 71 then 'snow_fall_slight'
        when 73 then 'snow_fall_moderate'
        when 75 then 'snow_fall_heavy'
        when 77 then 'snow_grains'
        when 80 then 'rain_showers_slight'
        when 81 then 'rain_showers_moderate'
        when 82 then 'rain_showers_violent'
        when 85 then 'snow_showers_slight'
        when 86 then 'snow_showers_heavy'
        when 95 then 'thunderstorm_slight_or_moderate'
        when 96 then 'thunderstorm_hail_slight'
        when 99 then 'thunderstorm_hail_heavy'
        else 'unknown'
    end as condition,
    ingested_at,
    raw_json
from source
  );
  