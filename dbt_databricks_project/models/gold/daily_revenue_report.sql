{{ config(
    materialized='incremental',
    unique_key='order_date'  )}}

SELECT
    order_date,
    revenue
FROM {{ ref('daily_revenue_stage') }}
ORDER BY order_date;
