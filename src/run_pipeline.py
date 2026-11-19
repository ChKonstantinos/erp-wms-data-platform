import logging
from src.run_silver_picking import run_silver_picking_pipeline
from src.run_silver_stock import run_silver_stock_pipeline
from src.run_wms_ingestion import run_wms_ingestion
from src.pipeline_audit import (
    start_pipeline_audit,
    finish_pipeline_audit
)
import uuid

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)



def run_pipeline():

    pipeline_run_id = str(uuid.uuid4())
    logger.info("Pipeline Run ID: %s", pipeline_run_id)

    current_step = "Initialization"

    try:
        start_pipeline_audit(
            pipeline_run_id,
            "ERP_WMS_PIPELINE"
        )

        current_step = "Bronze Ingestion"
        logger.info("Starting Bronze WMS Ingestion")
        run_wms_ingestion()

        current_step = "Silver Picking"
        logger.info("Starting Silver Picking")
        run_silver_picking_pipeline()

        current_step = "Silver Stock"
        logger.info("Starting Silver Stock")
        run_silver_stock_pipeline()

    except Exception as error:

        logger.exception(
            "ERP-WMS Pipeline FAILED at %s",
            current_step
        )

        if current_step != "Initialization":
            finish_pipeline_audit(
                pipeline_run_id,
                "FAILED",
                current_step,
                str(error)
            )

        raise

    else:
        finish_pipeline_audit(
            pipeline_run_id,
            "SUCCESS"
        )

        logger.info("ERP-WMS Pipeline completed")

    return pipeline_run_id

if __name__ == "__main__":
    run_pipeline()