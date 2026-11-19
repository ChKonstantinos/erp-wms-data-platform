from src.db_connection import get_connection


def test_latest_stock_uniqueness():

    sql = """
        SELECT COUNT(*)
        FROM (
            SELECT
                warehouse_id,
                product_id
            FROM silver.v_wms_latest_stock
            GROUP BY warehouse_id, product_id
            HAVING COUNT(*) > 1
        ) duplicates;
    """

    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(sql)

            duplicate_count = cursor.fetchone()[0]

            assert duplicate_count == 0

def test_latest_stock_correct_snapshot():

    sql = """
        WITH expected_latest AS (
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
        SELECT COUNT(*)
        FROM expected_latest e
        LEFT JOIN silver.v_wms_latest_stock v
            ON e.warehouse_id = v.warehouse_id
           AND e.product_id = v.product_id
        WHERE e.rn = 1
          AND (
              v.snapshot_id IS DISTINCT FROM e.snapshot_id
              OR v.snapshot_at IS DISTINCT FROM e.snapshot_at
              OR v.available_qty IS DISTINCT FROM e.available_qty
          );
    """

    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(sql)

            mismatch_count = cursor.fetchone()[0]

            assert mismatch_count == 0