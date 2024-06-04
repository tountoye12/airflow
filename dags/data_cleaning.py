

from datetime import datetime, timedelta

from airflow.utils.dates import days_ago
from airflow import DAG
from airflow.operators.python import PythonOperator
import pandas as pd


default_args = {
    'owner': 'Diallo'
}



def load_data():
    df = pd.read_csv('./dataframes/insurance.csv')

    print("################# DataFrame #################")
    
    print("Dataset shape ==>", df.shape)
    print(df)
    

    return df.to_json()



def clean_data(**kwargs):
    ti = kwargs['ti']

    json_data = ti.xcom_pull(task_ids='read_csv_file')


    df = pd.read_json(json_data)
    print("Dataset shape ==>", df.shape)
    df = df.dropna()
    print(df)

    return df.to_json()


def group_by_smoker(ti):
    json_data = ti.xcom_pull(task_ids='clean_data')

    df = pd.read_json(json_data)

    smoker_df = df.groupby('smoker').agg({
        'age': 'mean',
        'bmi': 'mean',
        'charges': 'mean'
    }).reset_index()


    print(smoker_df)

    smoker_df.to_csv('./output/group_by_smoker.csv', index=False)

def group_by_region(ti):

    json_data = ti.xcom_pull(task_ids='clean_data')

    print(json_data)


with DAG(
    dag_id = 'python_pipeline',
    description = 'Running a python pipeline using Airflow',
    default_args =  default_args,
    start_date = days_ago(1),
    schedule_interval = '@once',
    tags = ['simple', 'python', 'transform', 'pipeline']
) as dag:
    read_csv_file = PythonOperator(
        task_id = 'read_csv_file',
        python_callable = load_data
        
    )

    clean_data = PythonOperator(
        task_id = 'clean_data',
        python_callable = clean_data
        
    )

    groupby_smoker = PythonOperator(
        task_id = 'group_by_smoker',
        python_callable=group_by_smoker
    )

    groupby_region = PythonOperator(
        task_id = 'group_by_region',
        python_callable=group_by_region
    )

    

read_csv_file >> clean_data >> [groupby_region, groupby_smoker]