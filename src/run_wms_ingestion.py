from src.db_connection import get_connection
from src.ingest_wms import (
    read_wms_csv,
    validate_picking_columns,
    insert_wms_picking,
    validate_stock_columns,
    insert_wms_stock
)
import json
from src.file_utils import calculate_file_checksum
from src.ingest_wms import register_stock_snapshot
from pathlib import Path


def read_stock_metadata(file_path):

    with open(file_path, "r", encoding="utf-8") as file:
        metadata = json.load(file)

    return metadata

def run_wms_ingestion():

    metadata = read_stock_metadata(
        "data/wms_exports/wms_stock_metadata.json"
    )

    records = read_wms_csv(
        "data/wms_exports/wms_picking.csv"
    )

    stock_records = read_wms_csv(
        "data/wms_exports/wms_stock.csv"
    )

    validate_picking_columns(records)
    validate_stock_columns(stock_records)

    checksum = calculate_file_checksum(
        "data/wms_exports/wms_stock.csv"
    )

    print(f"Stock file checksum: {checksum}")

    with get_connection() as conn:
        register_stock_snapshot(conn, metadata, checksum)
        insert_wms_picking(
            conn,
            records,
            "wms_picking.csv"
        )
        insert_wms_stock(
            conn,
            stock_records,
            metadata["snapshot_id"],
            metadata["snapshot_at"],
            metadata["source_file"]
        )

    print("Bronze ingestion completed")


if __name__ == "__main__":
    run_wms_ingestion()