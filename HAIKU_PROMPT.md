# Handover Prompt for Claude Haiku — "Add Card" Feature

**Paste the entire contents below into a new Claude Haiku conversation. It is self-contained and does not require prior context.**

---

## ROLE

You are a senior Python + Flask + vanilla-JS engineer working inside an existing local desktop web app called **PSA × Collectr Tracer**. Your task is to implement a new **"Add Card"** feature end-to-end, following the exact specification in this brief. You must not invent architectural changes outside this spec. Ask the user a clarifying question only if the spec is contradictory — otherwise execute.

---

## 1 · PROJECT CONTEXT

The app is a single-user local tool that tracks a PSA-graded Japanese Pokemon card portfolio. It ingests a CSV exported from a collecting app, enriches it with live Collectr + PSA + eBay data, and renders a Flask + JS dashboard.

**Working directory:** `C:\Users\USER\Desktop\Claude Project\PSA x Collectr Tracer\PSA x Collectr Tracer`

**Currency convention:** All monetary values are in THB. USD→THB rate lives in `scripts/config.py` (`USD_TO_THB = 33.22`).

**Tech stack:** Python 3.11, Flask, openpyxl, Playwright (Collectr scraping), vanilla JS + Chart.js in a single `templates/index.html`. PyInstaller for EXE builds.

**Key existing files (DO NOT break these):**

```
PSA x Collectr Tracer/
├── webapp.py                          # Flask server (entry point)
├── templates/index.html               # Single-page UI (dark-navy nav, light body)
├── My Collection CSV - 19.csv         # Current source of truth (33 cols)
├── Pokemon_Portfolio_Intelligence.xlsx# Analytics OUTPUT (regenerated each refresh)
├── REFRESH.bat                        # User-facing launcher
├── start_webapp.bat                   # Web server launcher
├── cache/                             # PSA + Collectr image cache (.jpg/.webp)
├── scripts/
│   ├── config.py                      # Paths, rates, logging config
│   ├── ingest.py                      # CSV → cards[]
│   ├── matching.py                    # generate_match_key()
│   ├── refresh_live.py                # live_refresh() pipeline
│   ├── collectr_live_fetcher.py       # fetch_live_prices_sync()
│   ├── collectr_connector.py          # Collectr URL helpers
│   ├── psa_scraper.py                 # PSA cert page scraper
│   ├── psa_connector.py               # PSA API helpers
│   ├── ebay_connector.py              # eBay sold-comp fetcher
│   ├── excel_writer.py                # Writes Pokemon_Portfolio_Intelligence.xlsx
│   └── signals.py                     # compute_signal()
```

**Existing CSV columns (33):**

```
Item Status, Item, Cert Number, Grade Issuer, Grade, Autograph Grade, Year, Set,
Card Number, Subject, Variety, Serial, Category, My Cost, PSA Estimate, Gain/Loss,
My Value, Date Acquired, Source, My Notes, Vault Status, Vaulted Date, Days Vaulted,
Listing Status, Listing Date, Listing Price, Sold Status, Sold On, Sold Date,
Sold Price, Sold Fees, Sold Proceeds, Payment Date
```

---

## 2 · FEATURE GOAL

Add a new top-nav tab **"➕ Add Card"** that lets the user paste a PSA Cert Number, fetch merged card identity + prices from **PSA + Collectr + eBay in parallel**, validate the result via a full preview (images + metadata + comps + signal), and persist approved cards into a **new master Excel workbook** `Portfolio_Master.xlsx` that becomes the single source of truth. The existing CSV is auto-synced into this master on every BAT launch and every Refresh click.

User decisions (do not re-litigate):

- Single input field = PSA Cert # (everything else auto-fetched, then editable)
- All 3 sources fetched in parallel (PSA + Collectr + eBay)
- Duplicates are allowed (always append — user cleans up manually)
- Full preview with image validation required before save
- CSV→Master sync is automatic on every launch + every refresh

---

## 3 · MASTER WORKBOOK SCHEMA

**File:** `Portfolio_Master.xlsx` (create at workspace root)

### Sheet 1: `Cards`

The 33 existing CSV columns **plus** 6 new columns appended to the right:

| # | New Column | Type | Populated by |
|---|---|---|---|
| 34 | `collectr_url` | str | Collectr fetch |
| 35 | `collectr_price_thb` | float | Collectr fetch |
| 36 | `ebay_avg_thb` | float | eBay fetch |
| 37 | `ebay_n_comps` | int | eBay fetch |
| 38 | `image_match_ok` | bool | Visual-hash compare (PSA vs Collectr) |
| 39 | `last_updated` | ISO 8601 str | On every write |

Header row is bold navy `#1B2A4A` on white. Freeze row 1.

### Sheet 2: `Sync Log`

