CREATE OR REPLACE VIEW gold.v_inventory_summary AS
SELECT
    warehouse_id,
    product_id,
    snapshot_at,
    available_qty,
    CASE
        WHEN available_qty = 0 THEN 'OUT_OF_STOCK'::text
        WHEN available_qty <= 10 THEN 'LOW_STOCK'::text
        WHEN available_qty <= 30 THEN 'MEDIUM_STOCK'::text
        ELSE 'HEALTHY_STOCK'::text
    END AS stock_status
FROM silver.v_wms_latest_stock;