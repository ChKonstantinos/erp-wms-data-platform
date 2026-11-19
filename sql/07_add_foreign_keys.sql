DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1
        FROM pg_constraint
        WHERE conname = 'fk_sales_headers_customer'
          AND conrelid = 'erp_source.sales_headers'::regclass
    ) THEN
        ALTER TABLE erp_source.sales_headers
        ADD CONSTRAINT fk_sales_headers_customer
        FOREIGN KEY (customer_id)
        REFERENCES erp_source.customers(customer_id);
    END IF;
END $$;

DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1
        FROM pg_constraint
        WHERE conname = 'fk_sales_headers_warehouse'
          AND conrelid = 'erp_source.sales_headers'::regclass
    ) THEN
        ALTER TABLE erp_source.sales_headers
        ADD CONSTRAINT fk_sales_headers_warehouse
        FOREIGN KEY (warehouse_id)
        REFERENCES erp_source.warehouses(warehouse_id);
    END IF;
END $$;

DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1
        FROM pg_constraint
        WHERE conname = 'fk_sales_lines_product'
          AND conrelid = 'erp_source.sales_lines'::regclass
    ) THEN
        ALTER TABLE erp_source.sales_lines
        ADD CONSTRAINT fk_sales_lines_product
        FOREIGN KEY (product_id)
        REFERENCES erp_source.products(product_id);
    END IF;
END $$;
