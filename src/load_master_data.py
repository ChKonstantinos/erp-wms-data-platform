from src.generate_master_data import (
    generate_customers,
    generate_products,
    generate_warehouses
)

from src.db_connection import get_connection

def insert_customers(conn, customers):

    values = []

    sql = """
            INSERT INTO erp_source.customers (
                customer_id, customer_name, city, customer_type,
                is_active, created_at, updated_at)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (customer_id) DO NOTHING
        """

    for customer in customers:
        values.append((
            customer["customer_id"],
            customer["customer_name"],
            customer["city"],
            customer["customer_type"],
            customer["is_active"],
            customer["created_at"],
            customer["updated_at"],
        ))

    with conn.cursor() as cursor:
        cursor.executemany(sql, values)

def insert_products(conn, products):

    values = []

    sql = """
            INSERT INTO erp_source.products (
                product_id, product_name, category, unit_cost,
                is_active, created_at, updated_at)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (product_id) DO NOTHING
        """

    for product in products:
        values.append((
            product["product_id"],
            product["product_name"],
            product["category"],
            product["unit_cost"],
            product["is_active"],
            product["created_at"],
            product["updated_at"],
        ))

    with conn.cursor() as cursor:
        cursor.executemany(sql, values)

def insert_warehouses(conn, warehouses):

    values = []

    sql = """
            INSERT INTO erp_source.warehouses (
                warehouse_id, warehouse_name, city,
                is_active, created_at, updated_at)
            VALUES (%s, %s, %s, %s, %s, %s)
            ON CONFLICT (warehouse_id) DO NOTHING
        """

    for warehouse in warehouses:
        values.append((
            warehouse["warehouse_id"],
            warehouse["warehouse_name"],
            warehouse["city"],
            warehouse["is_active"],
            warehouse["created_at"],
            warehouse["updated_at"],
        ))

    with conn.cursor() as cursor:
        cursor.executemany(sql, values)


if __name__ == "__main__":

    customers = generate_customers(20)
    products = generate_products(100)
    warehouses = generate_warehouses()

    with get_connection() as conn:
        insert_customers(conn, customers)
        insert_products(conn, products)
        insert_warehouses(conn, warehouses)

    print("Master data loaded successfully")