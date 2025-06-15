SELECT
    appid::bigint AS appid,
    player_count::integer AS player_count,
    "timestamp"::timestamp AS collected_time
FROM {{ source('steam_dbt_schema', 'top_100_player_counts') }}