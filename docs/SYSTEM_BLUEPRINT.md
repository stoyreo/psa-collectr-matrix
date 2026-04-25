# Pokémon TCG Portfolio Intelligence System - System Blueprint

## Architecture Overview

Five-layer architecture: Excel Frontend → Data Engine → Source Connectors → Data Processing → Configuration & Logging

```
┌─────────────────────────────────────────────────────────┐
│    Layer 1: Excel Frontend (10 Sheets)                   │
│  DASHBOARD | PORTFOLIO | EBAY_COMPS | COLLECTR_MAP |    │
│   PSA_MAP | INSIGHTS | EXCEPTIONS | TARGETS | ALERT_LOG │
└─────────────────────────────────────────────────────────┘
                            ↑
┌─────────────────────────────────────────────────────────┐
│  Layer 2: Data Engine (refresh.py, signals.py)          │
│  Orchestrates: Ingest → Match → Enrich → Signal → Export│
└─────────────────────────────────────────────────────────┘
                            ↑
┌─────────────────────────────────────────────────────────┐
│  Layer 3: Source Connectors                             │
│  PSA CSV (Ready) | eBay (Demo) | Collectr (Stub)        │
└─────────────────────────────────────────────────────────┘
```

## Data Flow

PSA CSV (19 cards) → Parse & Normalize → Generate Match Keys → Fetch Market Comps → Cache Decision → Compute Confidence → Compute Signals → Write Excel

## File Structure

```
PSA x Collectr Tracer/
├── scripts/ (Python execution layer)
│   ├── main.py          Entry point
│   ├── refresh.py       7-step pipeline orchestrator
│   ├── config.py        Central config (340 lines)
│   ├── ingest.py        CSV parsing & normalization
│   ├── matching.py      Match key & confidence scoring
│   ├── ebay_connector.py eBay comps (demo mode)
│   ├── collectr_connector.py Collectr stub
│   ├── psa_connector.py PSA data mapping
│   ├── signals.py       BUY/SELL/HOLD rules
│   ├── excel_writer.py  Workbook generation
│   └── cache_manager.py Caching layer
├── cache/ (Runtime caching)
│   ├── comps_cache.json eBay comps cache (< 24h)
│   └── metadata_cache.json Card metadata (< 72h)
├── output/ (Generated artifacts)
│   ├── Pokemon_Portfolio_Intelligence.xlsx
│   └── portfolio_refresh.log
├── My Collection CSV - 19.csv (PSA export)
├── REFRESH.bat (Windows launcher)
├── requirements.txt (pip dependencies)
└── docs/
    ├── SETUP_GUIDE.md
    ├── SYSTEM_BLUEPRINT.md
    ├── PROMPTS.md
    ├── TEST_PLAN.md
    └── LIMITATIONS.md
```

## 10 Excel Sheets

| Sheet | Purpose | Rows |
|-------|---------|------|
| DASHBOARD | KPI summary, signal distribution | 20-25 |
| PORTFOLIO | Card-by-card breakdown | 1 header + 19 data |
| EBAY_COMPS | Pricing comps | 1 header + 228 (19 × 12) |
| COLLECTR_MAP | Collectr pricing (stub) | 1 header + 19 |
| PSA_MAP | PSA certificate data | 1 header + 19 |
| INSIGHTS | Top gainers, weak positions | 1 header + 20 |
| EXCEPTIONS | Data quality issues | 1 header + variable |
| TARGETS | Price alert triggers | Header + variable |
| ALERT_LOG | Alert delivery history | Header + variable |
| CONFIG | System configuration | Key-value pairs |

## Match Key Format

Canonical identifier: `{subject}_{set_code}_{card_number}_{psa_grade}_{variety}`

Example: `slowpoke_sv1v_082_psa8_artare`

## Confidence Scoring

- EXACT (90-100): All fields align
- STRONG (85-89): Minor variance acceptable
- MODERATE (70-84): Useful but fuzzy
- WEAK (50-69): Flag for review
- REJECT (0-49): Don't use

## Signal Rules

- **BUY**: market_value > cost × 1.15 AND liquidity ≥ MEDIUM AND confidence ≥ 85
- **SELL**: market_value < cost × 0.85 OR trend = DOWN AND confidence ≥ 70
- **REVIEW**: confidence < 80 OR missing data
- **HOLD**: Default (stable, illiquid, or mixed)

## Liquidity Classification

- **HIGH**: 8+ comps (80+ score)
- **MEDIUM**: 4-7 comps (50-79 score)
- **LOW**: 0-3 comps (0-49 score)

Factors: comp count, recency (0-30 days +20 bonus), price spread variance

## Trend Analysis

- **UP**: Recent median > older median by > 10%
- **DOWN**: Recent median < older median by > 10%
- **STABLE**: Within ±10%
- **INSUFFICIENT_DATA**: < 4 comps

## Demo Mode eBay Comps

Per card:
- 12 synthetic comps
- ±15% variance around PSA Estimate
- Grade multipliers: PSA 8 = 0.7x, PSA 9 = 0.85x, PSA 10 = 1.0x
- Sold dates: 30% last 7d, 50% last 30d, 15% last 90d, 5% older
- Shipping: 0-15% of sold price

## Portfolio Snapshot (Current)

- **Cards**: 19 Japanese PSA-graded
- **Cost basis**: $5,979 USD
- **Market value**: ~$2,052 USD (underwater)
- **P&L**: -$3,927 (-65.6%)
- **Signal allocation**: 7 BUY, 2 HOLD, 9 SELL, 1 REVIEW

## Cache Settings

- Comps: 24-hour max age
- Metadata: 72-hour max age
- Location: `cache/comps_cache.json`, `cache/metadata_cache.json`

## Configuration Parameters (config.py)

Key thresholds:
- Exact match confidence: 90
- Strong match confidence: 85
- Buy upside multiplier: 1.15 (15%)
- Sell downside multiplier: 0.85 (15%)
- High liquidity threshold: 8 comps
- Medium liquidity threshold: 4 comps
- Review confidence: 80
- Outlier detection: IQR method (1.5x multiplier)

## Cost Optimization Strategy

- **Opus tasks** (infrequent): Architecture, connectors, schema design
- **Haiku tasks** (daily): CSV ingest, comps, signals, Excel export
- **Token budget**: ~5,000/refresh × daily = sustainable cost

## Quality Gates

Build-time: CSV parsing, match key determinism, confidence monotonicity, signal consistency, Excel validity

Runtime: 100% card coverage, no negative values, confidence 0-100, formulas verified, no duplicates, clean logs

## Future Integrations

1. **eBay Live Connector** (high priority): Real sold listings via API or scraping
2. **Collectr Integration** (medium priority): Cross-validation of prices
3. **PSA Cert Verification** (low priority): Live cert status checking
4. **Telegram/LINE Alerts** (medium priority): Real-time notifications
5. **Scheduling** (low priority): Automated daily refreshes

See LIMITATIONS.md for detailed roadmap and implementation paths.

---

**Document Version:** 1.0  
**Audience:** Developers, System Architects, Power Users
