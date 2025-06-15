from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from datetime import datetime
from steam_api_func import get_app_ids, get_achievement_percentages

with DAG(
    dag_id='top_100_achievement_percentages',
    start_date=datetime(2024, 1, 1, 0, 5),
    schedule='@hourly',
    catchup=False,
    tags=["achievement_percentages"]
) as dag:

    get_app_ids_task = PythonOperator(
        task_id='get_app_ids',
        python_callable=get_app_ids,
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

get_app_ids_task >> get_achievement_percentages_task >> dbt_run