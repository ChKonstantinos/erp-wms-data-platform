CREATE TABLE IF NOT EXISTS silver.wms_stock_valid (
	snapshot_id INTEGER NOT NULL,
	warehouse_id INTEGER NOT NULL,
	product_id INTEGER NOT NULL,
	available_qty INTEGER NOT NULL,
	snapshot_at TIMESTAMP NOT NULL,
	processed_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
	PRIMARY KEY (snapshot_id, warehouse_id, product_id),
	CHECK (available_qty >= 0)
);