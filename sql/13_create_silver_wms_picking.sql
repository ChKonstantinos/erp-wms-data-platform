CREATE TABLE IF NOT EXISTS silver.wms_picking_valid (
	picking_id INTEGER PRIMARY KEY,
	order_line_id INTEGER NOT NULL,
	warehouse_id INTEGER NOT NULL,
	product_id INTEGER NOT NULL,
	requested_qty INTEGER NOT NULL,
	picked_qty INTEGER NOT NULL,
	picking_status VARCHAR(30) NOT NULL,
	processed_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS silver.wms_picking_rejected (
	rejection_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
	picking_id INTEGER,
	order_line_id INTEGER,
	warehouse_id INTEGER,
	product_id INTEGER,
	requested_qty INTEGER,
	picked_qty INTEGER,
	picking_status VARCHAR(30),
	rejection_reason VARCHAR(100) NOT NULL,
	processed_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);