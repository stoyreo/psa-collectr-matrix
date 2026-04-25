"""PSA Connector"""
import logging
from typing import Dict, Any, List
from pathlib import Path

logger = logging.getLogger(__name__)

def parse_psa_csv(filepath: Path) -> List[Dict[str, Any]]:
    """Parse PSA collection export CSV."""
    from ingest import ingest_collection
    return ingest_collection(filepath)

def map_psa_to_portfolio(psa_cards: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Map PSA card data to portfolio format."""
    portfolio_cards = []
    for card in psa_cards:
        if card.get("grade_issuer") != "PSA":
            logger.warning(f"Skipping non-PSA card: {card.get('subject')}")
            continue
        portfolio_card = {
            "subject": card.get("subject"),
            "grade": card.get("grade"),
            "set": card.get("set"),
            "card_number": card.get("card_number"),
            "variety": card.get("variety"),
            "year": card.get("year"),
            "cert_number": card.get("cert_number"),
            "cert_issuer": card.get("grade_issuer"),
            "my_cost": card.get("my_cost"),
            "psa_estimate": card.get("psa_estimate"),
            "date_acquired": card.get("date_acquired"),
            "source": card.get("source"),
            "notes": card.get("my_notes"),
        }
        portfolio_cards.append(portfolio_card)
    logger.info(f"Mapped {len(portfolio_cards)} PSA cards to portfolio format")
    return portfolio_cards

def lookup_psa_cert(cert_number: str) -> Dict[str, Any]:
    """Look up PSA cert details (stub)."""
    logger.debug(f"PSA cert lookup requested for: {cert_number}")
    return {"cert_number": cert_number, "status": "unavailable", "note": "PSA cert API not available in sandbox"}

def verify_psa_certs(cards: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Verify PSA certs for all cards."""
    for card in cards:
        cert_num = card.get("cert_number")
        if cert_num:
            cert_data = lookup_psa_cert(cert_num)
            if cert_data.get("status") == "unavailable":
                card["cert_verified"] = False
                card["cert_note"] = "PSA cert API not available"
            else:
                card["cert_verified"] = True
                card["cert_data"] = cert_data
        else:
            card["cert_verified"] = False
            card["cert_note"] = "No cert number"
    return cards

def get_psa_map(cards: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Build PSA mapping data for export."""
    psa_map = []
    for card in cards:
        psa_entry = {
            "subject": card.get("subject"),
            "cert_number": card.get("cert_number"),
            "grade": card.get("grade"),
            "set": card.get("set"),
            "card_number": card.get("card_number"),
            "variety": card.get("variety"),
            "year": card.get("year"),
            "status": "Active",
        }
        psa_map.append(psa_entry)
    return psa_map

if __name__ == "__main__":
    print("psa_connector module loaded")
