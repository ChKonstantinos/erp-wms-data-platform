from src.db_connection import get_connection


def test_gold_shortage_reconciliation():

    sql = """
        SELECT
            (SELECT COALESCE(SUM(shortage_qty), 0)
             FROM silver.v_order_fulfillment) AS silver_shortage,
            (SELECT total_shortage_qty
             FROM gold.v_order_fulfillment_kpis) AS gold_shortage;
    """

    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(sql)

            silver_shortage, gold_shortage = cursor.fetchone()

            assert silver_shortage == gold_shortage

def test_gold_kpi_reconciliation():

    sql = """
        SELECT
            s.total_order_lines,
            g.total_order_lines,
            s.total_ordered_qty,
            g.total_ordered_qty,
            s.total_picked_qty,
            g.total_picked_qty,
            s.total_shortage_qty,
            g.total_shortage_qty,
            s.total_overpicked_qty,
            g.total_overpicked_qty
        FROM (
            SELECT
                COUNT(*) AS total_order_lines,
                COALESCE(SUM(ordered_qty), 0) AS total_ordered_qty,
                COALESCE(SUM(picked_qty), 0) AS total_picked_qty,
                COALESCE(SUM(shortage_qty), 0) AS total_shortage_qty,
                COALESCE(SUM(overpicked_qty), 0) AS total_overpicked_qty
            FROM silver.v_order_fulfillment
        ) s
        CROSS JOIN gold.v_order_fulfillment_kpis g;
    """

    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(sql)


            (silver_lines, gold_lines,
             silver_ordered, gold_ordered,
             silver_picked, gold_picked,
             silver_shortage, gold_shortage,
             silver_overpicked, gold_overpicked) = cursor.fetchone()

            silver_values = [
                silver_lines,
                silver_ordered,
                silver_picked,
                silver_shortage,
                silver_overpicked
            ]

            gold_values = [
                gold_lines,
                gold_ordered,
                gold_picked,
                gold_shortage,
                gold_overpicked
            ]

            assert all(
                silver == gold
                for silver, gold in zip(silver_values, gold_values)
            )

def test_fulfillment_percentages():

    sql = """
        SELECT
            actual_fulfillment_pct,
            capped_fulfillment_pct,
            ROUND(
                total_picked_qty * 100.0 /
                NULLIF(total_ordered_qty, 0), 2
            ) AS expected_actual,
            ROUND(
                (total_ordered_qty - total_shortage_qty) * 100.0 /
                NULLIF(total_ordered_qty, 0), 2
            ) AS expected_capped
        FROM gold.v_order_fulfillment_kpis;
    """

    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(sql)

            actual, capped, expected_actual, expected_capped = cursor.fetchone()

            assert actual == expected_actual
            assert capped == expected_capped
            assert 0 <= capped <= 100
            assert capped <= actual
