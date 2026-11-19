import csv
from pathlib import Path
from datetime import datetime

from src.db_connection import get_connection


def read_wms_csv(file_path):

    file_path = Path(file_path)

    with file_path.open("r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        records = list(reader)

    return records

def insert_wms_picking(conn, records, source_file):

    sql = """
            INSERT INTO bronze.wms_picking (
                picking_id,
                order_line_id,
                warehouse_id,
                product_id,
                requested_qty,
                picked_qty,
                picking_status,
                source_file
            )
            VALUES (
                %(picking_id)s,
                %(order_line_id)s,
                %(warehouse_id)s,
                %(product_id)s,
                %(requested_qty)s,
                %(picked_qty)s,
                %(picking_status)s,
                %(source_file)s
            )
            ON CONFLICT (picking_id) DO NOTHING;
    """

    rows = [
        {**record, "source_file": source_file}
        for record in records
    ]

    with conn.cursor() as cursor:
        cursor.executemany(sql, rows)

def validate_picking_columns(records):

    required_columns = {
        "picking_id",
        "order_line_id",
        "warehouse_id",
        "product_id",
        "requested_qty",
        "picked_qty",
        "picking_status"
    }

    if not records:
        raise ValueError("No records to ingest")

    actual_columns = set(records[0].keys())

    missing_columns = required_columns - actual_columns

    if missing_columns:
        raise ValueError(
            f"Missing required columns: {missing_columns}"
        )

def insert_wms_stock(conn, records, snapshot_id, snapshot_at, source_file):

    sql = """
            INSERT INTO bronze.wms_stock (
                snapshot_id,
                warehouse_id,
                product_id,
                available_qty,
                snapshot_at,
                source_file
            )
            VALUES (
                %(snapshot_id)s,
                %(warehouse_id)s,
                %(product_id)s,
                %(available_qty)s,
                %(snapshot_at)s,
                %(source_file)s
            )
            ON CONFLICT (snapshot_id, warehouse_id, product_id) DO NOTHING;
    """

    rows = [
        {**record, "source_file": source_file, "snapshot_id" : snapshot_id, "snapshot_at" : snapshot_at}
        for record in records
    ]

    with conn.cursor() as cursor:
        cursor.executemany(sql, rows)

def validate_stock_columns(records):

    required_columns = {
        "warehouse_id",
        "product_id",
        "available_qty",
    }

    if not records:
        raise ValueError("No records to ingest")

    actual_columns = set(records[0].keys())

    missing_columns = required_columns - actual_columns

    if missing_columns:
        raise ValueError(
            f"Missing required columns: {missing_columns}"
        )

def register_stock_snapshot(conn, metadata, checksum):

    with conn.cursor() as cursor:

        cursor.execute("""
            SELECT snapshot_at, source_file, file_checksum
            FROM bronze.wms_snapshot_registry
            WHERE snapshot_id = %s
        """, (metadata["snapshot_id"],))

        existing = cursor.fetchone()

        if existing is not None:

            existing_at, existing_file, existing_checksum = existing

            if (
                existing_at != datetime.fromisoformat(metadata["snapshot_at"])
                or existing_file != metadata["source_file"]
                or existing_checksum != checksum
            ):
                raise ValueError(
                    f"Snapshot {metadata['snapshot_id']} "
                    "already exists with different metadata or content"
                )

            return

        cursor.execute("""
            INSERT INTO bronze.wms_snapshot_registry
                (snapshot_id, snapshot_at, source_file, file_checksum)
            VALUES (%s, %s, %s, %s)
        """, (
            metadata["snapshot_id"],
            metadata["snapshot_at"],
            metadata["source_file"],
            checksum
        ))
