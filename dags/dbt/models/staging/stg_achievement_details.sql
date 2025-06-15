SELECT 
	a.appid::bigint,
	(elem->>'name')::text AS name,
	(elem->>'defaultvalue')::int AS default_value,
	(elem->>'hidden')::int::boolean AS hidden,
	(elem->>'displayName')::text AS display_name,
	(elem->>'description')::text AS description,
	(elem->>'icon')::text AS icon_link,
	(elem->>'icongray')::text AS icon_gray_link
FROM
	{{ source('steam_dbt_schema', 'achievement_details') }} AS a,
	jsonb_array_elements(a.json_data) AS elem
