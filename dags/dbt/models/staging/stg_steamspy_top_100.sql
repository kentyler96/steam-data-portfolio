SELECT
    appid::bigint AS appid,
    name::text AS name,
    developer::text AS developer,
    publisher::text AS publisher,
    positive::bigint AS positive_ratings,
    negative::bigint AS negative_ratings
FROM {{ source('steam_dbt_schema', 'steamspy_top_100') }}
