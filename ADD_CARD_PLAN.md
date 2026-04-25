# Add Card Feature — UI/UX Plan

**Project:** PSA × Collectr Tracer
**Date:** 2026-04-17
**Status:** DRAFT — awaiting user validation

---

## 1. Goal

Add a new **"Add Card"** tab to the web app that lets the user paste a **PSA Cert Number**, fetch merged card identity + pricing from **PSA + Collectr + eBay** in parallel, validate the result via a full preview (image + metadata + comps + signal), and persist approved cards into a **new master Excel workbook** that becomes the single source of truth. The existing `My Collection CSV - XX.csv` is auto-synced into the master every BAT launch and every Refresh click.

---

## 2. User Flow (4 UI states)

```
  [EMPTY]  ──enter cert──▶  [SEARCHING]  ──fetch ok──▶  [PREVIEW]  ──approve──▶  [SAVED]
                                 │                         │
                                 └── fetch fail ──┐        └── cancel ──▶ [EMPTY]
                                                  ▼
                                              [ERROR]
```

| State | What the user sees |
|---|---|
| **EMPTY** | Big centered input: *"Paste PSA Cert #"* + `Search` button. Small caption: *"We'll fetch identity, images, live price, and eBay comps in parallel."* |
| **SEARCHING** | Same input (disabled), three status chips *(PSA · Collectr · eBay)* that animate from grey → spinning → green/red as each source resolves. ETA ~6–12 s. |
| **PREVIEW** | Full card preview *(see Section 4)*. All fields editable. Buttons: `✓ Approve & Save`, `✎ Edit`, `✕ Cancel`. |
| **SAVED** | Green banner: *"Cert XXXXX saved to master workbook ✓"* with links: *`View in Portfolio`* · *`Add another`*. Auto-resets to EMPTY after 5 s. |
| **ERROR** | Red banner with the failed source + retry button. User can still save partial data if at least PSA resolved. |

---

## 3. Placement & Navigation

New tab inserted in the existing top-nav between **Portfolio** and **Signals**:

```
 Dashboard │ Portfolio │ ➕ Add Card │ Signals │ Market
```

Reuses the existing tab-panel pattern in `templates/index.html`. Keyboard shortcut: `n` (for "new").

---

## 4. PREVIEW Layout

```
┌────────────────────────────────────────────────────────────────────────┐
│  [ Back ]                                                      [Cancel]│
├───────────────────────────┬────────────────────────────────────────────┤
│                           │  Cert #131858430         PSA 8 · ART RARE  │
│                           │  2023 POKEMON JAPANESE SV1V · #082          │
│      [ PSA IMAGE ]        │  SLOWPOKE                                   │
│     (from PSA scan)       │                                             │
│                           │  ── Market ──────────────────────────────   │
│      [ COLLECTR IMG ]     │  Collectr live:   ฿843  ✓ matched          │
│     (side by side)        │  PSA estimate:    ฿25.44                    │
│                           │  eBay sold (3mo): ฿780 avg (n=7)            │
│   Image match: ✓ OK       │                                             │
│                           │  ── My Info (editable) ──────────────────   │
│                           │  My Cost: [  ฿___  ]                        │
│                           │  Date Acquired: [ 2026-04-17 ]              │
│                           │  Source: [ _________ ]                      │
│                           │  Notes:  [ _________________ ]              │
│                           │                                             │
│                           │  ── Signal Preview ──────────────────────   │
│                           │  [BUY] · LOW risk · +17% upside            │
├───────────────────────────┴────────────────────────────────────────────┤
│                                          [ ✎ Edit ]  [ ✓ Approve & Save ]│
└────────────────────────────────────────────────────────────────────────┘
```

**Image validation** reuses the existing `_fetch_psa_cert_image` + `_fetch_collectr_image` + `validate_and_fetch_all` pipeline, writing to the same `cache/` folder. If images mismatch (visual hash diff), a warning chip appears — user can still approve, or open `manual_image_overrides/` workflow.

---

## 5. Master Workbook Design

**New file:** `Portfolio_Master.xlsx` (replaces CSV as source of truth)

**Sheets:**

| Sheet | Purpose |
|---|---|
| `Cards` | One row per cert. All 33 CSV columns + 6 new columns *(collectr_url, collectr_price_thb, ebay_avg_thb, ebay_n, image_match_ok, last_updated)* |
| `Sync Log` | Audit trail: timestamp · source *(csv\|add-card\|refresh)* · cert # · action *(added\|updated\|skipped)* |
| `Meta` | Schema version, last CSV sync, rate USD→THB, master workbook version |

**Primary key:** `Cert Number` — but per user decision, **duplicates are allowed** (always append). Sync Log records the action so the user can audit and dedupe manually.

**Why a separate workbook** (not the existing `Pokemon_Portfolio_Intelligence.xlsx`): that file is the *analytics output* regenerated every refresh. `Portfolio_Master.xlsx` is the *input of record* — never overwritten, only appended to.

---

## 6. CSV Auto-Sync

