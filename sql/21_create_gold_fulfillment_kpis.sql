CREATE OR REPLACE VIEW gold.v_order_fulfillment_kpis AS

SELECT
    COUNT(*) AS total_order_lines,

    SUM(ordered_qty) AS total_ordered_qty,
    SUM(picked_qty) AS total_picked_qty,

    SUM(shortage_qty) AS total_shortage_qty,
    SUM(overpicked_qty) AS total_overpicked_qty,

    COUNT(*) FILTER (
        WHERE fulfillment_status = 'COMPLETED'
    ) AS completed_lines,

    COUNT(*) FILTER (
        WHERE fulfillment_status = 'PARTIAL'
    ) AS partial_lines,

    COUNT(*) FILTER (
        WHERE fulfillment_status = 'NOT_PICKED'
    ) AS not_picked_lines,

    COUNT(*) FILTER (
        WHERE fulfillment_status = 'OVER_PICKED'
    ) AS overpicked_lines,

    ROUND(
        SUM(picked_qty) * 100.0 /
        NULLIF(SUM(ordered_qty), 0),
        2
    ) AS actual_fulfillment_pct,

    ROUND(
        SUM(LEAST(picked_qty, ordered_qty)) * 100.0 /
        NULLIF(SUM(ordered_qty), 0),
        2
    ) AS capped_fulfillment_pct,

    ROUND(
        COUNT(*) FILTER (
            WHERE fulfillment_status = 'COMPLETED'
        ) * 100.0 / NULLIF(COUNT(*), 0),
        2
    ) AS completed_lines_pct

FROM silver.v_order_fulfillment;