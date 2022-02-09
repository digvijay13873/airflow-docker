from airflow import DAG
from airflow.models import dag
from airflow.utils.dates import days_ago
from airflow.operators.python_operator import PythonOperator
from airflow.operators.trigger_dagrun import TriggerDagRunOperator
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.utils.trigger_rule import TriggerRule
from airflow.models.dagrun import DagRun

import psycopg2
import datetime as datetime
import pandas as pd

#document tags should be used to auto generate package documentation

import tweepy

import pytrends
from pytrends.request import TrendReq

import nltk
from nltk.sentiment.vader import  SentimentIntensityAnalyzer
nltk.download('vader_lexicon')
vader = SentimentIntensityAnalyzer()

from GoogleNews import GoogleNews

args = {"owner": "airflow", 'depends_on_past': False, 'wait_for_downstream': False}

dag = DAG(  dag_id ='psotgrressdftest',
            default_args=args,
            description='hmmmmmmmmmm',
            catchup=False, 
            start_date= datetime.datetime(2021, 7, 14), 
            schedule_interval= None,
            max_active_runs = 1
          )

consumerKey = "XR0J2M2JIprT5PwfyjTls3Tp1"
consumerSecret = "VrzwD86EdGdLqnrMWiOAyKaQ035NVmNXlGf3loX3zrxTEVOm6T"
accessToken = "1272240020200534017-zKrYbnySEvf18JTNByI4b0wzHUMrEg"
accessTokenSecret = "ZwqVhnAvYwBtC7E5PNDgevTNPzpQU6cIZVUtZj3pn5Ab6"    

auth = tweepy.OAuthHandler(consumerKey,consumerSecret)
auth.set_access_token(accessToken, accessTokenSecret)
api = tweepy.API(auth)  


def select_ticker(**kwargs):
  #should be placed into the airflow config (passwords and user)
  conn = psycopg2.connect(dbname='postgres', user='airflow', password='airflow', host='postgres')
  cur = conn.cursor()

  #helper code 
  cur.execute("SELECT COUNT(*) FROM stages")
  completedcount = cur.fetchone()
  completedcount = completedcount[0]
  print(completedcount)
  #log this instead, not print

  # cur.execute("SELECT * FROM tickers1")
  # print(str(cur.fetchall()))
  cur.execute("SELECT keyword from tickers1 WHERE ID = " + str(completedcount+1))
  current_ticker = cur.fetchone()
  print("SELECTED TICKER FROM tickers1: " + str(current_ticker))
  current_ticker = current_ticker[0]

  cur.execute("INSERT INTO stages (keyword) VALUES ('" + current_ticker + "')")

  print(current_ticker)

  conn.commit()
  cur.close()
  conn.close()
  return current_ticker

def news_extract(**kwargs):
  task_instance = kwargs['task_instance']
  ticker1 = task_instance.xcom_pull(task_ids='select_ticker')

  conn = psycopg2.connect(dbname='postgres', user='airflow', password='airflow', host='postgres')
  cur = conn.cursor()
  cur.execute("SELECT companyName from tickers1 WHERE keyword = '" + ticker1 + "'")
  ticker = cur.fetchone()
  ticker = str(ticker[0])
  googlenews = GoogleNews()
  googlenews.set_lang('en')
  print(ticker)
  googlenews.get_news(ticker)
  news_arr = googlenews.get_texts()
  
  cur.execute(f"UPDATE stages SET newsStage = newsStage + 1 WHERE keyword = '{ticker1}'")

  conn.commit()
  cur.close()
  conn.close()
  return news_arr

def news_postgres_table(**kwargs):
    task_instance = kwargs['task_instance']
    news_arr = task_instance.xcom_pull(task_ids='news_extract')
    ticker1 = task_instance.xcom_pull(task_ids='select_ticker')
    ticker = ticker1.replace(".","_")

    conn = psycopg2.connect(dbname='postgres', user='airflow', password='airflow', host='postgres')
    cur = conn.cursor()

    df1=pd.DataFrame(news_arr)
    f = lambda title: vader.polarity_scores(title)['compound']

    try:
      df1['compound'] = df1[0].apply(f)
    except:
      return 0

    for i in df1.index:
      
      a=str(df1[0][i])
      a = a.replace("\'","\"")
      b=str(df1['compound'][i])
      query = f"INSERT INTO news (keyword, news, sentiment) VALUES ('{ticker}','{a}', {b})"
      cur.execute(query) 

    d = 'SELECT * FROM newsSentiments_'+ticker
    cur.execute(d)
    g = cur.fetchall()
    print(g)
    
    cur.execute("UPDATE stages SET newsStage = newsStage + 1 WHERE keyword = '" + ticker1 + "'")

    conn.commit()
    cur.close()
    conn.close()

