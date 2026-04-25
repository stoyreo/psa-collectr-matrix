# Pokémon TCG Portfolio Intelligence System - Documentation

Welcome to the complete documentation for the Pokémon TCG Portfolio Intelligence System. This folder contains five comprehensive guides covering setup, architecture, operations, testing, and known limitations.

---

## Quick Navigation

### 1. **SETUP_GUIDE.md** - Getting Started (337 lines)
**For:** Users installing and running the system

- Prerequisites and installation steps
- How to place your PSA CSV
- Running the system (REFRESH.bat or command line)
- Understanding the 10 Excel sheets
- Customization and configuration
- Troubleshooting common issues
- System requirements

**Start here if you're:** Setting up the system for the first time

---

### 2. **SYSTEM_BLUEPRINT.md** - Architecture Deep Dive (173 lines)
**For:** Developers and architects understanding the design

- Five-layer architecture overview
- Complete data flow diagram
- File and folder structure
- 10 Excel sheet schemas (columns and purposes)
- Matching engine design (confidence scoring, canonical keys)
- eBay comp search and filtering logic
- Signal rules (BUY/HOLD/SELL/REVIEW)
- Liquidity and trend analysis
- Cache management
- Future integration points

**Start here if you're:** Understanding how the system works under the hood

---

### 3. **PROMPTS.md** - Claude Operational Prompts (170 lines)
**For:** Claude operators who will run daily operations

- **PROMPT 1:** Build & Architecture (Opus, infrequent)
- **PROMPT 2:** Daily Operations (Haiku, daily refresh)
- **PROMPT 3:** Review (Haiku, edge case validation)
- **PROMPT 4:** Escalation (Opus, production troubleshooting)

Includes cost analysis, when to use each prompt, and detailed requirements.

**Start here if you're:** Operating the system with Claude's help or delegating tasks

---

### 4. **TEST_PLAN.md** - Quality Assurance (305 lines)
**For:** QA engineers and developers testing the system

Comprehensive test cases covering:
- CSV ingest (parsing, normalization, nulls, encoding)
- Matching engine (determinism, confidence scoring)
- eBay connector (demo mode, filtering, outlier detection)
- Signal engine (BUY/SELL/HOLD/REVIEW rules)
- Excel writer (file generation, sheets, formatting)
- Cache manager (storage, expiration, disabling)
- Full refresh pipeline (end-to-end)
- Integration tests
- Data integrity checks
- Error handling
- Edge cases
- QA checklist

**Start here if you're:** Testing or validating the system before production use

---

### 5. **LIMITATIONS.md** - Current Constraints & Roadmap (469 lines)
**For:** Users understanding what's not yet implemented

Honest documentation of 10 limitations:

1. **DEMO MODE** - Sample eBay comps instead of live data (HIGH impact)
2. **Collectr Stub** - No Collectr data fetching yet (MEDIUM impact)
3. **PSA Cert Verification** - No live cert status checking (LOW impact)
4. **Live Alerts** - Telegram/LINE not configured (MEDIUM impact)
5. **Multi-User/Cloud** - Single-user, local-only (MEDIUM impact)
6. **Fixed Exchange Rates** - No live currency conversion (LOW impact)
7. **Single CSV** - Can't load multiple portfolios (LOW impact)
8. **No History Tracking** - No trend data over time (LOW impact)
9. **No Advanced Filtering** - No portfolio optimization (LOW impact)
10. **Excel Performance** - Slow with 1000+ cards (LOW impact)

Each limitation includes:
- Current state and impact assessment
- What's working vs. broken
- Complexity and timeline to fix
- Implementation paths with code examples
- Recommendation (Priority in roadmap)

**Start here if you're:** Evaluating what features exist and planning future work

---

## Quick Reference

### For Different Audiences

**First-time user?**  
→ Read: SETUP_GUIDE.md

**Want to understand the code?**  
→ Read: SYSTEM_BLUEPRINT.md + PROMPTS.md (PROMPT 1)

**Running daily operations?**  
→ Read: PROMPTS.md (PROMPT 2)

**Testing before production?**  
→ Read: TEST_PLAN.md

**Evaluating what's next?**  
→ Read: LIMITATIONS.md

**Troubleshooting an issue?**  
→ Check: SETUP_GUIDE.md (Troubleshooting section) + PROMPTS.md (PROMPT 4)

---

## System Status

