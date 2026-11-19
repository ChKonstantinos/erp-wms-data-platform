from src.run_pipeline import run_pipeline
from src.db_connection import get_connection


def test_pipeline_success():

    pipeline_run_id = run_pipeline()

    sql = """
        SELECT
            status,
            finished_at
        FROM gold.pipeline_audit_log
        WHERE pipeline_run_id = %s;
    """

    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(sql, (pipeline_run_id,))

            row = cursor.fetchone()

            assert row is not None, "Pipeline audit record not found"

            pipeline_status, pipeline_time = row

            assert pipeline_status == 'SUCCESS'
            assert pipeline_time is not None


def get_table_counts():

    sql = """
        SELECT
            (SELECT COUNT(*) FROM bronze.wms_picking),
            (SELECT COUNT(*) FROM bronze.wms_stock),
            (SELECT COUNT(*) FROM silver.wms_picking_valid),
            (SELECT COUNT(*) FROM silver.wms_stock_valid);
    """

    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(sql)

            bronze_picking, bronze_stock, silver_picking, silver_stock = cursor.fetchone()

            return {
                "bronze.wms_picking" : bronze_picking,
                "bronze.wms_stock" : bronze_stock,
                "silver.wms_picking_valid" : silver_picking,
                "silver.wms_stock_valid" : silver_stock
            }

def test_pipeline_idempotency():

    run_pipeline()
    counts_before = get_table_counts()
    run_pipeline()
    counts_after = get_table_counts()

    assert counts_before == counts_after