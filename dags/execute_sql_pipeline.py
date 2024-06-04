

from datetime import datetime, timedelta

from airflow.utils.dates import days_ago
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.sqlite_operator import SqliteOperator # type: ignore
import pandas as pd


default_args = {
    'owner': 'Diallo'
}


with DAG(
    dag_id = 'execute_sql_pipeline',
    description = 'Running a python pipeline using sql operators',
    default_args =  default_args,
    start_date = days_ago(1),
    schedule_interval = '@once',
    tags = ['pipeline', 'sql']
) as dag:
    create_table = SqliteOperator(
        task_id = 'create_table',
        sql = r"""
            CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY,
                    name VARCHAR(50) NOT NULL,
                    age INTEGER NOT NULL,
                    city VARCHAR(50),
                    is_active BOOLEAN DEFAULT true,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """,
        sqlite_conn_id = 'my_sqlite_conn',
        dag = dag
    )

    first_insert_values = SqliteOperator(
        task_id = 'first_insert_values',
        sql = r"""
            INSERT INTO users (name, age, is_active) VALUES 
                ('Julie', 30, false),
                ('Peter', 55, true),
                ('Emily', 37, false),
                ('Katrina', 54, false),
                ('Joseph', 27, true);
        """,
        sqlite_conn_id = 'my_sqlite_conn',
        dag = dag
    )

    second_insert_values =SqliteOperator(
        task_id = 'second_insert_values',
        sql = r"""
            INSERT INTO users (name, age) VALUES 
                ('Harry', 49),
                ('Nancy', 52),
                ('Elvis', 26),
                ('Mia', 20);
        """,
        sqlite_conn_id = 'my_sqlite_conn',
        dag = dag,
    )

    delete_values = SqliteOperator(
        task_id = 'delete_values',
        sql = r"""
            DELETE FROM users WHERE is_active = 0;
        """,
        sqlite_conn_id = 'my_sqlite_conn',
        dag = dag,
    )

    update_values = SqliteOperator(
        task_id = 'update_values',
        sql = r"""
            UPDATE users SET city = 'Seattle';
        """,
        sqlite_conn_id = 'my_sqlite_conn',
        dag = dag,
    )


    display_all_from_users = SqliteOperator(
        task_id = 'display_result',
        sql = r"""SELECT * FROM users""",
        sqlite_conn_id = 'my_sqlite_conn',
        dag = dag,
        do_xcom_push = True
    )


create_table >> [first_insert_values, second_insert_values] >>  delete_values >> update_values >> display_all_from_users