CREATE TABLE IF NOT EXISTS erp_source.sales_lines (
	sales_line_id INTEGER PRIMARY KEY,
	invoice_id INTEGER NOT NULL REFERENCES erp_source.sales_headers(invoice_id),
	product_id INTEGER NOT NULL,
	quantity NUMERIC(12, 3) NOT NULL,
	unit_price NUMERIC(12, 2) NOT NULL,
	discount_pct NUMERIC(5, 2) NOT NULL DEFAULT 0,
	created_at TIMESTAMP NOT NULL,
	updated_at TIMESTAMP NOT NULL,
	CHECK (quantity > 0),
	CHECK (unit_price >= 0),
	CHECK (discount_pct BETWEEN 0 AND 100),
	CHECK (updated_at >= created_at)
)