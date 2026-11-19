from pathlib import Path
from src.db_connection import get_connection
from src.sql_utils import load_sql_script

BASE_DIR = Path(__file__).resolve().parent.parent
SQL_DIR = BASE_DIR / "sql"

BOOTSTRAP_SCRIPTS = [
    "01_create_sales_headers.sql",
    "02_create_sales_lines.sql",
    "03_create_customers.sql",
    "04_create_products.sql",
    "05_create_warehouses.sql",
    "07_add_foreign_keys.sql",
    "08_create_sales_orders.sql",
    "09_create_sales_order_lines.sql",
    "10_create_bronze_wms_picking.sql",
    "11_create_bronze_wms_stock.sql",
    "13_create_silver_wms_picking.sql",
    "16_create_silver_wms_stock.sql",
    "24_create_wms_snapshot_registry.sql",
    "19_create_latest_stock_view.sql",
    "20_create_order_fulfillment_view.sql",
    "25_create_pipeline_audit_log.sql",
    "21_create_gold_fulfillment_kpis.sql",
    "22_create_gold_product_fulfillment.sql",
    "23_create_gold_order_fulfillment.sql",
    "26_create_pipeline_monitoring_view.sql"
]

def execute_sql_script(conn, filename):

    file_path = SQL_DIR / filename
    sql = load_sql_script(file_path)

    with conn.cursor() as cursor:
        cursor.execute(sql)

def initialize_database():

    with get_connection() as conn:

        schemas_path = BASE_DIR / "docker" / "init" / "00_create_schemas.sql"
        schemas_sql = load_sql_script(schemas_path)

        conn.execute(schemas_sql)

        for script in BOOTSTRAP_SCRIPTS:
            execute_sql_script(conn, script)

if __name__ == "__main__":
    initialize_database()