{{ config(
    materialized='incremental',
    incremental_strategy='insert_overwrite'
) }}

SELECT 
    o.order_date,
    ROUND(SUM(oi.order_item_subtotal), 2) AS revenue
FROM {{ ref('orders') }} AS o
JOIN {{ ref('order_items') }} AS oi
    ON o.order_id = oi.order_item_order_id
WHERE o.order_status IN ('COMPLETE', 'CLOSED')
  AND date_format(o.order_date, 'yyyyMM') = '201308'
GROUP BY o.order_date


