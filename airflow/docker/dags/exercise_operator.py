# define a dag
from airflow import models as af_models
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta
import requests
import hashlib

# setup args, this seems doesn't have anything to do with command line input
default_args = {
        'owner': 'airflow',
        'depends_on_past': False,
        'start_date': datetime(2019, 8, 14),
        'email': ['airflow@example.com'],
        'email_on_failure': False,
        'email_on_retry': False,
        'retries': 1,
        'retry_delay': timedelta(minutes=1),
        # 'queue': 'bash_queue',
        # 'pool': 'backfill',
        # 'priority_weight': 10,
        # 'end_date': datetime(2016, 1, 1),
}


my_dag = af_models.DAG(
    dag_id='exercise1_dag', start_date=datetime(2017, 6, 30),
    schedule_interval='0 10 * * *', default_args=default_args
  )


def task0():
    res = requests.get('http://www.google.com')
    has = hashlib.sha256()
    has.update(res.text.encode())
    hash_str = has.digest()
    print("hash string")
    print(hash_str)
    return


t0 = PythonOperator(
    task_id='task0',
    python_callable=task0,
    dag=my_dag,
    retries=3,
)
