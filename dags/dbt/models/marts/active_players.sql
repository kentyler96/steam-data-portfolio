SELECT counts.appid, spy.name, counts.player_count, TO_CHAR(counts.collected_time, 'mm/dd/yy HH12:MI') AS timestamp
FROM {{ ref('stg_active_players') }} AS counts
JOIN {{ ref('stg_steamspy_top_100') }} AS spy
ON counts.appid = spy.appid
WHERE counts.player_count IS NOT NULL
ORDER BY counts.player_count DESC, counts.collected_time DESC