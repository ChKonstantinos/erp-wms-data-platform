CREATE TABLE IF NOT EXISTS gold.pipeline_audit_log (
    pipeline_run_id UUID PRIMARY KEY,
    pipeline_name TEXT NOT NULL,
    started_at TIMESTAMP NOT NULL,
    finished_at TIMESTAMP,
    status TEXT NOT NULL
        CHECK (status IN ('RUNNING', 'SUCCESS', 'FAILED')),
    failed_step TEXT,
    error_message TEXT
);