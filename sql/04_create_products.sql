CREATE TABLE IF NOT EXISTS erp_source.products (
    product_id INTEGER PRIMARY KEY,
    product_name VARCHAR(150) NOT NULL,
    category VARCHAR(50) NOT NULL,
    unit_cost NUMERIC(12,2) NOT NULL,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP NOT NULL,

    CONSTRAINT chk_product_dates
        CHECK (updated_at >= created_at),

	CONSTRAINT chk_product_unit_cost
		CHECK (unit_cost >= 0)
);