from airflow import models as af_models
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta
from retrieve_helper import download_google, load_into_redis

arg_list = {
        'owner': 'airflow',
        'depends_on_past': False,
        'start_date': datetime(2019, 8, 21),
        'email': ['alex.yonder@yahoo.com'],
        'email_on_failure': False,
        'email_on_retry': False,
        'retries': 1,
        'retry_delay': timedelta(minutes=5),
        # 'queue': 'bash_queue',
        # 'pool': 'backfill',
        # 'priority_weight': 10,
        # 'end_date': datetime(2016, 1, 1),
}


my_dag = af_models.DAG(
    dag_id='google_webpage_downloader', start_date=datetime(2017, 6, 30),
    schedule_interval='0 10 * * *', default_args=arg_list
  )

# useful args for DAG
# 1. default_args->the args DAG would feed to every task, handy when there are many common args across all tasks
# 2. max_active_task: the tasks count airflow can run
# 3. concurrency: the max tasks count can run concurrently

# define a task

download_webpage_op = PythonOperator(
    task_id='read_task',
    python_callable=download_google,
    dag=my_dag,
    retries=2,
)

write_to_redis_op = PythonOperator(
    task_id='write_task',
    python_callable=load_into_redis,
    dag=my_dag,
    retries=2,
    op_kwargs={
        'file_path': '/tmp/downloader_test1'
    },
)


download_webpage_op >> write_to_redis_op
