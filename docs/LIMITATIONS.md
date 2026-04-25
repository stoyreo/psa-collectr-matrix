# Pokémon TCG Portfolio Intelligence System - Limitations & Roadmap

This document honestly documents current constraints and paths to remove them.

---

## Overview

The system is **functionally complete** for core workflow (CSV → matching → signals → Excel) and **production-ready for demo/analysis use**. However, several features are stubbed or limited.

---

## Limitation 1: DEMO MODE (eBay Comps)

### Current State

**DEMO mode is ACTIVE.** System does not fetch real eBay listings; generates realistic sample comps.

```python
DATA_SOURCES = {"demo_mode": True}  # ← ENABLED
```

### Impact

| Aspect | Impact | Severity |
|--------|--------|----------|
| Market Value Accuracy | Generated prices mirror PSA estimates, not real market | Medium |
| Signal Reliability | Based on synthetic data, not actual sales | High |
| Portfolio Decisions | Should not use for real investment decisions | High |

### What's Working

- ✓ Signal logic is sound
- ✓ Signals are deterministic
- ✓ Useful for portfolio analysis and what-if scenarios
- ✓ Confidence scoring based on card matching

### What's Broken

- ✗ Market values are synthetic
- ✗ Signals not based on real market activity
- ✗ Price trends are randomized

### To Go Live: eBay Connector

**Complexity:** HIGH (~500-1000 tokens, Opus)  
**Timeline:** 4-8 hours  
**Cost:** Free (API) or minimal (scraping)

#### Path 1: eBay API (Official, Recommended)

Requirements: eBay OAuth2 credentials, 5,000 calls/day limit

```python
def search_ebay_sold_live(query: str) -> List[Dict]:
    """Call eBay API v2/item_summary endpoint"""
    # 1. Authenticate via OAuth2
    # 2. Build search query
    # 3. Fetch sold listings
    # 4. Parse title, price, date, shipping
    # 5. Filter bundles, fakes, wrong grades
    # 6. Return cleaned list
```

Time: 6-8 hours

#### Path 2: Web Scraping (Browser Automation)

Requirements: Selenium or Playwright

Time: 4-6 hours  
Risk: eBay may block if overly aggressive

#### Path 3: Third-Party SaaS

Options: Bright Data, Apify, SerpAPI (~$0.001 per scrape)

Time: 2-3 hours

**Recommendation:** Start with Path 2 (web scraping), then migrate to Path 1 (official API) for sustainability.

---

## Limitation 2: Collectr Integration (Stub)

### Current State

**Collectr connector returns empty data.**

```python
def get_collectr_data(card: Dict) -> Dict:
    return {}  # ← Stub
```

### Impact

| Aspect | Impact | Severity |
|--------|--------|----------|
| Price Validation | Can't cross-check eBay against Collectr | Medium |
| Market Coverage | Missing major price source | Medium |
| Confidence Scoring | Would improve for sparse eBay comps | Low |

### What's Working

- ✓ COLLECTR_MAP sheet in Excel (ready for data)
- ✓ Data structure defined
- ✓ Code structured to accept integration

### To Activate

**Complexity:** MEDIUM (~400 tokens, Opus)  
**Timeline:** 3-4 hours

#### Path 1: Selenium Scraping (Faster)

```python
def search_collectr(card: Dict) -> Dict:
    """Automate Collectr.com via Selenium"""
    # 1. Build search URL
    # 2. Open headless Chrome
    # 3. Extract ask/bid/recent_sales
    # 4. Return standardized format
```

Time: 3-4 hours

#### Weighting Strategy (Once Both Available)

```python
weighted = (ebay_value × 0.6) + (collectr_value × 0.4)
```

eBay 60% (larger sample, more recent), Collectr 40% (local insight)

**Recommendation:** Implement after eBay live connector. Collectr is secondary validation.

---

## Limitation 3: PSA Cert Verification API (Stub)

### Current State

**PSA connector reads CSV only; no live verification.**

### Impact

| Aspect | Impact | Severity |
|--------|--------|----------|
| Data Accuracy | Can't detect cert number errors | Low |
| Removed Certs | Can't flag sold/liquidated certs | Low |
| Grade Disputes | Can't detect grade changes | Low |

### To Activate

**Complexity:** LOW (~200 tokens, Haiku)  
**Timeline:** 2-3 hours

