from src.db_connection import get_connection


def start_pipeline_audit(pipeline_run_id, pipeline_name):

    sql = """
        INSERT INTO gold.pipeline_audit_log (
        pipeline_run_id,
        pipeline_name,
        started_at,
        status
    )
    VALUES (
        %s,
        %s,
        CURRENT_TIMESTAMP,
        'RUNNING'
    )
    ON CONFLICT (pipeline_run_id)
    DO UPDATE SET
        started_at = CURRENT_TIMESTAMP,
        finished_at = NULL,
        status = 'RUNNING',
        failed_step = NULL,
        error_message = NULL;
    """

    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(sql, (pipeline_run_id, pipeline_name))

def finish_pipeline_audit(
    pipeline_run_id,
    status,
    failed_step=None,
    error_message=None
):

    sql = """
        UPDATE gold.pipeline_audit_log
        SET
            finished_at = CURRENT_TIMESTAMP,
            status = %s,
            failed_step = %s,
            error_message = %s
        WHERE pipeline_run_id = %s;
    """

    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(sql, (status, failed_step, error_message, pipeline_run_id))
