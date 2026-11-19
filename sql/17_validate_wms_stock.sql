SELECT
    snapshot_id,
    warehouse_id,
    product_id,
    available_qty,
    snapshot_at,
    CASE
        WHEN snapshot_id IS NULL
          OR warehouse_id IS NULL
          OR product_id IS NULL
          OR available_qty IS NULL
          OR snapshot_at IS NULL
        THEN 'REJECTED'

        WHEN available_qty < 0
        THEN 'REJECTED'

        ELSE 'VALID'
    END AS dq_status
FROM bronze.wms_stock;