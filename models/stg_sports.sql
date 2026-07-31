with source as (
    select
        id,
        source,
        raw_json,
        ingested_at,
        json_extract(raw_json, '$.events') as events_json,
        json_array_length(json_extract(raw_json, '$.events')) as events_count
    from {{ source('pulse', 'raw_sports') }}
),
indexed as (
    select
        id,
        source,
        raw_json,
        ingested_at,
        json_extract(events_json, '$[' || idx || ']') as event_obj
    from source
    join (select 0 as idx union all select 1 union all select 2 union all select 3 union all select 4 union all select 5 union all select 6 union all select 7 union all select 8 union all select 9) as idxs
    on idx < events_count
),
parsed as (
    select
        id,
        source,
        ingested_at,
        json_extract(event_obj, '$.date') as game_date,
        json_extract(event_obj, '$.competitions[0].competitors[0].team.abbreviation') as home_team,
        json_extract(event_obj, '$.competitions[0].competitors[0].score') as home_score,
        json_extract(event_obj, '$.competitions[0].competitors[1].team.abbreviation') as away_team,
        json_extract(event_obj, '$.competitions[0].competitors[1].score') as away_score
    from indexed
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
