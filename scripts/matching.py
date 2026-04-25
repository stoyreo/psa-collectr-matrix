"""Card Matching Engine"""
import re
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

def normalize_card_name(name: str) -> str:
    """Normalize card name for comparison."""
    if not name:
        return ""
    normalized = str(name).lower().strip()
    normalized = re.sub(r"[^\w\s-]", "", normalized)
    normalized = re.sub(r"\s+", " ", normalized).strip()
    return normalized

def normalize_set_code(set_name: str) -> str:
    """Extract canonical set code from full set name."""
    if not set_name:
        return ""
    set_lower = set_name.lower().strip()
    set_lower = set_lower.replace("pokemon", "").strip()
    set_lower = re.sub(r"(japanese|asian|english)", "", set_lower).strip()
    sv_match = re.search(r"(sv\d+[a-z]?)", set_lower)
    if sv_match:
        return sv_match.group(1)
    code_match = re.search(r"([a-z]+(?:-[a-z]+)?)", set_lower)
    if code_match:
        code = code_match.group(1)
        if "promo" in set_lower:
            if code == "promo":
                words = set_name.split()
                for i, word in enumerate(words):
                    if "promo" in word.lower() and i > 0:
                        prev_word = words[i - 1].lower()
                        if prev_word not in ["pokemon", "japanese", "asian", "english"]:
                            return f"{prev_word}-promo"
                return "unknown-promo"
            else:
                return f"{code}-promo"
        return code
    words = set_lower.split()
    if words:
        return words[0]
    return "unknown"

def generate_match_key(card: Dict[str, Any]) -> str:
    """Generate canonical match key for a card."""
    subject = normalize_card_name(card.get("subject", ""))
    set_code = normalize_set_code(card.get("set", ""))
    card_number = str(card.get("card_number", "")).strip().zfill(3)
    grade = str(card.get("grade", "")).lower().strip()
    variety = normalize_card_name(card.get("variety", "") or "")
    key_parts = [subject, set_code, card_number, f"psa{grade}"]
    if variety:
        key_parts.append(variety)
    match_key = "_".join(key_parts)
    match_key = re.sub(r"[^\w_-]", "", match_key)
    return match_key

def build_ebay_search_query(card: Dict[str, Any]) -> str:
    """Build optimal eBay search query string for a card."""
    subject = card.get("subject", "").strip()
    grade = card.get("grade", "").strip()
    set_code = normalize_set_code(card.get("set", ""))
    card_number = str(card.get("card_number", "")).strip()
    variety = (card.get("variety") or "").strip()
    query_parts = []
    if grade:
        query_parts.append(f"PSA {grade}")
    if subject:
        query_parts.append(subject)
    if set_code and set_code != "unknown":
        query_parts.append(set_code)
    if card_number:
        query_parts.append(f"#{card_number}")
    query_parts.append("japanese")
    if variety and variety.upper() not in ["-", "NONE"]:
        if "ART RARE" in variety.upper() or "SPECIAL ART" in variety.upper():
            query_parts.append(f'"{variety}')
    query = " ".join(query_parts)
    query = re.sub(r"\s+", " ", query).strip()
    return query

def compute_match_confidence(card: Dict[str, Any], comp: Dict[str, Any]) -> float:
    """Compute match confidence score (0-100) between a portfolio card and a comp."""
    score = 0.0
    portfolio_name = normalize_card_name(card.get("subject", ""))
    comp_title_lower = comp.get("title", "").lower()
    if portfolio_name and portfolio_name in comp_title_lower:
        score += 40
    elif portfolio_name:
        name_parts = portfolio_name.split()
        if name_parts and name_parts[0] in comp_title_lower:
            score += 25
    portfolio_set = normalize_set_code(card.get("set", ""))
    if portfolio_set and portfolio_set != "unknown":
        if portfolio_set in comp_title_lower:
            score += 25
        elif portfolio_set[:2] in comp_title_lower:
            score += 15
    portfolio_num = str(card.get("card_number", "")).strip()
    if portfolio_num:
        if portfolio_num in comp_title_lower or portfolio_num.zfill(3) in comp_title_lower:
            score += 20
    portfolio_grade = str(card.get("grade", "")).strip()
    comp_grade_confidence = comp.get("grade_confidence", 0)
    if comp_grade_confidence > 80:
        comp_grade_str = str(comp.get("grade", "")).strip()
        if portfolio_grade and comp_grade_str == portfolio_grade:
            score += 15
        elif portfolio_grade and comp_grade_str:
            try:
                if abs(int(portfolio_grade) - int(comp_grade_str)) <= 1:
                    score += 8
            except ValueError:
                pass
    else:
        if "psa" in comp_title_lower and portfolio_grade:
            if f"psa {portfolio_grade}" in comp_title_lower or f"{portfolio_grade}" in comp_title_lower:
                score += 10
            else:
                score += 3
    if "japanese" in comp_title_lower:
        score += 5
    else:
        score = max(0, score - 5)
    return min(100.0, score)

def classify_match(confidence: float) -> str:
    """Classify match based on confidence score."""
    if confidence >= 90:
        return "EXACT"
    elif confidence >= 85:
        return "STRONG"
    elif confidence >= 70:
        return "MODERATE"
    elif confidence >= 50:
        return "WEAK"
    else:
        return "REJECT"
