from src.generate_erp_data import generate_sales_orders, generate_sales_order_lines
from src.generate_wms_data import generate_wms_stock, generate_wms_picking

# 1. Δημιουργία 30 παραγγελιών
orders = generate_sales_orders(30)

# 2. Δημιουργία γραμμών για τις ίδιες παραγγελίες
order_lines = generate_sales_order_lines(orders)

# 3. Δημιουργία αρχικού αποθέματος WMS
product_ids = list(range(1, 101))
warehouse_ids = [1, 2]

wms_stock = generate_wms_stock(product_ids, warehouse_ids)

# 4. Εκτέλεση picking
picking_records, updated_stock = generate_wms_picking(
    orders, order_lines, wms_stock
)


print("Orders:", len(orders))
print("Order lines:", len(order_lines))
print("Picking records:", len(picking_records))
print("Stock records:", len(updated_stock))

print("Unique picking IDs:",
      len(set(p["picking_id"] for p in picking_records)))

print("Unique order line IDs:",
      len(set(p["order_line_id"] for p in picking_records)))

print("Negative stock:",
      sum(s["available_qty"] < 0 for s in updated_stock))


initial_stock = {
    (s["warehouse_id"], s["product_id"]): s["available_qty"]
    for s in wms_stock
}

final_stock = {
    (s["warehouse_id"], s["product_id"]): s["available_qty"]
    for s in updated_stock
}

picked_totals = {}

for p in picking_records:
    key = (p["warehouse_id"], p["product_id"])

    picked_totals[key] = (
        picked_totals.get(key, 0) + p["picked_qty"]
    )

reconciliation_errors = []

for key, initial_qty in initial_stock.items():

    total_picked = picked_totals.get(key, 0)
    final_qty = final_stock[key]

    if initial_qty - total_picked != final_qty:
        reconciliation_errors.append(key)

print("Stock reconciliation errors:", len(reconciliation_errors))

duplicate_lines = order_lines + [order_lines[0].copy()]

try:
    generate_wms_picking(orders, duplicate_lines, wms_stock)
except ValueError as e:
    print("Duplicate test:", e)

from src.export_wms_data import export_to_csv

export_to_csv(
    picking_records,
   "data/wms_exports/wms_picking.csv"
)

export_to_csv(
    updated_stock,
    "data/wms_exports/wms_stock.csv"
)

import csv

for filename in ["wms_picking.csv", "wms_stock.csv"]:

    path = f"data/wms_exports/{filename}"

    with open(path, "r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    print(filename, ":", len(rows))

from src.ingest_wms import read_wms_csv

records = read_wms_csv(
    "data/wms_exports/wms_picking.csv"
)

print("CSV records:", len(records))
print("First record:", records[0])
