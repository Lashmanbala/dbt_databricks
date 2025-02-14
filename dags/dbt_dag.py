from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.utils.dates import days_ago
from airflow.operators.python import PythonOperator

# Function to check if seed has already run
import os

def seed_check():
    if not os.path.exists('/tmp/dbt_seed_done'): 
        os.system('dbt seed --project-dir /home/ubuntu/dbt_databricks/dbt_databricks_project --select orders order_items')
        with open('/tmp/dbt_seed_done', 'w') as f:
            f.write('done')

with DAG(
    'dbt_dag',
    default_args={'owner': 'airflow', 'retries': 0},
    schedule_interval='@daily',
    start_date=days_ago(1),
    catchup=False,         # No backfill, only current and future runs
) as dag:

    seed_task = PythonOperator(
        task_id='dbt_seed_check',
        python_callable=seed_check,
    )

    run_silver = BashOperator(
        task_id='dbt_run_silver',
        bash_command='dbt run --project-dir /home/ubuntu/dbt_databricks/dbt_databricks_project --select silver --vars \'{target_date: "201310"}\''
    )

    run_gold = BashOperator(
        task_id='dbt_run_gold',
        bash_command='dbt run --project-dir /home/ubuntu/dbt_databricks/dbt_databricks_project --select gold'
    )

    run_silver >> run_gold
