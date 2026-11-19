from src.db_connection import get_connection


def test_silver_picking_valid_quantities():

    sql = """
        SELECT COUNT(*)
        FROM silver.wms_picking_valid
        WHERE requested_qty <= 0
           OR picked_qty < 0
           OR requested_qty IS NULL
           OR picked_qty IS NULL;
    """

    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(sql)

            invalid_count = cursor.fetchone()[0]

            assert invalid_count == 0

def test_silver_picking_reconciliation():

    sql = """
        SELECT
            (SELECT COUNT(*) FROM bronze.wms_picking),
            (SELECT COUNT(*) FROM silver.wms_picking_valid),
            (SELECT COUNT(*) FROM silver.wms_picking_rejected);
    """

    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(sql)

            bronze_count, valid_count, rejected_count = cursor.fetchone()

            assert bronze_count == valid_count + rejected_count

def test_silver_picking_record_reconciliation():

    sql = """
        SELECT COUNT(*)
        FROM bronze.wms_picking b
        WHERE NOT EXISTS (
            SELECT 1
            FROM silver.wms_picking_valid v
            WHERE v.picking_id = b.picking_id
        )
        AND NOT EXISTS (
            SELECT 1
            FROM silver.wms_picking_rejected r
            WHERE r.picking_id = b.picking_id
        );
    """

    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(sql)

            missing_records_count = cursor.fetchone()[0]

            assert missing_records_count == 0