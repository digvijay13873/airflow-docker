from airflow import DAG
from airflow.models import dag
from airflow.utils.dates import days_ago
from airflow.operators.python_operator import PythonOperator
from airflow.providers.postgres.operators.postgres import PostgresOperator
import psycopg2
import datetime as datetime

default_args = {"owner": "airflow"}

dag = DAG( dag_id= 'maintest',
            default_args=default_args,
            description='hmmmmmmmmmm',
            catchup=False, 
            start_date= datetime.datetime.now(), 
            schedule_interval= '* 7 * * *'  
          )


def select_ticker(**kwargs):
  conn = psycopg2.connect(dbname='postgres', user='airflow', password='airflow', host='postgres')
  cur = conn.cursor()
  # create_table = "Create table tickers1 (ID SERIAL, keyword VARCHAR(255) NOT NULL, companyName VARCHAR(255))"
  # cur.execute(create_table)
  cur.execute("DROP TABLE stages")
  cur.execute("DROP TABLE tickers1")
  cur.execute("CREATE TABLE tickers1 (ID SERIAL, keyword VARCHAR(255) NOT NULL, companyName VARCHAR(255))")
  cur.execute("CREATE TABLE stages (ID SERIAL, keyword VARCHAR(255) NOT NULL, twitterStage INTEGER DEFAULT 0, newsStage INTEGER DEFAULT 0, trendsStage INTEGER DEFAULT 0)")

  cur.execute("CREATE TABLE IF NOT EXISTS twitter (ID SERIAL, keyword VARCHAR(20), tweet TEXT, sentiment numeric(5,4))")
  cur.execute("CREATE TABLE IF NOT EXISTS trends (ID SERIAL, keyword VARCHAR(20), date DATE DEFAULT CURRENT_DATE, region VARCHAR(5), numberOfSearches NUMERIC(23,20))")
  cur.execute("CREATE TABLE IF NOT EXISTS news (ID SERIAL, keyword VARCHAR(20), news TEXT, sentiment numeric(5,4))")
  # create_table = "INSERT INTO tickers1 (keyword) VALUES ('AMZN')"
  # cur.execute(create_table)

  # create_table = "SELECT COUNT(*) FROM tickers1"
  # cur.execute(create_table)
  # index = cur.fetchone()
  # index = str(index[0])
  # selectticker = "SELECT keyword FROM tickers1 WHERE ID = " + index
  # cur.execute(selectticker)
  # current_ticker = cur.fetchone()
  # current_ticker = current_ticker[0]
  # print(type(current_ticker))
  conn.commit()
  cur.close() 
  conn.close()
  # return current_ticker  

# def select_ticker2(**kwargs):
#   task_instance = kwargs['task_instance']
#   current_ticker = task_instance.xcom_pull(task_ids='testtask')
#   print(current_ticker)

testtask = PythonOperator(task_id = 'testtask', 
                              python_callable = select_ticker, 
                              provide_context = True,
                              dag= dag )

# testtask2 = PythonOperator(task_id = 'testtask2', 
#                               python_callable = select_ticker2, 
#                               provide_context = True,
#                               dag= dag )


testtask