| timestamp | source | cert | action | note |
|---|---|---|---|---|
| 2026-04-17T14:02:33 | csv | 131858430 | added | From "My Collection CSV - 19.csv" row 2 |
| 2026-04-17T14:05:12 | add-card | 102808568 | added | Manual via web UI |
| 2026-04-17T14:30:00 | refresh | 131858430 | updated | Market values changed |

`source` ∈ {`csv`, `add-card`, `refresh`}
`action` ∈ {`added`, `updated`, `skipped`}

### Sheet 3: `Meta`

Two-column key/value sheet:

```
schema_version   | 1
created_at       | 2026-04-17T14:00:00
last_csv_sync    | 2026-04-17T14:02:33
usd_to_thb_rate  | 33.22
```

---

## 4 · BACKEND — NEW MODULES

Create these files inside `scripts/`:

### 4.1 `scripts/master_workbook.py`

```python
"""Read/write the Portfolio_Master.xlsx master workbook."""
from pathlib import Path
from openpyxl import Workbook, load_workbook
from datetime import datetime
import os, tempfile, shutil

MASTER_PATH = Path(__file__).parent.parent / "Portfolio_Master.xlsx"

CARD_COLUMNS = [  # 33 CSV + 6 new
    "Item Status", "Item", "Cert Number", "Grade Issuer", "Grade",
    "Autograph Grade", "Year", "Set", "Card Number", "Subject", "Variety",
    "Serial", "Category", "My Cost", "PSA Estimate", "Gain/Loss", "My Value",
    "Date Acquired", "Source", "My Notes", "Vault Status", "Vaulted Date",
    "Days Vaulted", "Listing Status", "Listing Date", "Listing Price",
    "Sold Status", "Sold On", "Sold Date", "Sold Price", "Sold Fees",
    "Sold Proceeds", "Payment Date",
    # new columns
    "collectr_url", "collectr_price_thb", "ebay_avg_thb", "ebay_n_comps",
    "image_match_ok", "last_updated",
]

def ensure_master_exists() -> Path:
    """Create a fresh Portfolio_Master.xlsx with 3 sheets if missing."""
    ...

def append_card(row: dict, source: str) -> int:
    """Append one row to Cards sheet; log to Sync Log. Returns new row index.
       source ∈ {'csv', 'add-card', 'refresh'}. Uses atomic save (tmp + rename)."""
    ...

def update_card(cert: str, fields: dict, source: str) -> int:
    """Update the most recent row for this cert. Always log to Sync Log.
       Returns updated row index. If cert not found, raises KeyError."""
    ...

def list_cards() -> list[dict]:
    """Return all Cards rows as list of dicts (header-keyed)."""
    ...

def append_sync_log(source: str, cert: str, action: str, note: str = "") -> None:
    ...
```

Use `openpyxl` throughout. Every save goes through an atomic write: write to `Portfolio_Master.xlsx.tmp`, then `os.replace(tmp, MASTER_PATH)`. Add a file-level lock using `filelock` package (add to `requirements.txt`) with a 10-second timeout.

### 4.2 `scripts/csv_master_sync.py`

```python
"""Diff CSV against master and append new/changed rows."""
from pathlib import Path
import csv, hashlib
from master_workbook import append_card, list_cards, append_sync_log
import logging

logger = logging.getLogger(__name__)
CSV_GLOB = "My Collection CSV - *.csv"

def _row_hash(row: dict) -> str:
    """Stable hash of (cert, grade, cost, date_acquired) for change detection."""
    key = f"{row.get('Cert Number','')}|{row.get('Grade','')}|{row.get('My Cost','')}|{row.get('Date Acquired','')}"
    return hashlib.sha1(key.encode()).hexdigest()[:12]

def run() -> dict:
    """Find latest CSV, sync into master. Returns {'added': N, 'updated': N, 'skipped': N}."""
    ...
```

- Run `ensure_master_exists()` first.
- Build a set of existing hashes from the Cards sheet.
- For each CSV row: if its hash is new and cert+grade+cost differs → log `updated` & append. If entirely new cert → log `added` & append. Else → `skipped`.
- Never delete. Append-only.

### 4.3 `scripts/add_card_service.py`

```python
"""Orchestrates the 3-source parallel fetch for Add Card."""
import asyncio
from dataclasses import dataclass, asdict
from datetime import datetime
from scripts.psa_scraper import fetch_cert_details          # existing
from scripts.collectr_live_fetcher import fetch_one_async   # existing
from scripts.ebay_connector import fetch_sold_comps          # existing

@dataclass
class PreviewCard:
    cert: str
    # identity (from PSA)
    item: str; year: int; set_name: str; card_number: str
    subject: str; variety: str; grade: int
    # prices
    collectr_url: str | None
    collectr_price_thb: float | None
    psa_estimate_thb: float | None
    ebay_avg_thb: float | None
    ebay_n_comps: int
    # images
    psa_image_ok: bool; collectr_image_ok: bool; image_match_ok: bool
    # signal (computed)
    signal: str; risk_level: str; upside_pct: float; confidence: float
    # errors per source (for UI chips)
    errors: dict  # {'psa': None | str, 'collectr': None | str, 'ebay': None | str}

async def search(cert: str) -> PreviewCard:
    """Parallel fetch PSA + Collectr + eBay using asyncio.gather."""
    ...
```

