from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from datetime import datetime
from steam_api_func import (
    fetch_top_100,
    get_app_ids,
    get_player_counts,
    get_achievement_names,
    get_achievement_percentages
)

with DAG(
    dag_id='bootstrap_dag',
    start_date=datetime(2024, 1, 1),
    schedule=None,
    catchup=False,
    tags=["initialization"],
) as dag:

    fetch_steam_top_100 = PythonOperator(
        task_id='fetch_steam_top_100',
        python_callable=fetch_top_100,
        dag=dag,
    )
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

    get_achievement_names_task = PythonOperator(
        task_id='get_achievement_names',
        python_callable=get_achievement_names,
        dag=dag,
    )

    get_achievement_percentages_task = PythonOperator(
        task_id='get_achievement_percentages',
        python_callable=get_achievement_percentages,
        dag=dag,
    )

dbt_run = BashOperator(
    task_id='dbt_run',
    bash_command='dbt run --project-dir /opt/airflow/dbt --profiles-dir /home/airflow/.dbt',
)

fetch_steam_top_100 >> get_app_ids_task >> get_player_counts_task >> get_achievement_names_task >> get_achievement_percentages_task >> dbt_run