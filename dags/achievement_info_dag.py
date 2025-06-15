from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from datetime import datetime
from steam_api_func import get_app_ids, get_achievement_names

with DAG(
    dag_id='top_100_achievement_info',
    start_date=datetime(2024, 1, 1, 0, 15),
    schedule='@daily',
    catchup=False,
    tags=["achievement_info"],
) as dag:

    get_app_ids_task = PythonOperator(
        task_id='get_app_ids',
        python_callable=get_app_ids,
        dag=dag,
    )

    get_achievement_names_task = PythonOperator(
        task_id='get_achievement_names',
        python_callable=get_achievement_names    ,
        dag=dag,
    )

dbt_run = BashOperator(
    task_id='dbt_run',
    bash_command='dbt run --project-dir /opt/airflow/dbt --profiles-dir /home/airflow/.dbt',
)

get_app_ids_task >> get_achievement_names_task >> dbt_run