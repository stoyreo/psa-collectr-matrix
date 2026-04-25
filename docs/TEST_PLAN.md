# Pokémon TCG Portfolio Intelligence System - Test Plan

## Overview

Comprehensive test cases for all system components with clear pass/fail criteria. Tests use existing portfolio of 19 Japanese cards.

---

## Test Philosophy

- **Deterministic:** Same input = same output always
- **Automated:** Scripts verify themselves
- **Comprehensive:** Happy path, edge cases, error conditions
- **Traceable:** Each test links to specific code
- **Realistic:** Use actual portfolio data where possible

---

## Component Tests

### Test 1: CSV Ingest (ingest.py)

**1.1 Happy Path:** Parse valid PSA CSV with 19 cards
- ✓ Returns list of exactly 19 dicts
- ✓ Each dict has: subject, grade, set, card_number, cert_number
- ✓ All values normalized (strings or None)
- ✓ No exceptions raised

**1.2 Missing File:**
- ✓ Raises FileNotFoundError (not silent)
- ✓ Error message includes path

**1.3 Normalization - Whitespace:**
- ✓ "  SLOWPOKE  " → "slowpoke" (lowercase, stripped)
- ✓ Extra spaces removed
- ✓ Card numbers become numeric

**1.4 Null Values:**
- ✓ "-", "N/A", "null" → None
- ✓ Not empty strings
- ✓ Downstream handles None correctly

**1.5 Field Order Independence:**
- ✓ Columns in any order map correctly
- ✓ No positional errors
- ✓ DictReader handles matching

**1.6 Missing Required Column:**
- ✓ Either raises ValueError or skips gracefully
- ✓ Error logged with row number

### Test 2: Matching Engine (matching.py)

**2.1 Match Key Deterministic:**
```python
card1 = {"subject": "SLOWPOKE", "grade": "8", ...}
card2 = {"subject": "  slowpoke  ", "grade": "8", ...}
key1 = generate_match_key(card1)
key2 = generate_match_key(card2)
assert key1 == key2  # "slowpoke_sv1v_082_psa8_artare"
```

**2.2 Set Code Normalization:**
- ✓ "POKEMON JAPANESE SV1V-VIOLET ex" → "sv1v"
- ✓ "POKEMON JAPANESE S PROMO" → "s-promo"
- ✓ "POKEMON JAPANESE TOPSUN" → "topsun"

**2.3 eBay Search Query:**
- ✓ Contains "PSA 8", "SLOWPOKE", "SV1V", "082", "JAPANESE"
- ✓ < 100 chars
- ✓ Variety appended if distinctive

**2.4 Confidence Scoring - Exact Match:**
- ✓ Perfect match scores 90-100 (EXACT band)

**2.5 Confidence - Grade Mismatch:**
- ✓ Same grade scores higher than different grade
- ✓ Score still in acceptable range

**2.6 Confidence - Subject Mismatch:**
- ✓ Wrong card (PIKACHU vs SLOWPOKE): confidence < 50 (REJECT)

### Test 3: eBay Connector (ebay_connector.py)

**3.1 Demo Mode - Generation:**
- ✓ Returns 12 comps per query
- ✓ Each has: title, sold_date, sold_price, shipping, total_price, currency
- ✓ Prices > 0
- ✓ total_price = sold_price + shipping (within rounding)

**3.2 Demo Mode - Variance:**
- ✓ Prices within ±15% of base
- ✓ Normal distribution
- ✓ No outliers > 2 std devs

**3.3 Filtering - Bundles:**
- ✓ Comps with "lot", "bundle", "x2", "playset" removed
- ✓ Only singles remain

**3.4 Filtering - Fakes:**
- ✓ "fake", "custom", "reproduction" removed

**3.5 Outlier Detection - IQR:**
- ✓ Price > Q3 + 1.5×IQR flagged
- ✓ Price < Q1 - 1.5×IQR flagged
- ✓ Normal range not flagged

**3.6 Stats Computation:**
```python
comps = [{30}, {32}, {31}, {33}, {32}]
stats = compute_ebay_stats(comps)
assert stats["min"] == 30
assert stats["median"] == 32
assert stats["max"] == 33
```

### Test 4: Signals Engine (signals.py)

**4.1 Signal - BUY:**
- ✓ market_value > cost × 1.15 AND liquidity ≥ MEDIUM AND confidence ≥ 85 → BUY
- ✓ risk_level == LOW

**4.2 Signal - SELL:**
- ✓ market_value < cost × 0.85 → SELL
- ✓ risk_level == HIGH

**4.3 Signal - REVIEW:**
- ✓ confidence < 80 → REVIEW
- ✓ Missing cost/market_value → REVIEW

**4.4 Signal - HOLD:**
- ✓ Default for mid-range positions
- ✓ Explains illiquidity, stability, or mixed signals

**4.5 Liquidity - HIGH:**
- ✓ 8+ comps → HIGH, score ≥ 80

**4.6 Liquidity - LOW:**
- ✓ 0-3 comps → LOW, score ≤ 50

**4.7 Trend - UP:**
- ✓ Recent median > old median by > 10% → UP

**4.8 Trend - DOWN:**
- ✓ Recent median < old median by > 10% → DOWN

