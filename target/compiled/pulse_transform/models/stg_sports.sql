with source as (
    select
        id,
        source,
        raw_json,
        ingested_at,
        raw_json::jsonb -> 'events' as events_json
    from "pulse"."public"."raw_sports"
),
parsed as (
    select
        id,
        source,
        raw_json,
        ingested_at,
        events_json -> 0 ->> 'date' as game_date,
        events_json -> 0 -> 'competitions' -> 0 -> 'competitors' -> 0 -> 'team' ->> 'abbreviation' as home_team,
        events_json -> 0 -> 'competitions' -> 0 -> 'competitors' -> 0 ->> 'score' as home_score,
        events_json -> 0 -> 'competitions' -> 0 -> 'competitors' -> 1 -> 'team' ->> 'abbreviation' as away_team,
        events_json -> 0 -> 'competitions' -> 0 -> 'competitors' -> 1 ->> 'score' as away_score
    from source
)
select
    id,
    source,
    trim(home_team) as home_team,
    trim(away_team) as away_team,
    cast(home_score as integer) as home_score,
    cast(away_score as integer) as away_score,
    game_date,
    ingested_at,
    raw_json
from parsed