| Component | Status | Notes |
|-----------|--------|-------|
| CSV Ingest | ✓ Ready | PSA collection export parsing works |
| Card Matching | ✓ Ready | Canonical keys, confidence scoring |
| eBay Comps | ⚠ Demo Mode | Working but synthetic data (±15% variance) |
| Collectr | ⚠ Stub | Framework ready, no data fetching |
| PSA Verification | ⚠ Stub | Reads CSV, no live cert checking |
| Signal Engine | ✓ Ready | BUY/HOLD/SELL/REVIEW logic implemented |
| Excel Export | ✓ Ready | 10 sheets with premium formatting |
| Alerts | ⚠ Framework Only | Logic ready, Telegram/LINE not configured |
| Scheduling | ⚠ Manual | REFRESH.bat works, no automation yet |
| Cache Manager | ✓ Ready | 24h/72h expiration, fallback strategies |

---

## Key Metrics

**Portfolio (19 Japanese PSA Cards):**
- Cost Basis: $5,979 USD
- Market Value: ~$2,052 USD (demo data)
- P&L: -$3,927 (-65.6%)
- Signal Distribution: 7 BUY, 2 HOLD, 9 SELL, 1 REVIEW

**System Performance:**
- Refresh Time: 10-30 seconds
- Excel File Size: ~500 KB (with 19 cards)
- Log File: ~50 KB per refresh
- Cache Size: ~100 KB (12 comps per card)

**Cost to Operate (with Claude):**
- Daily Refresh (Haiku): <$0.01/day (~$0.30/month)
- Weekly Review (Haiku): ~$0.01/week (~$0.15/month)
- Quarterly Architecture (Opus): ~$0.50/quarter
- **Total Monthly:** ~$2.00

---

## Getting Help

### For Setup Issues
1. Check SETUP_GUIDE.md → Troubleshooting section
2. Review portfolio_refresh.log in output/ directory
3. Verify Python 3.8+ and pip are installed

### For Understanding the System
1. Read SYSTEM_BLUEPRINT.md for architecture
2. Check matching.py, signals.py for specific logic
3. Review PROMPTS.md for operational context

### For Testing/Validation
1. Follow TEST_PLAN.md test cases
2. Check QA Checklist before production
3. Run manual spot-checks on 3 random cards

### For Feature Requests
1. Check LIMITATIONS.md for roadmap
2. Estimate impact (High/Medium/Low)
3. Estimate effort (hours)
4. Decide if worth implementing

---

## Document Structure Summary

| File | Lines | Purpose | Audience |
|------|-------|---------|----------|
| SETUP_GUIDE.md | 337 | Installation & usage | Users |
| SYSTEM_BLUEPRINT.md | 173 | Architecture & design | Developers |
| PROMPTS.md | 170 | Claude operations | Operators |
| TEST_PLAN.md | 305 | Quality assurance | QA/Developers |
| LIMITATIONS.md | 469 | Constraints & roadmap | Everyone |
| **TOTAL** | **1,454** | **Complete system documentation** | **All roles** |

---

## Production Readiness Checklist

Before using in production:

- [ ] SETUP_GUIDE.md → Follow installation steps
- [ ] SYSTEM_BLUEPRINT.md → Understand the architecture
- [ ] TEST_PLAN.md → Run all tests, verify pass criteria
- [ ] Review signal allocation on test portfolio (7 BUY, 2 HOLD, 9 SELL, 1 REVIEW)
- [ ] Excel output opens without corruption
- [ ] Manual spot-check: Verify 3 card calculations match rules
- [ ] Log file contains no ERROR messages
- [ ] LIMITATIONS.md → Understand known constraints
- [ ] Review PROMPTS.md for how to run daily operations

---

## Version History

| Version | Date | Status | Notes |
|---------|------|--------|-------|
| 1.0 | Apr 2026 | Production Ready | Initial release, all 5 docs complete |

---

## Contact & Support

For questions about:
- **Setup/Installation:** See SETUP_GUIDE.md → Getting Help section
- **Architecture/Code:** See SYSTEM_BLUEPRINT.md
- **Daily Operations:** See PROMPTS.md
- **Testing:** See TEST_PLAN.md
- **Feature Planning:** See LIMITATIONS.md

---

**Documentation Package Version:** 1.0  
**Last Updated:** April 2026  
**System Version:** 1.0  
**All Rights Reserved**