Tolerate individual source failures — only raise if PSA fails (identity is mandatory).

Compute the signal using `scripts.signals.compute_signal()` (or `refresh_live.compute_signal_live`) with a default `my_cost` of `None` so the preview shows a REVIEW signal until the user fills in cost.

---

## 5 · BACKEND — NEW ENDPOINTS IN `webapp.py`

Add these routes. Keep the existing ones untouched.

```python
@app.route("/api/add-card/search", methods=["POST"])
def api_add_card_search():
    """Body: {cert: str}. Runs add_card_service.search. Returns PreviewCard JSON."""
    data = request.get_json() or {}
    cert = (data.get("cert") or "").strip()
    if not re.match(r"^\d{6,10}$", cert):
        return jsonify(status="error", message="Cert must be 6-10 digits"), 400
    try:
        preview = asyncio.run(add_card_service.search(cert))
        return jsonify(status="ok", preview=asdict(preview))
    except Exception as e:
        app.logger.error(f"Add Card search failed: {e}", exc_info=True)
        return jsonify(status="error", message=str(e)), 500


@app.route("/api/add-card/save", methods=["POST"])
def api_add_card_save():
    """Body: {preview: {...}, my_info: {my_cost, date_acquired, source, notes, item_status}}.
       Appends to Portfolio_Master.xlsx. Returns {status, master_row: int}."""
    ...


@app.route("/api/csv-sync", methods=["POST"])
def api_csv_sync():
    """Manually trigger CSV->Master sync. Returns summary dict."""
    summary = csv_master_sync.run()
    return jsonify(status="ok", **summary)


@app.route("/api/add-card/image-validate/<cert>")
def api_image_validate(cert):
    """Returns {psa_ok, collectr_ok, visual_match} by running existing
       _fetch_psa_cert_image + _fetch_collectr_image + a perceptual hash compare."""
    ...
```

**Also modify `api_refresh`** at line ~485: call `csv_master_sync.run()` as the FIRST step inside the `_lock` block, before the live Collectr fetch. Log the summary.

**Also modify `index()` at line ~472**: on first request, call `ensure_master_exists()` + `csv_master_sync.run()` if master is older than the CSV file's mtime.

---

## 6 · FRONTEND — `templates/index.html`

### 6.1 Add the nav tab

Find the existing nav-tabs block (around line 340-360 — search for `nav-tab` class). Insert between Portfolio and Signals:

```html
<div class="nav-tab" data-tab="add-card">➕ Add Card</div>
```

### 6.2 Add the tab panel

After the existing `#tab-portfolio` div, add:

```html
<div class="tab-panel" id="tab-add-card">
  <div id="add-card-empty">
    <!-- Empty state from mockup: centered cert input + Search button -->
  </div>
  <div id="add-card-searching" style="display:none">
    <!-- 3 source chips that flip state: pending → loading → done/error -->
  </div>
  <div id="add-card-preview" style="display:none">
    <!-- 2-column grid: images left, details+editable form+signal right -->
    <!-- Approve / Edit / Cancel buttons -->
  </div>
  <div id="add-card-saved" style="display:none">
    <!-- Green check banner + links -->
  </div>
</div>
```

**Match the visual style exactly from `ADD_CARD_MOCKUP.html`** at the workspace root. That file is a standalone reference — copy its CSS into the `<style>` block of `index.html` (scoped to `#tab-add-card` to avoid class collisions), and its HTML structure into the new panel.

### 6.3 JS module

Add inline JS (no external files) that:

1. Listens for clicks on the Add Card nav-tab → shows `#tab-add-card`, focuses the cert input.
2. Global keyboard shortcut `n` (when no input focused) → switches to Add Card tab.
3. On Search button / Enter: disables input, switches to `#add-card-searching`, animates the 3 chips, calls `POST /api/add-card/search`.
4. On response: populates `#add-card-preview` fields from the `PreviewCard` JSON, switches state. Loads images via `/psa-img/<cert>` and `/card-img/<product_id>` (existing endpoints).
5. On Approve: POST to `/api/add-card/save`, on success show `#add-card-saved` for 5 s, then reset to empty and trigger a background refresh of Dashboard/Portfolio tabs (reuse existing `loadStatus()` function).
6. On Cancel: reset to empty.
7. On Edit: no-op (fields are already editable — button just pulses them).