### Test 5: Excel Writer (excel_writer.py)

**5.1 Excel Generation - Valid File:**
- ✓ File created and readable
- ✓ Valid .xlsx format
- ✓ No exceptions when opening

**5.2 Excel Sheets - All 10 Present:**
- ✓ DASHBOARD, PORTFOLIO, EBAY_COMPS, COLLECTR_MAP, PSA_MAP
- ✓ INSIGHTS, EXCEPTIONS, TARGETS, ALERT_LOG, CONFIG

**5.3 Excel - PORTFOLIO Row Count:**
- ✓ 1 header + 19 data rows = 20 total

**5.4 Excel - Signal Color Coding:**
- ✓ BUY = GREEN, SELL = RED, HOLD = BLUE, REVIEW = ORANGE

**5.5 Excel - P&L Calculation:**
- ✓ P&L % = (MV - Cost) / Cost × 100 (within 0.01% rounding)

**5.6 Excel - DASHBOARD KPIs:**
- ✓ total_cards == 19
- ✓ total_cost == $5,979
- ✓ total_market_value ≈ $2,052
- ✓ total_pnl == MV - Cost

### Test 6: Cache Manager (cache_manager.py)

**6.1 Cache - Store & Retrieve:**
- ✓ Comps stored and retrieved identically

**6.2 Cache - Age Expiration:**
- ✓ Comps > 24h old not returned
- ✓ Fresh comps returned

**6.3 Cache - Disabled Cache:**
- ✓ When disabled, comps not cached

### Test 7: Full Refresh (refresh.py)

**7.1 Full Refresh - End-to-End:**
- ✓ Result status == "success"
- ✓ 19 cards in portfolio
- ✓ All have match_key, confidence, signal
- ✓ No exceptions
- ✓ Summary.card_count == 19

**7.2 Full Refresh - Signal Distribution:**
- ✓ 7 BUY, 2 HOLD, 9 SELL, 1 REVIEW (as expected)
- ✓ Total == 19

**7.3 Full Refresh - Portfolio Totals:**
- ✓ Manual sum == reported total_cost
- ✓ Manual sum == reported total_market_value
- ✓ P&L % formula correct

**7.4 Full Refresh - Performance:**
- ✓ Completes in < 60 seconds (target: < 30s)

**7.5 Full Refresh - Logging:**
- ✓ Log file created
- ✓ Contains step names ([1/7], [2/7], etc.)
- ✓ No ERROR level messages (exceptions logged & caught)

---

## Integration Tests

**INT-1 CSV to Excel:**
- ✓ Excel created, valid, 10 sheets
- ✓ PORTFOLIO: 19 cards
- ✓ DASHBOARD: summary stats
- ✓ All signals assigned, no NULLs

**INT-2 Demo vs. Live Mode Toggle:**
- ✓ Both run without errors
- ✓ Demo comps marked "is_sample": True
- ✓ Signals may differ (different prices)

**INT-3 Consistency Across Runs:**
- ✓ Two runs with same data produce identical output
- ✓ Deterministic (only timestamp differs)

---

## Data Integrity Tests

**DI-1 Cost > Market Value (Underwater):**
- ✓ 17 cards underwater correctly identified
- ✓ P&L negative, signal likely SELL

**DI-2 No Negative Values:**
- ✓ cost ≥ 0, market_value ≥ 0, prices > 0
- ✓ All fields within valid range

**DI-3 Confidence Range 0-100:**
- ✓ All scores in valid range
- ✓ No NaN, NULL, or invalid values

---

## Error Handling Tests

**EH-1 Missing CSV:**
- ✓ Status == "error"
- ✓ Exceptions list contains error message
- ✓ No unhandled exception

**EH-2 Malformed CSV:**
- ✓ Skips malformed rows or errors gracefully
- ✓ Continues processing valid rows

**EH-3 Permission Denied (Cache):**
- ✓ Detects permission error
- ✓ Continues without caching
- ✓ Logs warning, completes successfully

---

## Edge Case Tests

**EC-1 Card with $0 Cost:**
- ✓ No division errors
- ✓ upside_pct handled safely

**EC-2 Identical Comp Prices:**
- ✓ Liquidity computed correctly
- ✓ Trend == STABLE (no price movement)

**EC-3 Single Comp:**
- ✓ Liquidity == LOW
- ✓ Trend == INSUFFICIENT_DATA (need 4+)

**EC-4 Very Old Comps (> 90 days):**
- ✓ Liquidity score reduced
- ✓ Signal may be REVIEW (stale)

---

## QA Checklist Before Production

- [ ] All component tests pass
- [ ] All integration tests pass
- [ ] All edge case tests pass
- [ ] Error handling demonstrates graceful failure
- [ ] Manual spot-check of 3 random cards
- [ ] Excel opens without corruption
- [ ] Signal allocation matches expectations
- [ ] Portfolio totals verified manually
- [ ] Performance acceptable (< 60s)
- [ ] Log file clean (no ERROR messages)
- [ ] Cache working as expected
- [ ] Documentation updated
- [ ] Deployment instructions reviewed

---

**Test Plan Version:** 1.0  
**Audience:** QA Engineers, Developers, System Administrators
