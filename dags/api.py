from airflow import DAG
from airflow.models import dag
from airflow.utils.dates import days_ago
from airflow.operators.python_operator import PythonOperator
from airflow.providers.postgres.operators.postgres import PostgresOperator
import psycopg2
import datetime as datetime
import json

default_args = {"owner": "airflow"}

dag = DAG( 'api',
            default_args=default_args,
            description='hmmmmmmmmmm',
            catchup=False, 
            start_date= datetime.datetime.now(), 
            schedule_interval= '* 7 * * *'  
          )

def jayson():
    conn = psycopg2.connect(dbname='postgres', user='airflow', password='airflow', host='postgres')
    cur = conn.cursor()
    x="SELECT * FROM tickers1"
    cur.execute(x)
    a=cur.fetchall()
    cur.close() 
    conn.close()
    json.dumps(a)

extract_task = PythonOperator(task_id = 'api_test', 
                              python_callable = jayson, 
                              provide_context = True,
                              dag= dag )

extract_task