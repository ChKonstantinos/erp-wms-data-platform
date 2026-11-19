import sys
import os
from datetime import datetime

from airflow.sdk import dag, task
from airflow.sdk import get_current_context

PROJECT_PATH = "/opt/airflow/erp-wms-data-platform"

if PROJECT_PATH not in sys.path:
    sys.path.insert(0, PROJECT_PATH)

def finalize_pipeline_audit(context):

    from src.pipeline_audit import finish_pipeline_audit

    dag_run = context["dag_run"]

    import uuid

    pipeline_run_id = str(
        uuid.uuid5(
            uuid.NAMESPACE_URL,
            f"{dag_run.dag_id}:{dag_run.run_id}"
        )
    )

    if dag_run.state == "success":
        status = "SUCCESS"
        failed_step = None
        error_message = None
    else:
        status = "FAILED"
        failed_step = "AIRFLOW_DAG"
        error_message = f"Airflow DAG Run state: {dag_run.state}"

    finish_pipeline_audit(
        pipeline_run_id,
        status,
        failed_step,
        error_message
    )


@dag(
    dag_id="erp_wms_data_platform",
    start_date=datetime(2026, 11, 1),
    schedule=None,
    catchup=False,
    max_active_runs=1,
    on_success_callback = finalize_pipeline_audit,
    on_failure_callback = finalize_pipeline_audit,
    tags=["erp", "wms", "data-engineering"]
)
def erp_wms_data_platform():

    @task
    def start_audit():
        import uuid
        from src.pipeline_audit import start_pipeline_audit

        context = get_current_context()

        pipeline_run_id = str(
            uuid.uuid5(
                uuid.NAMESPACE_URL,
                f"{context['dag'].dag_id}:{context['run_id']}"
            )
        )

        start_pipeline_audit(
            pipeline_run_id,
            "ERP_WMS_PIPELINE"
        )

        return pipeline_run_id

    @task
    def bronze_ingestion(pipeline_run_id):
        os.chdir(PROJECT_PATH)

        from src.run_wms_ingestion import run_wms_ingestion

        run_wms_ingestion()

        print(
            f"Bronze ingestion completed. "
            f"Pipeline Run ID: {pipeline_run_id}"
        )

    @task
    def silver_picking(pipeline_run_id):
        os.chdir(PROJECT_PATH)

        from src.run_silver_picking import run_silver_picking_pipeline

        run_silver_picking_pipeline()

        print(
            f"Silver Picking completed. "
            f"Pipeline Run ID: {pipeline_run_id}"
        )

    @task
    def silver_stock(pipeline_run_id):
        os.chdir(PROJECT_PATH)

        from src.run_silver_stock import run_silver_stock_pipeline

        run_silver_stock_pipeline()

        print(
            f"Silver Stock completed. "
            f"Pipeline Run ID: {pipeline_run_id}"
        )

    @task
    def dbt_build(pipeline_run_id):
        import subprocess

        dbt_project_path = f"{PROJECT_PATH}/erp_wms_dbt"

        command = [
            "dbt",
            "build",
            "--project-dir", dbt_project_path,
            "--profiles-dir", f"{dbt_project_path}/docker_profile",
            "--select", "order_fulfillment_summary", "inventory_summary"
        ]

        env = os.environ.copy()
        env["DBT_LOG_PATH"] = "/tmp/dbt_logs"
        env["DBT_TARGET_PATH"] = "/tmp/dbt_target"

        subprocess.run(
            command,
            env=env,
            check=True
        )

        print(
            f"dbt build completed. "
            f"Pipeline Run ID: {pipeline_run_id}"
        )


    run_id = start_audit()

    bronze = bronze_ingestion(run_id)
    picking = silver_picking(run_id)
    stock = silver_stock(run_id)
    dbt = dbt_build(run_id)

    bronze >> picking >> stock >> dbt


erp_wms_data_platform()