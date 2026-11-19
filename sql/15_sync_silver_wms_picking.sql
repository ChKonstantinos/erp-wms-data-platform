CREATE TEMP TABLE tmp_validated_picking
ON COMMIT DROP
AS
SELECT
    picking_id,
    order_line_id,
    warehouse_id,
    product_id,
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
FROM bronze.wms_picking;

INSERT INTO silver.wms_picking_valid (
    picking_id,
    order_line_id,
    warehouse_id,
    product_id,
    requested_qty,
    picked_qty,
    picking_status
)
SELECT
    picking_id,
    order_line_id,
    warehouse_id,
    product_id,
    requested_qty,
    picked_qty,
    picking_status
FROM tmp_validated_picking
WHERE dq_status = 'VALID'
ON CONFLICT (picking_id)
DO UPDATE SET
    order_line_id = EXCLUDED.order_line_id,
    warehouse_id = EXCLUDED.warehouse_id,
    product_id = EXCLUDED.product_id,
    requested_qty = EXCLUDED.requested_qty,
    picked_qty = EXCLUDED.picked_qty,
    picking_status = EXCLUDED.picking_status;

DELETE FROM silver.wms_picking_valid AS s
USING tmp_validated_picking AS t
WHERE
    s.picking_id = t.picking_id
    AND t.dq_status = 'REJECTED';

DELETE FROM silver.wms_picking_rejected;

INSERT INTO silver.wms_picking_rejected (
    picking_id,
    order_line_id,
    warehouse_id,
    product_id,
    requested_qty,
    picked_qty,
    picking_status,
    rejection_reason
)
SELECT
    picking_id,
    order_line_id,
    warehouse_id,
    product_id,
    requested_qty,
    picked_qty,
    picking_status,
    rejection_reason
FROM tmp_validated_picking
WHERE dq_status = 'REJECTED';

WITH counts AS (
    SELECT
        (SELECT COUNT(*) FROM tmp_validated_picking) AS bronze_count,
        (SELECT COUNT(*) FROM tmp_validated_picking
         WHERE dq_status = 'VALID') AS expected_valid,
        (SELECT COUNT(*) FROM tmp_validated_picking
         WHERE dq_status = 'REJECTED') AS expected_rejected,
        (SELECT COUNT(*) FROM silver.wms_picking_valid) AS actual_valid,
        (SELECT COUNT(*) FROM silver.wms_picking_rejected) AS actual_rejected
)
SELECT
    *,
    CASE
        WHEN bronze_count = expected_valid + expected_rejected
         AND expected_valid = actual_valid
         AND expected_rejected = actual_rejected
        THEN 'SUCCESS'
        ELSE 'FAILED'
    END AS reconciliation_status
FROM counts;