---

## 7 · LAUNCHER CHANGES

### `REFRESH.bat`

Before `python webapp.py`, add:

```
echo [1/2] Syncing CSV into master workbook...
python -c "import sys; sys.path.insert(0,'scripts'); import csv_master_sync; print(csv_master_sync.run())"
```

### `start_webapp.bat`

Same prepended step.

---

## 8 · DEPENDENCIES

Add to `requirements.txt`:

```
filelock>=3.12
imagehash>=4.3
pillow>=10.0
```

(`imagehash` + `pillow` for the visual-hash image match check.)

---

## 9 · IMPLEMENTATION ORDER (phases)

Work in this order so the app stays runnable between phases.

1. **Phase A — Master workbook infra** (no UI changes yet)
   - Write `scripts/master_workbook.py`
   - Write `scripts/csv_master_sync.py`
   - Smoke-test: run `python -c "import csv_master_sync; print(csv_master_sync.run())"` — verify `Portfolio_Master.xlsx` is created with 19 rows on the `Cards` sheet.

2. **Phase B — Add Card backend**
   - Write `scripts/add_card_service.py`
   - Add the 4 routes to `webapp.py`
   - Smoke-test with `curl -X POST http://127.0.0.1:5000/api/add-card/search -d '{"cert":"131858430"}' -H "Content-Type: application/json"`

3. **Phase C — Add Card frontend**
   - Copy CSS from `ADD_CARD_MOCKUP.html` into `index.html`
   - Add nav tab + `#tab-add-card` panel
   - Add JS for all 4 states
   - Manual test end-to-end in Chrome

4. **Phase D — Launcher wiring**
   - Update `REFRESH.bat` + `start_webapp.bat`
   - Modify `api_refresh` + `index()` in `webapp.py` to call sync

5. **Phase E — Image validation polish**
   - Implement `_perceptual_hash_compare(psa_bytes, collectr_bytes)` in `webapp.py` using `imagehash`
   - Wire into `/api/add-card/image-validate`

---

## 10 · ACCEPTANCE CRITERIA

- [ ] `Portfolio_Master.xlsx` is created with 3 sheets and 39 columns on `Cards`.
- [ ] First launch after merge auto-syncs all 19 rows from the CSV → visible in master + `Sync Log` shows 19 `added` entries from source=`csv`.
- [ ] Entering cert `131858430` in Add Card → preview appears within 15 s → clicking Approve adds a new row at the bottom of `Cards` + logs `added` from source=`add-card`.
- [ ] Duplicate cert save is permitted and creates a second row + log entry.
- [ ] `REFRESH.bat` reruns the CSV sync first, then the live Collectr fetch.
- [ ] Existing Dashboard/Portfolio/Signals/Market tabs still work unchanged.
- [ ] No breaking of PyInstaller build (`BUILD_EXE.bat` still completes).
- [ ] Smoke test: `pytest scripts/tests/test_master_workbook.py -v` passes (create minimal tests).

---

## 11 · OUT OF SCOPE

- Bulk upload (N certs at once)
- Auto-deduplication
- Mobile layout tuning
- Delete-from-UI
- i18n
- Migration of `Pokemon_Portfolio_Intelligence.xlsx` — keep it as-is (it's the analytics output, not source of truth)

---

## 12 · STYLE & CONVENTIONS

- Python: 4-space indent, type hints on every public function, `from __future__ import annotations` at top of new files, `logging` not `print`.
- JS: `const`/`let` only, no jQuery, fetch API, reuse existing helpers in `index.html` (`$`, `fmtTHB`, `loadStatus`).
- Currency formatting: `฿1,234` (already a helper in index.html).
- Dates: ISO 8601 in backend/storage, localised only in display.
- No emojis in code comments. Emojis allowed in UI copy (matches existing style).

---

## 13 · REFERENCE FILES (read before coding)

1. `ADD_CARD_PLAN.md` — full UX plan (workspace root)
2. `ADD_CARD_MOCKUP.html` — visual spec of all 4 UI states (workspace root)
3. `templates/index.html` — existing UI patterns to match
4. `webapp.py` around lines 256-570 — existing route + image-cache patterns to mirror
5. `scripts/refresh_live.py` — signal computation patterns

---

## 14 · WHEN YOU ARE DONE

Respond with:

1. A list of every file created/modified (with line counts).
2. The output of the smoke tests.
3. A screenshot (or text description) of each of the 4 UI states.
4. The first 10 lines of `Portfolio_Master.xlsx` > `Sync Log` as proof of end-to-end success.
5. Any deviations from this spec, with justification.

**Do not ship partial implementations.** Ship Phase A+B+C+D+E together, or stop at the last fully-working phase and report what's left.

---

*End of handover prompt. Begin implementation.*
