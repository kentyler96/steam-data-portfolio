from sqlalchemy import create_engine
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy import text
import pandas as pd
import steam_api_func


def to_db(df, name, if_exists, datatype=None, schema='steam_dbt_schema'):
    engine = create_engine(
        'postgresql+psycopg2://steam_dbt_role:password@db:5432/steam_dbt_db',
        connect_args={'connect_timeout': 10}
    )

    if if_exists == 'replace':
        with engine.begin() as conn:
            drop_table_sql = f'DROP TABLE IF EXISTS {schema}."{name}" CASCADE;'
            conn.execute(text(drop_table_sql))

            drop_type_sql = f"""
            DO $$
            BEGIN
                IF EXISTS (
                    SELECT 1 FROM pg_type t
                    JOIN pg_namespace n ON n.oid = t.typnamespace
                    WHERE t.typname = '{name}' AND n.nspname = '{schema}'
                ) THEN
                    EXECUTE 'DROP TYPE {schema}."{name}" CASCADE';
                END IF;
            END$$;
            """
            conn.execute(text(drop_type_sql))

    df.to_sql(
        name,
        engine,
        if_exists=if_exists,
        schema=schema,
        index=False,
        dtype=datatype
    )

    engine.dispose()