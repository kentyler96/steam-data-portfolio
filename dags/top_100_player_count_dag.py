from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from datetime import datetime
from steam_api_func import get_app_ids, get_player_counts

with DAG(
    dag_id='top_100_player_count',
    start_date=datetime(2024, 1, 1),
    schedule='*/15 * * * *',
    catchup=False,
    tags=["player_count"],
) as dag:

    get_app_ids_task = PythonOperator(
        task_id='get_app_ids',
        python_callable=get_app_ids,
        dag=dag,
    )

    get_player_counts_task = PythonOperator(
        task_id='get_player_counts',
        python_callable=get_player_counts,
        dag=dag,
    )

dbt_run = BashOperator(
    task_id='dbt_run',
    bash_command='dbt run --project-dir /opt/airflow/dbt --profiles-dir /home/airflow/.dbt',
)

get_app_ids_task >> get_player_counts_task >> dbt_run