```python
def verify_psa_cert(cert_number: str) -> Dict:
    """Query PSA's public verification"""
    response = requests.get(f"https://www.psacard.com/cert/{cert_number}/")
    # Parse HTML/JSON
    return {"cert_valid": True, "grade_current": 8, "status": "ACTIVE"}
```

**Recommendation:** Low priority. Only if you suspect cert changes or holding old certs.

---

## Limitation 4: Live Alerts (Telegram/LINE)

### Current State

**Alert framework implemented but not configured.**

System can:
- ✓ Detect when price targets hit
- ✓ Log to ALERT_LOG sheet
- ✓ Format messages

System cannot:
- ✗ Send Telegram messages (token not configured)
- ✗ Send LINE notifications (token not configured)
- ✗ Send emails (SMTP not configured)
- ✗ Trigger on schedule (manual REFRESH.bat only)

### Impact

| Aspect | Impact | Severity |
|--------|--------|----------|
| Real-Time Alerts | Can't be notified of price events immediately | Medium |
| Passive Monitoring | Requires manual Excel review | Low |
| Mobile Access | Can't get alerts on phone | Low |

### To Activate: Telegram (Recommended)

**Complexity:** MEDIUM (~300 tokens, Haiku)  
**Timeline:** 1-2 hours

1. Create bot via BotFather: `/newbot`
2. Get chat ID from `getUpdates`
3. Paste into CONFIG:
   ```
   Telegram Bot Token: 123456789:ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefgh
   Telegram Chat ID: 1234567890
   ```

```python
def send_telegram_alert(message: str, bot_token: str, chat_id: str) -> bool:
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {"chat_id": chat_id, "text": message, "parse_mode": "HTML"}
    return requests.post(url, json=payload).status_code == 200
```

### To Activate: Automatic Scheduling

#### Windows Task Scheduler (Easiest)

```batch
schtasks /create /tn "Pokemon Portfolio Refresh" /tr "C:\Path\REFRESH.bat" /sc DAILY /st 09:00
```

Time: 30 minutes

#### Python APScheduler

Time: 1-2 hours

**Recommendation:** Windows Task Scheduler (quick win) + Telegram alerts (1-2 hours).

---

## Limitation 5: Multi-User / Cloud Deployment

### Current State

**System is single-user, local-only.**

- CSV/Excel on local machine
- No cloud sync
- No shared portfolio
- No authentication
- No audit trail

### Impact

| Aspect | Impact | Severity |
|--------|--------|----------|
| Collaboration | Can't share portfolio with partner/advisor | Medium |
| Remote Access | Can't access from different computer | Medium |
| Backup | Manual backup required | Low |
| Version Control | No change history | Low |

### To Add Cloud Support

**Complexity:** HIGH (~1000+ tokens, Opus)  
**Timeline:** 1-2 weeks

#### Path 1: Google Sheets (Simplest)

Replace Excel with Google Sheets, share with other users

Time: 4-6 hours

#### Path 2: AWS DynamoDB + Lambda

Full cloud deployment, API for web/mobile

Time: 2-3 weeks

**Recommendation:** Not necessary for current use. Only if multiple users need access or portfolio expands to 100+ cards.

---

## Limitation 6: Currency Conversion (Fixed Rates)

### Current State

**Exchange rates are hardcoded.**

```python
CURRENCY = {
    "exchange_rates": {
        "USD_to_THB": 35.0,  # ← FIXED (should be live)
    }
}
```

### To Fix

**Complexity:** LOW (~150 tokens, Haiku)  
**Timeline:** 1 hour

```python
def get_live_exchange_rate(base: str, target: str) -> float:
    url = "https://openexchangerates.org/api/latest"
    params = {"app_id": API_KEY, "base": base, "symbols": target}
    return requests.get(url, params=params).json()["rates"][target]
```

Cost: Free (Open Exchange Rates, 1,000 calls/month)

**Recommendation:** Implement if working in Thai market. Otherwise, USD-only is fine.

---

## Limitation 7: Single Portfolio CSV

### Current State

**System reads exactly one CSV file.**

Cannot:
- ✗ Load multiple CSVs
- ✗ Merge collections from different PSA accounts
- ✗ Track historical snapshots

### To Support Multiple CSVs

**Complexity:** LOW (~200 tokens)  
**Timeline:** 1-2 hours

