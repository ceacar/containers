# define a dag
from airflow import models as af_models
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta
from random_print import task0, task1, taska, taskb, taskc, taskd, taske

# setup args, this seems doesn't have anything to do with command line input
default_args = {
        'owner': 'airflow',
        'depends_on_past': False,
        'start_date': datetime(2015, 6, 1),
        'email': ['airflow@example.com'],
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
    dag_id='my_dag', start_date=datetime(2017, 6, 30),
    schedule_interval='0 10 * * *', default_args=default_args
  )

# useful args for DAG
# 1. default_args->the args DAG would feed to every task, handy when there are many common args across all tasks
# 2. max_active_task: the tasks count airflow can run
# 3. concurrency: the max tasks count can run concurrently

# define a task

t0 = PythonOperator(
    task_id='task0',
    python_callable=task0,
    dag=my_dag,
    retries=3,
)

t1 = PythonOperator(
  task_id='task1',
  python_callable=task1,
  dag=my_dag
)

ta = PythonOperator(
    task_id='taska',
    python_callable=taska,
    dag=my_dag,
    retries=3,
)

tb = PythonOperator(
    task_id='taskb',
    python_callable=taskb,
    dag=my_dag,
    retries=3,
)

tc = PythonOperator(
    task_id='taskc',
    python_callable=taskc,
    dag=my_dag,
    retries=3,
)

td = PythonOperator(
    task_id='taskd',
    python_callable=taskd,
    dag=my_dag,
    retries=3,
)

te = PythonOperator(
    task_id='taske',
    python_callable=taske,
    dag=my_dag,
    retries=3,
)

# useful args for task
# 1. retries
# 2. pool: max concurrency tasks can run
# 3. queue : Parameters for only celery, assign specific worker
# 4. execution_time: timeout
# 5. trigger_rule: which task gets executed, for example-> some task failed, then run this task
# 6. Args for python callbacks:
# 7. Environmental Variables
# 8. Template Variables: Ginger templates??

# set first_task as dependency of second_task
# second_task.set_upstream(first_task)

"""
0-----
      |
a->b->c->d
  ^   |
  |    ->e
1-
setting up a complex pipelines to test the pooling of airflow
"""

t0 >> tc

ta >> tb >> tc >> td

t1 >> tb

tc >> te
