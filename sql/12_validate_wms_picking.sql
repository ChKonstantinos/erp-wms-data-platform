WITH validated AS (
    SELECT
    picking_id,
    requested_qty,
    picked_qty,
    picking_status,
    CASE
		WHEN picking_id IS NULL
	     OR order_line_id IS NULL
	     OR warehouse_id IS NULL
	     OR product_id IS NULL
	     OR requested_qty IS NULL
	     OR picked_qty IS NULL
	     OR picking_status IS NULL
		THEN 'REJECTED'
        WHEN requested_qty <= 0 THEN 'REJECTED'
        WHEN picked_qty < 0 THEN 'REJECTED'
		WHEN picking_status NOT IN ('FAILED', 'PARTIAL', 'COMPLETED', 'OVER_PICKED') THEN 'REJECTED'
		WHEN (picked_qty = 0) AND (picking_status <> 'FAILED') THEN 'REJECTED'
		WHEN (picked_qty > 0) AND (requested_qty > picked_qty) AND (picking_status <> 'PARTIAL') THEN 'REJECTED'
		WHEN (requested_qty = picked_qty) AND (picking_status <> 'COMPLETED') THEN 'REJECTED'
		WHEN (requested_qty < picked_qty) AND (picking_status <> 'OVER_PICKED') THEN 'REJECTED'
        ELSE 'VALID'
    END AS dq_status,

    CASE
       WHEN picking_id IS NULL
	    OR order_line_id IS NULL
	    OR warehouse_id IS NULL
	    OR product_id IS NULL
	    OR requested_qty IS NULL
	    OR picked_qty IS NULL
	    OR picking_status IS NULL
	    THEN 'NULL_VALUE'
	    WHEN requested_qty <= 0
	    OR picked_qty < 0
	    THEN 'INVALID_QUANTITY'
	    WHEN picking_status NOT IN ('FAILED', 'PARTIAL', 'COMPLETED', 'OVER_PICKED') THEN 'INVALID_STATUS'
	    WHEN (picked_qty = 0) AND (picking_status <> 'FAILED')
	    OR (picked_qty > 0) AND (requested_qty > picked_qty) AND (picking_status <> 'PARTIAL')
	    OR (requested_qty = picked_qty) AND (picking_status <> 'COMPLETED')
	    OR (requested_qty < picked_qty) AND (picking_status <> 'OVER_PICKED')
        THEN 'STATUS_QUANTITY_MISMATCH'
        ELSE NULL
    END AS rejection_reason
FROM bronze.wms_picking
)