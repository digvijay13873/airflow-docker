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

dag_psql = DAG(
    dag_id = "Table_Creation",
    default_args=args,
    # schedule_interval='0 0 * * *',
    schedule_interval='@once',	
    dagrun_timeout=timedelta(minutes=60),
    description='Create Tables in Postgres',
    start_date = airflow.utils.dates.days_ago(1)
)

#Specify Queries For Postgres
create_table_sql_query = """ 
  CREATE TABLE IF NOT EXISTS tickers1 (ID SERIAL, keyword VARCHAR(255) NOT NULL, companyName VARCHAR(255));
  CREATE TABLE IF NOT EXISTS stages (ID SERIAL, keyword VARCHAR(255) NOT NULL, twitterStage INTEGER DEFAULT 0, newsStage INTEGER DEFAULT 0, trendsStage INTEGER DEFAULT 0);
  CREATE TABLE IF NOT EXISTS twitter (ID SERIAL, keyword VARCHAR(20), tweet TEXT, sentiment numeric(5,4));
  CREATE TABLE IF NOT EXISTS trends (ID SERIAL, keyword VARCHAR(20), date DATE DEFAULT CURRENT_DATE, region VARCHAR(5), numberOfSearches NUMERIC(23,20));
  CREATE TABLE IF NOT EXISTS news (ID SERIAL, keyword VARCHAR(20), news TEXT, sentiment numeric(5,4));
  """

#Specify Operator For Dag
#postgres operator only works with sql commands
create_table = PostgresOperator(
      sql = create_table_sql_query,
      task_id = "create_table_task",
      postgres_conn_id = "postgres_config",
      dag = dag_psql
      )

create_table

if __name__ == "__main__":
          dag_psql.cli()
