# Add Card — Fine-Tuning Prompt for Haiku (v2 Delta)

**Context:** You previously implemented the Add Card feature per `HAIKU_PROMPT.md`. The current UI only accepts a PSA Cert Number. The user now wants a **global live search** that fires on every keystroke, queries external sources, returns a ranked list of best-match candidates, and lets the user pick one to validate + save.

**This is a DELTA spec.** Keep everything from `HAIKU_PROMPT.md` that still applies (master workbook, CSV sync, save endpoint, preview state, saved state). Replace ONLY the Empty state + Search logic as described below.

---

## 1 · THE PIVOT (one-line summary)

**Before:** User pastes a cert → server does a 3-source fetch → preview.
**After:** User types anything → debounced live search across **Collectr + eBay** → ranked **top-5** results dropdown → user clicks a candidate → full 3-source merge + preview (unchanged).

---

## 2 · USER-APPROVED DECISIONS

Already locked. Do not re-propose:

| Decision | Value |
|---|---|
| Search sources (live, per-keystroke) | **Collectr live search** + **eBay sold listings** |
| Cert fast-path | **YES** — pure 6–10 digit input skips search, goes direct to existing cert flow |
| Dropdown result count | **Top 5** |
| Local master workbook | NOT a search source — but show an *"Owned"* chip overlay on any result whose title/cardnumber matches a row in `Portfolio_Master.xlsx` |

---

## 3 · NEW USER FLOW

```
 User types "slowp..."
     │ (debounce 300ms)
     ▼
 POST /api/add-card/live-search  ──▶  parallel fetch: Collectr + eBay
     │
     ▼
 Top-5 ranked candidates render in a dropdown under the input
     │
     ▼
 User clicks one candidate
     │
     ▼
 POST /api/add-card/search  (existing 3-source merge — unchanged)
     │
     ▼
 Preview state (unchanged) → Approve → Saved (unchanged)
```

**Cert fast-path bypass:** If the current input value matches `/^\d{6,10}$/`, do NOT call live-search. Immediately call the existing `/api/add-card/search` cert flow and jump to preview. Show a subtle chip under the input: *"Cert detected → direct lookup"*.

---

## 4 · LIVE SEARCH SCOPE & RANKING

### Sources (in parallel, per query)

| Source | How | Timeout | Notes |
|---|---|---|---|
| Collectr search | Playwright navigate to `https://app.getcollectr.com/search?q={query}` — scrape result tiles | 4 s | Primary source; expect 10-30 raw results, filter to Pokemon + PSA-gradable |
| eBay sold | Reuse `ebay_connector.search_sold(query)` (extend if needed) | 5 s | Set `sold=1, completed=1`, limit 20 raw hits |

If a source times out, return whatever the other source produced. Never block on a slow source.

### Fields matched

The user may type any combination of these tokens — all should surface relevant results:

`subject` (Pokemon name) · `set` (e.g. "SV2a", "Pokemon 151") · `card_number` (e.g. "175", "#082") · `variety` (e.g. "Art Rare", "SAR", "SIR", "Special Art", "Full Art") · `year` (e.g. "2023") · `grade` (e.g. "PSA 10")

No need to parse — pass the raw query string to each source's search endpoint; each source does its own fuzzy matching.

### Ranking (merge + rerank)

After both sources return, merge into a single candidate list. Score each candidate:

```python
score = 0
score += 40  if query.lower() in candidate.subject.lower()       # subject hit
score += 25  if query_tokens ⊆ candidate.tokens                   # all words match
score += 15  if candidate.source == "collectr"                    # Collectr preferred (more reliable identity)
score += 10  if candidate.has_psa_grade_in_title                  # graded cards preferred
score +=  5  if candidate.year matches query's year token
score -= 20  if candidate.price_thb is None                       # no price = lower confidence
score -= 30  if candidate already in master by exact cert match   # penalise (show as "Owned" chip)
```

