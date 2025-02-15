from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.utils.dates import days_ago
from airflow.operators.python import PythonOperator

# Function to check if seed has already run
import os

def seed_and_test():
    """Run dbt seed and dbt test only if not already run."""
    if not os.path.exists('/tmp/dbt_seed_done'):
        # Run dbt seed
        os.system('dbt seed --project-dir /home/ubuntu/dbt_databricks/dbt_databricks_project --select orders order_items')
        # Run dbt test immediately after seeding
        os.system('dbt test --project-dir /home/ubuntu/dbt_databricks/dbt_databricks_project --select orders order_items')
        # Create a flag file to indicate seed completion
        with open('/tmp/dbt_seed_done', 'w') as f:
            f.write('done')

with DAG(
    'dbt_dag',
    default_args={'owner': 'airflow', 'retries': 0},
    schedule_interval='@daily',
    start_date=days_ago(1),
    catchup=False, # No backfill, only current and future runs
    # paused_on_creation=True,  # DAG stays paused initially
) as dag:

    seed_and_test_task = PythonOperator(
        task_id='dbt_seed_check',
        python_callable=seed_and_test,
    )

    run_silver = BashOperator(
        task_id='dbt_run_silver',
        bash_command='dbt run --project-dir /home/ubuntu/dbt_databricks/dbt_databricks_project --select silver --vars \'{target_date: "201308"}\''
    ) # update the date variable for the consecutive runs

    run_gold = BashOperator(
        task_id='dbt_run_gold',
        bash_command='dbt run --project-dir /home/ubuntu/dbt_databricks/dbt_databricks_project --select gold'
    )

    seed_and_test_task >> run_silver >> run_gold
