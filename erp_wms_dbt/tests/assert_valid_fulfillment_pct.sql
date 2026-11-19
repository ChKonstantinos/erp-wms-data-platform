SELECT
    order_id,
    fulfillment_pct
FROM {{ ref('order_fulfillment_summary') }}
WHERE fulfillment_pct IS NULL
   OR fulfillment_pct < 0
   OR fulfillment_pct > 100