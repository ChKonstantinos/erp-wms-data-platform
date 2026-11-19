CREATE OR REPLACE VIEW silver.v_wms_latest_stock AS

WITH ranked_stock AS (
    SELECT
        warehouse_id,
        product_id,
        snapshot_id,
        snapshot_at,
        available_qty,
        ROW_NUMBER() OVER (
            PARTITION BY warehouse_id, product_id
            ORDER BY snapshot_at DESC, snapshot_id DESC
        ) AS rn
    FROM silver.wms_stock_valid
)
SELECT
    warehouse_id,
    product_id,
    snapshot_id,
    snapshot_at,
    available_qty
FROM ranked_stock
WHERE rn = 1;