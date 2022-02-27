Airflow For Data Extraction

![image](https://user-images.githubusercontent.com/71278693/155889010-af56c5dc-1fb2-4682-b020-e64ac15520a5.png)

Objective : Extract Data from Yahoo finance , Trends,Twitter,Google News and store it in database.

Steps for Extracting Data :

1. Create tables in postgresql
2. Extract data from yahoo finance and load into database
3. Extract data from trends,twitter,google news.

Explore Sample Repository Here :
https://github.com/digvijay13873/airflow-docker.git

Steps To set up above sample repository on your local machine :

Prerequisites :
Docker Desktop Installed on local machine

Step : 1
Create Docker Image
docker build -t airflowdocker .

Step : 2
Give reference of created image in docker compose file.
![image](https://user-images.githubusercontent.com/71278693/155887807-ef7ea582-b87c-4b14-8e04-1a54f22c1089.png)

Step : 3
docker-compose up
This command creates all services needed for airflow under a single container
![image](https://user-images.githubusercontent.com/71278693/155887830-1c3a6757-1468-47f9-81e4-bdc325d15e3c.png)

Step : 4
Login to the airflow web UI from your browser.(localhost:8080)
Default Id : airflow
Default pass : airflow
![image](https://user-images.githubusercontent.com/71278693/155887888-0fc50eee-988d-426b-8e03-a7a873c7f8cc.png)

Setting Up PostgresHook

Goto Admin tab in airflow UI ----> Select Connections
![image](https://user-images.githubusercontent.com/71278693/155888632-e06e0750-ccbe-4c2b-8010-4d575d9040d4.png)
add new connection
![image](https://user-images.githubusercontent.com/71278693/155888688-1451dd11-b2bf-4b74-bb5a-d31fa7827153.png)
Connection Parameters
![image](https://user-images.githubusercontent.com/71278693/155888705-fe8ee113-2682-4b4f-a998-099d45b1aa17.png)
Click on save.

Iniatial Setup For Airflow Environment on Local machine is Completed.


Working With Dags
A DAG (Directed Acyclic Graph) is the core concept of Airflow, collecting Tasks together, organized with dependencies and relationships to say how they should run.
https://airflow.apache.org/docs/apache-airflow/stable/concepts/dags.html

Here defined mainly three DAGS in airflow :

1. Table_Creation dag : To create tables in postgres

2. Yahoo_Finance : To extract data from yahoo finance

3. Data_Extraction_Final : To extract data from trends,google news and twitter

How to run DAGS ?

DAGs will run in one of two ways:

1. When they are triggered either manually or via the API

2. On a defined schedule, which is defined as part of the DAG
Click on run dag button(for manually starting dags).If instances of dags are pending you can goto Graph tab and then click on instance to clear it or to get the logs.You can see success and failed dags in airflow UI home screen.
![image](https://user-images.githubusercontent.com/71278693/155888209-5efddc5c-d352-43aa-a923-e31ded9928f3.png)

Exploring Extracted Data
Goto Docker container ----> Login To the adminer web UI .
Use given credentials.You can see here the tables that we created and Data getting filled in those tables.
![image](https://user-images.githubusercontent.com/71278693/155888376-2879e4b4-bb30-441b-92e8-ef52d0d97f18.png)
![image](https://user-images.githubusercontent.com/71278693/155888381-b622b6dd-d669-431f-8469-3efed346a5c7.png)
![image](https://user-images.githubusercontent.com/71278693/155888408-75027c2e-eaa0-4152-b880-379aef1476e2.png)


Conclusion
Airflow along with docker saves a lot of time and effort by automating the tasks.

Happy Learning !!!







