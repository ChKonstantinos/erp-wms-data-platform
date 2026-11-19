CREATE TABLE IF NOT EXISTS erp_source.warehouses (
    warehouse_id INTEGER PRIMARY KEY,
    warehouse_name VARCHAR(100) NOT NULL,
    city VARCHAR(100) NOT NULL,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP NOT NULL,

    CONSTRAINT chk_warehouse_dates
        CHECK (updated_at >= created_at)
);