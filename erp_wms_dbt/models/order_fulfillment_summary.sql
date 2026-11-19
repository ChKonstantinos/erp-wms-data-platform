{{
    config(
        materialized='table',
        post_hook=[
            "ALTER TABLE {{ this }} ADD PRIMARY KEY (order_id)",
            "ALTER TABLE {{ this }} ALTER COLUMN total_ordered_qty SET NOT NULL",
            "ALTER TABLE {{ this }} ALTER COLUMN total_picked_qty SET NOT NULL",
            "ALTER TABLE {{ this }} ALTER COLUMN total_shortage_qty SET NOT NULL",
            "ALTER TABLE {{ this }} ALTER COLUMN total_overpicked_qty SET NOT NULL"
        ]
    )
}}

SELECT
    order_id,
    SUM(ordered_qty) AS total_ordered_qty,
    CAST(SUM(picked_qty) AS BIGINT) AS total_picked_qty,
    CAST(SUM(shortage_qty) AS BIGINT) AS total_shortage_qty,
    CAST(SUM(overpicked_qty) AS BIGINT) AS total_overpicked_qty,

    ROUND(
        100.0 * SUM(LEAST(picked_qty, ordered_qty))
        / NULLIF(SUM(ordered_qty), 0),
        2
    ) AS fulfillment_pct

FROM {{ source('silver', 'v_order_fulfillment') }}

GROUP BY order_id