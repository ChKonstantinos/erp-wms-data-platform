{{
    config(
        materialized='view',
        alias='v_inventory_summary'
    )
}}

SELECT
    warehouse_id,
    product_id,
    snapshot_at,
    available_qty,

    CASE
        WHEN available_qty = 0 THEN 'OUT_OF_STOCK'
        WHEN available_qty <= 10 THEN 'LOW_STOCK'
        WHEN available_qty <= 30 THEN 'MEDIUM_STOCK'
        ELSE 'HEALTHY_STOCK'
    END AS stock_status

FROM {{ source('silver', 'v_wms_latest_stock') }}