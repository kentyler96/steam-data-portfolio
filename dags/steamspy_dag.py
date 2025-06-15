from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from datetime import datetime
from steam_api_func import fetch_top_100

with DAG(
    dag_id='steam_top_100',
    start_date=datetime(2024, 1, 1),
    schedule='@daily',
    catchup=False,
    tags=["top_100"],
) as dag:

    fetch_steam_top_100 = PythonOperator(
        task_id='fetch_steam_top_100',
        python_callable=fetch_top_100,
        dag=dag,
    )

dbt_run = BashOperator(
    task_id='dbt_run',
    bash_command='dbt run --project-dir /opt/airflow/dbt --profiles-dir /home/airflow/.dbt',
)

fetch_steam_top_100 >> dbt_run