import os

from airflow import DAG
from datetime import datetime, timedelta

from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator

from sqlalchemy import create_engine

source_user = os.getenv('SOURCE_USER')
source_password = os.getenv('SOURCE_PASSWORD')
source_host = os.getenv('SOURCE_HOST')
source_db = os.getenv('SOURCE_DB')

opdb_user = os.getenv('OPDB_USER')
opdb_password = os.getenv('OPDB_PASSWORD')
opdb_host = os.getenv('OPDB_HOST')
opdb_db = os.getenv('OPDB_DB')


def get_data(user_1, password_1, host_1, db_1, user_2, password_2, host_2, db_2):
    source_engine = create_engine(f'mysql+mysqlconnector://{user_1}:{password_1}@{host_1}/{db_1}')

    with source_engine.connect() as source_connection:
        result = source_connection.execute('SELECT * FROM source_table')

    data = result.fetchall()

    source_engine.dispose()

    op_db_engine = create_engine(f'mysql+mysqlconnector://{user_2}:{password_2}@{host_2}/{db_2}')

    with op_db_engine.connect() as opdb_connection:
        for row in data:
            opdb_connection.execute(f"INSERT INTO op_table (source_id, op_data) VALUES {row}")

    op_db_engine.dispose()


default_args = {
    'owner': 'me',
    'retries': 0,
    'retry_delay': timedelta()
}

with DAG(
        dag_id='test_dag',
        description='This is a test airflow dag',
        default_args=default_args,
        start_date=datetime(2023, 3, 26, 2),
        schedule_interval=None,
        catchup=False,
) as dag:
    task1 = PythonOperator(
        task_id='get_data_from_mysql',
        python_callable=get_data,
        op_args=[source_user, source_password, source_host, source_db, opdb_user, opdb_password, opdb_host, opdb_db],
        dag=dag
    )

    task2 = BashOperator(
        task_id='test_bash_operator',
        bash_command='echo "Hello from bash operator"',
        dag=dag
    )

    # task1.set_downstream(task2)
    task1 >> task2
