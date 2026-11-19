CREATE TABLE IF NOT EXISTS erp_source.sales_orders (
    order_id INTEGER PRIMARY KEY,
    customer_id INTEGER NOT NULL,
    warehouse_id INTEGER NOT NULL,
    order_date TIMESTAMP NOT NULL,
    order_status VARCHAR(30) NOT NULL,
    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP NOT NULL,

    CONSTRAINT fk_orders_customer
        FOREIGN KEY (customer_id)
        REFERENCES erp_source.customers(customer_id),

    CONSTRAINT fk_orders_warehouse
        FOREIGN KEY (warehouse_id)
        REFERENCES erp_source.warehouses(warehouse_id),

    CONSTRAINT chk_order_status
        CHECK (order_status IN (
            'CREATED',
            'SENT_TO_WMS',
            'PICKED',
            'INVOICED',
            'CANCELLED'
        )),

    CONSTRAINT chk_order_dates
        CHECK (updated_at >= created_at)
);