Return top-5 after dedup (collapse same product across sources; prefer Collectr version but carry eBay's comp data).

### Owned-chip overlay

Before returning results, cross-reference each candidate against `master_workbook.list_cards()`. If `(subject, card_number, grade)` matches a master row, add `"owned": true, "owned_count": N` to the candidate dict. Frontend renders a small chip.

---

## 5 · BACKEND — NEW ENDPOINT

Add to `webapp.py`:

```python
@app.route("/api/add-card/live-search", methods=["POST"])
def api_live_search():
    """
    Body: {"query": str}
    Returns: {"status": "ok", "results": [Candidate, ...], "took_ms": int}

    Candidate = {
      "source": "collectr" | "ebay" | "both",
      "title": str,
      "subject": str, "set": str, "card_number": str, "variety": str, "year": int | null,
      "grade": int | null,          # if detectable in title, e.g. "PSA 10"
      "product_id": str | null,     # Collectr product id
      "url": str,                   # canonical URL
      "thumbnail_url": str | null,
      "price_thb": float | null,
      "ebay_n_comps": int | null,
      "owned": bool, "owned_count": int,
      "score": float,
    }
    """
    data = request.get_json() or {}
    query = (data.get("query") or "").strip()
    if len(query) < 2:
        return jsonify(status="ok", results=[], took_ms=0)
    # cert fast-path guard (frontend should already handle this, but defend in depth)
    if re.match(r"^\d{6,10}$", query):
        return jsonify(status="cert_detected", results=[], took_ms=0)
    try:
        t0 = time.time()
        results = asyncio.run(add_card_service.live_search(query, limit=5))
        return jsonify(status="ok", results=results, took_ms=int((time.time()-t0)*1000))
    except Exception as e:
        app.logger.error(f"live-search failed: {e}", exc_info=True)
        return jsonify(status="error", message=str(e)), 500
```

### New service function in `scripts/add_card_service.py`

```python
async def live_search(query: str, limit: int = 5) -> list[dict]:
    """Parallel Collectr + eBay search, merge, rank, return top-N."""
    collectr_task = asyncio.create_task(_search_collectr(query, timeout=4.0))
    ebay_task     = asyncio.create_task(_search_ebay(query, timeout=5.0))
    collectr, ebay = await asyncio.gather(collectr_task, ebay_task, return_exceptions=True)
    candidates = _merge_and_dedupe(collectr or [], ebay or [])
    candidates = _annotate_owned(candidates)   # reads master workbook
    candidates = _score_and_rank(candidates, query)
    return candidates[:limit]
```

### New helper functions (all in `add_card_service.py`)

- `_search_collectr(query, timeout)` — Playwright: navigate to Collectr's search URL, wait for result grid, extract tiles' title/url/thumbnail/price. Reuse the existing Playwright browser context from `collectr_live_fetcher` if possible (perf).
- `_search_ebay(query, timeout)` — extend `ebay_connector` with `search_sold(query, limit=20)` that returns raw comps. Aggregate: average, count, median, sample title.
- `_merge_and_dedupe(collectr, ebay)` — collapse by `(subject, card_number, grade)`; when a match is found across sources, prefer Collectr's identity fields but attach eBay's `ebay_avg_thb` and `ebay_n_comps`.
- `_annotate_owned(cands)` — one-shot call to `master_workbook.list_cards()`, build a dict keyed on `(subject, card_number, grade)`, set `owned` + `owned_count` on each.
- `_score_and_rank(cands, query)` — applies the formula from Section 4.

### Caching

Wrap `live_search` with a tiny LRU (`functools.lru_cache(maxsize=64)` won't work for async — use a manual dict keyed on query string, TTL 60 s). Prevents re-fetching while user types/backspaces.

### Playwright browser reuse

The existing `collectr_live_fetcher` spins up Playwright per call. For live search that's too slow. **Create a module-level persistent browser context** in `add_card_service.py` that:
- Lazily initializes on first search
- Stays alive for 5 minutes of inactivity then closes
- Uses one browser with multiple pages (parallel)

---

## 6 · FRONTEND — `templates/index.html`

### 6.1 Replace the Empty state layout

Current empty state has just the centered cert input. New layout — still centered, but the input is a **search bar** and results render in a dropdown directly below.

```html
<div id="add-card-empty">
  <div class="search-hero">
    <div class="search-icon">🔎</div>
    <h2>Find a Pokemon card</h2>
    <p>Start typing — name, set, card #, year, grade. Paste a PSA cert # for direct lookup.</p>

    <div class="search-wrap">
      <input id="add-card-query" class="search-input"
             placeholder="e.g. slowpoke art rare · 2023 · PSA 10 · or cert 131858430"
             autocomplete="off" />
      <span id="search-state" class="search-state"></span>  <!-- spinner / "Cert detected" chip -->
    </div>

    <div id="search-results" class="search-results" style="display:none">
      <!-- top-5 candidate cards rendered here -->
    </div>
    <div id="search-empty-hint" class="hint">Type 2+ characters to search</div>
  </div>
</div>
```

### 6.2 Candidate card template

Each result in `#search-results`:

```html
<div class="result-card" data-product-id="..." data-url="...">
  <img class="result-thumb" src="{thumbnail_url}" onerror="this.style.display='none'">
  <div class="result-body">
    <div class="result-title">{subject} · {variety}</div>
    <div class="result-meta">{year} · {set} · #{card_number} · PSA {grade}</div>
    <div class="result-tags">
      <span class="tag tag-collectr" v-if="source includes collectr">Collectr</span>
      <span class="tag tag-ebay" v-if="ebay_n_comps">eBay n={ebay_n_comps}</span>
      <span class="tag tag-owned" v-if="owned">✓ Owned ({owned_count})</span>
    </div>
  </div>
  <div class="result-price">
    <div class="price-val">฿{price_thb | locale}</div>
    <div class="price-src">{primary source}</div>
  </div>
</div>
```

**Style guide**: match existing `.panel` aesthetic — light card, 1px border, 8px radius, subtle hover lift. Owned chip = green pill. Collectr chip = blue. eBay chip = orange.

### 6.3 JS logic

```javascript
const $q = document.getElementById('add-card-query');
const $results = document.getElementById('search-results');
const $state = document.getElementById('search-state');
const CERT_RE = /^\d{6,10}$/;
let searchAbort = null;
let searchTimer = null;

$q.addEventListener('input', e => {
  const q = e.target.value.trim();
  clearTimeout(searchTimer);
  if (searchAbort) searchAbort.abort();

  // Cert fast-path
  if (CERT_RE.test(q)) {
    $state.innerHTML = '<span class="chip-mini">Cert detected → direct lookup</span>';
    $results.style.display = 'none';
    searchTimer = setTimeout(() => triggerCertLookup(q), 400);
    return;
  }

  $state.innerHTML = '';
  if (q.length < 2) { $results.style.display = 'none'; return; }

  // Debounced live search
  searchTimer = setTimeout(() => runLiveSearch(q), 300);
});

async function runLiveSearch(query) {
  searchAbort = new AbortController();
  $state.innerHTML = '<span class="spinner-mini"></span>';
  try {
    const r = await fetch('/api/add-card/live-search', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({query}),
      signal: searchAbort.signal
    });
    const data = await r.json();
    $state.innerHTML = '';
    renderResults(data.results || []);
  } catch (err) {
    if (err.name !== 'AbortError') {
      $state.innerHTML = '<span class="err-chip">Search failed</span>';
    }
  }
}

function renderResults(results) {
  if (!results.length) {
    $results.innerHTML = '<div class="no-results">No matches — try a different query or paste a PSA cert #</div>';
    $results.style.display = 'block';
    return;
  }
  $results.innerHTML = results.map(resultCardHTML).join('');
  $results.style.display = 'block';
  $results.querySelectorAll('.result-card').forEach(el => {
    el.addEventListener('click', () => pickCandidate(el.dataset));
  });
}

function pickCandidate(dataset) {
  // Hand off to existing 3-source merge flow.
  // If we have a product_id, pass it so Collectr step can skip search.
  // If we have a cert (rare in search results), use /api/add-card/search.
  // Otherwise, call a new endpoint /api/add-card/search-by-url with the candidate URL.
  startPreviewFetch(dataset);
}
```

### 6.4 Keyboard navigation

- `↑` / `↓` → move highlight across results
- `Enter` → pick highlighted result (or first result if none highlighted)
- `Esc` → clear input + hide dropdown

### 6.5 Handing a candidate to the Preview

The existing `/api/add-card/search` takes a cert. For Collectr candidates (no cert yet), add a second backend endpoint **`POST /api/add-card/search-by-candidate`** that accepts:

```json
{"product_id": "10010852", "url": "...", "title": "..."}
```

...and does: Collectr fetch (already have product_id — skip search) → optional PSA cert inference from scraped page → eBay comps → returns the same `PreviewCard` JSON. Preview state then works exactly as today.

---

## 7 · EDGE CASES

| Case | Behavior |
|---|---|
| User types fast (10 chars in 500ms) | AbortController cancels in-flight requests; only the last query resolves |
| Query returns 0 results | Friendly message + suggestion to paste cert # |
| Both sources time out | Show "Search unavailable — please retry or paste cert" |
| Candidate has no price | Still show; tag *"price unknown"*; let user proceed to preview |
| User clicks a candidate already owned | Allow (per existing duplicate-allowed rule); preview shows a soft warning banner |
| Input cleared | Hide dropdown, reset state chip |
| Focus shifts off input | Keep dropdown visible 200ms after blur so user can click a result |

---

## 8 · PERFORMANCE BUDGET

| Step | Target |
|---|---|
| Keystroke → API call fired | ≤ 350 ms (300ms debounce + setup) |
| Collectr search roundtrip | ≤ 2.5 s p50 / 4 s p95 |
| eBay search roundtrip | ≤ 3 s p50 / 5 s p95 |
| Total perceived latency | ≤ 4 s p95 |
| Persistent browser warm-up (first search of session) | ≤ 6 s — show a friendly "Warming up search engine…" state |

---

## 9 · FILES TO TOUCH (delta only)

| File | Change |
|---|---|
| `webapp.py` | +2 routes: `/api/add-card/live-search`, `/api/add-card/search-by-candidate` |
| `scripts/add_card_service.py` | +`live_search`, +`_search_collectr`, +`_search_ebay`, +`_merge_and_dedupe`, +`_annotate_owned`, +`_score_and_rank`, +persistent browser context mgmt |
| `scripts/ebay_connector.py` | +`search_sold(query, limit)` if not already present |
| `templates/index.html` | Replace empty-state HTML + JS for Add Card tab. All other states unchanged. |
| `requirements.txt` | No new deps (asyncio, Playwright, filelock already in) |

---

## 10 · ACCEPTANCE CRITERIA (delta)

- [ ] Typing "slowpoke" shows top-5 results within 4 s; results include at least one Collectr product.
- [ ] Typing "131858430" triggers cert fast-path (no dropdown); preview renders directly.
- [ ] Typing "2023 psyduck 175" returns the Psyduck Art Rare as the top candidate.
- [ ] A result whose cert/subject matches an existing master row shows a green **"Owned"** chip.
- [ ] Clicking a non-cert candidate calls `/api/add-card/search-by-candidate` and lands on the Preview state with merged data.
- [ ] Backspacing from 5 chars to 2 triggers at most **one** in-flight request (older ones aborted).
- [ ] Zero regressions: existing Dashboard, Portfolio, Signals, Market tabs still work; existing refresh still works; master workbook save still works.

---

## 11 · OUT OF SCOPE (v2)

- User-editable filters (grade, year, variety chips next to the search bar)
- Image-based search ("upload a card photo")
- Search history recall
- Autocomplete suggestions *before* Enter (we do full results on each keystroke, not suggestions)

---

## 12 · WHEN YOU ARE DONE

Report:

1. Files changed (line counts).
2. One sample successful query response JSON (redact nothing).
3. Screenshot of the dropdown state with 5 real results.
4. Measured p50 / p95 roundtrip for 3 queries: `"slowpoke"`, `"2023 pikachu art rare"`, `"131858430"` (cert).
5. Confirmation that all v1 acceptance criteria from `HAIKU_PROMPT.md` still pass.

**Do not** proceed past Phase C (frontend) until the live-search endpoint returns real Collectr results in a terminal curl test.

---

*End of fine-tuning delta. Apply on top of HAIKU_PROMPT.md. Preserve everything not explicitly changed here.*