**Trigger:** `BUILD_EXE.bat` launch, `REFRESH.bat` click, and the `/api/refresh` endpoint.

**Logic** (`scripts/csv_master_sync.py` — new module):

```
 1. Find latest "My Collection CSV - *.csv" in root folder
 2. For each row: compute stable row-hash (cert + grade + cost + date_acquired)
 3. If hash not in master.Cards → append as new row, log 'added' to Sync Log
 4. If hash matches but cert+grade+cost changed → append new version, log 'updated'
 5. Never delete rows (audit-friendly)
 6. Write compact summary to DRYRUN_REPORT.txt: "CSV sync: +2 added, +0 updated"
```

Auto-sync runs **before** live Collectr fetch so `refresh_live` sees the merged card set.

---

## 7. Backend — New Endpoints

Add to `webapp.py`:

| Method | Path | Purpose |
|---|---|---|
| `POST` | `/api/add-card/search` | Body: `{cert}` → launches parallel PSA + Collectr + eBay fetch → returns merged preview JSON + image URLs |
| `POST` | `/api/add-card/save` | Body: full edited preview payload → appends to `Portfolio_Master.xlsx`, returns `{ok, master_row_id}` |
| `POST` | `/api/csv-sync` | Manual re-trigger of CSV→Master sync (also called automatically on refresh) |
| `GET`  | `/api/add-card/image-validate/<cert>` | Returns `{psa_ok, collectr_ok, visual_match}` for the preview chip |

**New backend modules:**

| File | Role |
|---|---|
| `scripts/master_workbook.py` | Load/append/save `Portfolio_Master.xlsx` using openpyxl |
| `scripts/csv_master_sync.py` | CSV→Master diff-and-append logic |
| `scripts/add_card_service.py` | Orchestrates parallel fetch from `psa_scraper` + `collectr_live_fetcher` + `ebay_connector` with `asyncio.gather`, returns merged `PreviewCard` dataclass |

**Existing files touched:**

| File | Change |
|---|---|
| `webapp.py` | Add 4 endpoints + wire `csv_master_sync.run()` into `api_refresh` + `index` boot |
| `templates/index.html` | Add `#tab-add-card` panel, nav button, JS for the 3 states |
| `scripts/refresh_live.py` | Read from `Portfolio_Master.xlsx` instead of CSV |
| `scripts/ingest.py` | Gains `ingest_from_master()` alongside existing CSV path |
| `REFRESH.bat` / `start_webapp.bat` | Call `csv_master_sync.py` before webapp starts |

---

## 8. Edge Cases & Safeguards

1. **Cert not found on PSA** → Preview still renders with Collectr + eBay + manual edit fields; image slot shows placeholder; warning chip.
2. **Collectr not matched** → Row saves with `collectr_price_thb=null`; signal falls back to `REVIEW`.
3. **eBay has <3 comps** → Hide eBay section, label *"insufficient comps"*.
4. **Concurrent Add + Refresh** → Add Card uses a **write-lock** on `Portfolio_Master.xlsx` (file-level, 10s timeout). Refresh reads a copy.
5. **PSA cert typo / invalid format** → Client-side regex `^\d{6,10}$` + server echo.
6. **Master workbook missing** → First launch auto-creates it from the latest CSV.
7. **User closes browser mid-save** → Backend is idempotent; the row either committed or didn't — no partial writes (openpyxl atomic save to tmp + rename).

---

## 9. Acceptance Criteria

- [ ] User can paste cert `131858430`, see preview within 15 s, approve, and find the card in `Portfolio_Master.xlsx` > `Cards` sheet.
- [ ] Dashboard/Portfolio tabs auto-refresh to include the newly added card without a full reload.
- [ ] Running `REFRESH.bat` with an updated CSV pulls new rows into master and logs them to `Sync Log`.
- [ ] Duplicate cert saves are allowed and visible as separate rows.
- [ ] Image preview shows both PSA and Collectr images side-by-side, with a match-check badge.
- [ ] All new endpoints have a minimal pytest smoke test in `scripts/tests/`.

---

## 10. Out of Scope (for this iteration)

- Bulk CSV upload UI (paste 10 certs at once) — possible follow-up.
- Auto-dedupe / merge suggestions — user prefers manual cleanup for now.
- Mobile layout polish — desktop-first.
- Deleting a row from the master — read-only from UI in v1 (manual Excel edit).

---

## 11. File Deliverables (after implementation)

```
PSA x Collectr Tracer/
├── Portfolio_Master.xlsx          ← NEW master source of truth
├── scripts/
│   ├── master_workbook.py         ← NEW
│   ├── csv_master_sync.py         ← NEW
│   └── add_card_service.py        ← NEW
├── templates/index.html           ← MODIFIED (+ Add Card tab)
├── webapp.py                      ← MODIFIED (+ 4 endpoints)
└── REFRESH.bat / start_webapp.bat ← MODIFIED (CSV sync hook)
```

---

**Review checklist for user:** Does the flow match your expectation? Is the preview layout right? Any fields missing from the editable section? OK to proceed to the Haiku handover prompt?