```python
def ingest_all_collections(directory: Path) -> List[Dict]:
    all_cards = []
    for csv_file in directory.glob("My Collection*.csv"):
        cards = ingest_collection(csv_file)
        all_cards.extend(cards)
    # Deduplicate by cert number
    return list({c["cert_number"]: c for c in all_cards}.values())
```

**Recommendation:** Implement if you have multiple PSA accounts.

---

## Limitation 8: No Historical Tracking

### Current State

**Excel output overwrites each refresh.** No history of signals/values over time.

### To Add History

**Complexity:** MEDIUM (~300 tokens)  
**Timeline:** 2-3 hours

```python
def archive_results(result: Dict, timestamp: str):
    archive_dir = Path("archive")
    archive_dir.mkdir(exist_ok=True)
    dated_file = archive_dir / f"Portfolio_{timestamp}.xlsx"
    write_portfolio_excel(result, dated_file)
    json_file = archive_dir / f"Summary_{timestamp}.json"
    with open(json_file, "w") as f:
        json.dump(result["summary"], f)
```

**Recommendation:** Implement if want trend analysis or quarterly reviews.

---

## Limitation 9: No Advanced Filtering

### Current State

System provides basic signals but not:
- ✗ "What if I sell all SELL cards?"
- ✗ "Which cards most likely to rebound?"
- ✗ "Optimal sell sequence to minimize loss?"
- ✗ "Which sets are declining?"

### To Add

**Complexity:** HIGH (~500+ tokens, Opus)  
**Timeline:** 4-6 hours

**Recommendation:** Not necessary for v1. Could add in v2 if users request optimization features.

---

## Limitation 10: Excel Performance (Large Portfolios)

### Current State

Optimized for 19 cards. If scaling to 1000+:
- ✗ Excel file may become slow (100+ MB)
- ✗ EBAY_COMPS has 12,000+ rows
- ✗ Conditional formatting may slow opening

### To Fix (If Scaling)

1. Split into multiple sheets (by set, grade)
2. Archive old data (don't include 2-year-old comps)
3. Use database instead of Excel

**Recommendation:** Not necessary for current portfolio. Revisit if expanding to 100+ cards.

---

## Priority Roadmap

### Phase 1: Core Reliability (Weeks 1-2)
- [ ] eBay live connector (Path 2: Scraping)
  - **Impact:** High (real market data)
  - **Effort:** 4-8 hours
  - **Status:** Recommended

### Phase 2: Automation (Weeks 2-4)
- [ ] Windows Task Scheduler (30 min, quick win)
- [ ] Telegram alerts (1-2 hours, quick win)

### Phase 3: Enhancements (Month 2+)
- [ ] Collectr integration (3-4 hours)
- [ ] Historical tracking (2-3 hours)

### Phase 4: Advanced (Month 3+)
- [ ] Cloud deployment (1-2 weeks, if needed)
- [ ] Portfolio optimization (4-6 hours, if needed)

---

## What's Intentionally NOT Supported

**Out of scope** for current design:

1. **Real-Time Price Updates:** Would require $100+/month API subscription
2. **Automatic Trading:** System is analysis, not automation
3. **Tax Reporting:** Requires accounting integrations
4. **Mobile App:** Out of scope for Python CLI tool
5. **AI/ML Model Training:** Need 100+ cards and 12+ months history

---

## Frequently Asked Questions

**Q: Can I use live eBay data now?**  
A: No, demo mode enabled. Follow "Limitation 1" section to activate live connector.

**Q: Why is Collectr just a stub?**  
A: eBay is primary source. Collectr is validation. Implement after eBay.

**Q: Can I share with someone?**  
A: Not in current setup. Manually share Excel or implement cloud sync (Phase 4).

**Q: Does this work on Mac/Linux?**  
A: Yes, Python scripts are cross-platform. REFRESH.bat is Windows-only; use `python scripts/main.py` instead.

**Q: Can I have 100+ cards?**  
A: Yes, but Excel performance degrades. Consider splitting or switching to CSV output.

**Q: Is my data secure?**  
A: Yes. Everything runs locally. No cloud upload unless you enable it.

**Q: Can I sell cards directly through this system?**  
A: No, analysis-only. Use signals to inform manual eBay listings.

---

## Document Changelog

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | Apr 2026 | Initial release with 10 limitations documented |

---

**Document Version:** 1.0  
**Audience:** Users, Developers, Product Managers
