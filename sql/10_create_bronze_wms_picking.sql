CREATE TABLE IF NOT EXISTS bronze.wms_picking (
	picking_id INTEGER PRIMARY KEY,
	order_line_id INTEGER NOT NULL,
	warehouse_id INTEGER NOT NULL,
	product_id INTEGER NOT NULL,
	requested_qty INTEGER NOT NULL,
	picked_qty INTEGER NOT NULL,
	source_file VARCHAR(255),
	picking_status VARCHAR(30) NOT NULL,
	ingested_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);