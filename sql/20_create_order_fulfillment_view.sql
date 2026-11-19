CREATE OR REPLACE VIEW silver.v_order_fulfillment AS

WITH picking_aggregated AS (
    SELECT
        order_line_id,
        SUM(picked_qty) AS total_picked_qty
    FROM silver.wms_picking_valid
    GROUP BY order_line_id
),

order_fulfillment AS (
    SELECT
        e.order_line_id,
        e.order_id,
        e.product_id,
        e.requested_qty AS ordered_qty,
        COALESCE(w.total_picked_qty, 0) AS picked_qty
    FROM erp_source.sales_order_lines AS e
    LEFT JOIN picking_aggregated AS w
        ON e.order_line_id = w.order_line_id
)

SELECT
    order_line_id,
    order_id,
    product_id,
    ordered_qty,
    picked_qty,

    GREATEST(ordered_qty - picked_qty, 0) AS shortage_qty,

    GREATEST(picked_qty - ordered_qty, 0) AS overpicked_qty,

    ROUND(
        picked_qty * 100.0 / NULLIF(ordered_qty, 0),
        2
    ) AS actual_fulfillment_pct,

    ROUND(
        LEAST(picked_qty, ordered_qty) * 100.0
        / NULLIF(ordered_qty, 0),
        2
    ) AS capped_fulfillment_pct,

    CASE
        WHEN picked_qty = 0 THEN 'NOT_PICKED'
        WHEN picked_qty < ordered_qty THEN 'PARTIAL'
        WHEN picked_qty = ordered_qty THEN 'COMPLETED'
        WHEN picked_qty > ordered_qty THEN 'OVER_PICKED'
    END AS fulfillment_status

FROM order_fulfillment;