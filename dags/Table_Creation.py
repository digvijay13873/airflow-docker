import airflow
from datetime import timedelta
from airflow import DAG
from airflow.operators.postgres_operator import PostgresOperator
from airflow.utils.dates import days_ago

args={'owner': 'airflow'}

default_args = {
    'owner': 'airflow',    
    #'start_date': airflow.utils.dates.days_ago(2),
    # 'end_date': datetime(),
    # 'depends_on_past': False,
    #'email': ['airflow@example.com'],
    #'email_on_failure': False,
    # 'email_on_retry': False,
    # If a task fails, retry it once after waiting
    # at least 5 minutes
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with DAG (
    dag_id = "Table_Creation",
    default_args=args,
    # schedule_interval='0 0 * * *',
    schedule_interval='@once',	
    dagrun_timeout=timedelta(minutes=60),
    description='Create Tables in Postgres',
    start_date = airflow.utils.dates.days_ago(1),
    template_searchpath='/opt/airflow/fromlocal',
    catchup=False
) as dag :

#Specify Queries For Postgres

#Specify Operator For Dag
#postgres operator only works with sql commands
        create_table = PostgresOperator(
        task_id='create_table',
        postgres_conn_id='postgres_config',
        sql='tables.sql',

        )

create_table

