CREATE OR REPLACE VIEW gold.v_pipeline_monitoring AS

SELECT
    pipeline_name,

    COUNT(*) FILTER (
        WHERE status IN ('SUCCESS', 'FAILED')
    ) AS total_completed_runs,

    COUNT(*) FILTER (
        WHERE status = 'SUCCESS'
    ) AS successful_runs,

    COUNT(*) FILTER (
        WHERE status = 'FAILED'
    ) AS failed_runs,

    COUNT(*) FILTER (
        WHERE status = 'RUNNING'
    ) AS running_runs,

    ROUND(
        COUNT(*) FILTER (
            WHERE status = 'SUCCESS'
        ) * 100.0 /
        NULLIF(
            COUNT(*) FILTER (
                WHERE status IN ('SUCCESS', 'FAILED')
            ), 0
        ),
        2
    ) AS success_rate_pct,

    ROUND(
        AVG(
            EXTRACT(
                EPOCH FROM (finished_at - started_at)
            )
        ) FILTER (
            WHERE status IN ('SUCCESS', 'FAILED')
              AND finished_at IS NOT NULL
        ),
        2
    ) AS avg_duration_seconds

FROM gold.pipeline_audit_log

GROUP BY pipeline_name;