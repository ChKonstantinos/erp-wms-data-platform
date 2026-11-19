CREATE TABLE IF NOT EXISTS erp_source.customers (
    customer_id INTEGER PRIMARY KEY,
    customer_name VARCHAR(150) NOT NULL,
    city VARCHAR(100) NOT NULL,
    customer_type VARCHAR(30) NOT NULL,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP NOT NULL,

    CONSTRAINT chk_customer_dates
        CHECK (updated_at >= created_at)
);