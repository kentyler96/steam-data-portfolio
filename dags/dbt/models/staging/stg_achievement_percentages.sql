SELECT 
	appid::bigint,
	name::text,
	achievement_percent::numeric(5,2),
	timestamp::timestamp
FROM {{ source('steam_dbt_schema', 'achievement_percentages') }}