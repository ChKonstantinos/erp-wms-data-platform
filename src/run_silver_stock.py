from src.db_connection import get_connection
from src.sql_utils import load_sql_script


def run_silver_stock_pipeline():

    sql_script = load_sql_script(
        "sql/18_load_silver_wms_stock.sql"
    )

    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(sql_script)

if __name__ == "__main__":
    run_silver_stock_pipeline()