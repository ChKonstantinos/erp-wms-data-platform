import random
from datetime import datetime
from decimal import Decimal

def generate_customers(
        n : int,
        seed : int =42
) -> list[dict]:

    if not isinstance(n, int) or isinstance(n, bool):
        raise TypeError("n must be an integer")

    if n <= 0:
        raise ValueError("n must be positive")

    rng = random.Random(seed)
    customers = []

    for customer_id in range(1, n + 1):


        customer_type = rng.choice([
            "KIOSK",
            "MINI_MARKET",
            "CONVENIENCE_STORE"
        ])

        customer_name = f"{customer_type}_{customer_id:03d}"

        created_at = datetime(
            2026,
            10,
            rng.randint(1, 31),
            rng.randint(0, 23),
            rng.randint(0, 59)
        )

        customer = {
            "customer_id" : customer_id,
            "customer_name" : customer_name,
            "city" : rng.choice(["Livadia", "Thebes", "Athens", "Chalkida"]),
            "customer_type" : customer_type,
            "is_active" : rng.random() < 0.9,
            "created_at" : created_at,
            "updated_at" : created_at
        }

        customers.append(customer)

    return customers

def generate_products(
        n : int,
        seed : int =42
) -> list[dict]:

    if not isinstance(n, int) or isinstance(n, bool):
        raise TypeError("n must be an integer")

    if n <= 0:
        raise ValueError("n must be positive")

    rng = random.Random(seed)
    products = []

    for product_id in range(1, n + 1):

        category = rng.choice([
            "TOBACCO",
            "LIGHTERS",
            "ROLLING_PAPERS",
            "ACCESSORIES"
        ])

        product_name = f"{category}_{product_id:03d}"

        unit_cost = Decimal(rng.randint(20, 1500)) / Decimal("100")

        created_at = datetime(
            2026,
            10,
            rng.randint(1, 31),
            rng.randint(0, 23),
            rng.randint(0, 59)
        )

        product = {
            "product_id" : product_id,
            "product_name" : product_name,
            "category" : category,
            "unit_cost" : unit_cost,
            "is_active" : rng.random() < 0.95,
            "created_at": created_at,
            "updated_at": created_at
        }

        products.append(product)

    return products

def generate_warehouses(seed=42):

    rng = random.Random(seed)

    created_at = datetime(
        2026,
        10,
        rng.randint(1, 31),
        rng.randint(0, 23),
        rng.randint(0, 59)
    )

    warehouses = [
        {
            "warehouse_id" : 1,
            "warehouse_name" : "Central Warehouse",
            "city" : "Livadia",
            "is_active" : True,
            "created_at" : created_at,
            "updated_at" : created_at
        },
        {
            "warehouse_id": 2,
            "warehouse_name": "Branch Warehouse",
            "city": "Thebes",
            "is_active": True,
            "created_at": created_at,
            "updated_at": created_at
        }
    ]

    return warehouses

if __name__ == "__main__":
    customers = generate_customers(20)
    products = generate_products(100)
    warehouses = generate_warehouses()

    print("Customers:", len(customers))
    print("Products:", len(products))
    print("Warehouses:", len(warehouses))
    print("Active customers:", sum(c["is_active"] for c in customers))
    print("Active products:", sum(p["is_active"] for p in products))
    print("First customer:", customers[0])
    print("First product:", products[0])