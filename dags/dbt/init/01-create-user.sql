CREATE USER steam_dbt_role WITH PASSWORD 'password';
GRANT ALL PRIVILEGES ON DATABASE steam_dbt_db TO steam_dbt_role;