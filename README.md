# Revenue Reporting Pipeline on Databricks by DBT and Airflow

## Overview

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
    ```

2. **Create an unity catalog and a schema in Databricks**

3. **Configure dbt project with DBT configurations**
    ```bash
    dbt init
    ```
4.
