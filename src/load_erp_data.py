from src.generate_erp_data import (
    generate_sales_headers,
    generate_sales_lines,
    generate_sales_orders,
    generate_sales_order_lines
)

from src.db_connection import get_connection


def insert_sales_headers(conn, invoices):

    values = []

    sql = """
            INSERT INTO erp_source.sales_headers (
                invoice_id, customer_id, warehouse_id, invoice_date,
                document_type, payment_method, created_at, updated_at,
                created_by_user_id, updated_by_user_id)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (invoice_id) DO NOTHING
        """

    for invoice in invoices:
        values.append((
            invoice["invoice_id"],
            invoice["customer_id"],
            invoice["warehouse_id"],
            invoice["invoice_date"],
            invoice["document_type"],
            invoice["payment_method"],
            invoice["created_at"],
            invoice["updated_at"],
            invoice["created_by_user_id"],
            invoice["updated_by_user_id"]
        ))

    with conn.cursor() as cursor:
        cursor.executemany(sql, values)

def insert_sales_lines(conn, sales):

    values = []

    sql = """
            INSERT INTO erp_source.sales_lines (
                sales_line_id, invoice_id, product_id, quantity,
                unit_price, discount_pct, created_at, updated_at)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (sales_line_id) DO NOTHING
        """

    for sale in sales:
        values.append((
            sale["sales_line_id"],
            sale["invoice_id"],
            sale["product_id"],
            sale["quantity"],
            sale["unit_price"],
            sale["discount_pct"],
            sale["created_at"],
            sale["updated_at"]
        ))

    with conn.cursor() as cursor:
        cursor.executemany(sql, values)

def insert_sales_orders(conn, orders):
    query = """
        INSERT INTO erp_source.sales_orders (
            order_id, customer_id, warehouse_id,
            order_date, order_status,
            created_at, updated_at
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (order_id) DO NOTHING
    """

    rows = [
        (
            o["order_id"],
            o["customer_id"],
            o["warehouse_id"],
            o["order_date"],
            o["order_status"],
            o["created_at"],
            o["updated_at"]
        )
        for o in orders
    ]

    with conn.cursor() as cursor:
        cursor.executemany(query, rows)


def insert_sales_order_lines(conn, lines):
    query = """
        INSERT INTO erp_source.sales_order_lines (
            order_line_id, order_id, product_id,
            requested_qty, unit_price, discount_pct,
            created_at, updated_at
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (order_line_id) DO NOTHING
    """

    rows = [
        (
            line["order_line_id"],
            line["order_id"],
            line["product_id"],
            line["requested_qty"],
            line["unit_price"],
            line["discount_pct"],
            line["created_at"],
            line["updated_at"]
        )
        for line in lines
    ]

    with conn.cursor() as cursor:
        cursor.executemany(query, rows)


if __name__ == "__main__":

    orders = generate_sales_orders(30)
    lines = generate_sales_order_lines(orders)

    with get_connection() as conn:
        insert_sales_orders(conn, orders)
        insert_sales_order_lines(conn, lines)

    print("ERP data loaded successfully")