# Revenue Reporting Pipeline on Databricks by DBT and Airflow

## Overview

![Alt text](architecture_4.png)

The requirement is to develope a revenue reporting system in databricks and modularize the transormation logics using dbt.

The data is provided in csv format. 

I used DBT to seed data into databricks. And I have developed the transformation logics to compute daily revenue in the form of models in DBT.

Transformations done with DBT models and data is stored in 3 layers bronze, silver and gold in Databricks.

To ensure the data quality, I have written tests with custom macros in DBT.

These DBT models are orchatrated and scheduled by Airflow.

Each run processes the data of one month and computes daily revenue which will be used by analyst teams. 

The DBT seed will create the raw tables in bronze layer and the data in these tables are quality checked with DBT tests.

The intermediate result is stored in staging table in the silver layer. And in the each consecutive runs the older data is cleaned and the current data is stored in the staging table.

The final reporting table is updated with the new data from staging table and stored in gold layer for reporting.

## Setup
To setup this project locally, follow these steps

1. **Create a virtual environment and install dbt and airflow with databricks dependencies:**
    ```bash
    pip3 install dbt-core
    pip3 install dbt-databricks
    pip install apache-airflow
    pip install apache-airflow-providers-databricks
    pip install psycopg2-binary
    ```

2. **Create an unity catalog and a schema in Databricks**

3. **Configure dbt project with DBT configurations**
    ```bash
    dbt init
    ```

4. **Copy Dbt files:**
   
   Copy seeds, models, macros directories in dbt_databricks_project directory from this repo, replace the ones in your dbt project directory.

5. **Setup postgres db for airflow:**
   
    Copy the airflow_Dockerfile and docker-compose.yml files from this repo and run:
   ```bash
    docker-compose up
   ```

6. **Setup Airflow:**
   
   (i) Create dags directory copy dbt_dag in dags directory from this repo

   (ii) Update the airflow.cfg file with:
   
       executor = LocalExecutor
       parallelism = 4
       sql_alchemy_conn = postgresql+psycopg2://postgres:postgres123@localhost:5432/airflow_db

   (iii) Setup airflow home to the pwd
       ```bash
        export AIRFLOW_HOME= <your/pwd/>
        echo $AIRFLOW_HOME
       ```
   
   (iv) Init Airflow:
   
       ```bash
        airflow db init
        airflow users create --username admin --password admin --firstname Air --lastname Flow --role Admin --email admin@example.com
        airflow webserver -D --port 8080 
        airflow scheduler
       ```
7. **Create Databricks connection in Airflow web UI:**

       localhost:8080

    Go to the Airflow UI -> Admin -> Connections.
   
    Add a new connection with:
   
        Conn ID: databricks_default
   
        Conn Type: Databricks
   
        Host: https://<your-databricks-instance>

        login: (optional)
   
        Password: <your-databricks-personal-access-token>
   
8. **Trigger dbt_dag in the web UI:**

    From the next consecutive triggers update the date variable in the dbt_dag file with the next month for incremental processing
