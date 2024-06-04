
from datetime import datetime
from airflow.utils.dates import days_ago
from airflow.decorators import dag, task


default_args = {
    'owner': 'Diallo'
}



@dag(
    dag_id = 'dag_with_task_flow',
    description = 'My first dag using task flow api',
    default_args = default_args,
    start_date =  days_ago(1),
    schedule_interval = '@once',
    tags = ['dependences', 'python', 'taskflow_api'])
def dag_with_task_flow():
    
    @task
    def task_a():
        print("first task with taskflow api")
    
    task_a()

 
dag_with_task_flow()