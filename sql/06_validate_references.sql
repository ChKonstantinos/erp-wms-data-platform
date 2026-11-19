-- Παραστατικά με ανύπαρκτο πελάτη
SELECT COUNT(*) AS invalid_customers
FROM erp_source.sales_headers h
LEFT JOIN erp_source.customers c
    ON h.customer_id = c.customer_id
WHERE c.customer_id IS NULL;

-- Παραστατικά με ανύπαρκτη αποθήκη
SELECT COUNT(*) AS invalid_warehouses
FROM erp_source.sales_headers h
LEFT JOIN erp_source.warehouses w
    ON h.warehouse_id = w.warehouse_id
WHERE w.warehouse_id IS NULL;

-- Γραμμές πωλήσεων με ανύπαρκτο προϊόν
SELECT COUNT(*) AS invalid_products
FROM erp_source.sales_lines l
LEFT JOIN erp_source.products p
    ON l.product_id = p.product_id
WHERE p.product_id IS NULL;