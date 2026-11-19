from src.db_connection import get_connection
from src.generate_master_data import (
    generate_customers,
    generate_products,
    generate_warehouses
)
from src.generate_erp_data import (
    generate_sales_headers,
    generate_sales_lines,
    generate_sales_orders,
    generate_sales_order_lines
)
from src.load_master_data import (
    insert_customers,
    insert_products,
    insert_warehouses
)
from src.load_erp_data import (
    insert_sales_lines,
    insert_sales_headers,
    insert_sales_orders,
    insert_sales_order_lines
)

def seed_erp_database():

    customers = generate_customers(20)
    products = generate_products(100)
    warehouses = generate_warehouses()
    invoices = generate_sales_headers(10)
    sales = generate_sales_lines(invoices)
    orders = generate_sales_orders(30)
    lines = generate_sales_order_lines(orders)

    with get_connection() as conn:
        insert_customers(conn, customers)
        insert_products(conn, products)
        insert_warehouses(conn, warehouses)
        insert_sales_headers(conn, invoices)
        insert_sales_lines(conn, sales)
        insert_sales_orders(conn, orders)
        insert_sales_order_lines(conn, lines)

if __name__ == "__main__":
    seed_erp_database()