from airflow import DAG
from airflow.models import dag
from airflow.utils.dates import days_ago
from airflow.operators.python_operator import PythonOperator
import os 
script_dir_path = os.path.dirname(os.path.realpath(__file__))
import time
from time import sleep

from xlwt import Workbook
import pandas as pd
from csv import writer
from csv import DictReader
from datetime import datetime
from selenium import webdriver
import psycopg2

opt = webdriver.FirefoxOptions()
       
wb=Workbook()
sheet1=wb.add_sheet('Sheet 1',cell_overwrite_ok=False)
i=0
j=0
default_args = {
     'owner': 'airflow',
     'retries': 1
    }

dag = DAG( 'ticker_yahoo',
            default_args=default_args,
            description='fetching ticker symbol',
            catchup=False, 
            start_date= datetime.now(), 
            schedule_interval= '* 7 * * *'  
          )  

def extract():
  conn = psycopg2.connect(dbname='postgres', user='airflow', password='airflow', host='postgres')
  cur = conn.cursor()
  with open(r'./fromlocal/EQUITY_L.csv') as read_obj:
    csv_dict_reader = DictReader(read_obj)
    url = "https://finance.yahoo.com"
    driver = webdriver.Remote("http://selenium:4444/wd/hub", options=opt)
    driver.get(url)
    for row in csv_dict_reader:
      time.sleep(4)
      # action = ActionChains(driver)
      time.sleep(4)

      searchBox = driver.find_element_by_id('yfin-usr-qry')
      time.sleep(4)

      searchBox.send_keys(row['SYMBOL'])
      time.sleep(4)

      # clicking on search
      driver.find_element_by_xpath('//*[@id="header-desktop-search-button"]').click()
      time.sleep(15)

      companyname = driver.find_elements_by_xpath('//*[@id="quote-header-info"]/div[2]/div[1]/div[1]/h1')
      ticker = companyname = str(companyname[0].text)
      print("comapny name: "+ companyname)
      ticker = ticker[::-1]
      ticker = ticker[1:ticker.find("(")]
      ticker = ticker[::-1]
      print("extracted ticker: " + ticker)
      companyname = companyname[:companyname.find(" (")]
      companyname = companyname.replace("'","''")
      cur.execute("INSERT INTO tickers1 (keyword,companyName) values ('" + ticker + "','" + companyname + "')")
      conn.commit()
    
    cur.close() 
    conn.close()

print(script_dir_path)

extract_task = PythonOperator(task_id = 'extract_task', 
                              python_callable = extract, 
                              provide_context = True,
                              dag= dag )

extract_task


