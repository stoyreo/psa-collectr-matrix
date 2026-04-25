"""CSV Ingestion Module"""
import csv
import logging
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any

from config import NORMALIZATION

logger = logging.getLogger(__name__)

def normalize_value(value):
    if value is None or value == "":
        return None
    value_str = str(value).strip()
    if value_str in NORMALIZATION["null_values"]:
        return None
    return value_str

def parse_csv(csv_path):
    if not csv_path.exists():
        raise FileNotFoundError(f"CSV file not found: {csv_path}")
    cards = []
    with open(csv_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        reader.fieldnames = [col.strip() for col in reader.fieldnames]
        for row_num, row in enumerate(reader, start=2):
            try:
                nr = {k.strip(): normalize_value(v) for k, v in row.items()}
                card = {
                    "item_status":    nr.get("Item Status"),
                    "item":           nr.get("Item"),
                    "cert_number":    nr.get("Cert Number"),
                    "grade_issuer":   nr.get("Grade Issuer"),
                    "grade":          nr.get("Grade"),
                    "year":           nr.get("Year"),
                    "set":            nr.get("Set"),
                    "card_number":    nr.get("Card Number"),
                    "subject":        nr.get("Subject"),
                    "variety":        nr.get("Variety"),
                    "serial":         nr.get("Serial"),
                    "category":       nr.get("Category"),
                    "my_cost":        None,
                    "psa_estimate":   None,
                    "gain_loss":      None,
                    "my_value":       None,
                    "date_acquired":  None,
                    "source":         nr.get("Source"),
                    "my_notes":       nr.get("My Notes"),
                    "vault_status":   nr.get("Vault Status"),
                    "vaulted_date":   None,
                    "days_vaulted":   nr.get("Days Vaulted"),
                    "listing_status": nr.get("Listing Status"),
                    "listing_date":   None,
                    "listing_price":  None,
                    "sold_status":    nr.get("Sold Status"),
                    "sold_on":        nr.get("Sold On"),
                    "sold_date":      None,
                    "sold_price":     None,
                    "sold_fees":      None,
                    "sold_proceeds":  None,
                    "payment_date":   None,
                }
                # Explicit mapping — .title() breaks "PSA Estimate" -> "Psa Estimate"
                numeric_map = {
                    "my_cost":       "My Cost",
                    "psa_estimate":  "PSA Estimate",
                    "gain_loss":     "Gain/Loss",
                    "my_value":      "My Value",
                    "listing_price": "Listing Price",
                    "sold_price":    "Sold Price",
                    "sold_fees":     "Sold Fees",
                    "sold_proceeds": "Sold Proceeds",
                }
                for field, col in numeric_map.items():
                    try:
                        val = nr.get(col)
                        if val:
                            card[field] = float(val)
                    except (ValueError, TypeError):
                        pass
                date_map = {
                    "date_acquired": "Date Acquired",
                    "vaulted_date":  "Vaulted Date",
                    "listing_date":  "Listing Date",
                    "sold_date":     "Sold Date",
                    "payment_date":  "Payment Date",
                }
                for fk, fn in date_map.items():
                    try:
                        if nr.get(fn):
                            card[fk] = datetime.strptime(nr[fn], NORMALIZATION["date_format"]).date()
                    except (ValueError, TypeError):
                        pass
                if card["grade"]:
                    card["grade"] = str(card["grade"]).strip()
                cards.append(card)
            except Exception as e:
                logger.error(f"Row {row_num}: Failed to parse - {e}")
                raise
    logger.info(f"Successfully ingested {len(cards)} cards from {csv_path.name}")
    return cards

def ingest_collection(csv_path):
    return parse_csv(csv_path)

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG, format="[%(levelname)s] %(message)s")
    cards = ingest_collection(Path(__file__).parent.parent / "My Collection CSV - 19.csv")
    for c in cards[:5]:
        print(f"  {c['subject']:25s}  cost={c['my_cost']}  psa_est={c['psa_estimate']}")
