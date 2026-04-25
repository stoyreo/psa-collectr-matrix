# Pokémon TCG Portfolio Intelligence System - Operational Prompts

Four reusable prompts for Claude to assist with system operations. Each is designed for a specific task.

---

## PROMPT 1: OPUS BUILD & ARCHITECTURE

**Use case:** Initial construction, major architectural changes, connector implementation, schema redesign

**Cost:** High (~5,000-10,000 tokens)  
**Frequency:** Infrequent (setup, quarterly reviews)  
**Model:** Claude Opus (preferred)

You are architecting a Pokémon TCG portfolio management system for Japanese graded cards. Core requirements: ingest 19 PSA cards from CSV, fetch eBay market comps, compute match confidence (0-100%), generate investment signals (BUY/HOLD/SELL/REVIEW), export premium Excel workbook (10 sheets).

**System context:**
- 19 Japanese PSA-graded cards
- Cost basis: $5,979, Market value: ~$2,052 (underwater)
- DEMO mode: sample comps (±15% around PSA estimates)
- Signal distribution: 7 BUY, 2 HOLD, 9 SELL, 1 REVIEW
- Five-layer architecture: Excel → Data Engine → Connectors → Processing → Config

**Deliverables:**
- Production-ready code
- Updated documentation
- Test cases for edge cases
- Deployment instructions

---

## PROMPT 2: HAIKU DAILY OPERATIONS

**Use case:** Routine portfolio refresh, daily operations

**Cost:** Very low (~5,000 tokens per run)  
**Frequency:** Daily or on-demand  
**Model:** Claude Haiku

Execute complete portfolio refresh: (1) Parse CSV, (2) Generate match keys, (3) Fetch/generate comps, (4) Cache decision, (5) Compute confidence, (6) Compute signals, (7) Generate insights.

**Output format (JSON):**
```json
{
  "status": "success",
  "portfolio": [19 card dicts with signals],
  "insights": {top_undervalued, top_gainers, weak_positions, liquidity_summary, signal_allocation},
  "summary": {card_count, total_cost, total_market_value, total_pnl, pnl_pct},
  "exceptions": [],
  "timestamp": "ISO"
}
```

**Quality checks:**
- All 19 cards present
- Market value ≥ 0
- Confidence 0-100
- P&L % = (MV - Cost) / Cost × 100
- No duplicate match keys
- All comps have sold_price > 0

**Time target:** < 30 seconds

---

## PROMPT 3: HAIKU REVIEW

**Use case:** Manual review of ambiguous matches, low-confidence decisions

**Cost:** Low (~2,000 tokens per batch)  
**Frequency:** As needed (< 5% of cards)  
**Model:** Claude Haiku

Review card match decisions. For each card:
- Accept (confidence ≥ 85): All 5 fields match exactly
- Moderate (70-84): 4 of 5 match, 1 has minor variance
- Weak (50-69): 3 of 5 match, 2+ variance
- Reject (< 50): Subject/set/grade wildly off

**Edge cases to handle:**
1. Variety ambiguity (ART RARE vs SPECIAL ART)
2. Grade confusion (PSA 8 vs 9, grade_tolerance check)
3. Language issues (JAPANESE vs JAP vs missing marker)
4. Duplicate comps (same title/price/date)

**Output format:**
```json
{
  "card_subject": "SLOWPOKE",
  "decision": "ACCEPT",
  "confidence": 85,
  "accepted_comps": [1, 3, 4],
  "rejected_comps": [2],
  "flagged_comps": [5],
  "reasoning": "Specific field comparisons",
  "market_value": 33.50,
  "escalate": false
}
```

---

## PROMPT 4: OPUS ESCALATION

**Use case:** Broken connectors, mass mismatches, schema failures, production troubleshooting

**Cost:** High (~5,000-15,000 tokens)  
**Frequency:** 1-2x per quarter  
**Model:** Claude Opus

**Escalation trigger:** Choose one:
- eBay Connector Failure: No comps for X% of cards
- Mass Match Failure: Confidence < 70 for > 30%
- CSV Parsing Error: Cards not ingesting
- Schema Mismatch: Excel structure broken
- Cache Corruption: Stale/unreadable cache
- Signal Anomaly: BUY/SELL misaligned with expectations

**Investigation checklist:**
1. Root cause: input data, logic, dependencies, external source, or file system?
2. Verify dependencies: Python 3.8+, requirements.txt installed, recent config changes
3. Data integrity: CSV structure valid, sample 3 cards manually, no duplicates
4. Logic validation: thresholds make sense, confidence formula correct, outlier detection < 5%
5. Output verification: Excel opens, row count correct, spot-check calculations

**Remediation paths:**
- CSV errors: Validate encoding (UTF-8), inspect headers, check columns
- Confidence issues: Review formula, adjust thresholds, test on subset
- Signal anomalies: Manually calculate P&L for 3 cards, verify rule order, check edge cases
- Excel errors: Verify openpyxl version, check output/ is writable, open manually

**Success criteria:**
- All 19 cards process without exceptions
- Confidence distribution: > 80% have confidence ≥ 70
- No ERROR logs (WARN acceptable)
- Excel opens without corruption
- Spot-check shows correct calculations
- Refresh < 60 seconds

---

## Usage Guide

1. Copy entire prompt for your task
2. Substitute placeholders (dates, card data, error messages)
3. Include necessary context (error logs, code snippets, sample data)
4. Submit to Claude (appropriate model)
5. Review output carefully before implementation

## Cost Management

| Prompt | Model | Cost/Run | Frequency | Monthly |
|--------|-------|----------|-----------|---------|
| PROMPT 1 (Build) | Opus | $0.10-0.30 | 4x/year | ~$1.00 |
| PROMPT 2 (Daily) | Haiku | <$0.01 | Daily | ~$0.30 |
| PROMPT 3 (Review) | Haiku | ~$0.01 | 2-3x/week | ~$0.15 |
| PROMPT 4 (Escalation) | Opus | $0.20-0.50 | 1-2x/quarter | ~$0.50 |
| **TOTAL MONTHLY** | — | — | — | **~$2.00** |

## When to Use Each

- **PROMPT 1:** Adding sources, redesigning schema, major rule changes, quarterly review
- **PROMPT 2:** Daily refresh, weekly/monthly reports, portfolio state diagnostics
- **PROMPT 3:** Low confidence (< 70%), edge case validation, match quality review
- **PROMPT 4:** System errors, unexpected signals, Excel corruption, production troubleshooting

---

**Document Version:** 1.0  
**Audience:** Claude operators, system administrators
