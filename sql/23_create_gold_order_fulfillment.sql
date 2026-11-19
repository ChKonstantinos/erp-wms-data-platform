CREATE OR REPLACE VIEW gold.v_order_fulfillment AS
SELECT
    order_id,
    COUNT(*) AS total_order_lines,
    SUM(ordered_qty) AS total_ordered_qty,
    SUM(picked_qty) AS total_picked_qty,
    SUM(shortage_qty) AS total_shortage_qty,
    SUM(overpicked_qty) AS total_overpicked_qty,
    ROUND(
        SUM(LEAST(picked_qty, ordered_qty)) * 100.0 /
        NULLIF(SUM(ordered_qty), 0),
        2
    ) AS capped_fulfillment_pct
FROM silver.v_order_fulfillment
GROUP BY order_id;