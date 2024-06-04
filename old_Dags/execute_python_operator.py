

from datetime import datetime, timedelta

from airflow.utils.dates import days_ago
from airflow import DAG
from airflow.operators.python import PythonOperator


default_args = {
    'owner': 'Diallo'
}

def print_function():
    print("The simple possible python operator by Diallo")



with DAG(
    dag_id = 'python_ops',
    description = 'Using python operators',
    default_args =  default_args,
    start_date = days_ago(1),
    schedule_interval = '@daily',
    tags = ['simple', 'python']
) as dag:
    task = PythonOperator(
        task_id = 'python_operator',
        python_callable = print_function
    )