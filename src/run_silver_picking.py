from src.db_connection import get_connection
from src.sql_utils import load_sql_script


def run_silver_picking_pipeline():

    sql_script = load_sql_script(
        "sql/15_sync_silver_wms_picking.sql"
    )

    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(sql_script)

            while cursor.nextset():
                pass

            result = cursor.fetchone()

            if result is None:
                raise ValueError("No reconciliation result returned")

            status = result[-1]

            if status != 'SUCCESS':
                raise ValueError("Silver Picking reconciliation failed")

    print("Silver Picking Pipeline completed")

if __name__ == "__main__":
    run_silver_picking_pipeline()