CREATE TABLE IF NOT EXISTS erp_source.sales_headers (
	invoice_id INTEGER PRIMARY KEY,
	customer_id INTEGER NOT NULL,
	warehouse_id INTEGER NOT NULL,
	invoice_date DATE NOT NULL,
	document_type VARCHAR(30) NOT NULL,
	payment_method VARCHAR(30) NOT NULL,
	created_at TIMESTAMP NOT NULL,
	updated_at TIMESTAMP NOT NULL,
	created_by_user_id INTEGER,
	updated_by_user_id INTEGER,
	CHECK (updated_at >= created_at)
);
