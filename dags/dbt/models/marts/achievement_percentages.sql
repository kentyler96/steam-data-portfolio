SELECT 
	ach.appid, 
	spy.name AS game_name, 
	det.name,
	det.display_name,
	ach.achievement_percent,
	ach.timestamp
FROM {{ ref('stg_achievement_percentages') }} AS ach
JOIN {{ ref('stg_steamspy_top_100') }} AS spy
ON ach.appid = spy.appid
JOIN {{ ref('stg_achievement_details') }} AS det
ON ach.appid = det.appid AND ach.name = det.name