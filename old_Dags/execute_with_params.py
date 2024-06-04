

from datetime import datetime, timedelta

from airflow.utils.dates import days_ago
from airflow import DAG
from airflow.operators.python import PythonOperator


default_args = {
    'owner': 'Diallo'
}

def say_hello(name):
    print("hello {name}".format(name=name))


def say_hello_with_city(name, city):
    print("hello {name} nice to see you at {city}".format(name=name, city=city))



with DAG(
    dag_id = 'python_operators_with_param',
    description = 'Using python operators',
    default_args =  default_args,
    start_date = days_ago(1),
    schedule_interval = '@daily',
    tags = ['simple', 'python']
) as dag:
    taskA = PythonOperator(
        task_id = 'taskA_Hello',
        python_callable = say_hello,
        op_kwargs = {'name' : 'Diallo'}
    )

    taskB = PythonOperator(
        task_id = 'taskB_with_city',
        python_callable = say_hello_with_city,
        op_kwargs = {
            'name' : 'Diallo',
            'city' : 'Fairfield'
        }
    )

taskA >> taskB