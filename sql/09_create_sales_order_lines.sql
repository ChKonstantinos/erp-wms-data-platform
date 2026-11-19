CREATE TABLE IF NOT EXISTS erp_source.sales_order_lines (
    order_line_id INTEGER PRIMARY KEY,
    order_id INTEGER NOT NULL,
    product_id INTEGER NOT NULL,
    requested_qty INTEGER NOT NULL,
    unit_price NUMERIC(12,2) NOT NULL,
    discount_pct NUMERIC(5,2) NOT NULL,
    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP NOT NULL,

    CONSTRAINT fk_orders_lines
        FOREIGN KEY (order_id)
        REFERENCES erp_source.sales_orders(order_id),

    CONSTRAINT fk_lines_products
        FOREIGN KEY (product_id)
        REFERENCES erp_source.products(product_id),

    CONSTRAINT chk_requested_qty
        CHECK (requested_qty > 0),

    CONSTRAINT chk_unit_price
        CHECK (unit_price >= 0),

    CONSTRAINT chk_discount_pct
        CHECK (discount_pct BETWEEN 0 AND 100),

    CONSTRAINT chk_order_line_dates
        CHECK (updated_at >= created_at)
);