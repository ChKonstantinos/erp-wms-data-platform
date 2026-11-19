import csv
from pathlib import Path

def export_to_csv(records, output_path):

    if not records:
        raise ValueError("Picking records list cannot be empty")

    output_path = Path(output_path)

    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, "w", newline="", encoding="utf-8") as f:

        writer = csv.DictWriter(
            f,
            fieldnames=records[0].keys()
        )

        writer.writeheader()
        writer.writerows(records)