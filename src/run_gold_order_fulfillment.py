from src.db_connection import get_connection


def run_gold_order_fulfillment():

    sql = """
        INSERT INTO gold.order_fulfillment_summary (
            order_id,
            total_ordered_qty,
            total_picked_qty,
            total_shortage_qty,
            total_overpicked_qty,
            fulfillment_pct
        )
        SELECT
            order_id,
            SUM(ordered_qty),
            SUM(picked_qty),
            SUM(shortage_qty),
            SUM(overpicked_qty),
            ROUND(
                100.0 * SUM(LEAST(picked_qty, ordered_qty))
                / NULLIF(SUM(ordered_qty), 0),
                2
            )
        FROM silver.v_order_fulfillment
        GROUP BY order_id

        ON CONFLICT (order_id)
        DO UPDATE SET
            total_ordered_qty = EXCLUDED.total_ordered_qty,
            total_picked_qty = EXCLUDED.total_picked_qty,
            total_shortage_qty = EXCLUDED.total_shortage_qty,
            total_overpicked_qty = EXCLUDED.total_overpicked_qty,
            fulfillment_pct = EXCLUDED.fulfillment_pct;
    """

    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(sql)

    print("Gold order fulfillment transformation completed")