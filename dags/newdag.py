from airflow import DAG
from airflow.models import dag
from airflow.utils.dates import days_ago
from airflow.operators.python_operator import PythonOperator
from airflow.operators.trigger_dagrun import TriggerDagRunOperator
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.utils.trigger_rule import TriggerRule
from airflow.models.dagrun import DagRun

import psycopg2
import datetime as datetime
import pandas as pd

import tweepy

import pytrends
from pytrends.request import TrendReq

import nltk
from nltk.sentiment.vader import  SentimentIntensityAnalyzer
nltk.download('vader_lexicon')
vader = SentimentIntensityAnalyzer()

from GoogleNews import GoogleNews