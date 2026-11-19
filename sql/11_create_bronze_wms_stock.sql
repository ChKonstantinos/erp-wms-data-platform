CREATE TABLE IF NOT EXISTS bronze.wms_stock (
	snapshot_id INTEGER NOT NULL,
	warehouse_id INTEGER NOT NULL,
	product_id INTEGER NOT NULL,
	available_qty INTEGER NOT NULL,
	snapshot_at TIMESTAMP NOT NULL,
	source_file VARCHAR(255),
	ingested_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
	PRIMARY KEY (snapshot_id, warehouse_id, product_id)
);