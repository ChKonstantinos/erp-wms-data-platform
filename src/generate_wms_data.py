import random

def generate_wms_stock(
    product_ids,
    warehouse_ids,
    seed=42
):

    if not isinstance(product_ids, list):
        raise TypeError("Product Ids must be a list")

    if not isinstance(warehouse_ids, list):
        raise TypeError("Warehouse Ids must be a list")

    if not product_ids:
        raise ValueError("Product IDs list cannot be empty")

    if not warehouse_ids:
        raise ValueError("Warehouse IDs list cannot be empty")

    for product_id in product_ids:
        if type(product_id) is not int or product_id <= 0:
            raise ValueError("Product IDs must be positive integers")

    for warehouse_id in warehouse_ids:
        if type(warehouse_id) is not int or warehouse_id <= 0:
            raise ValueError("Warehouse IDs must be positive integers")

    if len(product_ids) != len(set(product_ids)):
        raise ValueError("Duplicate product IDs detected")

    if len(warehouse_ids) != len(set(warehouse_ids)):
        raise ValueError("Duplicate warehouse IDs detected")

    rng = random.Random(seed)

    wms_stock = []

    for warehouse_id in warehouse_ids:

        for product_id in product_ids:

            stock = {
                "warehouse_id" : warehouse_id,
                "product_id" : product_id,
                "available_qty" : rng.randint(0, 150)
            }

            wms_stock.append(stock)

    return wms_stock

def execute_picking(requested_qty, available_qty, picked_qty):

    if not isinstance(requested_qty, int) or isinstance(requested_qty, bool):
        raise TypeError("Requested quantity must be an integer")

    if not isinstance(available_qty, int) or isinstance(available_qty, bool):
        raise TypeError("Available quantity must be an integer")

    if not isinstance(picked_qty, int) or isinstance(picked_qty, bool):
        raise TypeError("Picked quantity must be an integer")

    if (requested_qty < 0) or (available_qty < 0) or (picked_qty < 0):
        raise ValueError("Quantities cannot be negative")

    if requested_qty <= 0:
        raise ValueError("Requested quantity must be positive")

    if (picked_qty > available_qty):
        raise ValueError("Picked quantity is not available")


    if picked_qty == 0:
        picking_status = "FAILED"
    elif picked_qty < requested_qty:
        picking_status = "PARTIAL"
    elif picked_qty == requested_qty:
        picking_status = "COMPLETED"
    else:
        picking_status = "OVER_PICKED"

    remaining_stock = available_qty - picked_qty

    return {"picking_status" : picking_status, "remaining_stock" : remaining_stock}

def generate_wms_picking(orders, order_lines, wms_stock, seed=42):

    rng = random.Random(seed)

    line_ids = [
        line["order_line_id"]
        for line in order_lines
    ]

    if len(line_ids) != len(set(line_ids)):
        raise ValueError("Duplicate order_line_id detected")

    warehouse_lookup = {
        order["order_id"]: order["warehouse_id"]
        for order in orders
    }

    order_dates = {
        order["order_id"]: order["order_date"]
        for order in orders
    }

    stock_lookup = {
        (row["warehouse_id"], row["product_id"]): row["available_qty"]
        for row in wms_stock
    }

    picking_records = []
    picking_id = 1

    sorted_lines = sorted(
        order_lines,
        key=lambda line: (
            order_dates[line["order_id"]],
            line["order_line_id"]
        )
    )

    for line in sorted_lines:

        order_id = line["order_id"]
        warehouse_id = warehouse_lookup[order_id]

        product_id = line["product_id"]
        requested_qty = line["requested_qty"]

        available_qty = stock_lookup[(warehouse_id, product_id)]

        scenario = rng.choices(
            ["NORMAL", "PARTIAL", "OVER"],
            weights=[75, 15, 10],
            k=1
        )[0]

        if scenario == "NORMAL":
            desired_qty = requested_qty
        elif scenario == "PARTIAL":
            desired_qty = rng.randint(0, (requested_qty - 1))
        else:
            desired_qty = rng.randint((requested_qty + 1), (requested_qty + 10))

        picked_qty = min(desired_qty, available_qty)


        result = execute_picking(requested_qty, available_qty, picked_qty)

        remaining_stock = result["remaining_stock"]

        stock_lookup[(warehouse_id, product_id)] = remaining_stock

        picking_record = {
            "picking_id" : picking_id,
            "order_line_id" : line["order_line_id"],
            "warehouse_id" : warehouse_id,
            "product_id" : product_id,
            "requested_qty" : requested_qty,
            "picked_qty" : picked_qty,
            "picking_status" : result["picking_status"]
        }

        picking_records.append(picking_record)

        picking_id += 1

    updated_stock = [
        {
            "warehouse_id": warehouse_id,
            "product_id": product_id,
            "available_qty": qty
        }
        for (warehouse_id, product_id), qty in stock_lookup.items()
    ]

    return picking_records, updated_stock