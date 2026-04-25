"""Diff CSV against master and append new/changed rows."""
from __future__ import annotations

import csv
import hashlib
import logging
from pathlib import Path

from master_workbook import ensure_master_exists, append_card, list_cards, append_sync_log

logger = logging.getLogger(__name__)

PROJECT_ROOT = Path(__file__).parent.parent
CSV_GLOB = "My Collection CSV - *.csv"


def _row_hash(row: dict) -> str:
    """Stable hash of (cert, grade, cost, date_acquired) for change detection."""
    key = f"{row.get('Cert Number', '')}|{row.get('Grade', '')}|{row.get('My Cost', '')}|{row.get('Date Acquired', '')}"
    return hashlib.sha1(key.encode()).hexdigest()[:12]


def run() -> dict:
    """Find latest CSV, sync into master. Returns {'added': N, 'updated': N, 'skipped': N}."""

    # Ensure master exists
    ensure_master_exists()

    # Find latest CSV
    csv_files = sorted(PROJECT_ROOT.glob(CSV_GLOB))
    if not csv_files:
        logger.warning("No CSV files found matching pattern")
        return {"added": 0, "updated": 0, "skipped": 0}

    csv_path = csv_files[-1]
    logger.info(f"Syncing CSV: {csv_path.name}")

    # Load existing master cards and build hash map
    existing_cards = list_cards()
    existing_hashes = {}
    existing_certs = {}
    for card in existing_cards:
        if card.get("Cert Number"):
            cert = str(card.get("Cert Number"))
            h = _row_hash(card)
            existing_hashes[h] = cert
            existing_certs[cert] = card

    # Read CSV and sync
    added_count = 0
    updated_count = 0
    skipped_count = 0

    with open(csv_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for csv_row in reader:
            if not csv_row.get("Cert Number"):
                skipped_count += 1
                continue

            cert = str(csv_row.get("Cert Number"))
            current_hash = _row_hash(csv_row)

            # Check if this is a new row
            if current_hash not in existing_hashes:
                # Check if cert exists but has different grade/cost/date
                if cert in existing_certs:
                    # Card exists but differs — log as updated
                    append_sync_log("csv", cert, "updated", f"From {csv_path.name}")
                    updated_count += 1
                else:
                    # Entirely new card
                    append_card(csv_row, source="csv")
                    added_count += 1
            else:
                # Row already in master
                skipped_count += 1

    logger.info(f"CSV sync complete: {added_count} added, {updated_count} updated, {skipped_count} skipped")
    return {"added": added_count, "updated": updated_count, "skipped": skipped_count}


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    result = run()
    print(result)
