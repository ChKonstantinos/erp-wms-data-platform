WITH validated_stock AS (
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
              OR available_qty < 0
            THEN 'REJECTED'
            ELSE 'VALID'
        END AS dq_status
    FROM bronze.wms_stock
)
INSERT INTO silver.wms_stock_valid (
    snapshot_id,
    warehouse_id,
    product_id,
    available_qty,
    snapshot_at
)
SELECT
    snapshot_id,
    warehouse_id,
    product_id,
    available_qty,
    snapshot_at
FROM validated_stock
WHERE dq_status = 'VALID'
ON CONFLICT (snapshot_id, warehouse_id, product_id)
DO UPDATE SET
    available_qty = EXCLUDED.available_qty,
    snapshot_at = EXCLUDED.snapshot_at,
    processed_at = CURRENT_TIMESTAMP;