import random
from datetime import datetime
from decimal import Decimal


def generate_sales_headers(
    n: int,
    seed: int = 42
) -> list[dict]:

    if not isinstance(n, int) or isinstance(n, bool):
        raise TypeError("n must be an integer")

    if n <= 0:
        raise ValueError("n must be positive")

    rng = random.Random(seed)
    invoices = []

    for invoice_id in range(1, n + 1):

        created_at = datetime(
            2026,
            10,
            rng.randint(1, 31),
            rng.randint(0, 23),
            rng.randint(0, 59)
        )

        user_id = rng.randint(1, 5)

        invoice = {
            "invoice_id": invoice_id,
            "customer_id": rng.randint(1, 20),
            "warehouse_id": rng.choice([1, 2]),
            "invoice_date": created_at.date(),
            "document_type": rng.choice(["SALE", "RETURN"]),
            "payment_method": rng.choice(["CASH", "CREDIT"]),
            "created_at": created_at,
            "updated_at": created_at,
            "created_by_user_id": user_id,
            "updated_by_user_id": user_id
        }

        invoices.append(invoice)

    return invoices


def generate_sales_lines(invoices : list[dict],
                         seed : int = 42) -> list[dict]:

    if not isinstance(invoices, list):
        raise TypeError("Invoices must be a list")

    if len(invoices) == 0:
        raise ValueError("Empty list")

    rng = random.Random(seed)
    sales = []
    line_cnt = 1

    for invoice in invoices:

        for _ in range(rng.randint(1, 5)):

            sale = {
                "sales_line_id" : line_cnt,
                "invoice_id" : invoice["invoice_id"],
                "product_id" : rng.randint(1, 100),
                "quantity" : rng.randint(1, 20),
                "unit_price" : rng.randint(50, 10000) / 100,
                "discount_pct" : rng.choice([0, 5, 10, 15, 20]),
                "created_at" : invoice["created_at"],
                "updated_at" : invoice["created_at"]
            }

            line_cnt += 1

            sales.append(sale)

    return sales

def generate_sales_orders(n, seed=42):

    if not isinstance(n, int) or isinstance(n, bool):
        raise TypeError("n must be an integer")

    if n <= 0:
        raise ValueError("n must be positive")

    rng = random.Random(seed)
    orders = []

    for order_id in range(1, n + 1):
        created_at = datetime(
            2026,
            10,
            rng.randint(1, 31),
            rng.randint(0, 23),
            rng.randint(0, 59)
        )

        order = {
            "order_id": order_id,
            "customer_id": rng.randint(1, 20),
            "warehouse_id": rng.choice([1, 2]),
            "order_date": created_at,
            "order_status": "CREATED",
            "created_at": created_at,
            "updated_at": created_at
        }

        orders.append(order)

    return orders

def generate_sales_order_lines(orders, seed=42):

    if not isinstance(orders, list):
        raise TypeError("Orders must be a list")

    if len(orders) == 0:
        raise ValueError("Empty list")

    rng = random.Random(seed)
    order_lines = []
    line_cnt = 1

    for order in orders:

        num_lines = rng.randint(1, 5)
        product_ids = rng.sample(range(1, 101), k=num_lines)

        for product_id in product_ids:

            unit_price = Decimal(rng.randint(20, 1500)) / Decimal("100")

            order_line = {
                "order_line_id" : line_cnt,
                "order_id" : order["order_id"],
                "product_id" : product_id,
                "requested_qty" : rng.randint(1, 30),
                "unit_price" : unit_price,
                "discount_pct" : rng.randint(0, 20),
                "created_at" : order["created_at"],
                "updated_at" : order["created_at"]
            }

            line_cnt += 1

            order_lines.append(order_line)

    return order_lines

if __name__ == "__main__":

    invoices = generate_sales_headers(10)
    sales = generate_sales_lines(invoices)

    print("Invoices:", len(invoices))
    print("Sales lines:", len(sales))
    print("Unique line IDs:", len({s["sales_line_id"] for s in sales}))

    sales_1 = generate_sales_lines(invoices, seed=42)
    sales_2 = generate_sales_lines(invoices, seed=42)
    sales_3 = generate_sales_lines(invoices, seed=100)

    print(sales_1 == sales_2)
    print(sales_1 == sales_3)

    from collections import Counter

    orders = generate_sales_orders(30)
    lines = generate_sales_order_lines(orders)

    counts = Counter(line["order_id"] for line in lines)

    print("Orders:", len(orders))
    print("Order lines:", len(lines))

    print("Every order has 1-5 lines:",
          len(counts) == len(orders)
          and all(1 <= count <= 5 for count in counts.values()))

    pairs = [
        (line["order_id"], line["product_id"])
        for line in lines
    ]

    print("Unique products per order:",
          len(pairs) == len(set(pairs)))