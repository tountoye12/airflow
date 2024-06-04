

from datetime import datetime
from airflow.utils.dates import days_ago
from airflow import DAG

from airflow.operators.bash import BashOperator


default_args = {
    'owner': 'Diallo'
}

dag = DAG (
    dag_id = 'hello_world',
    description = 'My first dag in airflow',
    default_args = default_args,
    start_date = days_ago(1),
    schedule_interval = None
)


task = BashOperator(
    task_id = 'Hello_world_task',
    bash_command = 'echo Hello world',
    dag = dag
)

task
