CREATE TABLE IF NOT EXISTS bronze.wms_snapshot_registry (
    snapshot_id INTEGER PRIMARY KEY,
    snapshot_at TIMESTAMP NOT NULL,
    source_file TEXT NOT NULL,
    file_checksum VARCHAR(64) NOT NULL,
    registered_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);