def extract_trends(**kwargs):
    conn = psycopg2.connect(dbname='postgres', user='airflow', password='airflow', host='postgres')
    cur = conn.cursor()
    region = ['IN','US','GB','AU','JP']
    task_instance = kwargs['task_instance']
    temp = task_instance.xcom_pull(task_ids='select_ticker')

    ticker = []
    ticker.append(temp)
    print(ticker)

    number_of_searches = []
    for i in region:
        pytrends = TrendReq(hl='en-IN', tz=330, geo='IN', )
        pytrends.build_payload(ticker, cat = 0 , timeframe = 'now 1-d' , geo = i , gprop='')
        data = pytrends.interest_over_time()
        mean = data.mean()
        mean = mean.tolist()
        try:
          number_of_searches.append(mean[0])
        except:
          number_of_searches.append(0.0)
    print("number of searches: " + str(number_of_searches))
    
    cur.execute("UPDATE stages SET trendsStage = trendsStage + 1 WHERE keyword = '" + temp + "'")
    conn.commit()
    cur.close()
    conn.close()

    return number_of_searches

def transform_trends(**kwargs):
    task_instance = kwargs['task_instance']
    temp = task_instance.xcom_pull(task_ids='select_ticker')
    temp1 = temp
    ticker = []
    ticker.append(temp)
    
    conn = psycopg2.connect(dbname='postgres', user='airflow', password='airflow', host='postgres')
    cur = conn.cursor()

    number_of_searches = task_instance.xcom_pull(task_ids='extract_trends')
    region = ['IN','US','GB','AU','JP']
    conn = psycopg2.connect(dbname='postgres', user='airflow', password='airflow', host='postgres')
    cur = conn.cursor()
    temp = temp.replace(".", "_")
    
    for i in range(len(region)):
      query = f"INSERT INTO trends (keyword, region, numberOfSearches) VALUES ('{temp}', '{str(region[i])}', {str(number_of_searches[i])})"
      cur.execute(query) 
  
    cur.execute("UPDATE stages SET trendsStage = trendsStage + 1 WHERE keyword = '" + temp1 + "'")
    
    conn.commit()
    cur.close()
    conn.close()


def extract_tweets(**kwargs):
  conn = psycopg2.connect(dbname='postgres', user='airflow', password='airflow', host='postgres')
  cur = conn.cursor()
  task_instance = kwargs['task_instance']
  ticker1 = task_instance.xcom_pull(task_ids='select_ticker')
  ticker = ticker1[:ticker1.find(".")]
  arr1=[]
  public_tweets=api.search(ticker)

  for j in public_tweets:
    data=j
    arr1.append(data.text)

  cur.execute("UPDATE stages SET twitterStage = twitterStage + 1 WHERE keyword = '" + ticker1 + "'")

  conn.commit()
  cur.close()
  conn.close()
  return arr1

def tweets_postgres_table(**kwargs):
    task_instance = kwargs['task_instance']

    tweets_arr = task_instance.xcom_pull(task_ids='extract_tweets')
    ticker1 = task_instance.xcom_pull(task_ids='select_ticker')
    ticker = ticker1.replace(".","_")

    conn = psycopg2.connect(dbname='postgres', user='airflow', password='airflow', host='postgres')
    cur = conn.cursor()
    
    df1=pd.DataFrame(tweets_arr)
    f = lambda title: vader.polarity_scores(title)['compound']

    try:
      df1['compound'] = df1[0].apply(f)
    except:
      return 0 

    for i in df1.index:
      a=str(df1[0][i])
      a = a.replace("\'","\"")
      b=str(df1['compound'][i])
      query = f"INSERT INTO twitter (keyword, tweet, sentiment) VALUES ('{ticker}','{a}', {b})"
      cur.execute(query) 

    d = "select * from tweetsSentiments_"+ticker
    cur.execute(d)
    g = cur.fetchall()
    print(g)

    cur.execute("UPDATE stages SET twitterStage = twitterStage + 1 WHERE keyword = '" + ticker1 + "'")

    conn.commit()
    cur.close()
    conn.close()


select_ticker = PythonOperator(task_id = 'select_ticker', 
                              python_callable = select_ticker, 
                              provide_context = True,
                              dag= dag )

news_extract =  PythonOperator(task_id = 'news_extract', 
                              python_callable = news_extract, 
                              provide_context = True,
                              dag= dag )      

news_postgres_table =  PythonOperator(task_id = 'news_postgres_table', 
                              python_callable = news_postgres_table, 
                              provide_context = True,
                              dag= dag )   

extract_trends =  PythonOperator(task_id = 'extract_trends', 
                              python_callable = extract_trends, 
                              provide_context = True,
                              dag= dag )                                                       

transform_trends =  PythonOperator(task_id = 'transform_trends', 
                              python_callable = transform_trends, 
                              provide_context = True,
                              dag= dag )      

extract_tweets =  PythonOperator(task_id = 'extract_tweets', 
                              python_callable = extract_tweets, 
                              provide_context = True,
                              dag= dag )  
                              
tweets_postgres_table =  PythonOperator(task_id = 'tweets_postgres_table', 
                              python_callable = tweets_postgres_table, 
                              provide_context = True,
                              dag= dag )                  

trigger = TriggerDagRunOperator(
        task_id="restart_test",
        trigger_dag_id="psotgrressdftest", trigger_rule=TriggerRule.ALL_DONE
    )                


select_ticker >> news_extract >> news_postgres_table
select_ticker >> extract_tweets >> tweets_postgres_table
select_ticker >> extract_trends >> transform_trends 

news_postgres_table >> trigger
transform_trends >> trigger
tweets_postgres_table >> trigger